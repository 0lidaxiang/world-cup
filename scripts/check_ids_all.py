#!/usr/bin/env python3
"""T502: Check knowledge_all.csv ID uniqueness and related_ids. Network: none."""

from __future__ import annotations

import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TARGET = ROOT / "data" / "knowledge_all.csv"


def main() -> int:
    rows = list(csv.DictReader(TARGET.open(encoding="utf-8")))
    ids = [r["id"] for r in rows]
    issues: list[str] = []
    if len(ids) != len(set(ids)):
        issues.append("duplicate ids")
    all_ids = set(ids)
    for r in rows:
        for rid in (r.get("related_ids") or "").split(","):
            rid = rid.strip()
            if rid and rid not in all_ids:
                issues.append(f"{r['id']} invalid related_id {rid}")
    if issues:
        print(f"FAIL: {len(issues)} issue(s)")
        for i in issues[:20]:
            print(i)
        return 1
    print(f"PASS: {len(ids)} unique ids, related_ids valid")
    return 0


if __name__ == "__main__":
    sys.exit(main())
