#!/usr/bin/env python3
"""Publish audited Cloud Exit ledger snapshots from the research workspace."""

from __future__ import annotations

import hashlib
import json
import shutil
from datetime import date
from pathlib import Path


SITE_ROOT = Path(__file__).resolve().parents[1]
RESEARCH_ROOT = SITE_ROOT.parent / "cloud" / "research"
DATA_ROOT = SITE_ROOT / "static" / "data"

RELEASES = {
    "cloud-pricing": {
        "source": "cloud-pricing-2026",
        "version": "2026-08-22-v1",
        "snapshot": "2026-08-22",
        "analysis_as_of": "2026-08-24",
    },
    "build-vs-buy": {
        "source": "cloud-build-vs-buy-2026",
        "version": "2026-08-24-v1",
        "snapshot": "2026-08-22",
        "analysis_as_of": "2026-08-24",
    },
    "price-history": {
        "source": "cloud-price-history-2026",
        "version": "2026-08-24-v1",
        "snapshot": "2026-08-22",
        "analysis_as_of": "2026-08-24",
    },
}


def publish_release(dataset: str, spec: dict[str, str]) -> Path:
    source_root = RESEARCH_ROOT / spec["source"]
    target_root = DATA_ROOT / dataset / spec["version"]
    tables_root = target_root / "tables"
    charts_root = target_root / "charts"
    tables_root.mkdir(parents=True, exist_ok=True)
    charts_root.mkdir(parents=True, exist_ok=True)

    for source_file in sorted((source_root / "data").iterdir()):
        if source_file.is_file():
            shutil.copy2(source_file, tables_root / source_file.name)
    shutil.copy2(source_root / "report-source.md", target_root / "report.md")

    source_charts = source_root / "charts"
    if source_charts.is_dir():
        for chart in sorted(source_charts.iterdir()):
            if chart.suffix.lower() in {".png", ".svg"}:
                shutil.copy2(chart, charts_root / chart.name)

    release = {
        "dataset": dataset,
        "version": spec["version"],
        "snapshot": spec["snapshot"],
        "analysis_as_of": spec["analysis_as_of"],
        "published_in_site_source": str(date.today()),
        "source_project": f"pgsty/cloud/research/{spec['source']}",
        "status": "released-snapshot",
        "warning": "Historical snapshot; not a live provider quote.",
    }
    (target_root / "release.json").write_text(
        json.dumps(release, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    return target_root


def write_checksums(target_root: Path) -> None:
    checksum_path = target_root / "checksums.txt"
    entries = []
    for path in sorted(target_root.rglob("*")):
        if path.is_file() and path != checksum_path:
            digest = hashlib.sha256(path.read_bytes()).hexdigest()
            entries.append(f"{digest}  {path.relative_to(target_root).as_posix()}")
    checksum_path.write_text("\n".join(entries) + "\n", encoding="utf-8")


def main() -> None:
    missing = [spec["source"] for spec in RELEASES.values() if not (RESEARCH_ROOT / spec["source"]).is_dir()]
    if missing:
        raise SystemExit(f"missing research sources: {', '.join(missing)}")

    targets = {dataset: publish_release(dataset, spec) for dataset, spec in RELEASES.items()}
    for target in targets.values():
        write_checksums(target)
    print("ledger data snapshots built")


if __name__ == "__main__":
    main()

