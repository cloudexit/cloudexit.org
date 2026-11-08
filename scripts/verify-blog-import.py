#!/usr/bin/env python3
"""Verify the imported essay inventory and every recorded file digest."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
MANIFEST = ROOT / "data" / "blog" / "imports.json"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def fail(message: str) -> None:
    raise SystemExit(message)


def verify_file(record: dict[str, object]) -> None:
    path = ROOT / str(record["path"])
    if not path.is_file():
        fail(f"missing imported file: {record['path']}")
    if path.stat().st_size != int(record["bytes"]):
        fail(f"size mismatch for imported file: {record['path']}")
    if sha256(path) != record["sha256"]:
        fail(f"digest mismatch for imported file: {record['path']}")


def main() -> int:
    manifest = json.loads(MANIFEST.read_text())
    selection = manifest["selection"]
    articles = manifest["articles"]
    if selection != {
        "cloud_column": 123,
        "cross_column": 35,
        "total_articles": 158,
    }:
        fail(f"unexpected blog selection counts: {selection}")
    if len(articles) != selection["total_articles"]:
        fail("article inventory length does not match selection total")

    slugs = [article["slug"] for article in articles]
    if len(slugs) != len(set(slugs)):
        fail("duplicate slugs in imported article inventory")
    bundle_slugs = sorted(
        path.name
        for path in (ROOT / "content" / "blog").iterdir()
        if path.is_dir()
    )
    if sorted(slugs) != bundle_slugs:
        fail("content/blog bundle set does not match the import manifest")

    for article in articles:
        languages = set(article["languages"])
        bundle = ROOT / "content" / "blog" / article["slug"]
        if not (bundle / "index.zh.md").is_file():
            fail(f"missing Chinese article: {article['slug']}")
        if ("en" in languages) != (bundle / "index.md").is_file():
            fail(f"English article inventory mismatch: {article['slug']}")
        for record in article["files"]:
            verify_file(record)

    for record in manifest["support_files"]:
        verify_file(record)

    print(
        "blog import OK: "
        f"{selection['cloud_column']} Cloud + "
        f"{selection['cross_column']} cross-column articles"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
