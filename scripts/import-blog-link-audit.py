#!/usr/bin/env python3
"""Normalize local link-audit snapshots into repository-owned data files."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
OUTPUT_ROOT = ROOT / "data" / "blog"


def sanitize(value: object) -> object:
    if isinstance(value, dict):
        return {key: sanitize(item) for key, item in value.items()}
    if isinstance(value, list):
        return [sanitize(item) for item in value]
    if not isinstance(value, str):
        return value
    if "/content/blog/" in value:
        return "content/blog/" + value.split("/content/blog/", 1)[1]
    if value.startswith(str(ROOT) + "/"):
        return value.removeprefix(str(ROOT) + "/")
    if value.startswith("/tmp/"):
        return Path(value).name
    if value.startswith("/Users/"):
        return "local-input:" + Path(value).name
    return value


def read(path: Path) -> dict[str, object]:
    return json.loads(path.read_text())


def write(name: str, payload: dict[str, object]) -> None:
    path = OUTPUT_ROOT / name
    path.write_text(json.dumps(sanitize(payload), ensure_ascii=False, indent=2) + "\n")
    print(f"wrote {path.relative_to(ROOT)}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--wechat", type=Path, required=True)
    parser.add_argument("--external", type=Path, required=True)
    parser.add_argument("--fixes", type=Path, required=True)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    OUTPUT_ROOT.mkdir(parents=True, exist_ok=True)
    wechat = read(args.wechat)
    external = read(args.external)
    fixes = read(args.fixes)
    fixes["source_audit"] = "data/blog/external-link-audit.json"
    write("wechat-map.json", wechat)
    write("external-link-audit.json", external)
    write("link-fixes.json", fixes)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
