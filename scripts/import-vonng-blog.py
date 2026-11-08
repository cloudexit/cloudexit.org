#!/usr/bin/env python3
"""Import the Cloud Exit essay archive from the sibling vonng.com checkout.

The import is intentionally a snapshot operation. It copies every leaf bundle
from vonng.com's Cloud column plus a reviewed set of cross-column essays whose
main subject is cloud exit, data sovereignty, local-first software, or
self-hosted infrastructure.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import subprocess
import tempfile
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit

from table_reading import add_table_reading


TARGET_ROOT = Path(__file__).resolve().parent.parent
SOURCE_SITE = "https://vonng.com"
SOURCE_REPOSITORY = "https://github.com/Vonng/vonng.com"

EXTRA_BUNDLES: dict[str, tuple[str, ...]] = {
    "local-ai-and-sovereignty": (
        "ai/cloud-agent",
        "ai/local-200b",
        "ai/local-ai-inference",
        "ai/open-weight",
    ),
    "open-data-and-local-first": (
        "db/goodbye-gpl",
        "db/open-data-standard",
        "db/ontology-again",
        "db/redis-oss",
    ),
    "self-hosted-data-stack": (
        "db/cheap-polar",
        "db/minio-alternative",
        "db/minio-is-dead",
        "db/supabase",
    ),
    "infrastructure-capability": (
        "misc/entrepreneur-vs-rds",
        "misc/infra-needs-advanced-tech",
        "misc/infra-road-ahead",
        "misc/infra-team-needed",
        "misc/sre-outdated",
    ),
    "postgres-platform": (
        "pg/dify-setup",
        "pg/pigsty-intro",
        "pg/pigsty-relicense",
        "pg/proprity-pg",
        "pg/supabase-series-c",
        "pg/what-is-pg-distro",
    ),
    "pigsty-self-hosting": (
        "pigsty/better-rds-alternative",
        "pigsty/monitor-existing-pg",
        "pigsty/v1.4-preview",
        "pigsty/v2.0",
        "pigsty/v2.0-launch",
        "pigsty/v2.0-outlook",
        "pigsty/v2.4",
        "pigsty/v3.0",
        "pigsty/v3.1",
        "pigsty/v3.6",
        "pigsty/what-is-pigsty",
        "pigsty/year-2024",
    ),
}

KNOWN_SOURCE_SECTIONS = {"ai", "cloud", "db", "misc", "pg", "pigsty", "trip"}
ROOT_LINK_RE = re.compile(
    r"(?P<prefix>\]\(|href=[\"']|src=[\"'])(?P<url>/[^)\s\"']+)"
)
INLINE_ALIAS_RE = re.compile(r"^aliases:\s*\[(?P<values>[^]]*)\]\s*$", re.MULTILINE)
QUOTED_VALUE_RE = re.compile(r"[\"'](?P<value>/[^\"']+)[\"']")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def source_commit(source_root: Path) -> str:
    return subprocess.check_output(
        ["git", "-C", str(source_root), "rev-parse", "HEAD"], text=True
    ).strip()


def article_inventory(content_root: Path) -> list[dict[str, object]]:
    articles: list[dict[str, object]] = []
    for bundle in sorted((content_root / "cloud").iterdir()):
        if bundle.is_dir() and (bundle / "index.md").is_file():
            articles.append(
                {
                    "section": "cloud",
                    "slug": bundle.name,
                    "reason": "cloud-column",
                    "source": bundle,
                }
            )

    for reason, paths in EXTRA_BUNDLES.items():
        for relative in paths:
            section, slug = relative.split("/", 1)
            bundle = content_root / relative
            if not (bundle / "index.md").is_file():
                raise FileNotFoundError(f"missing source article: {bundle / 'index.md'}")
            articles.append(
                {
                    "section": section,
                    "slug": slug,
                    "reason": reason,
                    "source": bundle,
                }
            )

    slugs = [str(item["slug"]) for item in articles]
    duplicates = sorted({slug for slug in slugs if slugs.count(slug) > 1})
    if duplicates:
        raise ValueError(f"duplicate target blog slugs: {', '.join(duplicates)}")
    return sorted(articles, key=lambda item: str(item["slug"]))


def aliases(markdown: Path) -> set[str]:
    if not markdown.is_file():
        return set()
    match = INLINE_ALIAS_RE.search(markdown.read_text(errors="replace"))
    if not match:
        return set()
    return {value.group("value") for value in QUOTED_VALUE_RE.finditer(match.group("values"))}


def build_route_map(articles: list[dict[str, object]]) -> dict[str, dict[str, object]]:
    route_map: dict[str, dict[str, object]] = {}
    for article in articles:
        source = Path(article["source"])
        section = str(article["section"])
        slug = str(article["slug"])
        languages = {"zh"}
        if (source / "index.en.md").is_file():
            languages.add("en")
        target = {"slug": slug, "languages": sorted(languages)}
        routes = {
            f"/{section}/{slug}/",
            f"/en/{section}/{slug}/",
            *aliases(source / "index.md"),
            *aliases(source / "index.en.md"),
        }
        for route in routes:
            route_map[normalize_route(route)] = target
    return route_map


def normalize_route(path: str) -> str:
    return "/" + path.strip("/") + "/"


def local_article_route(target: dict[str, object], language: str) -> str:
    languages = set(target["languages"])
    slug = str(target["slug"])
    if language == "en" and "en" in languages:
        return f"/blog/{slug}/"
    if language == "zh" and "zh" in languages:
        return f"/zh/blog/{slug}/"
    if "en" in languages:
        return f"/blog/{slug}/"
    return f"/zh/blog/{slug}/"


def rewrite_root_url(
    raw_url: str, language: str, route_map: dict[str, dict[str, object]]
) -> str:
    if raw_url.startswith("//"):
        return raw_url
    parsed = urlsplit(raw_url)
    normalized = normalize_route(parsed.path)
    target = route_map.get(normalized)
    if target:
        path = local_article_route(target, language)
        return urlunsplit(("", "", path, parsed.query, parsed.fragment))

    if normalized in {"/cloud/", "/en/cloud/"}:
        path = "/blog/" if language == "en" else "/zh/blog/"
        return urlunsplit(("", "", path, parsed.query, parsed.fragment))

    parts = [part for part in parsed.path.split("/") if part]
    source_section = parts[1] if parts and parts[0] == "en" and len(parts) > 1 else (
        parts[0] if parts else ""
    )
    if source_section in KNOWN_SOURCE_SECTIONS or (parts and parts[0] == "en"):
        return f"{SOURCE_SITE}{raw_url}"
    return raw_url


def rewrite_links(
    markdown: str, language: str, route_map: dict[str, dict[str, object]]
) -> str:
    def replace(match: re.Match[str]) -> str:
        url = rewrite_root_url(match.group("url"), language, route_map)
        return f"{match.group('prefix')}{url}"

    return ROOT_LINK_RE.sub(replace, markdown)


def add_archive_metadata(markdown: str, source_url: str, section: str) -> str:
    if not markdown.startswith("---\n"):
        raise ValueError("article does not use YAML front matter")
    if re.search(r"^archive_source:", markdown, flags=re.MULTILINE):
        raise ValueError("source article already defines archive_source")
    closing = markdown.find("\n---", 4)
    if closing < 0:
        raise ValueError("article has no closing YAML front matter delimiter")
    metadata = (
        f'\narchive_source: {json.dumps(source_url, ensure_ascii=False)}'
        f'\narchive_section: {json.dumps(section, ensure_ascii=False)}'
    )
    return f"{markdown[:closing]}{metadata}{markdown[closing:]}"


def record_files(root: Path, paths: list[Path]) -> list[dict[str, object]]:
    records = []
    for path in sorted(paths):
        records.append(
            {
                "path": path.relative_to(root).as_posix(),
                "bytes": path.stat().st_size,
                "sha256": sha256(path),
            }
        )
    return records


def copy_article(
    article: dict[str, object],
    destination_root: Path,
    route_map: dict[str, dict[str, object]],
    source_git_commit: str,
) -> dict[str, object]:
    source = Path(article["source"])
    section = str(article["section"])
    slug = str(article["slug"])
    destination = destination_root / slug
    destination.mkdir(parents=True)
    source_en = source / "index.en.md"
    has_english = source_en.is_file()

    for path in sorted(source.rglob("*")):
        if not path.is_file():
            continue
        if path.name in {"index.md", "index.en.md"} or path.name.endswith(".en.md"):
            continue
        relative = path.relative_to(source)
        if not has_english:
            relative = relative.with_name(
                f"{relative.stem}.zh{relative.suffix}" if relative.suffix else f"{relative.name}.zh"
            )
        target = destination / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, target)

    languages = ["zh"]
    source_zh = source / "index.md"
    target_zh = destination / "index.zh.md"
    zh_url = f"{SOURCE_SITE}/{section}/{slug}/"
    zh_markdown = add_archive_metadata(source_zh.read_text(), zh_url, section)
    target_zh.write_text(add_table_reading(rewrite_links(zh_markdown, "zh", route_map))[0])

    source_urls: dict[str, str] = {"zh": zh_url}
    if has_english:
        languages.insert(0, "en")
        target_en = destination / "index.md"
        en_url = f"{SOURCE_SITE}/en/{section}/{slug}/"
        en_markdown = add_archive_metadata(source_en.read_text(), en_url, section)
        target_en.write_text(add_table_reading(rewrite_links(en_markdown, "en", route_map))[0])
        source_urls["en"] = en_url

    files = [path for path in destination.rglob("*") if path.is_file()]
    return {
        "slug": slug,
        "source_path": f"content/{section}/{slug}",
        "source_commit": source_git_commit,
        "source_urls": source_urls,
        "reason": article["reason"],
        "languages": languages,
        "files": record_files(destination_root.parent.parent, files),
    }


def copy_language_tree(
    source: Path,
    destination: Path,
    route_map: dict[str, dict[str, object]],
) -> None:
    for path in sorted(source.rglob("*")):
        relative = path.relative_to(source)
        if path.is_dir():
            (destination / relative).mkdir(parents=True, exist_ok=True)
            continue
        if path.name == "_index.en.md":
            target = destination / relative.with_name("_index.md")
            target.write_text(rewrite_links(path.read_text(), "en", route_map))
        elif path.name == "_index.md":
            target = destination / relative.with_name("_index.zh.md")
            target.write_text(rewrite_links(path.read_text(), "zh", route_map))
        else:
            shutil.copy2(path, destination / relative)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--source",
        type=Path,
        default=Path.home() / "www" / "vonng.com",
        help="path to the vonng.com repository",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    source_root = args.source.resolve()
    content_root = source_root / "content"
    final_paths = {
        "blog": TARGET_ROOT / "content" / "blog",
        "authors": TARGET_ROOT / "content" / "authors",
        "images": TARGET_ROOT / "assets" / "img",
        "manifest": TARGET_ROOT / "data" / "blog",
    }
    existing = [str(path) for path in final_paths.values() if path.exists()]
    if existing:
        raise FileExistsError(
            "refusing to overwrite an existing import target: " + ", ".join(existing)
        )

    articles = article_inventory(content_root)
    route_map = build_route_map(articles)
    commit = source_commit(source_root)

    with tempfile.TemporaryDirectory(prefix="cloudexit-blog-import-") as temp:
        stage_root = Path(temp)
        stage_blog = stage_root / "content" / "blog"
        stage_authors = stage_root / "content" / "authors"
        stage_images = stage_root / "assets" / "img"
        stage_manifest = stage_root / "data" / "blog"
        stage_blog.mkdir(parents=True)
        stage_authors.mkdir(parents=True)
        stage_manifest.mkdir(parents=True)

        imported = [
            copy_article(article, stage_blog, route_map, commit) for article in articles
        ]
        copy_language_tree(content_root / "authors", stage_authors, route_map)
        shutil.copytree(source_root / "assets" / "img", stage_images)

        article_files = [entry for item in imported for entry in item["files"]]
        support_paths = [
            path
            for base in (stage_authors, stage_images)
            for path in base.rglob("*")
            if path.is_file()
        ]
        manifest = {
            "schema": 1,
            "source_repository": SOURCE_REPOSITORY,
            "source_commit": commit,
            "selection": {
                "cloud_column": 123,
                "cross_column": len(articles) - 123,
                "total_articles": len(articles),
            },
            "articles": imported,
            "support_files": record_files(stage_root, support_paths),
            "totals": {
                "article_files": len(article_files),
                "article_bytes": sum(int(item["bytes"]) for item in article_files),
                "support_files": len(support_paths),
                "support_bytes": sum(path.stat().st_size for path in support_paths),
            },
        }
        (stage_manifest / "imports.json").write_text(
            json.dumps(manifest, ensure_ascii=False, indent=2) + "\n"
        )

        for key, final in final_paths.items():
            staged = stage_manifest if key == "manifest" else {
                "blog": stage_blog,
                "authors": stage_authors,
                "images": stage_images,
            }[key]
            final.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(staged), str(final))

    print(
        f"imported {len(articles)} articles "
        f"({123} Cloud + {len(articles) - 123} cross-column) from {commit}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
