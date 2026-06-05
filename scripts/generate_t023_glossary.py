#!/usr/bin/env python3
"""Generate T023 glossary batch: 50 English abbreviation terms (append).

Network: none (local structured data). Outbound HTTP must use fetch_utils.RateLimitedFetcher (>=1s/request); see docs/data-collection-policy.md and .cursor/rules/world-cup-data-collection.mdc."""

from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUTPUT = ROOT / "data" / "knowledge_glossary.csv"
START_ID = 151

COLUMNS = [
    "id", "category_l1", "category_l2", "category_l3", "scope", "priority",
    "question", "question_aliases", "answer_short", "answer_detail", "answer_format",
    "keywords", "tags", "entities", "related_ids", "difficulty",
    "era_start", "era_end", "region", "language", "fact_type", "confidence",
    "source_type", "source_ref", "content_flags", "updated_at",
]

ENTRIES = [
    ("FIFA", "FIFA是什么意思?", "国际足联|FIFA缩写",
     "FIFA是Fédération Internationale de Football Association，即国际足球联合会，世界杯主办方。",
     "FIFA负责世界杯、世少赛等全球赛事与规则推广，总部位于瑞士苏黎世。",
     "FIFA,国际足联,世界杯,组织", "入门"),
    ("IFAB", "IFAB是什么?", "国际足球理事会|IFAB缩写",
     "IFAB是International Football Association Board，负责制定与修改足球竞赛规则。",
     "IFAB由FIFA与四英国足协组成，每年发布《足球竞赛规则》。",
     "IFAB,规则,理事会,竞赛规则", "进阶"),
    ("VAR", "VAR是什么意思?", "视频助理裁判|Video Assistant Referee",
     "VAR是Video Assistant Referee，视频助理裁判，协助主裁复核进球、点球、红牌等关键判罚。",
     "世界杯2018俄罗斯首次全面使用VAR。",
     "VAR,视频裁判,复核,世界杯", "入门"),
    ("AVAR", "AVAR是什么?", "助理视频裁判|Assistant VAR",
     "AVAR是Assistant Video Assistant Referee，协助VAR操作回放与沟通。",
     "AVAR通常在视频操作室与VAR协同工作。",
     "AVAR,视频裁判,助理,VAR", "进阶"),
    ("GK", "GK是什么位置?", "Goalkeeper|门将缩写",
     "GK是Goalkeeper，门将/守门员，唯一可在禁区内用手触球的球员。",
     "数据与阵容表常用GK表示门将。",
     "GK,门将,Goalkeeper,位置", "入门"),
    ("CB", "CB是什么位置?", "Center Back|中卫缩写",
     "CB是Center Back，中后卫/中卫，镇守防线中央。",
     "三中卫体系常标注为CB或LCB/RCB。",
     "CB,中卫,Center Back,后卫", "入门"),
    ("RB", "RB是什么位置?", "Right Back|右后卫缩写",
     "RB是Right Back，右后卫，负责右路防守与助攻。",
     "与RW（右边锋）不同，RB为防守位置。",
     "RB,右后卫,Right Back,后卫", "入门"),
    ("LB", "LB是什么位置?", "Left Back|左后卫缩写",
     "LB是Left Back，左后卫，负责左路防守与助攻。",
     "阵容名单与战术图常见LB标注。",
     "LB,左后卫,Left Back,后卫", "入门"),
    ("WB", "WB是什么位置?", "Wing Back|翼卫缩写",
     "WB是Wing Back，翼卫/边翼卫，比边后卫更靠前，常见于352等阵型。",
     "RWB与LWB分别表示左右翼卫。",
     "WB,翼卫,Wing Back,位置", "入门"),
    ("CDM", "CDM是什么位置?", "Defensive Midfielder|后腰缩写",
     "CDM是Central Defensive Midfielder，防守型中场/后腰，主责拦截与保护防线。",
     "与CAM（前腰）相对应。",
     "CDM,后腰,防守中场,位置", "入门"),
    ("CM", "CM是什么位置?", "Central Midfielder|中前卫缩写",
     "CM是Central Midfielder，中前卫/中央中场，连接攻防。",
     "可细分为CM、CDM、CAM等。",
     "CM,中前卫,Central Midfielder,中场", "入门"),
    ("CAM", "CAM是什么位置?", "Attacking Midfielder|前腰缩写",
     "CAM是Central Attacking Midfielder，攻击型中场/前腰，负责组织进攻。",
     "常与10号位球员联系在一起。",
     "CAM,前腰,攻击中场,位置", "入门"),
    ("LW", "LW是什么位置?", "Left Winger|左边锋缩写",
     "LW是Left Winger，左边锋，在左路进攻。",
     "与LM（左前卫）相比位置通常更靠前。",
     "LW,左边锋,Left Winger,边锋", "入门"),
    ("RW", "RW是什么位置?", "Right Winger|右边锋缩写",
     "RW是Right Winger，右边锋，在右路进攻。",
     "数据网站与转播字幕常用RW/LW。",
     "RW,右边锋,Right Winger,边锋", "入门"),
    ("ST", "ST是什么位置?", "Striker|前锋缩写",
     "ST是Striker，前锋/射手，主要任务是进球。",
     "与CF（中锋）常混用但ST更强调射门得分。",
     "ST,前锋,Striker,射手", "入门"),
    ("CF", "CF是什么位置?", "Center Forward|中锋缩写",
     "CF是Center Forward，中锋，活动于禁区前沿与中路。",
     "9号球员常对应CF或ST。",
     "CF,中锋,Center Forward,前锋", "入门"),
    ("SS", "SS是什么位置?", "Second Striker|影锋缩写",
     "SS是Second Striker，第二前锋/影锋，介于前腰与中锋之间。",
     "托蒂等球员曾踢SS角色。",
     "SS,影锋,Second Striker,前锋", "进阶"),
    ("WC", "WC在足球里指什么?", "World Cup|世界杯缩写",
     "WC是World Cup的缩写，指世界杯；语境中勿与项目知识ID前缀WC混淆。",
     "赛程、论坛与英文报道常见WC或FIFA WC。",
     "WC,World Cup,世界杯,缩写", "入门"),
    ("UEFA", "UEFA是什么?", "欧足联|欧洲足联",
     "UEFA是Union of European Football Associations，欧洲足球协会联盟。",
     "欧冠、欧洲杯由UEFA主办。",
     "UEFA,欧足联,欧冠,欧洲杯", "入门"),
    ("CONMEBOL", "CONMEBOL是什么?", "南美足联|南美洲足联",
     "CONMEBOL是南美洲足球联合会，组织南美世界杯预选赛与美洲杯。",
     "巴西、阿根廷等国足协隶属CONMEBOL。",
     "CONMEBOL,南美,预选赛,美洲杯", "进阶"),
    ("AFC", "AFC在足球里指什么?", "亚足联|亚洲足联",
     "AFC是Asian Football Confederation，亚洲足球联合会。",
     "亚洲世界杯预选赛与亚洲杯由AFC组织。",
     "AFC,亚足联,亚洲,预选赛", "入门"),
    ("CAF", "CAF是什么?", "非洲足联|非洲足球联合会",
     "CAF是Confederation of African Football，非洲足球联合会。",
     "非洲世界杯预选赛与非洲杯由CAF主办。",
     "CAF,非洲,预选赛,非洲杯", "进阶"),
    ("CONCACAF", "CONCACAF是什么?", "中北美足联",
     "CONCACAF是中北美及加勒比海足球协会，美国、墨西哥、加拿大等队属此。",
     "2026世界杯由该区域三国联合主办。",
     "CONCACAF,中北美,预选赛,2026", "进阶"),
    ("EPL", "EPL是什么联赛?", "英超|Premier League",
     "EPL是English Premier League，英格兰超级联赛，俗称英超。",
     "世界杯年英超为各队输送大量国脚。",
     "EPL,英超,Premier League,联赛", "入门"),
    ("UCL", "UCL是什么?", "欧冠|UEFA Champions League",
     "UCL是UEFA Champions League，欧洲冠军联赛，俱乐部最高水平赛事。",
     "世界杯前UCL赛季结束时间影响球员状态。",
     "UCL,欧冠,Champions League,俱乐部", "入门"),
    ("OG", "OG在比分里是什么意思?", "Own Goal|乌龙球缩写",
     "OG是Own Goal，乌龙球，球员不慎将球打入本方球门。",
     "技术统计与比分转播常用OG标注。",
     "OG,乌龙球,Own Goal,比分", "入门"),
    ("PK", "PK在足球里指什么?", "Penalty Kick|点球缩写",
     "PK是Penalty Kick，点球，禁区内犯规等情况下的十二码罚球。",
     "美式口语也常用PK表示点球大战中的点球。",
     "PK,点球,Penalty Kick,十二码", "入门"),
    ("ET", "ET在比赛表上是什么意思?", "Extra Time|加时赛",
     "ET是Extra Time，加时赛，淘汰赛平局后进行的两段15分钟加时。",
     "仍平局则进入点球大战（有时标注PEN）。",
     "ET,加时,Extra Time,淘汰赛", "入门"),
    ("HT", "HT是什么意思?", "Half Time|半场",
     "HT是Half Time，半场休息或半场比分时刻。",
     "赛程表HT后显示中场休息。",
     "HT,半场,Half Time,休息", "入门"),
    ("FT", "FT是什么意思?", "Full Time|全场结束",
     "FT是Full Time，全场比赛结束（含常规时间，不含加时则视语境）。",
     "直播比分FT表示终场哨响。",
     "FT,全场,Full Time,结束", "入门"),
    ("MOTM", "MOTM是什么?", "Man of the Match|最佳球员",
     "MOTM是Man of the Match，全场最佳球员，赛后由官方或媒体评选。",
     "世界杯决赛MOTM备受关注。",
     "MOTM,最佳球员,Man of the Match,评选", "入门"),
    ("xG", "xG数据是什么?", "Expected Goals|预期进球",
     "xG是Expected Goals，根据射门质量估算的进球期望值。",
     "xG>1表示机会质量高但未必转化为进球。",
     "xG,预期进球,数据,射门", "进阶"),
    ("xA", "xA是什么?", "Expected Assists|预期助攻",
     "xA是Expected Assists，根据传球创造机会质量估算的助攻期望值。",
     "与xG配合可评估球员进攻贡献。",
     "xA,预期助攻,数据,传球", "进阶"),
    ("B2B", "B2B中场是什么意思?", "Box to Box|全能中场",
     "B2B是Box to Box，指攻防两端覆盖大的全能中场。",
     "亚亚图雷、莫德里奇等常被称作B2B中场。",
     "B2B,全能中场,Box to Box,中场", "进阶"),
    ("WCQ", "WCQ是什么?", "World Cup Qualifiers|世预赛",
     "WCQ是World Cup Qualifiers，世界杯预选赛。",
     "各大洲WCQ赛制与名额不同。",
     "WCQ,世预赛,预选赛,世界杯", "入门"),
    ("AM", "AM是什么位置?", "Attacking Midfielder|前腰",
     "AM是Attacking Midfielder，攻击型中场，与CAM同义。",
     "战术板与英文解说常用AM。",
     "AM,前腰,Attacking Midfielder,中场", "入门"),
    ("CS", "CS在数据里指什么?", "Clean Sheet|零封",
     "CS是Clean Sheet，零封，门将或球队在本场未失球。",
     "门将统计常看CS次数。",
     "CS,零封,Clean Sheet,门将", "入门"),
    ("DF", "DF是什么?", "Defender|后卫线",
     "DF是Defender，后卫，泛指CB、RB、LB等防守球员。",
     "FIFA阵容分类常用DF/MF/FW。",
     "DF,后卫,Defender,位置", "入门"),
    ("MF", "MF是什么?", "Midfielder|中场线",
     "MF是Midfielder，中场球员总称。",
     "涵盖CDM、CM、CAM、LM、RM等。",
     "MF,中场,Midfielder,位置", "入门"),
    ("FW", "FW是什么?", "Forward|前锋线",
     "FW是Forward，前锋，包括ST、CF、LW、RW等攻击球员。",
     "与MF、DF构成位置三大类。",
     "FW,前锋,Forward,位置", "入门"),
    ("YC", "YC是什么意思?", "Yellow Card|黄牌",
     "YC是Yellow Card，黄牌警告。",
     "数据表YC列显示球员黄牌数。",
     "YC,黄牌,Yellow Card,纪律", "入门"),
    ("RC", "RC是什么意思?", "Red Card|红牌",
     "RC是Red Card，红牌罚下。",
     "Second yellow也可导致RC。",
     "RC,红牌,Red Card,罚下", "入门"),
    ("Sub", "Sub是什么意思?", "Substitute|替补",
     "Sub是Substitute，替补球员；动词substitute表示换人。",
     "阵容Sub列列出替补名单。",
     "Sub,替补,Substitute,换人", "入门"),
    ("KO", "KO在赛程里指什么?", "Knockout|淘汰赛",
     "KO是Knockout stage，淘汰赛阶段，即小组赛后的单场决胜。",
     "R16、QF、SF、F均属KO阶段。",
     "KO,淘汰赛,Knockout,世界杯", "入门"),
    ("R16", "R16是什么?", "Round of 16|16强",
     "R16是Round of 16，世界杯16强/八分之一决赛。",
     "32队小组赛出线后进入R16。",
     "R16,16强,八分之一,淘汰赛", "入门"),
    ("QF", "QF是什么?", "Quarter Final|八强",
     "QF是Quarter Final，四分之一决赛/八强战。",
     "世界杯每届QF产生四支半决赛球队。",
     "QF,八强,Quarter Final,淘汰赛", "入门"),
    ("SF", "SF是什么?", "Semi Final|半决赛",
     "SF是Semi Final，半决赛；胜者进决赛，败者争季军。",
     "世界杯SF常是全球收视率最高场次之一。",
     "SF,半决赛,Semi Final,淘汰赛", "入门"),
    ("GD", "GD在积分榜上是什么?", "Goal Difference|净胜球",
     "GD是Goal Difference，净胜球，进球数减失球数。",
     "世界杯小组赛积分相同常比较GD。",
     "GD,净胜球,Goal Difference,积分榜", "入门"),
    ("GF", "GF是什么?", "Goals For|进球数",
     "GF是Goals For，球队总进球数。",
     "与GA（失球）一起构成GD。",
     "GF,进球,Goals For,数据", "入门"),
    ("GA", "GA是什么?", "Goals Against|失球数",
     "GA是Goals Against，球队总失球数。",
     "GD=GF-GA。",
     "GA,失球,Goals Against,数据", "入门"),
]


def row(seq: int, entry: tuple) -> dict[str, str]:
    l3, q, aliases, short, detail, kw, diff = entry
    return {
        "id": f"WC-GLOS-{seq:05d}",
        "category_l1": "术语与百科",
        "category_l2": "英文缩写",
        "category_l3": l3,
        "scope": "both",
        "priority": "4",
        "question": q,
        "question_aliases": aliases,
        "answer_short": short,
        "answer_detail": detail,
        "answer_format": "definition",
        "keywords": kw,
        "tags": "英文缩写,术语",
        "entities": "",
        "related_ids": "",
        "difficulty": diff,
        "era_start": "",
        "era_end": "",
        "region": "全球",
        "language": "zh-CN",
        "fact_type": "term",
        "confidence": "verified",
        "source_type": "FIFA",
        "source_ref": "FIFA/IFAB official terminology; common football data conventions",
        "content_flags": "",
        "updated_at": "2026-06-03",
    }


def main() -> None:
    if len(ENTRIES) != 50:
        raise SystemExit(f"expected 50 entries, got {len(ENTRIES)}")

    new_rows = [row(START_ID + i - 1, e) for i, e in enumerate(ENTRIES, start=1)]

    existing: list[dict[str, str]] = []
    if OUTPUT.exists():
        with OUTPUT.open(newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            if list(reader.fieldnames) != COLUMNS:
                raise SystemExit("existing glossary header mismatch")
            existing = [dict(r) for r in reader if any((v or "").strip() for v in r.values())]

    ids = {r["id"] for r in existing}
    for r in new_rows:
        if r["id"] in ids:
            raise SystemExit(f"duplicate id {r['id']}")

    with OUTPUT.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=COLUMNS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(existing)
        writer.writerows(new_rows)

    print(f"Appended {len(new_rows)} rows (total {len(existing) + len(new_rows)}) to {OUTPUT}")


if __name__ == "__main__":
    main()
