#!/usr/bin/env python3
"""Apply only high-confidence internal-link and dead-link replacements."""

from __future__ import annotations

import html
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
BLOG_ROOT = ROOT / "content" / "blog"
DATA_ROOT = ROOT / "data" / "blog"
FENCE_RE = re.compile(r"^\s*(`{3,}|~{3,})")


def route(slug: str, language: str, languages: set[str]) -> str:
    if language == "en" and "en" in languages:
        return f"/blog/{slug}/"
    if language == "zh" and "zh" in languages:
        return f"/zh/blog/{slug}/"
    if "en" in languages:
        return f"/blog/{slug}/"
    return f"/zh/blog/{slug}/"


def replace_outside_fences(text: str, replacements: dict[str, str]) -> tuple[str, int]:
    lines = text.splitlines(keepends=True)
    fence_marker: str | None = None
    changed = 0
    for index, line in enumerate(lines):
        match = FENCE_RE.match(line)
        if match:
            marker = match.group(1)[0]
            if fence_marker is None:
                fence_marker = marker
            elif fence_marker == marker:
                fence_marker = None
            continue
        if fence_marker is not None:
            continue
        for old, new in replacements.items():
            occurrences = line.count(old)
            if occurrences:
                line = line.replace(old, new)
                changed += occurrences
            escaped = html.escape(old, quote=False)
            if escaped != old:
                occurrences = line.count(escaped)
                if occurrences:
                    line = line.replace(escaped, new)
                    changed += occurrences
        lines[index] = line
    return "".join(lines), changed


def main() -> int:
    manifest = json.loads((DATA_ROOT / "imports.json").read_text())
    wechat = json.loads((DATA_ROOT / "wechat-map.json").read_text())
    fixes = json.loads((DATA_ROOT / "link-fixes.json").read_text())
    overrides = json.loads((DATA_ROOT / "link-overrides.json").read_text())

    languages_by_slug = {
        article["slug"]: set(article["languages"]) for article in manifest["articles"]
    }
    archive_routes: dict[str, str] = {}
    for article in manifest["articles"]:
        for source_url in article["source_urls"].values():
            archive_routes[source_url] = article["slug"]

    total = 0
    changed_files = 0
    for page in sorted(BLOG_ROOT.glob("*/index*.md")):
        slug = page.parent.name
        language = "zh" if page.name == "index.zh.md" else "en"
        replacements: dict[str, str] = {}

        for record in wechat["records"]:
            target = record["slug"]
            if target == slug:
                continue
            target_route = route(target, language, languages_by_slug[target])
            for old in record["original_urls"]:
                replacements[old] = target_route

        for old, target in archive_routes.items():
            if target == slug:
                continue
            replacements[old] = route(target, language, languages_by_slug[target])

        for fix in fixes["fixes"]:
            if fix["kind"] == "spelling":
                replacement = fix["replacement"]
            else:
                replacement = fix["replacement_by_language"][language]
            for old in fix["old_urls"]:
                replacements[old] = replacement

        for fix in overrides["replacements"]:
            replacements[fix["old"]] = fix["new"]
        for fix in overrides["language_replacements"]:
            replacements[fix["old"]] = fix[language]

        original = page.read_text()
        updated, count = replace_outside_fences(original, replacements)
        expected_source = next(
            article["source_urls"][language]
            for article in manifest["articles"]
            if article["slug"] == slug
        )
        updated, restored = re.subn(
            r'^archive_source:\s*.*$',
            f'archive_source: "{expected_source}"',
            updated,
            count=1,
            flags=re.MULTILINE,
        )
        if restored != 1:
            raise ValueError(f"missing archive_source in {page}")
        if count:
            changed_files += 1
            total += count
        if updated != original:
            page.write_text(updated)

    print(f"applied {total} high-confidence link replacements in {changed_files} files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
