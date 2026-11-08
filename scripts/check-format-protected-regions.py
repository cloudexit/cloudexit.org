#!/usr/bin/env python3
"""Ensure a prose formatter did not alter Markdown's protected regions."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


FENCE_RE = re.compile(r"^\s*(`{3,}|~{3,})")
INLINE_CODE_RE = re.compile(r"(`+)(.+?)\1")
LINK_DEST_RE = re.compile(r"\]\((<[^>]+>|[^)\s]+)(?:\s+[\"'][^)]*[\"'])?\)")
RAW_URL_RE = re.compile(r"https?://[^\s<>\"')\]，。；：！？（）【】《》“”*]+")
MATH_RE = re.compile(r"\\\(.+?\\\)|\\\[.+?\\\]|\$\$.+?\$\$", re.DOTALL)


def regions(path: Path) -> dict[str, list[str]]:
    text = path.read_text(errors="replace")
    lines = text.splitlines(keepends=True)
    fences: list[str] = []
    prose: list[str] = []
    marker: str | None = None
    current: list[str] = []
    for line in lines:
        match = FENCE_RE.match(line)
        if match:
            token = match.group(1)[0]
            if marker is None:
                marker = token
                current = [line]
            elif marker == token:
                current.append(line)
                fences.append("".join(current))
                marker = None
                current = []
            else:
                current.append(line)
            continue
        if marker is None:
            prose.append(line)
        else:
            current.append(line)
    searchable = "".join(prose)
    return {
        "fenced_code": fences,
        "inline_code": [match.group(0) for match in INLINE_CODE_RE.finditer(searchable)],
        "link_destinations": [match.group(1) for match in LINK_DEST_RE.finditer(searchable)],
        "raw_urls": [match.group(0) for match in RAW_URL_RE.finditer(searchable)],
        "math": [match.group(0) for match in MATH_RE.finditer(searchable)],
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("before", type=Path)
    parser.add_argument("after", type=Path)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    failures: list[str] = []
    before_files = sorted(args.before.glob("*/index*.md"))
    for before in before_files:
        relative = before.relative_to(args.before)
        after = args.after / relative
        if not after.is_file():
            failures.append(f"missing after file: {relative}")
            continue
        old = regions(before)
        new = regions(after)
        for kind in old:
            if old[kind] != new[kind]:
                failures.append(f"{relative}: changed {kind}")
    if failures:
        print("\n".join(failures))
        return 1
    print(f"protected Markdown regions unchanged in {len(before_files)} files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
