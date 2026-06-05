#!/usr/bin/env python3
"""Generate T013: World Cup tournament entities 1982-2006 (append).

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

# 1982-2006 七届 men's World Cup + 五届联合会杯(同周期 FIFA 赛事，便于检索)
TOURNAMENTS = [
    ("1982", "1982年西班牙世界杯", "1982 FIFA World Cup Spain", "第12届世界杯|1982世界杯|西班牙世界杯", "ESP"),
    ("1986", "1986年墨西哥世界杯", "1986 FIFA World Cup Mexico", "第13届世界杯|1986世界杯|墨西哥世界杯", "MEX"),
    ("1990", "1990年意大利世界杯", "1990 FIFA World Cup Italy", "第14届世界杯|1990世界杯|意大利世界杯", "ITA"),
    ("1994", "1994年美国世界杯", "1994 FIFA World Cup USA", "第15届世界杯|1994世界杯|美国世界杯", "USA"),
    ("1998", "1998年法国世界杯", "1998 FIFA World Cup France", "第16届世界杯|1998世界杯|法国世界杯", "FRA"),
    ("2002", "2002年韩日世界杯", "2002 FIFA World Cup Korea Japan", "第17届世界杯|2002世界杯|韩日世界杯", "KOR"),
    ("2006", "2006年德国世界杯", "2006 FIFA World Cup Germany", "第18届世界杯|2006世界杯|德国世界杯", "GER"),
    ("1992", "1992年联合会杯", "1992 King Fahd Cup", "联合会杯前身|法赫德国王杯", "KSA"),
    ("1995", "1995年联合会杯", "1995 FIFA Confederations Cup", "1995联合会杯", "KSA"),
    ("1997", "1997年联合会杯", "1997 FIFA Confederations Cup", "1997联合会杯", "KSA"),
    ("2001", "2001年联合会杯", "2001 FIFA Confederations Cup", "2001联合会杯|韩日联合会杯", "KOR"),
    ("2005", "2005年联合会杯", "2005 FIFA Confederations Cup", "2005联合会杯|德国联合会杯", "GER"),
]


def main() -> None:
    if len(TOURNAMENTS) != 12:
        raise SystemExit(f"expected 12 tournaments, got {len(TOURNAMENTS)}")

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
