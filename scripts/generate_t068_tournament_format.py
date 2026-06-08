#!/usr/bin/env python3
"""Generate T068: 50 World Cup fair play & group ranking entries (append).

Network: none (local structured data). Outbound HTTP must use fetch_utils.RateLimitedFetcher (>=1s/request); see docs/maintainers/data-collection-policy.md and .cursor/rules/world-cup-data-collection.mdc."""

from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUTPUT = ROOT / "data" / "knowledge_tournament_format.csv"
START_ID = 401

COLUMNS = [
    "id", "category_l1", "category_l2", "category_l3", "scope", "priority",
    "question", "question_aliases", "answer_short", "answer_detail", "answer_format",
    "keywords", "tags", "entities", "related_ids", "difficulty",
    "era_start", "era_end", "region", "language", "fact_type", "confidence",
    "source_type", "source_ref", "content_flags", "updated_at",
]

ENTRIES = [
    ("积分规则", "小组赛怎么算分?", "group points",
     "胜3分、平1分、负0分，按积分高低排名。",
     "与多数足球联赛胜3制一致。",
     "积分,胜3,平1,小组赛", "入门", "world_cup", "rule"),
    ("净胜球", "积分相同看什么?", "goal difference",
     "积分相同先比净胜球（进球减失球）。",
     "仍相同则依次比较进球数等。",
     "净胜球,积分,相同,排名", "入门", "world_cup", "rule"),
    ("进球数", "净胜球相同怎么办?", "goals scored",
     "净胜球相同则比较小组赛总进球数，多者靠前。",
     "再相同则进入后续公平竞赛等比较。",
     "进球数,净胜球,相同,比较", "入门", "world_cup", "rule"),
    ("相互战绩", "三项仍相同呢?", "head-to-head",
     "涉及两队时直接比较相互比赛结果与数据。",
     "三队及以上时仅比较相关场次 mini 积分榜。",
     "相互,战绩,两队,三队", "入门", "world_cup", "rule"),
    ("公平竞赛分", "公平竞赛分怎么算?", "fair play points",
     "黄牌扣1分、两黄变红扣3分、直接红牌扣4分、加时黄不扣。",
     "扣分少者排名靠前。",
     "公平竞赛,黄牌,红牌,扣分", "入门", "world_cup", "rule"),
    ("抽签决定", "全部相同怎么办?", "drawing of lots",
     "若所有比较项仍相同，FIFA抽签决定排名。",
     "历史极少动用，但规程保留该条款。",
     "抽签,相同,排名,FIFA", "入门", "world_cup", "rule"),
    ("小组前二", "小组前几名出线?", "top two advance",
     "4队小组前两名晋级淘汰赛。",
     "48队时代另设8个最佳第三进32强。",
     "前二,出线,晋级,小组", "入门", "world_cup"),
    ("最佳第三", "48队第三怎么比?", "best third place",
     "12组第三中按积分、净胜球等取前8名进32强。",
     "细则见当届FIFA World Cup Regulations。",
     "第三,最佳,8名,48队", "入门", "world_cup", "rule"),
    ("同分第三", "多个第三同分?", "third place tiebreak",
     "最佳第三比较同样遵循积分、净胜球、进球、公平竞赛等顺序。",
     "可能跨组比较不同对手强度。",
     "第三,同分,跨组,比较", "进阶", "world_cup", "rule"),
    ("末轮同开", "末轮同开与排名?", "simultaneous final round",
     "末轮同组同时开球防止知晓他队赛果后控分。",
     "保障公平竞赛与排名公正。",
     "末轮,同开,控分,公平", "入门", "world_cup"),
    ("红牌停赛", "小组赛红牌停赛?", "group stage suspension",
     "小组赛最后一场吃牌可能导致淘汰赛首场停赛。",
     "累积两张黄牌亦触发停赛。",
     "红牌,停赛,黄牌,累积", "入门", "world_cup", "rule"),
    ("黄牌清零", "淘汰赛黄牌清零吗?", "yellow card reset",
     "进入淘汰赛后黄牌累积规则依当届规程，通常1/4决赛前清零。",
     "具体以当届文件为准。",
     "黄牌,清零,淘汰赛,累积", "进阶", "world_cup", "rule"),
    ("公平竞赛奖", "公平竞赛奖与排名?", "Fair Play award vs rank",
     "公平竞赛奖为赛后荣誉，与小组出线排名规则相关但非同一奖项。",
     "排名中的公平竞赛分为 tiebreaker 使用。",
     "公平竞赛,排名,奖项,区分", "入门", "world_cup"),
    ("1982阿尔及利亚", "1982德国奥地利?", "1982 Disgrace of Gijon",
     "1982末轮西德1比0奥地利使双方同进，推动末轮同开规则。",
     "史称希洪丑闻。",
     "1982,希洪,同开,历史", "进阶", "world_cup", "history"),
    ("1994墨西哥", "1994公平竞赛队?", "1994 Fair Play",
     "1994墨西哥获公平竞赛队，该届美国主办。",
     "展示纪律与体育精神。",
     "1994,墨西哥,公平竞赛,美国", "入门", "world_cup", "history"),
    ("2018日本", "2018日本公平竞赛?", "Japan 2018 fair play",
     "2018日本凭公平竞赛分淘汰塞内加尔晋级16强。",
     "两队积分净胜球进球均相同。",
     "2018,日本,塞内加尔,黄牌", "入门", "world_cup", "history"),
    ("2018哥伦比亚", "2018公平竞赛队谁得?", "2018 Fair Play team",
     "2018公平竞赛队为西班牙，非哥伦比亚。",
     "西班牙该届16强出局。",
     "2018,西班牙,公平竞赛,球队", "入门", "world_cup", "history"),
    ("2006阿根廷", "2006阿根廷德国同组?", "2006 Group A",
     "2006阿根廷与荷兰同组，厄瓜多尔第二，克罗地亚第三。",
     "德国该届东道主另组。",
     "2006,阿根廷,荷兰,同组", "进阶", "world_cup", "history"),
    ("死亡之组", "死亡之组影响排名吗?", "group of death",
     "死亡之组指强队集中，排名规则不变。",
     "仍按积分与 tiebreaker 决出线。",
     "死亡之组,排名,规则,不变", "入门", "world_cup"),
    ("0分出局", "0分能否出线?", "zero points advance",
     "理论上可能但极罕见，需极端 tiebreaker 与第三比较。",
     "通常至少需1分才有出线可能。",
     "0分,出线,罕见,积分", "进阶", "world_cup"),
    ("全胜出线", "全胜一定第一吗?", "perfect record",
     "小组赛全胜9分必为小组第一（3队制不适用世界杯4队组）。",
     "4队组全胜即头名出线。",
     "全胜,9分,第一,出线", "入门", "world_cup"),
    ("三连平", "三场全平能出线吗?", "three draws",
     "三场平局3分可能出线取决于他队战绩。",
     "1998智利曾3分出线16强。",
     "三连平,3分,出线,可能", "入门", "world_cup", "history"),
    ("相互净胜", "相互比赛净胜球?", "H2H goal difference",
     "两队 tiebreaker 含相互场次净胜球。",
     "仅计直接对话的两场比赛。",
     "相互,净胜球,直接,对话", "入门", "world_cup", "rule"),
    ("相互进球", "相互比赛进球数?", "H2H goals scored",
     "相互净胜球相同则比相互比赛进球数。",
     "三队 mini 积分榜同理。",
     "相互,进球,三队,mini", "入门", "world_cup", "rule"),
    ("mini积分榜", "三队 tiebreaker?", "three-way mini table",
     "三队积分相同则剔除与其他队比赛，仅比三队间 mini 积分榜。",
     "仍相同则比 mini 净胜球与进球。",
     "三队,mini,积分榜,剔除", "进阶", "world_cup", "rule"),
    ("48队12组", "48队小组排名?", "48-team groups",
     "12组各4队，每组前二直接进32强。",
     "8个最佳第三依跨组规则筛选。",
     "12组,48队,第三,32强", "入门", "world_cup"),
    ("第三对阵", "第三对阵如何定?", "third place bracket",
     "32强对阵表预先设定各组第一、第二与特定第三相遇位置。",
     "最佳第三确定后填入对应槽位。",
     "第三,对阵,32强,槽位", "进阶", "world_cup", "rule"),
    ("小组第三历史", "32队时代第三出线吗?", "32-team third place",
     "1986至1994曾设最佳4第三进16强，后改回仅前二。",
     "2026起恢复部分第三晋级。",
     "第三,1986,1994,32队", "进阶", "world_cup", "history"),
    ("积分并列第一", "两队同分同第一?", "joint first place",
     "同分且 tiebreaker 全相同则并列第一，抽签决定淘汰赛落位。",
     "影响16强对阵半区。",
     "并列,第一,抽签,落位", "进阶", "world_cup", "rule"),
    ("消极比赛", "消极比赛如何处罚?", "unsporting conduct",
     "FIFA可调查明显消极比赛，纪律委员会可扣分或罚款。",
     "1982后规则与舆论监督更严。",
     "消极,处罚,纪律,调查", "进阶", "world_cup", "rule"),
    ("放弃比赛", "弃权怎么算分?", "forfeit points",
     "弃权判0比3负，积分与数据按规程处理。",
     "极少发生在世界杯决赛圈。",
     "弃权,0比3,积分,规程", "入门", "world_cup", "rule"),
    ("场上人数", "少于7人怎么算?", "fewer than seven",
     "一方场上不足7人比赛终止，判负。",
     "影响积分与公平竞赛记录。",
     "7人,终止,判负,排名", "入门", "both", "rule"),
    ("申诉排名", "排名能申诉吗?", "ranking protest",
     "场上事实由裁判与竞赛委员会裁定，排名依规程自动计算。",
     "纪律申诉不影响正常积分排名。",
     "申诉,排名,竞赛委员会,规程", "入门", "world_cup"),
    ("实时排名", "比赛中排名会变吗?", "live ranking",
     "末轮同开前实时排名随他组赛果变化。",
     "同开后各组独立决出最终名次。",
     "实时,排名,末轮,同开", "入门", "world_cup"),
    ("净胜球战略", "刷净胜球违规吗?", "running up score",
     "大比分获胜合法，但若明显侮辱性动作可能纪律处罚。",
     "1982后末轮同开减少控分动机。",
     "净胜球,大比分,纪律,合法", "入门", "world_cup"),
    ("相互仅一场", "两队只赛一场?", "single H2H match",
     "4队小组每两队仅交手一次，相互 tiebreaker 基于单场。",
     "平局则相互积分各1分。",
     "一场,相互,平局,积分", "入门", "world_cup"),
    ("加时进球", "小组赛有加时吗?", "group stage extra time",
     "小组赛平局即结束，无加时无点球。",
     "加时进球仅出现在淘汰赛。",
     "小组赛,无加时,平局,点球", "入门", "world_cup", "rule"),
    ("乌龙球排名", "乌龙影响净胜球吗?", "own goal ranking",
     "乌龙计为对方进球，影响该队失球与对手净胜球。",
     "射手榜与排名统计均计入。",
     "乌龙,净胜球,失球,统计", "入门", "world_cup", "rule"),
    ("点球进球", "点球算进球数吗?", "penalty goals ranking",
     "运动战与点球进球均计入进球数与净胜球。",
     "点球大战进球不计。",
     "点球,进球,运动战,统计", "入门", "world_cup", "rule"),
    ("公平竞赛历史", "谁常获公平竞赛队?", "Fair Play history",
     "巴西、西班牙、德国等曾多次获公平竞赛队奖。",
     "依当届全部比赛纪律数据。",
     "公平竞赛,巴西,西班牙,历史", "入门", "world_cup", "history"),
    ("2014哥伦比亚", "2014哥伦比亚第三?", "Colombia 2014 group",
     "2014哥伦比亚小组第一出线，非第三。",
     "该届希腊为公平竞赛队。",
     "2014,哥伦比亚,希腊,第一", "入门", "world_cup", "history"),
    ("2022日本", "2022日本小组第几?", "Japan 2022 group",
     "2022日本E组第一出线，击败西班牙与德国。",
     "该届公平竞赛队为英格兰。",
     "2022,日本,E组,第一", "入门", "world_cup", "history"),
    ("排名公示", "排名何时官方确认?", "official ranking confirm",
     "每组最后一场结束后竞赛委员会确认最终排名。",
     "随后更新32强或16强对阵。",
     "公示,确认,最后一场,对阵", "入门", "world_cup"),
    ("FIFA排名", "小组排名与FIFA排名?", "FIFA ranking separate",
     "世界杯小组排名仅依当届规程，与FIFA世界排名无关。",
     "世界排名用于分档抽签非场内排名。",
     "FIFA排名,无关,分档,抽签", "入门", "both"),
    ("女子世界杯", "女足排名规则一样吗?", "women ranking rules",
     "女子世界杯小组赛排名原则与男子相同。",
     "具体 tiebreaker 以当届规程为准。",
     "女足,排名,相同,规程", "入门", "both"),
    ("电子屏幕", "球员能看排名屏吗?", "ranking screen",
     "末轮同开前球场大屏可能显示其他组实时积分。",
     "同开后各场独立进行。",
     "大屏,实时,积分,末轮", "入门", "world_cup"),
    ("教练计算", "教练需要算分吗?", "coach calculations",
     "末轮前教练团队常模拟多种赛果组合确定战术。",
     "同开规则减少实时信息优势。",
     "教练,算分,模拟,战术", "入门", "world_cup"),
    ("出线条件", "末轮出线条件?", "qualification scenarios",
     "媒体常发布出线算术：胜平负各需何种他组结果。",
     "以FIFA官方竞赛规程为最终依据。",
     "出线,算术,条件,规程", "入门", "world_cup"),
    ("历史抽签", "世界杯用过抽签排名吗?", "lots in history",
     "1990爱尔兰与荷兰积分相同靠抽签分一二。",
     "现规程仍保留最终抽签条款。",
     "1990,爱尔兰,荷兰,抽签", "进阶", "world_cup", "history"),
    ("规程优先", "排名以何为准?", "regulations authority",
     "当届FIFA World Cup Regulations为排名与 tiebreaker 最高依据。",
     "与IFAB竞赛规则并行适用。",
     "规程,最高,依据,IFAB", "入门", "world_cup", "rule"),
]


def row(seq: int, entry: tuple) -> dict[str, str]:
    l3, q, aliases, short, detail, kw, diff = entry[:7]
    scope, fact_type, flags = "world_cup", "rule", ""
    for x in entry[7:]:
        if x in ("world_cup", "both", "football_general"):
            scope = x
        elif x in ("history", "rule"):
            fact_type = x
        else:
            flags = x
    return {
        "id": f"WC-TFMT-{seq:05d}",
        "category_l1": "世界杯赛制与组织",
        "category_l2": "公平竞赛与排名",
        "category_l3": l3,
        "scope": scope,
        "priority": "5",
        "question": q,
        "question_aliases": aliases,
        "answer_short": short,
        "answer_detail": detail,
        "answer_format": "definition",
        "keywords": kw,
        "tags": "赛制,排名",
        "entities": "",
        "related_ids": "",
        "difficulty": diff,
        "era_start": "",
        "era_end": "",
        "region": "全球",
        "language": "zh-CN",
        "fact_type": fact_type,
        "confidence": "official",
        "source_type": "FIFA",
        "source_ref": "FIFA World Cup regulations",
        "content_flags": flags,
        "updated_at": "2026-06-03",
    }


def main() -> None:
    assert len(ENTRIES) == 50
    for e in ENTRIES:
        assert len(e[3]) <= 120, e[0]
        assert len(e[5].split(",")) >= 3, e[0]
    new_rows = [row(START_ID + i - 1, e) for i, e in enumerate(ENTRIES, start=1)]
    existing: list[dict[str, str]] = []
    if OUTPUT.exists():
        with OUTPUT.open(newline="", encoding="utf-8") as f:
            existing = [dict(r) for r in csv.DictReader(f) if (r.get("id") or "").strip()]

    ids = {r["id"] for r in existing}
    for r in new_rows:
        if r["id"] in ids:
            raise SystemExit(f"duplicate id {r['id']}")

    with OUTPUT.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=COLUMNS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(existing)
        writer.writerows(new_rows)
    print(f"Appended {len(new_rows)} rows (total {len(existing) + len(new_rows)})")


if __name__ == "__main__":
    main()
