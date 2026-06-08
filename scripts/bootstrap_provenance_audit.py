#!/usr/bin/env python3
"""
Bootstrap default provenance rows from knowledge CSV files.

For v1 local-structured batches: rewrite_mode=local_structured, fetch_method=none.
External-fetch rows should be edited manually with source_url and collected_at.

Network: none (local structured data only).
"""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
AUDIT_COLUMNS = [
    "knowledge_id",
    "source_url",
    "collected_at",
    "rewrite_mode",
    "fetch_method",
    "notes",
]
REWRITE_MODES = {"local_structured", "fact_restated", "verbatim_excerpt"}
FETCH_METHODS = {"none", "rate_limited_script", "agent_manual"}


def discover_knowledge_files(data_dir: Path) -> list[Path]:
    files = sorted(data_dir.glob("knowledge_*.csv"))
    return [p for p in files if p.name not in ("knowledge_template.csv", "knowledge_all.csv")]


def load_existing_audit(path: Path) -> dict[str, dict[str, str]]:
    if not path.exists():
        return {}
    with path.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    return {(r.get("knowledge_id") or "").strip(): r for r in rows if (r.get("knowledge_id") or "").strip()}


def default_row(knowledge_id: str, updated_at: str, source_ref: str) -> dict[str, str]:
    notes = "v1 local structured batch"
    if source_ref.strip():
        notes = f"{notes}; source_ref={source_ref.strip()[:120]}"
    return {
        "knowledge_id": knowledge_id,
        "source_url": "",
        "collected_at": updated_at or "2026-06-05",
        "rewrite_mode": "local_structured",
        "fetch_method": "none",
        "notes": notes,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Bootstrap provenance_audit.csv from knowledge files")
    parser.add_argument(
        "--output",
        type=Path,
        default=ROOT / "data" / "provenance_audit.csv",
        help="Output provenance audit CSV",
    )
    parser.add_argument("--dry-run", action="store_true", help="Print counts only")
    parser.add_argument("--overwrite", action="store_true", help="Replace file; default merges new ids only")
    args = parser.parse_args()

    data_dir = ROOT / "data"
    existing = {} if args.overwrite else load_existing_audit(args.output)
    added = 0

    for path in discover_knowledge_files(data_dir):
        with path.open(newline="", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                kid = (row.get("id") or "").strip()
                if not kid or kid in existing:
                    continue
                existing[kid] = default_row(
                    kid,
                    (row.get("updated_at") or "").strip(),
                    (row.get("source_ref") or "").strip(),
                )
                added += 1

    if args.dry_run:
        print(f"would write {len(existing)} rows ({added} new)")
        return 0

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=AUDIT_COLUMNS, lineterminator="\n")
        writer.writeheader()
        for kid in sorted(existing.keys()):
            writer.writerow(existing[kid])

    print(f"wrote {len(existing)} provenance rows to {args.output} ({added} new)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
