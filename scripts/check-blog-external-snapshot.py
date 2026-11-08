#!/usr/bin/env python3
"""Ensure no URL previously confirmed dead remains in the edited blog corpus."""

from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
BLOG_ROOT = ROOT / "content" / "blog"
DATA_ROOT = ROOT / "data" / "blog"
URL_RE = re.compile(r"https?://[^\s<>\"')\]，。；：！？（）【】《》“”*]+")
FENCE_RE = re.compile(r"^\s*(`{3,}|~{3,})")


def current_urls() -> set[str]:
    urls: set[str] = set()
    for path in BLOG_ROOT.glob("*/index*.md"):
        text = path.read_text(errors="replace")
        body = text.split("---", 2)[2]
        fence: str | None = None
        for line in body.splitlines():
            match = FENCE_RE.match(line)
            if match:
                marker = match.group(1)[0]
                fence = marker if fence is None else (None if fence == marker else fence)
                continue
            if fence is None:
                urls.update(match.group(0).rstrip(".,;:") for match in URL_RE.finditer(line))
    return urls


def main() -> int:
    audit = json.loads((DATA_ROOT / "external-link-audit.json").read_text())
    urls = current_urls()
    hard = {
        record["url"]
        for record in audit["records"]
        if record["classification"] == "hard-404"
    }
    remaining = sorted(urls & hard)
    if remaining:
        print("confirmed dead external links remain:")
        print("\n".join(remaining))
        return 1
    print(
        f"external-link snapshot OK: {len(hard)} confirmed dead URLs removed or replaced; "
        f"blocked/timeouts remain classified as uncertain"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
