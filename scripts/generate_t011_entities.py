#!/usr/bin/env python3
"""Generate T011: 80 FIFA national team entities batch 2 (append).

Network: none (local structured data only). Outbound HTTP must use
fetch_utils.RateLimitedFetcher (>=1s/request); see docs/data-collection-policy.md
and .cursor/rules/world-cup-data-collection.mdc."""

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

# (code, name_zh, name_en, aliases) — 其余国家队与历史队名，不与 T010 重复
TEAMS = [
    ("BLR", "白俄罗斯", "Belarus", "白俄罗斯国家队"),
    ("EST", "爱沙尼亚", "Estonia", "爱沙尼亚国家队"),
    ("LVA", "拉脱维亚", "Latvia", "拉脱维亚国家队"),
    ("LTU", "立陶宛", "Lithuania", "立陶宛国家队"),
    ("MDA", "摩尔多瓦", "Moldova", "摩尔多瓦国家队"),
    ("GEO", "格鲁吉亚", "Georgia", "格鲁吉亚国家队"),
    ("ARM", "亚美尼亚", "Armenia", "亚美尼亚国家队"),
    ("AZE", "阿塞拜疆", "Azerbaijan", "阿塞拜疆国家队"),
    ("KAZ", "哈萨克斯坦", "Kazakhstan", "哈萨克斯坦国家队"),
    ("KGZ", "吉尔吉斯斯坦", "Kyrgyzstan", "吉尔吉斯斯坦国家队"),
    ("TJK", "塔吉克斯坦", "Tajikistan", "塔吉克斯坦国家队"),
    ("TKM", "土库曼斯坦", "Turkmenistan", "土库曼斯坦国家队"),
    ("BHR", "巴林", "Bahrain", "巴林国家队"),
    ("KWT", "科威特", "Kuwait", "科威特国家队"),
    ("SYR", "叙利亚", "Syria", "叙利亚国家队"),
    ("LBN", "黎巴嫩", "Lebanon", "黎巴嫩国家队"),
    ("YEM", "也门", "Yemen", "也门国家队"),
    ("PLE", "巴勒斯坦", "Palestine", "巴勒斯坦国家队"),
    ("MYS", "马来西亚", "Malaysia", "马来西亚国家队"),
    ("SGP", "新加坡", "Singapore", "新加坡国家队"),
    ("PHI", "菲律宾", "Philippines", "菲律宾国家队"),
    ("IND", "印度", "India", "印度国家队"),
    ("BGD", "孟加拉国", "Bangladesh", "孟加拉国国家队"),
    ("PAK", "巴基斯坦", "Pakistan", "巴基斯坦国家队"),
    ("NPL", "尼泊尔", "Nepal", "尼泊尔国家队"),
    ("AFG", "阿富汗", "Afghanistan", "阿富汗国家队"),
    ("CPV", "佛得角", "Cape Verde", "佛得角国家队"),
    ("MLI", "马里", "Mali", "马里国家队"),
    ("BFA", "布基纳法索", "Burkina Faso", "布基纳法索国家队"),
    ("ZAM", "赞比亚", "Zambia", "赞比亚国家队"),
    ("ZWE", "津巴布韦", "Zimbabwe", "津巴布韦国家队"),
    ("ANG", "安哥拉", "Angola", "安哥拉国家队"),
    ("TOG", "多哥", "Togo", "多哥国家队"),
    ("GAB", "加蓬", "Gabon", "加蓬国家队"),
    ("GUI", "几内亚", "Guinea", "几内亚国家队"),
    ("SLE", "塞拉利昂", "Sierra Leone", "塞拉利昂国家队"),
    ("BEN", "贝宁", "Benin", "贝宁国家队"),
    ("NER", "尼日尔", "Niger", "尼日尔国家队"),
    ("MRT", "毛里塔尼亚", "Mauritania", "毛里塔尼亚国家队"),
    ("LBY", "利比亚", "Libya", "利比亚国家队"),
    ("COD", "刚果民主共和国", "DR Congo", "刚果金|扎伊尔|民主刚果国家队"),
    ("COG", "刚果共和国", "Congo", "刚果共和国国家队"),
    ("UGA", "乌干达", "Uganda", "乌干达国家队"),
    ("TAN", "坦桑尼亚", "Tanzania", "坦桑尼亚国家队"),
    ("KEN", "肯尼亚", "Kenya", "肯尼亚国家队"),
    ("ETH", "埃塞俄比亚", "Ethiopia", "埃塞俄比亚国家队"),
    ("RWA", "卢旺达", "Rwanda", "卢旺达国家队"),
    ("MWI", "马拉维", "Malawi", "马拉维国家队"),
    ("MOZ", "莫桑比克", "Mozambique", "莫桑比克国家队"),
    ("NAM", "纳米比亚", "Namibia", "纳米比亚国家队"),
    ("BWA", "博茨瓦纳", "Botswana", "博茨瓦纳国家队"),
    ("MAD", "马达加斯加", "Madagascar", "马达加斯加国家队"),
    ("SUR", "苏里南", "Suriname", "苏里南国家队"),
    ("GUY", "圭亚那", "Guyana", "圭亚那国家队"),
    ("TTO", "特立尼达和多巴哥", "Trinidad and Tobago", "特立尼达国家队|特多"),
    ("SLV", "萨尔瓦多", "El Salvador", "萨尔瓦多国家队"),
    ("GTM", "危地马拉", "Guatemala", "危地马拉国家队"),
    ("NIC", "尼加拉瓜", "Nicaragua", "尼加拉瓜国家队"),
    ("CUB", "古巴", "Cuba", "古巴国家队"),
    ("LUX", "卢森堡", "Luxembourg", "卢森堡国家队"),
    ("ALB", "阿尔巴尼亚", "Albania", "阿尔巴尼亚国家队"),
    ("BUL", "保加利亚", "Bulgaria", "保加利亚国家队"),
    ("CYP", "塞浦路斯", "Cyprus", "塞浦路斯国家队"),
    ("MLT", "马耳他", "Malta", "马耳他国家队"),
    ("AND", "安道尔", "Andorra", "安道尔国家队"),
    ("SMR", "圣马力诺", "San Marino", "圣马力诺国家队"),
    ("MNE", "黑山", "Montenegro", "黑山国家队"),
    ("SOV", "苏联", "Soviet Union", "前苏联|苏联国家队|历史队"),
    ("TCH", "捷克斯洛伐克", "Czechoslovakia", "捷克斯洛伐克国家队|历史队"),
    ("YUG", "南斯拉夫", "Yugoslavia", "南斯拉夫国家队|历史队"),
    ("SCG", "塞尔维亚和黑山", "Serbia and Montenegro", "塞黑|塞尔维亚和黑山国家队|历史队"),
    ("GDR", "东德", "East Germany", "民主德国|东德国家队|历史队"),
    ("FRG", "西德", "West Germany", "联邦德国|西德国家队|历史队"),
    ("ZAI", "扎伊尔", "Zaire", "扎伊尔国家队|历史队名"),
    ("RHO", "南罗得西亚", "Rhodesia", "罗得西亚|历史队名"),
    ("DEI", "荷属东印度", "Dutch East Indies", "荷属东印度队|历史队名"),
    ("IFS", "爱尔兰自由邦", "Irish Free State", "爱尔兰历史队名|1924爱尔兰"),
    ("DGE", "德意志帝国", "German Empire", "1912德意志帝国队|历史队"),
    ("BOH", "波希米亚", "Bohemia", "波希米亚国家队|历史队"),
    ("AUH", "奥匈帝国", "Austria-Hungary", "奥匈帝国时期足球队|历史队"),
]


def main() -> None:
    if len(TEAMS) != 80:
        raise SystemExit(f"expected 80 teams, got {len(TEAMS)}")

    existing: list[dict[str, str]] = []
    if OUTPUT.exists():
        with OUTPUT.open(newline="", encoding="utf-8") as f:
            existing = list(csv.DictReader(f))

    existing_ids = {r["entity_id"] for r in existing}
    new_rows = []
    for code, zh, en, aliases in TEAMS:
        eid = f"ENT-TEAM-{code}"
        if eid in existing_ids:
            raise SystemExit(f"duplicate entity_id {eid} (already in entities.csv)")
        new_rows.append({
            "entity_id": eid,
            "entity_type": "team",
            "name_zh": zh,
            "name_en": en,
            "aliases": aliases,
            "country_code": code,
            "related_knowledge_ids": "",
        })

    all_rows = existing + new_rows
    with OUTPUT.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=COLUMNS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(all_rows)
    print(f"Appended {len(new_rows)} teams; total {len(all_rows)} entities")


if __name__ == "__main__":
    main()
