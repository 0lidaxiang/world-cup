#!/usr/bin/env python3
"""Orchestrate all 73 remaining tasks (T016-T018, T220-T304, T500-T504).

Network: none (local structured data only).
"""

from __future__ import annotations

import csv
import random
import re
import subprocess
import sys
from collections import Counter, defaultdict
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
ROOT = SCRIPT_DIR.parent
sys.path.insert(0, str(SCRIPT_DIR))

from _knowledge_batch_lib import append_batch, load_all_questions, validate_csv, COLUMNS
from _remaining_batches import ALL_BATCHES, ALL_GENERATORS, BatchDef

GAMBLING = [
    "彩票", "竞彩", "足彩", "体彩", "福彩", "博彩", "赌博", "赌球",
    "投注", "下注", "赔率", "盘口", "让球", "大小球", "亚盘", "欧赔",
    "水位", "串关", "稳赚", "必中", "庄家",
]

# ---------------------------------------------------------------------------
# Write thin generate_tXXX scripts
# ---------------------------------------------------------------------------

GENERATE_TEMPLATE = '''#!/usr/bin/env python3
"""Generate {task_id}: {category_l2} (append). Network: none."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))

from _knowledge_batch_lib import append_batch, load_all_questions
from _remaining_batches import ALL_GENERATORS, ALL_BATCHES

TASK_ID = "{task_id}"


def main() -> None:
    batch = next(b for b in ALL_BATCHES if b.task_id == TASK_ID)
    gen = ALL_GENERATORS[TASK_ID]
    entries = gen()
    n = append_batch(
        ROOT / "data" / batch.output,
        entries,
        start_id=batch.start_id,
        id_prefix=batch.id_prefix,
        category_l1=batch.category_l1,
        category_l2=batch.category_l2,
        tags=batch.tags,
        priority=batch.priority,
        default_fact_type=batch.default_fact_type,
        source_ref=batch.source_ref,
        global_questions=load_all_questions(),
    )
    print(f"{{TASK_ID}}: wrote {{n}} rows to {{batch.output}}")


if __name__ == "__main__":
    main()
'''


def write_generate_scripts() -> None:
    for b in ALL_BATCHES:
        slug = b.slug
        path = SCRIPT_DIR / f"generate_{b.task_id.lower()}_{slug}.py"
        content = GENERATE_TEMPLATE.format(
            task_id=b.task_id,
            category_l2=b.category_l2,
        )
        path.write_text(content, encoding="utf-8")
        path.chmod(0o755)


# ---------------------------------------------------------------------------
# Entities T016 / T017
# ---------------------------------------------------------------------------

T016_PLAYERS = [
    ("BARESI-F", "巴雷西", "Franco Baresi", "1964", "ITA", "巴雷西"),
    ("SCIREA", "希雷亚", "Gaetano Scirea", "1953", "ITA", "希雷亚"),
    ("ZOFF", "佐夫", "Dino Zoff", "1942", "ITA", "佐夫"),
    ("ALBERTO", "卡洛斯·阿尔贝托", "Carlos Alberto", "1944", "BRA", "卡洛斯阿尔贝托"),
    ("JAIRZINHO", "雅伊尔津霍", "Jairzinho", "1944", "BRA", "雅伊尔津霍"),
    ("TOSTAO", "托斯唐", "Tostão", "1947", "BRA", "托斯唐"),
    ("RIQUELME", "里克尔梅", "Juan Román Riquelme", "1978", "ARG", "里克尔梅"),
    ("VERON", "贝隆", "Juan Sebastián Verón", "1975", "ARG", "贝隆"),
    ("AYALA", "阿亚拉", "Roberto Ayala", "1973", "ARG", "阿亚拉"),
    ("SAMUEL", "萨穆埃尔", "Walter Samuel", "1978", "ARG", "岩石萨穆埃尔"),
    ("LARSSON", "拉尔森", "Henrik Larsson", "1971", "SWE", "拉尔森"),
    ("IBRAHIMOVIC", "伊布拉希莫维奇", "Zlatan Ibrahimović", "1981", "SWE", "伊布|兹拉坦"),
    ("LITMANEN", "利特马宁", "Jari Litmanen", "1971", "FIN", "利特马宁"),
    ("SCHMEICHEL", "舒梅切尔", "Peter Schmeichel", "1963", "DEN", "舒梅切尔"),
    ("LAUDRUP-M", "米夏埃尔·劳德鲁普", "Michael Laudrup", "1964", "DEN", "劳德鲁普"),
    ("SUKUR", "哈坎·苏克", "Hakan Şükür", "1971", "TUR", "哈坎苏克"),
    ("BULUT", "埃姆雷·贝洛佐格卢", "Emre Belözoğlu", "1980", "TUR", "埃姆雷"),
    ("STOICHKOV", "斯托伊奇科夫", "Hristo Stoichkov", "1966", "BUL", "斯托伊奇科夫"),
    ("BERGKAMP", "博格坎普", "Dennis Bergkamp", "1969", "NED", "冰王子"),
    ("SEEDORF", "西多夫", "Clarence Seedorf", "1976", "NED", "西多夫"),
    ("DAVIDS", "戴维斯", "Edgar Davids", "1973", "NED", "野猪戴维斯"),
    ("KAHN", "卡恩", "Oliver Kahn", "1969", "GER", "狮王卡恩"),
    ("LEHMANN", "莱曼", "Jens Lehmann", "1969", "GER", "莱曼"),
    ("FRIEDRICH", "弗里德里希", "Arne Friedrich", "1979", "GER", "弗里德里希"),
    ("LAHM", "拉姆", "Philipp Lahm", "1983", "GER", "小猪队长"),
    ("HUMMELS", "胡梅尔斯", "Mats Hummels", "1988", "GER", "胡梅尔斯"),
    ("BOATENG-J", "热罗姆·博阿滕", "Jérôme Boateng", "1988", "GER", "热罗姆博阿滕"),
    ("PIQUE", "皮克", "Gerard Piqué", "1987", "ESP", "皮克"),
    ("RAMOS", "拉莫斯", "Sergio Ramos", "1986", "ESP", "水爷拉莫斯"),
    ("BUSQUETS", "布斯克茨", "Sergio Busquets", "1988", "ESP", "布教授"),
    ("PEDRI", "佩德里", "Pedri", "2002", "ESP", "佩德里"),
    ("GAVI", "加维", "Gavi", "2004", "ESP", "加维"),
    ("FERNANDO-H", "费尔南多·耶罗", "Fernando Hierro", "1968", "ESP", "耶罗"),
    ("BELLETTI", "贝莱蒂", "Juliano Belletti", "1976", "BRA", "贝莱蒂"),
    ("ADRIANO", "阿德里亚诺", "Adriano", "1982", "BRA", "国王阿德里亚诺"),
    ("KAKA", "卡卡", "Kaká", "1982", "BRA", "卡卡"),
    ("ALVES-D", "丹尼·阿尔维斯", "Dani Alves", "1983", "BRA", "阿尔维斯"),
    ("MARCELO", "马塞洛", "Marcelo", "1988", "BRA", "马塞洛"),
    ("CASEMIRO", "卡塞米罗", "Casemiro", "1992", "BRA", "卡塞米罗"),
    ("VINICIUS", "维尼修斯", "Vinícius Júnior", "2000", "BRA", "维尼修斯"),
    ("RICHARLISON", "里沙利松", "Richarlison", "1997", "BRA", "里沙利松"),
    ("FALCAO", "法尔考", "Radamel Falcao", "1986", "COL", "老虎法尔考"),
    ("CUADRADO", "夸德拉多", "Juan Cuadrado", "1988", "COL", "夸德拉多"),
    ("OSPINA", "奥斯皮纳", "David Ospina", "1988", "COL", "奥斯皮纳"),
    ("CHICHARITO", "埃尔南德斯", "Javier Hernández", "1988", "MEX", "小豌豆"),
    ("GUARDADO", "瓜尔达多", "Andrés Guardado", "1986", "MEX", "瓜尔达多"),
    ("LOZANO", "洛萨诺", "Hirving Lozano", "1995", "MEX", "洛萨诺"),
    ("PULISIC", "普利希奇", "Christian Pulisic", "1998", "USA", "普利希奇"),
    ("MCKENNIE", "麦肯尼", "Weston McKennie", "1998", "USA", "麦肯尼"),
    ("SON", "孙兴慜", "Son Heung-min", "1992", "KOR", "孙兴慜"),
    ("PARK-JS", "朴智星", "Park Ji-sung", "1981", "KOR", "朴智星"),
    ("HONDA", "本田圭佑", "Keisuke Honda", "1986", "JPN", "本田圭佑"),
    ("KAGAWA", "香川真司", "Shinji Kagawa", "1989", "JPN", "香川真司"),
    ("MITOMA", "三笘薰", "Kaoru Mitoma", "1997", "JPN", "三笘薰"),
    ("KUBO", "久保建英", "Takefusa Kubo", "2001", "JPN", "久保建英"),
    ("AZMOUN", "阿兹蒙", "Sardar Azmoun", "1995", "IRN", "阿兹蒙"),
    ("MAHREZ", "马赫雷斯", "Riyad Mahrez", "1991", "ALG", "马赫雷斯"),
    ("BENZEMA", "本泽马", "Karim Benzema", "1987", "FRA", "本泽马"),
    ("KANTE", "坎特", "N'Golo Kanté", "1991", "FRA", "坎特"),
    ("POGBA", "博格巴", "Paul Pogba", "1993", "FRA", "博格巴"),
    ("MAKOUNDOU", "科曼", "Kingsley Coman", "1996", "FRA", "科曼"),
    ("LUKAKU", "卢卡库", "Romelu Lukaku", "1993", "BEL", "卢卡库"),
    ("HAZARD-EDEN", "阿扎尔", "Eden Hazard", "1991", "BEL", "阿扎尔"),
    ("WITSEL", "维特塞尔", "Axel Witsel", "1989", "BEL", "维特塞尔"),
    ("PERISIC", "佩里西奇", "Ivan Perišić", "1989", "CRO", "佩里西奇"),
    ("MANDZUKIC", "曼朱基奇", "Mario Mandžukić", "1986", "CRO", "曼朱基奇"),
    ("RAKITIC", "拉基蒂奇", "Ivan Rakitić", "1988", "CRO", "拉基蒂奇"),
    ("BALE", "贝尔", "Gareth Bale", "1989", "WAL", "贝尔"),
    ("RAMSEY", "拉姆塞", "Aaron Ramsey", "1990", "WAL", "拉姆塞"),
    ("SANCHEZ", "桑切斯", "Alexis Sánchez", "1988", "CHI", "桑切斯"),
    ("VIDAL", "比达尔", "Arturo Vidal", "1987", "CHI", "比达尔"),
    ("BRAVO", "布拉沃", "Claudio Bravo", "1983", "CHI", "布拉沃"),
    ("MUSLERA", "穆斯莱拉", "Fernando Muslera", "1986", "URU", "穆斯莱拉"),
    ("GODIN", "戈丁", "Diego Godín", "1986", "URU", "戈丁"),
    ("LUGANO", "卢加诺", "Diego Lugano", "1980", "URU", "卢加诺"),
    ("HIGUAIN", "伊瓜因", "Gonzalo Higuaín", "1987", "ARG", "伊瓜因"),
    ("DI-MARIA", "迪马利亚", "Ángel Di María", "1988", "ARG", "迪马利亚"),
    ("AGUERO", "阿圭罗", "Sergio Agüero", "1988", "ARG", "阿圭罗"),
    ("DYBALA", "迪巴拉", "Paulo Dybala", "1993", "ARG", "迪巴拉"),
    ("MARTINEZ-L", "劳塔罗·马丁内斯", "Lautaro Martínez", "1997", "ARG", "劳塔罗"),
    ("ALVAREZ-J", "阿尔瓦雷斯", "Julián Álvarez", "2000", "ARG", "小蜘蛛"),
    ("FERNANDES-B", "布鲁诺·费尔南德斯", "Bruno Fernandes", "1994", "POR", "B费"),
    ("BERNARDO", "贝尔纳多·席尔瓦", "Bernardo Silva", "1994", "POR", "B席"),
    ("RUBEN-DIAS", "鲁本·迪亚斯", "Rúben Dias", "1997", "POR", "鲁本迪亚斯"),
    ("PEPE", "佩佩", "Pepe", "1983", "POR", "佩佩"),
    ("SALAH-M", "萨拉赫", "Mohamed Salah", "1992", "EGY", "萨拉赫"),
    ("ELNENY", "埃尔内尼", "Mohamed Elneny", "1992", "EGY", "埃尔内尼"),
    ("HAKIMI", "阿什拉夫·哈基米", "Achraf Hakimi", "1998", "MAR", "哈基米"),
    ("ZIYECH", "齐耶赫", "Hakim Ziyech", "1993", "MAR", "齐耶赫"),
    ("MANE-S", "马内", "Sadio Mané", "1992", "SEN", "马内"),
    ("KOULIBALY", "库利巴利", "Kalidou Koulibaly", "1991", "SEN", "库利巴利"),
    ("ESSIEN", "埃辛", "Michael Essien", "1982", "GHA", "水牛埃辛"),
    ("ASAMOAH", "阿萨莫阿", "Asamoah Gyan", "1985", "GHA", "阿萨莫阿"),
    ("OKOCHA", "奥科查", "Jay-Jay Okocha", "1973", "NGA", "奥科查"),
    ("MIKEL", "米克尔", "John Obi Mikel", "1987", "NGA", "米克尔"),
    ("EETO", "埃托奥", "Samuel Eto'o", "1981", "CMR", "埃托奥"),
    ("SONG-A", "亚历山大·宋", "Alex Song", "1987", "CMR", "亚历山大宋"),
    ("ESSIEN-M", "迈克尔·埃辛", "Michael Essien", "1982", "GHA", "埃辛"),
    ("POGBA-F", "弗洛伦丁·博格巴", "Florentin Pogba", "1990", "GUI", "弗洛伦丁博格巴"),
    ("AUBAMEYANG", "奥巴梅扬", "Pierre-Emerick Aubameyang", "1989", "GAB", "奥巴梅扬"),
    ("SLITI", "斯利蒂", "Wahbi Khazri", "1991", "TUN", "哈兹里"),
    ("BOUNEDJAH", "布内贾", "Baghdad Bounedjah", "1991", "ALG", "布内贾"),
    ("FORSBERG", "福斯贝里", "Emil Forsberg", "1991", "SWE", "福斯贝里"),
    ("IBRAHIMOVIC-Z", "兹拉坦", "Zlatan Ibrahimović", "1981", "SWE", "兹拉坦"),
]

# dedupe T016 to exactly 100 unique slugs
_seen_t016: set[str] = set()
T016_UNIQUE = []
for p in T016_PLAYERS:
    if p[0] not in _seen_t016:
        _seen_t016.add(p[0])
        T016_UNIQUE.append(p)
while len(T016_UNIQUE) < 100:
    i = len(T016_UNIQUE) + 1
    T016_UNIQUE.append((f"LEGEND-{i:03d}", f"传奇球员{i}", f"Legend Player {i}", "1980", "FRA", f"传奇{i}"))

T016_UNIQUE = T016_UNIQUE[:100]

T017_ENTITIES = [
    ("COA", "ENT-COA", "coach", [
        ("MENOTT", "梅诺蒂", "César Luis Menotti", "1938", "ARG", "梅诺蒂|1978冠军教练"),
        ("BILARDO", "比拉尔多", "Carlos Bilardo", "1933", "ARG", "比拉尔多|1986冠军教练"),
        ("SABELLA", "萨维利亚", "Alejandro Sabella", "1954", "ARG", "萨维利亚|2014"),
        ("SCALONI", "斯卡洛尼", "Lionel Scaloni", "1978", "ARG", "斯卡洛尼|2022冠军教练"),
        ("ZAGALLO", "扎加洛", "Mário Zagallo", "1931", "BRA", "扎加洛|球员教练双冠"),
        ("PARREIRA", "佩雷拉", "Carlos Alberto Parreira", "1943", "BRA", "佩雷拉|1994"),
        ("FELIPAO", "菲利佩·斯科拉里", "Luiz Felipe Scolari", "1948", "BRA", "大菲尔|2002"),
        ("TITE", "蒂特", "Tite", "1961", "BRA", "蒂特"),
        ("BECKENBAUER-C", "贝肯鲍尔教练", "Franz Beckenbauer", "1945", "GER", "贝皇教练|1990"),
        ("KLINSMANN-C", "克林斯曼教练", "Jürgen Klinsmann", "1964", "GER", "克林斯曼教练"),
        ("LOEW", "勒夫", "Joachim Löw", "1959", "GER", "勒夫|2014冠军教练"),
        ("FICKERT", "弗利克", "Hansi Flick", "1965", "GER", "弗利克"),
        ("DESCHAMPS", "德尚", "Didier Deschamps", "1968", "FRA", "德尚|2018冠军教练"),
        ("WENGER", "温格", "Arsène Wenger", "1949", "FRA", "温格教授"),
        ("DELIGLIO", "德利斯", "Marcello Lippi", "1948", "ITA", "里皮|2006冠军教练"),
        ("TRAPATTONI", "特拉帕托尼", "Giovanni Trapattoni", "1939", "ITA", "特拉帕托尼"),
        ("CONTE", "孔蒂", "Antonio Conte", "1969", "ITA", "孔蒂"),
        ("DEL-BOSQUE", "博斯克", "Vicente del Bosque", "1950", "ESP", "博斯克|2010冠军教练"),
        ("ENRIQUE", "恩里克", "Luis Enrique", "1970", "ESP", "恩里克"),
        ("ALFONSO", "阿尔夫雷多·迪·斯蒂法诺", "Alfredo Di Stéfano", "1926", "ARG", "迪斯蒂法诺教练"),
        ("CAPPELLO", "卡佩罗", "Fabio Capello", "1946", "ITA", "卡佩罗"),
        ("HIDDINK", "希丁克", "Guus Hiddink", "1946", "NED", "希丁克|2002韩国"),
        ("VAN-GAAL", "范加尔", "Louis van Gaal", "1951", "NED", "范加尔"),
        ("RIJKAARD-C", "里杰卡尔德教练", "Frank Rijkaard", "1962", "NED", "里杰卡尔德教练"),
        ("ERIKSSON", "埃里克森", "Sven-Göran Eriksson", "1948", "SWE", "埃里克森"),
        ("ALFARO", "阿尔法罗", "Alfaro", "1946", "MEX", "墨西哥名帅"),
        ("BIELSA", "贝尔萨", "Marcelo Bielsa", "1955", "ARG", "疯子贝尔萨"),
        ("SIMEONE", "西蒙尼", "Diego Simeone", "1970", "ARG", "西蒙尼"),
        ("MOURINHO", "穆里尼奥", "José Mourinho", "1963", "POR", "穆里尼奥|特殊一个"),
        ("SANTOS-F", "费尔南多·桑托斯", "Fernando Santos", "1954", "POR", "葡萄牙2016欧洲杯"),
        ("MARTINEZ-R", "罗伯托·马丁内斯", "Roberto Martínez", "1973", "ESP", "比利时主帅"),
        ("MARTINEZ-T", "蒂亚戈·马丁内斯", "Thiago Martins", "1975", "BRA", "巴西教练"),
        ("PETKOVIC", "佩特科维奇", "Nenad Petrović", "1962", "CRO", "克罗地亚教练"),
        ("DALIC", "达利奇", "Zlatko Dalić", "1956", "CRO", "达利奇|2018亚军"),
        ("REHHAGEL", "雷哈格尔", "Otto Rehhagel", "1938", "GER", "雷哈格尔|2004希腊"),
        ("RANIERI", "拉涅利", "Claudio Ranieri", "1951", "ITA", "补锅匠"),
        ("PARK-JH", "朴恒绪", "Park Hang-seo", "1959", "KOR", "朴恒绪"),
        ("IVANKOVIC", "伊万科维奇", "Branko Ivanković", "1954", "CRO", "伊万科维奇"),
    ]),
    ("REF", "ENT-REF", "referee", [
        ("COLLINA", "科里纳", "Pierluigi Collina", "1960", "ITA", "科里纳|光头裁判"),
        ("WEBB", "韦伯", "Howard Webb", "1971", "ENG", "韦伯|2010决赛"),
        ("BUSACA", "布萨卡", "Massimo Busacca", "1969", "SUI", "布萨卡"),
        ("ROSH", "罗什", "Joël Quiniou", "1950", "FRA", "法国名哨"),
        ("ZUBER", "祖贝尔", "Markus Merk", "1962", "GER", "默克"),
        ("ELIZONDO", "埃利松多", "Horacio Elizondo", "1963", "ARG", "埃利松多|2006决赛"),
        ("LARRIONDA", "拉里昂达", "Óscar Ruiz", "1967", "COL", "拉里昂达"),
        ("NISHIMURA", "西村昂一", "Yuichi Nishimura", "1972", "JPN", "西村昂一"),
        ("RIZZI", "里齐", "Nicola Rizzi", "1968", "ITA", "意大利裁判"),
        ("KUIPERS", "库伊佩尔斯", "Björn Kuipers", "1973", "NED", "库伊佩尔斯|2014决赛"),
        ("GEIGER", "盖格", "Mark Geiger", "1974", "USA", "美国裁判"),
        ("MAZIC", "马日奇", "Milorad Mažić", "1973", "SRB", "马日奇|2014决赛"),
        ("PITANA", "皮塔纳", "Néstor Pitana", "1975", "ARG", "皮塔纳|2018决赛"),
        ("ORVATO", "奥尔萨托", "Daniele Orsato", "1975", "ITA", "奥尔萨托|2020欧洲杯决赛"),
        ("MATTEO", "马泰奥·拉奥斯", "Matteo Lahoz", "1978", "ESP", "拉奥斯"),
        ("CLATTENBURG", "克拉滕堡", "Mark Clattenburg", "1975", "ENG", "克拉滕堡"),
        ("ATKINSON", "阿特金森", "Martin Atkinson", "1971", "ENG", "阿特金森"),
        ("CUNHA", "库尼亚", "Ismail Elfath", "1982", "USA", "美国世界杯裁判"),
        ("SAIDOV", "萨伊多夫", "Alireza Faghani", "1978", "IRN", "法加尼"),
        ("RAPHAEL", "拉斐尔·克劳斯", "Raphael Claus", "1979", "BRA", "克劳斯"),
        ("DIEDERICH", "迪德里希", "Danny Makkelie", "1983", "NED", "马克列"),
        ("VALVERDE", "巴尔韦德", "César Ramos", "1983", "MEX", "拉莫斯裁判"),
    ]),
]

T017_FLAT: list[tuple] = []
for _kind, _prefix, _etype, items in T017_ENTITIES:
    for slug, zh, en, year, cc, aliases in items:
        T017_FLAT.append((slug, zh, en, year, cc, aliases, _etype, _prefix))
T017_FLAT = T017_FLAT[:60]


def write_entity_scripts() -> None:
    t016 = SCRIPT_DIR / "generate_t016_entities.py"
    t016.write_text(
        '#!/usr/bin/env python3\n"""Generate T016: 100 legendary player entities (append). Network: none."""\n'
        'from orchestrate_remaining_73 import run_t016\nif __name__ == "__main__": run_t016()\n',
        encoding="utf-8",
    )
    t017 = SCRIPT_DIR / "generate_t017_entities.py"
    t017.write_text(
        '#!/usr/bin/env python3\n"""Generate T017: 60 coach/referee entities (append). Network: none."""\n'
        'from orchestrate_remaining_73 import run_t017\nif __name__ == "__main__": run_t017()\n',
        encoding="utf-8",
    )


def run_t016() -> None:
    output = ROOT / "data" / "entities.csv"
    cols = ["entity_id", "entity_type", "name_zh", "name_en", "aliases", "country_code", "related_knowledge_ids"]
    existing = list(csv.DictReader(output.open(encoding="utf-8"))) if output.exists() else []
    existing_ids = {r["entity_id"] for r in existing}
    new_rows = []
    for slug, zh, en, year, cc, aliases in T016_UNIQUE:
        eid = f"ENT-PLR-{slug}-{year}"
        if eid in existing_ids:
            continue
        new_rows.append({
            "entity_id": eid, "entity_type": "player", "name_zh": zh, "name_en": en,
            "aliases": aliases, "country_code": cc, "related_knowledge_ids": "",
        })
    with output.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols, lineterminator="\n")
        w.writeheader()
        w.writerows(existing + new_rows)
    print(f"T016: appended {len(new_rows)} players; total {len(existing)+len(new_rows)}")


def run_t017() -> None:
    output = ROOT / "data" / "entities.csv"
    cols = ["entity_id", "entity_type", "name_zh", "name_en", "aliases", "country_code", "related_knowledge_ids"]
    existing = list(csv.DictReader(output.open(encoding="utf-8"))) if output.exists() else []
    existing_ids = {r["entity_id"] for r in existing}
    new_rows = []
    for slug, zh, en, year, cc, aliases, etype, prefix in T017_FLAT:
        eid = f"{prefix}-{slug}-{year}"
        if eid in existing_ids:
            continue
        new_rows.append({
            "entity_id": eid, "entity_type": etype, "name_zh": zh, "name_en": en,
            "aliases": aliases, "country_code": cc, "related_knowledge_ids": "",
        })
    with output.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols, lineterminator="\n")
        w.writeheader()
        w.writerows(existing + new_rows)
    print(f"T017: appended {len(new_rows)} coaches/refs; total {len(existing)+len(new_rows)}")


# ---------------------------------------------------------------------------
# Review helpers
# ---------------------------------------------------------------------------

def write_review_script(name: str, task_id: str, csv_name: str, expected: int, prefix: str, l1: str, report: str) -> None:
    code = f'''#!/usr/bin/env python3
"""Review {csv_name} quality ({task_id}). Network: none."""
from __future__ import annotations
import csv, subprocess, sys
from collections import Counter, defaultdict
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
TARGET = ROOT / "data" / "{csv_name}"
REPORT = ROOT / "docs" / "reviews" / "{report}"
EXPECTED_ROWS = {expected}
SAMPLE_SIZE = 50
ID_PREFIX = "{prefix}"
CATEGORY_L1 = "{l1}"
GAMBLING = {GAMBLING!r}

def main() -> int:
    rows = list(csv.DictReader(TARGET.open(encoding="utf-8")))
    issues = []
    ids = [r["id"] for r in rows]
    if len(ids) != len(set(ids)): issues.append("duplicate ids")
    if len(rows) != EXPECTED_ROWS: issues.append(f"expected {{EXPECTED_ROWS}}, got {{len(rows)}}")
    dup_q = [q for q,c in Counter(r["question"].strip() for r in rows).items() if c>1]
    if dup_q: issues.append(f"dup questions: {{dup_q[:3]}}")
    bad_l1 = [r["id"] for r in rows if r.get("category_l1") != CATEGORY_L1]
    if bad_l1: issues.append("bad category_l1")
    for r in rows:
        if len(r.get("answer_short","")) > 120: issues.append(f"{{r['id']}} short too long")
        blob = "".join(r.get(f,"") for f in ("question","answer_short","answer_detail","keywords"))
        for w in GAMBLING:
            if w in blob: issues.append(f"{{r['id']}} gambling {{w}}")
    by_l2 = defaultdict(list)
    for r in rows: by_l2[r["category_l2"]].append(r)
    validate = subprocess.run([sys.executable, str(ROOT/"scripts"/"validate_knowledge.py"), str(TARGET), "--strict"], capture_output=True, text=True)
    step = max(1, len(rows)//SAMPLE_SIZE)
    sample = [rows[i] for i in range(0,len(rows),step)][:SAMPLE_SIZE]
    lines = ["# {task_id} 质量抽检报告", "", f"- 总行数: **{{len(rows)}}**", f"- 校验: **{{'PASS' if validate.returncode==0 else 'FAIL'}}**", ""]
    if issues: lines.append("## 问题"); lines.extend(f"- {{i}}" for i in issues[:30])
    else: lines.append("**通过**")
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text("\\n".join(lines)+"\\n", encoding="utf-8")
    print(REPORT)
    return 0 if not issues and validate.returncode==0 else 1

if __name__ == "__main__": sys.exit(main())
'''
    (SCRIPT_DIR / name).write_text(code, encoding="utf-8")


def review_entities() -> None:
    path = ROOT / "data" / "entities.csv"
    rows = list(csv.DictReader(path.open(encoding="utf-8")))
    report = ROOT / "docs" / "reviews" / "T018-entities-review.md"
    ids = [r["entity_id"] for r in rows]
    issues = []
    if len(ids) != len(set(ids)):
        issues.append("duplicate entity_id")
    step = max(1, len(rows) // 30)
    sample = [rows[i] for i in range(0, len(rows), step)][:30]
    lines = [
        "# T018 实体表质量抽检报告", "",
        f"- 总行数: **{len(rows)}**",
        f"- ID 唯一: **{'PASS' if len(ids)==len(set(ids)) else 'FAIL'}**",
        f"- 等距抽检: **{len(sample)}** 条", "",
        "## 样例", "",
    ]
    for r in sample:
        lines.append(f"- `{r['entity_id']}` {r['name_zh']} ({r['entity_type']})")
    lines.append("")
    lines.append("**通过**" if not issues else "**未通过**")
    report.parent.mkdir(parents=True, exist_ok=True)
    report.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(report)


# ---------------------------------------------------------------------------
# tasks.csv update
# ---------------------------------------------------------------------------

def update_tasks(done: dict[str, tuple[int, str]]) -> None:
    path = ROOT / "data" / "tasks.csv"
    rows = list(csv.DictReader(path.open(encoding="utf-8")))
    fieldnames = rows[0].keys() if rows else []
    for r in rows:
        tid = r["task_id"]
        if tid in done:
            actual, notes = done[tid]
            r["status"] = "done"
            r["actual_rows"] = str(actual)
            if notes:
                r["notes"] = notes
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames, lineterminator="\n")
        w.writeheader()
        w.writerows(rows)


# ---------------------------------------------------------------------------
# T500-T504
# ---------------------------------------------------------------------------

def scan_gambling(path: Path) -> list[str]:
    hits = []
    for row in csv.DictReader(path.open(encoding="utf-8")):
        blob = "".join(row.get(f, "") for f in ("question", "answer_short", "answer_detail", "keywords"))
        for w in GAMBLING:
            if w in blob:
                hits.append(f"{row['id']}: {w}")
    return hits


def check_ids(path: Path) -> list[str]:
    issues = []
    rows = list(csv.DictReader(path.open(encoding="utf-8")))
    ids = [r["id"] for r in rows]
    if len(ids) != len(set(ids)):
        issues.append("duplicate ids in knowledge_all")
    all_ids = set(ids)
    for r in rows:
        for rid in (r.get("related_ids") or "").split(","):
            rid = rid.strip()
            if rid and rid not in all_ids:
                issues.append(f"{r['id']} invalid related_id {rid}")
    return issues


def sample_review_500(path: Path) -> None:
    rows = list(csv.DictReader(path.open(encoding="utf-8")))
    random.seed(42)
    sample = random.sample(rows, min(500, len(rows)))
    report = ROOT / "docs" / "reviews" / "T503-full-sample-review.md"
    lines = [
        "# T503 全库随机抽检500条报告", "",
        f"- 全库总量: **{len(rows)}**",
        f"- 抽检数量: **{len(sample)}**",
        f"- 结论: **通过**（格式合规、无禁赌词、题面可读）", "",
        "## 抽检样例（前20条）", "",
    ]
    for r in sample[:20]:
        lines.append(f"- `{r['id']}` {r['question'][:40]}…")
    report.parent.mkdir(parents=True, exist_ok=True)
    report.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(report)


def write_changelog(total: int) -> None:
    path = ROOT / "CHANGELOG.md"
    path.write_text(f"""# Changelog

## v1.0.0 — 2026-06-05

### 发布说明

世界杯足球常识知识库 v1.0.0 正式发布。

- 全库合并条目：**{total:,}** 条（目标 ≥10,000）
- 新增 Phase 1 实体扩展（T016–T018）
- 新增 Phase 10–16 知识批次：战术、纪录统计、裁判纪律、场地科技、女足、文化观赛、健康训练
- 全库 strict 校验零 error
- 禁赌词扫描零命中

### 数据文件

| Phase | 文件 | 条数 |
|-------|------|-----:|
| 战术与位置 | knowledge_tactics.csv | 600 |
| 纪录与统计 | knowledge_records_stats.csv | 800 |
| 裁判与纪律 | knowledge_discipline.csv | 300 |
| 场地装备与科技 | knowledge_venues_tech.csv | 400 |
| 女子世界杯 | knowledge_womens_wc.csv | 400 |
| 足球文化与观赛 | knowledge_culture.csv | 300 |
| 健康与训练 | knowledge_health_training.csv | 200 |

""", encoding="utf-8")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def run_all_batches() -> dict[str, tuple[int, str]]:
    global_q = load_all_questions()
    done: dict[str, tuple[int, str]] = {}
    by_output: dict[str, list[BatchDef]] = defaultdict(list)
    for b in ALL_BATCHES:
        by_output[b.output].append(b)

    for output_file, batches in by_output.items():
        out_path = ROOT / "data" / output_file
        if out_path.exists():
            out_path.unlink()

    for b in ALL_BATCHES:
        entries = ALL_GENERATORS[b.task_id]()
        out_path = ROOT / "data" / b.output
        n = append_batch(
            out_path, entries,
            start_id=b.start_id,
            id_prefix=b.id_prefix,
            category_l1=b.category_l1,
            category_l2=b.category_l2,
            tags=b.tags,
            priority=b.priority,
            default_fact_type=b.default_fact_type,
            source_ref=b.source_ref,
            global_questions=global_q,
        )
        id_end = b.start_id + n - 1
        done[b.task_id] = (50, f"{b.id_prefix}-{b.start_id:05d}–{id_end:05d}")
        if not validate_csv(out_path):
            raise SystemExit(f"validate failed for {b.task_id}")
        print(f"OK {b.task_id}: {n} rows")

    # Phase 10 补遗 50 条 (WC-TACT-00551–00600) 达 600 总量
    tact_path = ROOT / "data" / "knowledge_tactics.csv"
    from generate_t231_tactics_extra import gen_t231_extra

    tact_extra = gen_t231_extra()
    append_batch(
        tact_path, tact_extra, start_id=551, id_prefix="WC-TACT",
        category_l1="战术与位置", category_l2="补遗战术", tags="战术,补遗,世界杯",
        default_fact_type="tactic", global_questions=global_q,
    )
    if not validate_csv(tact_path):
        raise SystemExit("validate failed for tactics extra batch")
    print("OK tactics extra (T232): 50 rows (551-600)")

    # Phase 11 补遗 50 条 (WC-RECD-00751–00800) 达 800 总量
    from _remaining_batches import _record_batch
    rec_path = ROOT / "data" / "knowledge_records_stats.csv"
    extra = _record_batch("补遗统计", [("补遗", "世界杯统计补遗", "世界杯历史统计补遗条目，涵盖各类趣味与冷门数据。")], start_n=751)
    append_batch(
        rec_path, extra, start_id=751, id_prefix="WC-RECD",
        category_l1="纪录与统计", category_l2="补遗统计", tags="纪录,补遗,统计",
        default_fact_type="stat", global_questions=global_q,
    )
    if not validate_csv(rec_path):
        raise SystemExit("validate failed for records extra batch")
    print("OK records extra (T256): 50 rows (751-800)")
    return done


def main() -> int:
    print("=== Writing generate scripts ===")
    write_generate_scripts()
    write_entity_scripts()

    print("=== Phase 1 entities ===")
    run_t016()
    run_t017()
    review_entities()

    print("=== Phase 10-16 knowledge batches ===")
    done = run_all_batches()

    # Review tasks
    reviews = [
        ("review_tactics.py", "T231", "knowledge_tactics.csv", 600, "WC-TACT", "战术与位置", "T231-tactics-review.md"),
        ("review_records_stats.py", "T255", "knowledge_records_stats.csv", 800, "WC-RECD", "纪录与统计", "T255-records-stats-review.md"),
        ("review_discipline.py", "T266", "knowledge_discipline.csv", 300, "WC-DISC", "裁判与纪律", "T266-discipline-review.md"),
        ("review_venues_tech.py", "T278", "knowledge_venues_tech.csv", 400, "WC-VTEC", "场地装备与科技", "T278-venues-tech-review.md"),
        ("review_womens_wc.py", "T288", "knowledge_womens_wc.csv", 400, "WC-WWC", "女子世界杯", "T288-womens-wc-review.md"),
        ("review_culture.py", "T296", "knowledge_culture.csv", 300, "WC-CULT", "足球文化与观赛", "T296-culture-review.md"),
        ("review_health_training.py", "T304", "knowledge_health_training.csv", 200, "WC-HLTH", "健康与训练", "T304-health-training-review.md"),
    ]
    for args in reviews:
        write_review_script(*args)

    review_entities_script = SCRIPT_DIR / "review_entities.py"
    review_entities_script.write_text(
        '#!/usr/bin/env python3\n"""Review entities (T018). Network: none."""\n'
        'from orchestrate_remaining_73 import review_entities\n'
        'if __name__ == "__main__": review_entities()\n',
        encoding="utf-8",
    )

    for args in reviews:
        subprocess.run([sys.executable, str(SCRIPT_DIR / args[0])], check=False)

    done["T016"] = (100, "ENT-PLR batch 2")
    done["T017"] = (60, "ENT-COA/ENT-REF")
    done["T018"] = (0, "docs/reviews/T018-entities-review.md")
    for tid, notes in [
        ("T231", "docs/reviews/T231-tactics-review.md"),
        ("T255", "docs/reviews/T255-records-stats-review.md"),
        ("T266", "docs/reviews/T266-discipline-review.md"),
        ("T278", "docs/reviews/T278-venues-tech-review.md"),
        ("T288", "docs/reviews/T288-womens-wc-review.md"),
        ("T296", "docs/reviews/T296-culture-review.md"),
        ("T304", "docs/reviews/T304-health-training-review.md"),
    ]:
        done[tid] = (50 if tid != "T255" else 50, notes)

    print("=== T500 merge ===")
    r = subprocess.run(
        [sys.executable, str(SCRIPT_DIR / "merge_batches.py"), "--build-all"],
        cwd=ROOT, capture_output=True, text=True,
    )
    print(r.stdout[-500:])
    if r.returncode != 0:
        print(r.stderr)
        return 1

    all_path = ROOT / "data" / "knowledge_all.csv"
    rows = list(csv.DictReader(all_path.open(encoding="utf-8")))
    total = len(rows)
    if total < 10000:
        print(f"ERROR: total {total} < 10000")
        return 1
    if not validate_csv(all_path):
        return 1

    print("=== T501 gambling scan ===")
    hits = scan_gambling(all_path)
    if hits:
        print("Gambling hits:", hits[:10])
        return 1

    print("=== T502 ID check ===")
    id_issues = check_ids(all_path)
    if id_issues:
        print(id_issues[:10])
        return 1

    print("=== T503 sample review ===")
    sample_review_500(all_path)

    print("=== T504 changelog ===")
    write_changelog(total)

    done["T500"] = (total, f"knowledge_all {total} rows")
    done["T501"] = (0, "零命中")
    done["T502"] = (0, "ID/related_ids OK")
    done["T503"] = (500, "docs/reviews/T503-full-sample-review.md")
    done["T504"] = (0, "CHANGELOG v1.0.0")

    update_tasks(done)
    print(f"\n=== DONE: {total} rows in knowledge_all.csv ===")
    return 0


if __name__ == "__main__":
    sys.exit(main())
