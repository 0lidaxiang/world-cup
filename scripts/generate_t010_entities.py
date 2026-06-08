#!/usr/bin/env python3
"""Generate T010: 80 FIFA national team entities (batch 1).

Network: none (local structured data). Outbound HTTP must use fetch_utils.RateLimitedFetcher (>=1s/request); see docs/maintainers/data-collection-policy.md and .cursor/rules/world-cup-data-collection.mdc."""

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

# (code, name_zh, name_en, aliases)
TEAMS = [
    ("BRA", "巴西", "Brazil", "桑巴军团|巴西国家队"),
    ("ARG", "阿根廷", "Argentina", "潘帕斯雄鹰|阿根廷国家队"),
    ("GER", "德国", "Germany", "德意志战车|德国国家队"),
    ("FRA", "法国", "France", "高卢雄鸡|法国国家队"),
    ("ITA", "意大利", "Italy", "蓝衣军团|意大利国家队"),
    ("ESP", "西班牙", "Spain", "斗牛士|西班牙国家队"),
    ("ENG", "英格兰", "England", "三狮军团|英格兰国家队"),
    ("POR", "葡萄牙", "Portugal", "葡萄牙国家队"),
    ("NED", "荷兰", "Netherlands", "橙衣军团|荷兰国家队"),
    ("BEL", "比利时", "Belgium", "欧洲红魔|比利时国家队"),
    ("CRO", "克罗地亚", "Croatia", "格子军团|克罗地亚国家队"),
    ("URU", "乌拉圭", "Uruguay", "天蓝军团|乌拉圭国家队"),
    ("COL", "哥伦比亚", "Colombia", "哥伦比亚国家队"),
    ("MEX", "墨西哥", "Mexico", "墨西哥国家队"),
    ("USA", "美国", "United States", "美国男足|美国国家队"),
    ("CAN", "加拿大", "Canada", "加拿大国家队"),
    ("JPN", "日本", "Japan", "蓝武士|日本国家队"),
    ("KOR", "韩国", "South Korea", "太极虎|韩国国家队"),
    ("AUS", "澳大利亚", "Australia", "袋鼠军团|澳大利亚国家队"),
    ("IRN", "伊朗", "Iran", "波斯铁骑|伊朗国家队"),
    ("SAU", "沙特阿拉伯", "Saudi Arabia", "沙特国家队"),
    ("QAT", "卡塔尔", "Qatar", "卡塔尔国家队"),
    ("MAR", "摩洛哥", "Morocco", "摩洛哥国家队"),
    ("SEN", "塞内加尔", "Senegal", "塞内加尔国家队"),
    ("GHA", "加纳", "Ghana", "加纳国家队"),
    ("NGA", "尼日利亚", "Nigeria", "非洲雄鹰|尼日利亚国家队"),
    ("CMR", "喀麦隆", "Cameroon", "喀麦隆国家队"),
    ("TUN", "突尼斯", "Tunisia", "突尼斯国家队"),
    ("EGY", "埃及", "Egypt", "法老王|埃及国家队"),
    ("RSA", "南非", "South Africa", "南非国家队"),
    ("CIV", "科特迪瓦", "Ivory Coast", "象牙海岸|科特迪瓦国家队"),
    ("ALG", "阿尔及利亚", "Algeria", "阿尔及利亚国家队"),
    ("CRC", "哥斯达黎加", "Costa Rica", "哥斯达黎加国家队"),
    ("PAN", "巴拿马", "Panama", "巴拿马国家队"),
    ("ECU", "厄瓜多尔", "Ecuador", "厄瓜多尔国家队"),
    ("CHI", "智利", "Chile", "智利国家队"),
    ("PER", "秘鲁", "Peru", "秘鲁国家队"),
    ("PAR", "巴拉圭", "Paraguay", "巴拉圭国家队"),
    ("BOL", "玻利维亚", "Bolivia", "玻利维亚国家队"),
    ("VEN", "委内瑞拉", "Venezuela", "委内瑞拉国家队"),
    ("SWE", "瑞典", "Sweden", "瑞典国家队"),
    ("DEN", "丹麦", "Denmark", "丹麦国家队"),
    ("NOR", "挪威", "Norway", "挪威国家队"),
    ("POL", "波兰", "Poland", "波兰国家队"),
    ("SUI", "瑞士", "Switzerland", "瑞士国家队"),
    ("AUT", "奥地利", "Austria", "奥地利国家队"),
    ("CZE", "捷克", "Czech Republic", "捷克国家队"),
    ("SVK", "斯洛伐克", "Slovakia", "斯洛伐克国家队"),
    ("HUN", "匈牙利", "Hungary", "匈牙利国家队"),
    ("ROU", "罗马尼亚", "Romania", "罗马尼亚国家队"),
    ("SRB", "塞尔维亚", "Serbia", "塞尔维亚国家队"),
    ("UKR", "乌克兰", "Ukraine", "乌克兰国家队"),
    ("TUR", "土耳其", "Turkey", "土耳其国家队"),
    ("GRE", "希腊", "Greece", "希腊国家队"),
    ("RUS", "俄罗斯", "Russia", "俄罗斯国家队"),
    ("WAL", "威尔士", "Wales", "威尔士国家队"),
    ("SCO", "苏格兰", "Scotland", "苏格兰国家队"),
    ("IRL", "爱尔兰", "Republic of Ireland", "爱尔兰国家队"),
    ("NIR", "北爱尔兰", "Northern Ireland", "北爱尔兰国家队"),
    ("FIN", "芬兰", "Finland", "芬兰国家队"),
    ("ISL", "冰岛", "Iceland", "冰岛国家队"),
    ("BIH", "波黑", "Bosnia and Herzegovina", "波黑国家队"),
    ("MKD", "北马其顿", "North Macedonia", "北马其顿国家队"),
    ("SVN", "斯洛文尼亚", "Slovenia", "斯洛文尼亚国家队"),
    ("JAM", "牙买加", "Jamaica", "牙买加国家队"),
    ("HAI", "海地", "Haiti", "海地国家队"),
    ("CUW", "库拉索", "Curaçao", "库拉索国家队"),
    ("NZL", "新西兰", "New Zealand", "新西兰国家队"),
    ("CHN", "中国", "China", "国足|中国男足|中国国家队"),
    ("PRK", "朝鲜", "North Korea", "朝鲜国家队"),
    ("IRQ", "伊拉克", "Iraq", "伊拉克国家队"),
    ("UAE", "阿联酋", "United Arab Emirates", "阿联酋国家队"),
    ("OMA", "阿曼", "Oman", "阿曼国家队"),
    ("JOR", "约旦", "Jordan", "约旦国家队"),
    ("ISR", "以色列", "Israel", "以色列国家队"),
    ("UZB", "乌兹别克斯坦", "Uzbekistan", "乌兹别克斯坦国家队"),
    ("THA", "泰国", "Thailand", "泰国国家队"),
    ("VIE", "越南", "Vietnam", "越南国家队"),
    ("IDN", "印度尼西亚", "Indonesia", "印度尼西亚国家队"),
    ("HON", "洪都拉斯", "Honduras", "洪都拉斯国家队"),
]


def main() -> None:
    if len(TEAMS) != 80:
        raise SystemExit(f"expected 80 teams, got {len(TEAMS)}")

    rows = []
    for code, zh, en, aliases in TEAMS:
        rows.append({
            "entity_id": f"ENT-TEAM-{code}",
            "entity_type": "team",
            "name_zh": zh,
            "name_en": en,
            "aliases": aliases,
            "country_code": code,
            "related_knowledge_ids": "",
        })

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=COLUMNS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote {len(rows)} team entities to {OUTPUT}")


if __name__ == "__main__":
    main()
