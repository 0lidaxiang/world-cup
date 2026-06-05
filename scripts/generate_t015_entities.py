#!/usr/bin/env python3
"""Generate T015: 100 legendary player entities (append).

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

# (slug, name_zh, name_en, birth_year, country_code, aliases)
PLAYERS = [
    ("PELE", "贝利", "Pelé", "1940", "BRA", "球王|佩莱|贝利三世"),
    ("MARADONA", "马拉多纳", "Diego Maradona", "1960", "ARG", "迭戈|球王马拉多纳|上帝之手"),
    ("MESSI", "梅西", "Lionel Messi", "1987", "ARG", "里奥·梅西|梅老板|小跳蚤"),
    ("RONALDO", "罗纳尔多", "Ronaldo Nazário", "1976", "BRA", "大罗|外星人|R9"),
    ("CRISTIANO", "C罗", "Cristiano Ronaldo", "1985", "POR", "克里斯蒂亚诺·罗纳尔多|C罗"),
    ("ZIDANE", "齐达内", "Zinedine Zidane", "1972", "FRA", "齐祖|齐达内"),
    ("CRUYFF", "克鲁伊夫", "Johan Cruyff", "1947", "NED", "飞翔的荷兰人|克鲁伊夫"),
    ("BECKENBAUER", "贝肯鲍尔", "Franz Beckenbauer", "1945", "GER", "足球皇帝|贝皇"),
    ("PLATINI", "普拉蒂尼", "Michel Platini", "1955", "FRA", "普拉蒂尼"),
    ("KLOSE", "克洛泽", "Miroslav Klose", "1978", "GER", "米洛|世界杯射手王"),
    ("MULLER", "盖德·穆勒", "Gerd Müller", "1945", "GER", "轰炸机|盖德穆勒"),
    ("FONTAINE", "方丹", "Just Fontaine", "1933", "FRA", "方丹|单届13球"),
    ("BATISTUTA", "巴蒂斯图塔", "Gabriel Batistuta", "1969", "ARG", "战神巴蒂|巴蒂"),
    ("ROMARIO", "罗马里奥", "Romário", "1966", "BRA", "独狼|罗马里奥"),
    ("RIVALDO", "里瓦尔多", "Rivaldo", "1972", "BRA", "里瓦尔多"),
    ("RONALDINHO", "罗纳尔迪尼奥", "Ronaldinho", "1980", "BRA", "小罗|Ronaldinho Gaúcho"),
    ("NEYMAR", "内马尔", "Neymar", "1992", "BRA", "内马尔"),
    ("CAFU", "卡福", "Cafu", "1970", "BRA", "卡福队长"),
    ("CARLOS", "罗伯特·卡洛斯", "Roberto Carlos", "1973", "BRA", "重炮手|卡洛斯"),
    ("GARRINCHA", "加林查", "Garrincha", "1933", "BRA", "小鸟|加林查"),
    ("ZICO", "济科", "Zico", "1953", "BRA", "白贝利|济科"),
    ("SOCRATES", "苏格拉底", "Sócrates", "1954", "BRA", "苏格拉底博士"),
    ("DIDA", "迪达", "Dida", "1973", "BRA", "迪达门将"),
    ("TAFFAREL", "塔法雷尔", "Cláudio Taffarel", "1966", "BRA", "塔法雷尔"),
    ("RUMMENIGGE", "鲁梅尼格", "Karl-Heinz Rummenigge", "1955", "GER", "鲁梅尼格"),
    ("MATTHAUS", "马特乌斯", "Lothar Matthäus", "1961", "GER", "马特乌斯"),
    ("KLINSMANN", "克林斯曼", "Jürgen Klinsmann", "1964", "GER", "金色轰炸机|克林斯曼"),
    ("SCHWEINSTEIGER", "施魏因施泰格", "Bastian Schweinsteiger", "1984", "GER", "小猪|施魏因施泰格"),
    ("BALLACK", "巴拉克", "Michael Ballack", "1976", "GER", "巴拉克"),
    ("NEUER", "诺伊尔", "Manuel Neuer", "1986", "GER", "小新|诺伊尔"),
    ("KROOS", "克罗斯", "Toni Kroos", "1990", "GER", "TK|克罗斯"),
    ("THOMAS-MULLER", "托马斯·穆勒", "Thomas Müller", "1989", "GER", "二娃|托马斯穆勒"),
    ("OZIL", "厄齐尔", "Mesut Özil", "1988", "GER", "厄齐尔|272"),
    ("GOTZE", "格策", "Mario Götze", "1992", "GER", "格策"),
    ("MALDINI", "马尔蒂尼", "Paolo Maldini", "1968", "ITA", "保罗马尔蒂尼|马尔蒂尼"),
    ("BARESI", "巴雷西", "Franco Baresi", "1964", "ITA", "巴雷西"),
    ("NESTA", "内斯塔", "Alessandro Nesta", "1976", "ITA", "内斯塔"),
    ("CANNAVARO", "卡纳瓦罗", "Fabio Cannavaro", "1973", "ITA", "卡纳瓦罗"),
    ("BUFFON", "布冯", "Gianluigi Buffon", "1978", "ITA", "布冯|Gigi"),
    ("BAGGIO", "巴乔", "Roberto Baggio", "1967", "ITA", "忧郁王子|巴乔"),
    ("DEL-PIERO", "德尔·皮耶罗", "Alessandro Del Piero", "1974", "ITA", "皮耶罗|德尔皮耶罗"),
    ("TOTTI", "托蒂", "Francesco Totti", "1976", "ITA", "罗马王子|托蒂"),
    ("PIRLO", "皮尔洛", "Andrea Pirlo", "1979", "ITA", "皮尔洛|睡皮"),
    ("ROSSI", "罗西", "Paolo Rossi", "1946", "ITA", "保罗·罗西|1982罗西"),
    ("SCHILLACI", "斯基拉奇", "Salvatore Schillaci", "1964", "ITA", "斯基拉奇|世界杯英雄"),
    ("CHARLTON", "博比·查尔顿", "Bobby Charlton", "1937", "ENG", "查尔顿爵士|博比查尔顿"),
    ("MOORE", "博比·摩尔", "Bobby Moore", "1941", "ENG", "博比摩尔|1966队长"),
    ("BANKS", "班克斯", "Gordon Banks", "1937", "ENG", "戈登·班克斯|班克斯"),
    ("LINEKER", "莱因克尔", "Gary Lineker", "1960", "ENG", "莱因克尔|九爷"),
    ("BECKHAM", "贝克汉姆", "David Beckham", "1975", "ENG", "小贝|贝克汉姆"),
    ("OWEN", "欧文", "Michael Owen", "1979", "ENG", "迈克尔·欧文|追风少年"),
    ("ROONEY", "鲁尼", "Wayne Rooney", "1985", "ENG", "鲁尼|小胖"),
    ("GERRARD", "杰拉德", "Steven Gerrard", "1980", "ENG", "杰拉德|Captain Fantastic"),
    ("LAMPARD", "兰帕德", "Frank Lampard", "1978", "ENG", "兰帕德|神灯"),
    ("KANE", "凯恩", "Harry Kane", "1993", "ENG", "哈里·凯恩|凯恩"),
    ("XAVI", "哈维", "Xavi Hernández", "1980", "ESP", "哈维|巴萨大脑"),
    ("INIESTA", "伊涅斯塔", "Andrés Iniesta", "1984", "ESP", "小白|伊涅斯塔"),
    ("PUJOL", "普约尔", "Carles Puyol", "1978", "ESP", "普约尔|狮王"),
    ("CASILLAS", "卡西利亚斯", "Iker Casillas", "1981", "ESP", "卡西|圣卡西"),
    ("RAUL", "劳尔", "Raúl González", "1978", "ESP", "劳尔|指环王"),
    ("VILLA", "比利亚", "David Villa", "1981", "ESP", "葫芦娃|比利亚"),
    ("TORRES", "托雷斯", "Fernando Torres", "1984", "ESP", "金童|托雷斯"),
    ("HENRY", "亨利", "Thierry Henry", "1977", "FRA", "海布里之王|亨利"),
    ("THURAM", "图拉姆", "Lilian Thuram", "1972", "FRA", "图拉姆"),
    ("VIEIRA", "维埃拉", "Patrick Vieira", "1970", "FRA", "维埃拉"),
    ("TREZEGUET", "特雷泽盖", "David Trezeguet", "1977", "FRA", "特雷泽盖"),
    ("DESAILLY", "德塞利", "Marcel Desailly", "1968", "FRA", "德塞利"),
    ("PETIT", "佩蒂", "Emmanuel Petit", "1970", "FRA", "佩蒂"),
    ("MBAPPE", "姆巴佩", "Kylian Mbappé", "1998", "FRA", "姆巴佩|姆总"),
    ("GRIEZMANN", "格列兹曼", "Antoine Griezmann", "1991", "FRA", "格子|格列兹曼"),
    ("MODRIC", "莫德里奇", "Luka Modrić", "1985", "CRO", "魔笛|莫德里奇"),
    ("SUKER", "苏克", "Davor Šuker", "1968", "CRO", "苏克|金左脚"),
    ("FIGO", "菲戈", "Luís Figo", "1972", "POR", "菲戈|黄金一代"),
    ("EUSEBIO", "尤西比奥", "Eusébio", "1942", "POR", "黑豹|尤西比奥"),
    ("VAN-BASTEN", "范巴斯滕", "Marco van Basten", "1964", "NED", "范巴斯滕|芭蕾王子"),
    ("GULLIT", "古利特", "Ruud Gullit", "1963", "NED", "古利特|路德"),
    ("RIJKARD", "里杰卡尔德", "Frank Rijkaard", "1962", "NED", "里杰卡尔德"),
    ("ROBBEN", "罗本", "Arjen Robben", "1984", "NED", "罗本|小飞侠"),
    ("VAN-PERSIE", "范佩西", "Robin van Persie", "1983", "NED", "范佩西|罗宾侠"),
    ("YASHIN", "雅辛", "Lev Yashin", "1929", "SOV", "黑蜘蛛|雅辛"),
    ("PUSKAS", "普斯卡什", "Ferenc Puskás", "1927", "HUN", "普斯卡什|匈牙利魔术师"),
    ("DI-STEFANO", "迪·斯蒂法诺", "Alfredo Di Stéfano", "1926", "ARG", "迪斯蒂法诺|金箭头"),
    ("KEMPES", "肯佩斯", "Mario Kempes", "1954", "ARG", "肯佩斯|1978英雄"),
    ("PASSARELLA", "帕萨雷拉", "Daniel Passarella", "1953", "ARG", "帕萨雷拉"),
    ("NEDVED", "内德维德", "Pavel Nedvěd", "1972", "CZE", "内德维德|捷克铁人"),
    ("SHEVCHENKO", "舍甫琴科", "Andriy Shevchenko", "1976", "UKR", "舍瓦|舍甫琴科"),
    ("FORLAN", "弗兰", "Diego Forlán", "1979", "URU", "弗兰|2010金球"),
    ("SUAREZ", "苏亚雷斯", "Luis Suárez", "1987", "URU", "苏牙|苏亚雷斯"),
    ("CAVANI", "卡瓦尼", "Edinson Cavani", "1987", "URU", "卡瓦尼|El Matador"),
    ("ETO", "埃托奥", "Samuel Eto'o", "1981", "CMR", "埃托奥|猎豹"),
    ("DROGBA", "德罗巴", "Didier Drogba", "1978", "CIV", "魔兽|德罗巴"),
    ("WEAH", "维阿", "George Weah", "1966", "LBR", "维阿|非洲金球"),
    ("SALAH", "萨拉赫", "Mohamed Salah", "1992", "EGY", "萨拉赫|埃及法老"),
    ("MANE", "马内", "Sadio Mané", "1992", "SEN", "马内"),
    ("DONOVAN", "多诺万", "Landon Donovan", "1982", "USA", "多诺万|美国队长"),
    ("VALDERRAMA", "巴尔德拉马", "Carlos Valderrama", "1961", "COL", "金毛狮王|巴尔德拉马"),
    ("JAMES", "J罗", "James Rodríguez", "1991", "COL", "哈梅斯·罗德里格斯|J罗"),
    ("HAZARD", "阿扎尔", "Eden Hazard", "1991", "BEL", "阿扎尔|扎球王"),
    ("DE-BRUYNE", "德布劳内", "Kevin De Bruyne", "1991", "BEL", "丁丁|德布劳内"),
    ("BEST", "乔治·贝斯特", "George Best", "1946", "NIR", "乔治贝斯特|北爱尔兰传奇"),
]

assert len(PLAYERS) == 100


def main() -> None:
    if len(PLAYERS) != 100:
        raise SystemExit(f"expected 100 players, got {len(PLAYERS)}")

    seen_slug_year: set[tuple[str, str]] = set()
    for slug, _zh, _en, year, _cc, _aliases in PLAYERS:
        key = (slug, year)
        if key in seen_slug_year:
            raise SystemExit(f"duplicate slug+year: {slug}-{year}")
        seen_slug_year.add(key)

    existing: list[dict[str, str]] = []
    if OUTPUT.exists():
        with OUTPUT.open(newline="", encoding="utf-8") as f:
            existing = list(csv.DictReader(f))

    existing_ids = {r["entity_id"] for r in existing}
    new_rows = []
    for slug, zh, en, year, cc, aliases in PLAYERS:
        eid = f"ENT-PLR-{slug}-{year}"
        if eid in existing_ids:
            raise SystemExit(f"duplicate entity_id {eid} (already in entities.csv)")
        new_rows.append({
            "entity_id": eid,
            "entity_type": "player",
            "name_zh": zh,
            "name_en": en,
            "aliases": aliases,
            "country_code": cc,
            "related_knowledge_ids": "",
        })

    all_rows = existing + new_rows
    with OUTPUT.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=COLUMNS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(all_rows)
    print(f"Appended {len(new_rows)} players; total {len(all_rows)} entities")


if __name__ == "__main__":
    main()
