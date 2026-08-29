#!/usr/bin/env python3
"""Verify published ledger snapshots, checksums, and headline source values."""

from __future__ import annotations

import csv
import hashlib
import json
import math
import sys
from pathlib import Path


SITE_ROOT = Path(__file__).resolve().parents[1]
DATA_ROOT = SITE_ROOT / "static" / "data"


def rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def close(actual: str, expected: float, label: str, tolerance: float = 1e-6) -> None:
    if not math.isclose(float(actual), expected, rel_tol=tolerance, abs_tol=tolerance):
        raise AssertionError(f"{label}: expected {expected}, got {actual}")


def verify_checksums(release_root: Path) -> None:
    checksum_file = release_root / "checksums.txt"
    if not checksum_file.is_file():
        raise AssertionError(f"missing {checksum_file}")
    for line in checksum_file.read_text(encoding="utf-8").splitlines():
        digest, relative = line.split("  ", 1)
        target = release_root / relative
        if not target.is_file():
            raise AssertionError(f"missing checksummed file: {target}")
        actual = hashlib.sha256(target.read_bytes()).hexdigest()
        if actual != digest:
            raise AssertionError(f"checksum mismatch: {target}")


def main() -> int:
    index = json.loads((DATA_ROOT / "index.json").read_text(encoding="utf-8"))
    if len(index.get("datasets", [])) != 3:
        raise AssertionError("expected three ledger datasets")

    pricing = DATA_ROOT / "cloud-pricing/2026-08-22-v1"
    build = DATA_ROOT / "build-vs-buy/2026-08-24-v1"
    history = DATA_ROOT / "price-history/2026-08-24-v1"
    for release in (pricing, build, history):
        verify_checksums(release)
        for required in ("README.md", "methodology.md", "schema.json", "release.json", "report.md"):
            if not (release / required).is_file():
                raise AssertionError(f"missing release file: {release / required}")

    block = rows(pricing / "tables/block_storage_scenarios.csv")
    by_block = {(r["product"], r["capacity_gib"], r["target_iops"]): r for r in block}
    close(by_block[("EBS gp3", "200", "3000")]["monthly_cny"], 108.5072, "gp3 baseline")
    close(by_block[("EBS gp3", "200", "11800")]["monthly_cny"], 432.67246, "gp3 performance match")
    close(by_block[("ESSD AutoPL baseline", "200", "11800")]["monthly_cny"], 200.0, "AutoPL performance match")

    compute = {r["cloud_offer"]: r for r in rows(build / "tables/compute_breakpoints.csv")}
    if compute["AWS EC2 c7a on-demand"]["durable_cash_crossing_vcpu"] != "14":
        raise AssertionError("AWS on-demand compute crossing changed")
    if compute["Alibaba ECS c8i 5y public term"]["durable_cash_crossing_vcpu"] != "2972":
        raise AssertionError("Alibaba 5y durable compute crossing changed")

    objects = {(r["topology_key"], r["cloud_offer"]): r for r in rows(build / "tables/object_breakpoints.csv")}
    if objects[("aistor8_single", "Alibaba OSS Standard LRS 1y package")]["durable_crossing_logical_tb"] != "199":
        raise AssertionError("single-site object crossing changed")
    if objects[("aistor8_three", "Alibaba OSS Standard LRS 1y package")]["durable_crossing_logical_tb"] != "1223":
        raise AssertionError("three-site object crossing changed")

    baskets = {(r["provider"], r["scenario"]): r for r in rows(history / "tables/basket_metrics.csv")}
    close(baskets[("AWS", "capacity basket")]["change_pct"], -62.954, "AWS basket change")
    close(baskets[("Alibaba Cloud", "monthly subscription basket")]["change_pct"], -4.799, "Alibaba basket change")

    print("ledger assets and headline values OK")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (AssertionError, OSError, ValueError, KeyError) as exc:
        print(f"ledger verification failed: {exc}", file=sys.stderr)
        raise SystemExit(1)

