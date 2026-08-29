#!/usr/bin/env python3
"""Check generated root-relative links without network access."""

from __future__ import annotations

import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit


class LinkParser(HTMLParser):
    def __init__(self, source: Path, output_root: Path) -> None:
        super().__init__()
        self.source = source
        self.output_root = output_root
        self.missing: set[tuple[str, str]] = set()

    def handle_starttag(self, _tag: str, attrs: list[tuple[str, str | None]]) -> None:
        for key, value in attrs:
            if key != "href" or not value or not value.startswith("/") or value.startswith("//"):
                continue
            path = unquote(urlsplit(value).path).lstrip("/")
            if not path:
                continue
            candidate = self.output_root / path
            checks = [candidate]
            if value.endswith("/") or not candidate.suffix:
                checks.append(candidate / "index.html")
            if not any(item.exists() for item in checks):
                self.missing.add((str(self.source), value))


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: check-links.py OUTPUT_ROOT", file=sys.stderr)
        return 2
    output_root = Path(sys.argv[1]).resolve()
    missing: set[tuple[str, str]] = set()
    for page in output_root.rglob("*.html"):
        parser = LinkParser(page, output_root)
        parser.feed(page.read_text(errors="replace"))
        missing.update(parser.missing)
    if missing:
        for source, href in sorted(missing):
            print(f"{source}: {href}", file=sys.stderr)
        print(f"{len(missing)} missing internal links", file=sys.stderr)
        return 1
    print("generated internal links OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

