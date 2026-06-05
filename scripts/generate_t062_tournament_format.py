#!/usr/bin/env python3
"""Generate T062: 50 World Cup 32-team finals format entries (append).

Network: none (local structured data). Outbound HTTP must use fetch_utils.RateLimitedFetcher (>=1s/request); see docs/data-collection-policy.md and .cursor/rules/world-cup-data-collection.mdc."""

from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUTPUT = ROOT / "data" / "knowledge_tournament_format.csv"
START_ID = 101

COLUMNS = [
    "id", "category_l1", "category_l2", "category_l3", "scope", "priority",
    "question", "question_aliases", "answer_short", "answer_detail", "answer_format",
    "keywords", "tags", "entities", "related_ids", "difficulty",
    "era_start", "era_end", "region", "language", "fact_type", "confidence",
    "source_type", "source_ref", "content_flags", "updated_at",
]

ENTRIES = [
    ("32队结构", "32强世界杯怎么踢?", "32-team format",
     "32队分8组双循环，小组前两名进16强单场淘汰。",
     "1998至2022年长期采用此结构。",
     "32队,8组,16强,淘汰", "入门", "world_cup"),
    ("小组数量", "世界杯分几个小组?", "eight groups",
     "32队时代共分8个小组，每组4队。",
     "每组6场小组赛。",
     "8组,每组4队,小组,数量", "入门", "world_cup"),
    ("小组赛程", "小组赛踢几场?", "group matches",
     "每组4队双循环，每队3场、每组共6场。",
     "全组共48场小组赛。",
     "3场,双循环,48场,小组", "入门", "world_cup"),
    ("积分制", "小组赛积分规则?", "group points",
     "胜3分、平1分、负0分，积分高者排名靠前。",
     "同分依规程比较净胜球等。",
     "胜3,平1,积分,排名", "入门", "world_cup"),
    ("出线名额", "每组出线几队?", "top two advance",
     "每组前两名晋级淘汰赛，共16队。",
     "第三名、第四名出局。",
     "前两名,出线,16队,淘汰", "入门", "world_cup"),
    ("同分细则", "小组赛同分怎么排?", "tie-breakers group",
     "通常依次比较净胜球、进球数、相互战绩、公平竞赛积分等。",
     "仍无法区分可抽签。",
     "同分,净胜球,相互,抽签", "进阶", "world_cup"),
    ("无加时小组", "小组赛平局怎么办?", "draw in group",
     "小组赛90分钟平局即结束，不踢加时与点球。",
     "各得1分。",
     "平局,小组赛,无加时,1分", "入门", "world_cup"),
    ("16强对阵", "16强如何配对?", "round of 16",
     "各组第一对阵其他组第二，具体对阵依抽签结果。",
     "同组出线队淘汰赛不再相遇。",
     "16强,对阵,第一,第二", "入门", "world_cup"),
    ("单场淘汰", "淘汰赛踢几场?", "single elimination",
     "16强起为单场决胜，无主场累积。",
     "平局进入加时与点球。",
     "单场,淘汰,加时,点球", "入门", "world_cup"),
    ("8强", "四分之一决赛规则?", "quarter-finals",
     "16强胜者进入8强，仍为单场90分钟。",
     "胜者晋级半决赛。",
     "8强,四分之一,单场,晋级", "入门", "world_cup"),
    ("半决赛", "半决赛规则?", "semi-finals",
     "两场半决赛胜者进决赛，负者进三四名赛。",
     "赛制与16强相同。",
     "半决赛,决赛,三四名,负者", "入门", "world_cup"),
    ("三四名", "季军争夺战规则?", "third place",
     "半决赛负者单场决季军，通常无加时直接点球（依当届规程）。",
     "部分届次曾取消。",
     "季军,三四名,半决赛,点球", "入门", "world_cup"),
    ("决赛", "决赛规则?", "final rules",
     "冠军战90分钟平则加时，仍平则点球大战。",
     "全球单场关注度最高。",
     "决赛,加时,点球,冠军", "入门", "world_cup"),
    ("加时赛", "淘汰赛加时多久?", "extra time",
     "加时赛为上下半场各15分钟，共30分钟。",
     "仍平局则点球。",
     "加时,30分钟,15分钟,点球", "入门", "world_cup"),
    ("点球大战", "点球大战顺序?", "penalty shootout",
     "依IFAB点球程序，先五轮后骤死，门将可更换。",
     "须在球门线技术支持下进行。",
     "点球,IFAB,骤死,门将", "入门", "both"),
    ("换人名额", "世界杯每场换几人?", "five subs",
     "近年决赛圈正赛多允许每场最多5次换人。",
     "脑震荡协议可额外换人。",
     "换人,5次,脑震荡,正赛", "入门", "world_cup"),
    ("大名单", "决赛圈大名单人数?", "squad size",
     "每队报名大名单人数依当届规程，含门将与场上球员。",
     "赛前截止，赛中调整有限。",
     "大名单,人数,报名,截止", "入门", "world_cup"),
    ("每场报名", "每场首发名单几人?", "match sheet",
     "每场提交11人首发与替补席名单，人数上限依规程。",
     "未报名球员不得出场。",
     "首发,11人,替补,名单", "入门", "world_cup"),
    ("黄牌累积", "小组赛黄牌停赛?", "booking suspension",
     "累积两张黄牌停赛一场，淘汰赛阈值依当届规程。",
     "决赛前可能部分清零。",
     "黄牌,累积,停赛,清零", "进阶", "world_cup"),
    ("红牌停赛", "世界杯红牌停赛?", "red card ban",
     "直红通常至少停赛一场，严重暴力由纪律委员会追加。",
     "适用世界杯纪律条例。",
     "红牌,停赛,纪律,追加", "进阶", "world_cup"),
    ("VAR", "决赛圈VAR规则?", "VAR finals",
     "2018起全面VAR，2022起半自动越位辅助。",
     "仅用于四类清晰错误。",
     "VAR,半自动,越位,四类", "入门", "both"),
    ("开球时间", "比赛开球时间?", "kick-off schedule",
     "小组赛多分散时段，淘汰赛关键战多在 prime time。",
     "主办国时区决定当地时间。",
     "开球,赛程,时区,prime", "入门", "world_cup"),
    ("休息天数", "球队休息间隔?", "rest days",
     "FIFA赛程尽量保证淘汰赛球队休息不少于两天。",
     "高温届次可能调整。",
     "休息,间隔,赛程,两天", "进阶", "world_cup"),
    ("同组回避淘汰", "淘汰赛同组回避?", "group avoid KO",
     "16强对阵避免同组前两名再碰，依抽签 bracket 设计。",
     "8强后可能相遇。",
     "回避,同组,16强,bracket", "入门", "world_cup"),
    ("积分相同三队", "三队同分怎么办?", "three-way tie",
     "先比较三队间小循环积分与净胜球，再回全体比较。",
     "细则在当届规程附件。",
     "三队,同分,小循环,净胜球", "进阶", "world_cup"),
    ("0分出线可能", "能否0分出线?", "zero point advance",
     "理论可能但极罕见，需极端净胜球与相互战绩组合。",
     "实际极少出现。",
     "0分,出线,罕见,净胜球", "进阶", "world_cup"),
    ("进球纪录", "小组赛进球算金靴吗?", "Golden Boot group",
     "金靴统计含淘汰赛全部进球，小组赛同样计入。",
     "助攻评选依技术定义。",
     "金靴,进球,统计,淘汰", "入门", "world_cup"),
    ("加时金球", "世界杯有金球制胜吗?", "golden goal abolished",
     "金球制曾短期使用，现已取消，加时踢满30分钟。",
     "与现行IFAB一致。",
     "金球制,取消,加时,IFAB", "进阶", "world_cup", "history"),
    ("银球制", "银球制还在吗?", "silver goal",
     "银球制已废止，加时必须打满上下半场。",
     "历史规则，现行无效。",
     "银球制,废止,历史,加时", "进阶", "world_cup", "history"),
    ("并列小组第一", "小组第一重要吗?", "group winner",
     "小组第一在16强对阵中通常面对较弱第二，位置有利。",
     "仍取决于抽签 bracket。",
     "小组第一,对阵,bracket,有利", "入门", "world_cup"),
    ("净胜球", "为何重视净胜球?", "goal difference",
     "同分时净胜球常为第一 tie-breaker，鼓励进攻。",
     "极端情况可致保守战术争议。",
     "净胜球,同分,tie-break,进攻", "入门", "world_cup"),
    ("公平竞赛分", "公平竞赛积分作用?", "fair play points",
     "极端同分情形可能比较球队公平竞赛分（黄红牌少者优）。",
     "亦关系公平竞赛奖评选。",
     "公平竞赛,黄牌,同分,奖项", "进阶", "world_cup"),
    ("抽签后位置", "小组第三能出线吗?", "third place",
     "32队制下小组第三不能出线，仅前二晋级。",
     "与部分俱乐部赛不同。",
     "小组第三,出局,前二,不同", "入门", "world_cup"),
    ("6队小组历史", "世界杯有5队小组吗?", "historical groups",
     "1930年曾有2队小组踢1场，1950有循环决赛组，非现行32制。",
     "现行规程为4队一组。",
     "历史,小组,1930,现行", "进阶", "world_cup", "history"),
    ("并列出线", "两队同分携手出线?", "both advance",
     "若前两名积分相同且tie-break后仍并列，可同时出线。",
     "第三名则出局。",
     "并列,出线,前二,第三", "入门", "world_cup"),
    ("淘汰赛场次", "夺冠最多踢几场?", "matches to title",
     "若小组第三出线不可能，冠军最多7场：3小组+4淘汰。",
     "季军最多8场含三四名。",
     "7场,冠军,小组,淘汰", "入门", "world_cup"),
    ("点球统计", "点球大战算进球吗?", "penalty goals stats",
     "点球大战进球不计入球员金靴，但计入比赛总进球纪录讨论。",
     "赛果记为点球胜。",
     "点球大战,金靴,不计,赛果", "进阶", "world_cup"),
    ("乌龙球", "乌龙算谁进球?", "own goals",
     "乌龙球计入对方球员个人统计规则依技术报告。",
     "金靴评选有专门说明。",
     "乌龙,统计,金靴,对方", "进阶", "world_cup"),
    ("补时", "世界杯补时规则?", "stoppage time",
     "裁判依IFAB指引裁定上下半场补时，VAR检查时间可追加。",
     "无无限加时。",
     "补时,裁判,IFAB,VAR", "入门", "both"),
    ("中场休息", "中场休息多久?", "half-time",
     "中场休息不超过15分钟，加时中场可更短。",
     "组委会可安排简短仪式。",
     "中场,15分钟,休息,加时", "入门", "both"),
    ("赛前热身", "赛前热身时间?", "warm-up",
     "双方各有规定分钟数在场内热身，依竞赛通告。",
     "迟到可被罚。",
     "热身,赛前,通知,迟到", "入门", "world_cup"),
    ("队长袖标", "队长袖标要求?", "captain armband",
     "场上队长须佩戴官方袖标，替补登场须移交。",
     "礼仪与识别用途。",
     "队长,袖标,移交,识别", "入门", "world_cup"),
    ("球衣冲突", "球衣颜色冲突?", "kit clash",
     "客队通常更换备用颜色，裁判赛前检查对比度。",
     "守门员须与场上球员区分。",
     "球衣,颜色,客队,门将", "入门", "world_cup"),
    ("医疗暂停", "脑震荡换人流程?", "concussion sub",
     "疑似脑震荡可触发额外换人，球员须离场检查。",
     "保护球员健康优先。",
     "脑震荡,换人,检查,保护", "进阶", "world_cup"),
    ("补水暂停", "高温补水暂停?", "cooling break",
     "极端高温可设官方补水暂停，依赛前气象指引。",
     "2022等届次曾使用。",
     "补水,高温,暂停,气象", "进阶", "world_cup"),
    ("未用完换人", "换人名额能留吗?", "unused subs",
     "每场换人名额不可累积到下一场。",
     "5次换人指5名不同球员可上场替换次数规则依规程。",
     "换人,名额,不累积,每场", "入门", "world_cup"),
    ("门将换人", "用完换人还能换门将吗?", "GK substitution",
     "若门将受伤且换人已用完，可特殊允许（依当届脑震荡/伤病条款）。",
     "具体以当届规程为准。",
     "门将,受伤,特殊,换人", "进阶", "world_cup"),
    ("积分盘", "如何读世界杯积分榜?", "standings table",
     "官网公布每组积分、进球、净胜球与出线形势。",
     "末轮多组同时开球防默契球。",
     "积分榜,净胜球,末轮,官网", "入门", "world_cup"),
    ("默契球防范", "末轮同时开球?", "simultaneous kickoff",
     "小组赛末轮同组两场常同时开球，降低默契球风险。",
     "FIFA赛程组惯例安排。",
     "末轮,同时开球,默契球,赛程", "入门", "world_cup"),
    ("32制结束", "32队制用到何时?", "end of 32",
     "2022卡塔尔为最后一届32队决赛圈，2026起扩军48队。",
     "新赛制见当届规程。",
     "32队,2022,2026,48队", "入门", "world_cup"),
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
        "category_l2": "正赛赛制",
        "category_l3": l3,
        "scope": scope,
        "priority": "5",
        "question": q,
        "question_aliases": aliases,
        "answer_short": short,
        "answer_detail": detail,
        "answer_format": "definition",
        "keywords": kw,
        "tags": "赛制,正赛",
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
