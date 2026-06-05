#!/usr/bin/env python3
"""Generate T014: World Cup tournament entities 2010-2026 (append).

Network: none (local structured data). Outbound HTTP must use fetch_utils.RateLimitedFetcher (>=1s/request); see docs/data-collection-policy.md and .cursor/rules/world-cup-data-collection.mdc."""

from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUTPUT = ROOT / "data" / "entities.csv"

COLUMNS = [
    "entity_id",
    "entity_type",
    "name_zh",
    "name_en",
    "aliases",
    "country_code",
    "related_knowledge_ids",
]

TOURNAMENTS = [
    ("2010", "2010年南非世界杯", "2010 FIFA World Cup South Africa", "第19届世界杯|2010世界杯|南非世界杯", "RSA"),
    ("2014", "2014年巴西世界杯", "2014 FIFA World Cup Brazil", "第20届世界杯|2014世界杯", "BRA"),
    ("2018", "2018年俄罗斯世界杯", "2018 FIFA World Cup Russia", "第21届世界杯|2018世界杯|俄罗斯世界杯", "RUS"),
    ("2022", "2022年卡塔尔世界杯", "2022 FIFA World Cup Qatar", "第22届世界杯|2022世界杯|卡塔尔世界杯", "QAT"),
    ("2026", "2026年美加墨世界杯", "2026 FIFA World Cup USA Canada Mexico", "第23届世界杯|2026世界杯|扩军48队", "USA"),
]


def main() -> None:
    if len(TOURNAMENTS) != 5:
        raise SystemExit(f"expected 5 tournaments, got {len(TOURNAMENTS)}")

    existing: list[dict[str, str]] = []
    if OUTPUT.exists():
        with OUTPUT.open(newline="", encoding="utf-8") as f:
            existing = list(csv.DictReader(f))

    existing_ids = {r["entity_id"] for r in existing}
    new_rows = []
    for year, zh, en, aliases, host in TOURNAMENTS:
        eid = f"ENT-WC-{year}"
        if eid in existing_ids:
            continue
        new_rows.append({
            "entity_id": eid,
            "entity_type": "tournament",
            "name_zh": zh,
            "name_en": en,
            "aliases": aliases,
            "country_code": host,
            "related_knowledge_ids": "",
        })

    all_rows = existing + new_rows
    with OUTPUT.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=COLUMNS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(all_rows)
    print(f"Appended {len(new_rows)} tournaments; total {len(all_rows)} entities")


if __name__ == "__main__":
    main()
