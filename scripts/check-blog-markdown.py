#!/usr/bin/env python3
"""Check the normalized Markdown and front-matter contract for blog pages."""

from __future__ import annotations

import re
from pathlib import Path
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parent.parent
BLOG_ROOT = ROOT / "content" / "blog"
FENCE_RE = re.compile(r"^\s*(`{3,}|~{3,})(?P<info>.*)$")
HEADING_RE = re.compile(r"^(?P<marks>#{1,6})\s+(?P<title>.+)$")
IMAGE_RE = re.compile(r"!\[(?P<alt>[^\]]*)\]\((?P<dest><[^>]+>|[^)\s]+)")
GENERIC_ALT_RE = re.compile(
    r"^(?:图片|图像|配图|截图|image|img|picture|photo|loading|featured)(?:[\s_-]*\d+)?$",
    re.IGNORECASE,
)


def fail(errors: list[str], path: Path, line: int, message: str) -> None:
    errors.append(f"{path.relative_to(ROOT)}:{line}: {message}")


def generic_alt(alt: str, destination: str) -> bool:
    normalized = re.sub(r"[`*_~#]", "", alt).strip()
    if not normalized or GENERIC_ALT_RE.fullmatch(normalized):
        return True
    basename = Path(unquote(urlsplit(destination.strip("<>")).path)).name
    return normalized.lower() in {basename.lower(), Path(basename).stem.lower()}


def check_page(path: Path, errors: list[str]) -> None:
    text = path.read_text(errors="replace")
    if not text.startswith("---\n"):
        fail(errors, path, 1, "missing YAML front matter")
        return
    parts = text.split("---", 2)
    frontmatter = parts[1]
    for field in ("title", "date", "authors", "summary", "categories", "tags", "archive_source", "archive_section"):
        if not re.search(rf"^{field}:\s*\S", frontmatter, flags=re.MULTILINE):
            fail(errors, path, 1, f"missing front-matter field {field}")
    if re.search(r"^author:\s*", frontmatter, flags=re.MULTILINE):
        fail(errors, path, 1, "legacy singular author field")
    archive_source = re.search(
        r'^archive_source:\s*["\']?(?P<url>[^"\'\s]+)',
        frontmatter,
        flags=re.MULTILINE,
    )
    if not archive_source or not archive_source.group("url").startswith("https://vonng.com/"):
        fail(errors, path, 1, "archive_source is not a vonng.com URL")

    body = parts[2]
    fence: str | None = None
    previous_heading = 0
    offset = len(parts[0].splitlines()) + len(parts[1].splitlines()) + 2
    for index, line in enumerate(body.splitlines(), 1):
        line_number = offset + index
        fence_match = FENCE_RE.match(line)
        if fence_match:
            marker = fence_match.group(1)[0]
            if fence is None:
                fence = marker
                if not fence_match.group("info").strip():
                    fail(errors, path, line_number, "code fence has no language")
            elif fence == marker:
                fence = None
            continue
        if fence is not None:
            continue
        heading = HEADING_RE.match(line)
        if heading:
            level = len(heading.group("marks"))
            if level == 1:
                fail(errors, path, line_number, "body must not contain H1")
            if previous_heading and level > previous_heading + 1:
                fail(errors, path, line_number, "heading level jumps")
            previous_heading = level
        if re.search(r"(?<!!)\[\s*\]\(", line):
            fail(errors, path, line_number, "empty link label")
        if ")[" in line:
            fail(errors, path, line_number, "adjacent links lack a separator")
        if line.rstrip().endswith("\\"):
            fail(errors, path, line_number, "imported hard-break escape")
        if re.match(r"^\s*\d+[.)](?![\d\s])", line):
            fail(errors, path, line_number, "numbered list marker lacks spacing")
        if "•" in line:
            fail(errors, path, line_number, "non-Markdown bullet character")
        for image in IMAGE_RE.finditer(line):
            if generic_alt(image.group("alt"), image.group("dest")):
                fail(errors, path, line_number, "empty or generic image alt text")
    if fence is not None:
        fail(errors, path, len(text.splitlines()), "unclosed code fence")


def main() -> int:
    errors: list[str] = []
    pages = sorted(BLOG_ROOT.glob("*/index*.md"))
    for path in pages:
        check_page(path, errors)
    if errors:
        print("\n".join(errors))
        print(f"{len(errors)} blog Markdown errors")
        return 1
    print(f"blog Markdown OK: {len(pages)} pages")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
