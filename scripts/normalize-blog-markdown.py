#!/usr/bin/env python3
"""Apply conservative source-level Markdown normalization outside code fences."""

from __future__ import annotations

import argparse
import re
from pathlib import Path

from table_reading import add_table_reading


ROOT = Path(__file__).resolve().parent.parent
BLOG_ROOT = ROOT / "content" / "blog"
FENCE_RE = re.compile(r"^\s*(`{3,}|~{3,})")


def normalize(path: Path, write: bool) -> int:
    lines = path.read_text().splitlines(keepends=True)
    fence: str | None = None
    changes = 0
    for index, line in enumerate(lines):
        match = FENCE_RE.match(line)
        if match:
            marker = match.group(1)[0]
            fence = marker if fence is None else (None if fence == marker else fence)
            continue
        if fence is not None:
            continue
        ending = "\n" if line.endswith("\n") else ""
        content = line.removesuffix("\n")
        if content.endswith("\\"):
            content = content[:-1].rstrip()
            lines[index] = content + ending
            changes += 1
        if path.name == "index.zh.md":
            localized = re.sub(
                r"^(#{2,6})\s+References?\s*$",
                r"\1 参考资料",
                content,
                flags=re.IGNORECASE,
            )
            if localized != content:
                lines[index] = localized + ending
                changes += 1
                content = localized
            punctuated = re.sub(r"[ \t]+([，。；：！？、）》】])", r"\1", content)
            punctuated = re.sub(r"([（《【“])[ \t]+", r"\1", punctuated)
            if punctuated != content:
                lines[index] = punctuated + ending
                changes += 1
    normalized, table_changes = add_table_reading("".join(lines))
    changes += table_changes
    if changes and write:
        path.write_text(normalized)
    return changes


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    pages = sorted(BLOG_ROOT.glob("*/index*.md"))
    changes = sum(normalize(path, args.write) for path in pages)
    action = "normalized" if args.write else "would normalize"
    print(f"{action} {changes} imported Markdown artifacts across {len(pages)} pages")
    return 0 if args.write or changes == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
