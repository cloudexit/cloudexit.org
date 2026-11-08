#!/usr/bin/env python3
"""Check generated root-relative links without network access."""

from __future__ import annotations

import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit


class IdParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.ids: set[str] = set()

    def handle_starttag(self, _tag: str, attrs: list[tuple[str, str | None]]) -> None:
        for key, value in attrs:
            if key == "id" and value:
                self.ids.add(value)


class LinkParser(HTMLParser):
    def __init__(
        self, source: Path, output_root: Path, document_ids: dict[Path, set[str]]
    ) -> None:
        super().__init__()
        self.source = source
        self.output_root = output_root
        self.document_ids = document_ids
        self.missing: set[tuple[str, str]] = set()

    def check_url(self, value: str, check_fragment: bool = False) -> None:
        if value.startswith("//"):
            return
        parsed = urlsplit(value)
        if value.startswith("#"):
            candidate = self.source
        elif value.startswith("/"):
            path = unquote(parsed.path).lstrip("/")
            if not path:
                candidate = self.output_root / "index.html"
            else:
                candidate = self.output_root / path
        else:
            return

        checks = [candidate]
        if parsed.path.endswith("/") or not candidate.suffix:
            checks.append(candidate / "index.html")
        target = next((item for item in checks if item.is_file()), None)
        if target is None:
            self.missing.add((str(self.source), value))
            return

        if check_fragment and parsed.fragment and target.suffix == ".html":
            fragment = unquote(parsed.fragment)
            if fragment not in self.document_ids.get(target, set()):
                self.missing.add((str(self.source), value))

    def handle_starttag(self, _tag: str, attrs: list[tuple[str, str | None]]) -> None:
        for key, value in attrs:
            if not value:
                continue
            if key == "href":
                self.check_url(value, check_fragment=True)
            elif key == "src":
                self.check_url(value)
            elif key == "srcset":
                for candidate in value.split(","):
                    parts = candidate.strip().split()
                    if parts:
                        self.check_url(parts[0])


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: check-links.py OUTPUT_ROOT", file=sys.stderr)
        return 2
    output_root = Path(sys.argv[1]).resolve()
    missing: set[tuple[str, str]] = set()
    pages = sorted(output_root.rglob("*.html"))
    page_text = {page: page.read_text(errors="replace") for page in pages}
    document_ids: dict[Path, set[str]] = {}
    for page, source in page_text.items():
        parser = IdParser()
        parser.feed(source)
        document_ids[page] = parser.ids
    for page, source in page_text.items():
        parser = LinkParser(page, output_root, document_ids)
        parser.feed(source)
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
