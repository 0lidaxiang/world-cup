#!/usr/bin/env python3
"""Generate T012: World Cup tournament entities 1930-1978 (append to entities.csv).

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

# (year, name_zh, name_en, aliases, host_code)
TOURNAMENTS = [
    ("1930", "1930年乌拉圭世界杯", "1930 FIFA World Cup Uruguay", "第一届世界杯|1930世界杯", "URY"),
    ("1934", "1934年意大利世界杯", "1934 FIFA World Cup Italy", "第二届世界杯|1934世界杯", "ITA"),
    ("1938", "1938年法国世界杯", "1938 FIFA World Cup France", "第三届世界杯|1938世界杯", "FRA"),
    ("1942", "1942年世界杯(取消)", "1942 FIFA World Cup (cancelled)", "因二战取消|未举办", ""),
    ("1950", "1950年巴西世界杯", "1950 FIFA World Cup Brazil", "第四届世界杯|1950世界杯|马拉卡纳", "BRA"),
    ("1954", "1954年瑞士世界杯", "1954 FIFA World Cup Switzerland", "第五届世界杯|1954世界杯", "SUI"),
    ("1958", "1958年瑞典世界杯", "1958 FIFA World Cup Sweden", "第六届世界杯|1958世界杯", "SWE"),
    ("1962", "1962年智利世界杯", "1962 FIFA World Cup Chile", "第七届世界杯|1962世界杯", "CHI"),
    ("1966", "1966年英格兰世界杯", "1966 FIFA World Cup England", "第八届世界杯|1966世界杯", "ENG"),
    ("1970", "1970年墨西哥世界杯", "1970 FIFA World Cup Mexico", "第九届世界杯|1970世界杯", "MEX"),
    ("1974", "1974年西德世界杯", "1974 FIFA World Cup West Germany", "第十届世界杯|1974世界杯", "GER"),
    ("1978", "1978年阿根廷世界杯", "1978 FIFA World Cup Argentina", "第十一届世界杯|1978世界杯", "ARG"),
]


def main() -> None:
    if len(TOURNAMENTS) != 12:
        raise SystemExit(f"expected 12 tournaments, got {len(TOURNAMENTS)}")

    existing: list[dict[str, str]] = []
    if OUTPUT.exists():
        with OUTPUT.open(newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            existing = list(reader)

    new_rows = []
    for year, zh, en, aliases, host in TOURNAMENTS:
        new_rows.append({
            "entity_id": f"ENT-WC-{year}",
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
