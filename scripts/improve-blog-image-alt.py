#!/usr/bin/env python3
"""Replace empty or filename-only image alt text with contextual descriptions."""

from __future__ import annotations

import argparse
import re
from pathlib import Path
from urllib.parse import unquote, urlsplit

import yaml


ROOT = Path(__file__).resolve().parent.parent
BLOG_ROOT = ROOT / "content" / "blog"
IMAGE_RE = re.compile(
    r"!\[(?P<alt>[^\]]*)\]\((?P<dest><[^>]+>|[^)\s]+)(?P<title>\s+[\"'][^)]*[\"'])?\)"
)
HEADING_RE = re.compile(r"^#{2,6}\s+(?P<title>.+?)\s*$")
GENERIC_RE = re.compile(
    r"^(?:图片|图像|配图|截图|image|img|picture|photo|loading|featured)(?:[\s_-]*\d+)?$",
    re.IGNORECASE,
)
ACRONYMS = {
    "ai": "AI",
    "api": "API",
    "aws": "AWS",
    "cdn": "CDN",
    "cf": "Cloudflare",
    "dba": "DBA",
    "dns": "DNS",
    "ebs": "EBS",
    "ecs": "ECS",
    "gcp": "GCP",
    "ha": "HA",
    "iam": "IAM",
    "k8s": "Kubernetes",
    "minio": "MinIO",
    "oss": "OSS",
    "pg": "PostgreSQL",
    "rds": "RDS",
    "s3": "S3",
    "sla": "SLA",
}


def clean_text(value: str) -> str:
    value = re.sub(r"<[^>]+>", "", value)
    value = re.sub(r"!?\[([^\]]+)\]\([^)]+\)", r"\1", value)
    value = re.sub(r"[`*_~#]", "", value)
    return re.sub(r"\s+", " ", value).strip(" ：:—-。.!！?？")


def filename_label(destination: str) -> str | None:
    raw = destination.strip("<>")
    basename = Path(unquote(urlsplit(raw).path)).name
    stem = Path(basename).stem
    if not stem or stem.lower() in {"featured", "image", "img", "picture", "loading"}:
        return None
    if re.fullmatch(r"(?:img|image|pic|figure)?[\s_-]*\d+", stem, re.IGNORECASE):
        return None
    words = [word for word in re.split(r"[-_\s]+", stem) if word]
    if not words or all(word.isdigit() for word in words):
        return None
    rendered = [ACRONYMS.get(word.lower(), word) for word in words]
    return " ".join(rendered)


def is_generic(alt: str, destination: str) -> bool:
    normalized = clean_text(alt)
    if not normalized or GENERIC_RE.fullmatch(normalized):
        return True
    basename = Path(unquote(urlsplit(destination.strip("<>")).path)).name
    return normalized.lower() in {basename.lower(), Path(basename).stem.lower()}


def replacement_alt(
    article_title: str,
    heading: str | None,
    destination: str,
    sequence: int,
    language: str,
) -> str:
    basename = Path(unquote(urlsplit(destination.strip("<>")).path)).name
    if Path(basename).stem.lower() == "featured":
        return f"{article_title}封面" if language == "zh" else f"{article_title} cover"
    context = clean_text(heading or article_title) or article_title
    label = filename_label(destination)
    if language == "zh":
        return f"{context}：{label}" if label else f"{context}（图 {sequence}）"
    return f"{context} — {label}" if label else f"{context} (figure {sequence})"


def update_page(path: Path, write: bool) -> int:
    text = path.read_text()
    parts = text.split("---", 2)
    metadata = yaml.safe_load(parts[1]) or {}
    article_title = str(metadata.get("title", path.parent.name))
    language = "zh" if path.name == "index.zh.md" else "en"
    lines = text.splitlines(keepends=True)
    heading: str | None = None
    fence: str | None = None
    sequence = 0
    changed = 0
    for index, line in enumerate(lines):
        fence_match = re.match(r"^\s*(`{3,}|~{3,})", line)
        if fence_match:
            marker = fence_match.group(1)[0]
            fence = marker if fence is None else (None if fence == marker else fence)
            continue
        if fence is not None:
            continue
        heading_match = HEADING_RE.match(line)
        if heading_match:
            heading = clean_text(heading_match.group("title"))

        def replace(match: re.Match[str]) -> str:
            nonlocal changed, sequence
            sequence += 1
            alt = match.group("alt")
            destination = match.group("dest")
            if not is_generic(alt, destination):
                return match.group(0)
            changed += 1
            new_alt = replacement_alt(
                article_title, heading, destination, sequence, language
            ).replace("[", "").replace("]", "")
            return f"![{new_alt}]({destination}{match.group('title') or ''})"

        lines[index] = IMAGE_RE.sub(replace, line)
    if changed and write:
        path.write_text("".join(lines))
    return changed


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    pages = sorted(BLOG_ROOT.glob("*/index*.md"))
    changes = sum(update_page(path, args.write) for path in pages)
    action = "updated" if args.write else "would update"
    print(f"{action} {changes} image alt texts across {len(pages)} pages")
    return 0 if args.write or changes == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
