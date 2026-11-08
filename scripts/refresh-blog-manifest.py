#!/usr/bin/env python3
"""Refresh current archive digests while retaining the original import hashes."""

from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
MANIFEST = ROOT / "data" / "blog" / "imports.json"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def file_record(path: Path, original: dict[str, object] | None) -> dict[str, object]:
    current = sha256(path)
    record: dict[str, object] = {
        "path": path.relative_to(ROOT).as_posix(),
        "bytes": path.stat().st_size,
        "sha256": current,
    }
    if original:
        imported = str(original.get("import_sha256") or original["sha256"])
        record["import_sha256"] = imported
        if current != imported:
            record["editorially_modified"] = True
    else:
        record["editorially_added"] = True
    return record


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--note",
        default="taxonomy, Markdown, punctuation, and link editorial pass",
        help="short description stored with the revision",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    manifest = json.loads(MANIFEST.read_text())
    previous_removed = manifest.get("editorial_revision", {}).get(
        "removed_import_files", []
    )
    removed_by_path = {item["path"]: item for item in previous_removed}

    for article in manifest["articles"]:
        bundle = ROOT / "content" / "blog" / article["slug"]
        old = {item["path"]: item for item in article["files"]}
        paths = sorted(path for path in bundle.rglob("*") if path.is_file())
        article["files"] = [
            file_record(path, old.get(path.relative_to(ROOT).as_posix())) for path in paths
        ]
        current_paths = {item["path"] for item in article["files"]}
        for path, record in old.items():
            if path not in current_paths:
                removed_by_path[path] = {
                    "path": path,
                    "import_sha256": record.get("import_sha256") or record["sha256"],
                }

    old_support = {item["path"]: item for item in manifest["support_files"]}
    support_paths = sorted(
        path
        for base in (ROOT / "content" / "authors", ROOT / "assets" / "img")
        for path in base.rglob("*")
        if path.is_file()
    )
    manifest["support_files"] = [
        file_record(path, old_support.get(path.relative_to(ROOT).as_posix()))
        for path in support_paths
    ]

    article_files = [item for article in manifest["articles"] for item in article["files"]]
    support_files = manifest["support_files"]
    removed = [removed_by_path[path] for path in sorted(removed_by_path)]
    manifest["totals"] = {
        "article_files": len(article_files),
        "article_bytes": sum(int(item["bytes"]) for item in article_files),
        "support_files": len(support_files),
        "support_bytes": sum(int(item["bytes"]) for item in support_files),
        "editorially_modified_files": sum(
            bool(item.get("editorially_modified")) for item in article_files
        ),
        "editorially_added_files": sum(
            bool(item.get("editorially_added")) for item in article_files
        ),
        "editorially_removed_files": len(removed),
    }
    manifest["editorial_revision"] = {
        "schema": 1,
        "updated_at": datetime.now(timezone.utc).isoformat(),
        "note": args.note,
        "removed_import_files": removed,
    }
    MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n")
    print(
        "refreshed blog manifest: "
        f"{manifest['totals']['editorially_modified_files']} modified, "
        f"{manifest['totals']['editorially_added_files']} added, "
        f"{manifest['totals']['editorially_removed_files']} removed"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
