#!/usr/bin/env python3
"""Generate T025 glossary batch: 50 referee terminology entries (append).

Network: none (local structured data). Outbound HTTP must use fetch_utils.RateLimitedFetcher (>=1s/request); see docs/maintainers/data-collection-policy.md and .cursor/rules/world-cup-data-collection.mdc."""

from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUTPUT = ROOT / "data" / "knowledge_glossary.csv"
START_ID = 251

COLUMNS = [
    "id", "category_l1", "category_l2", "category_l3", "scope", "priority",
    "question", "question_aliases", "answer_short", "answer_detail", "answer_format",
    "keywords", "tags", "entities", "related_ids", "difficulty",
    "era_start", "era_end", "region", "language", "fact_type", "confidence",
    "source_type", "source_ref", "content_flags", "updated_at",
]

ENTRIES = [
    ("主裁判", "主裁判的职责是什么?", "主裁|Referee",
     "主裁判全场执法，拥有最终判罚权，负责鸣哨、出牌、判定位球与确认进球。",
     "世界杯决赛主裁由FIFA指派国际级裁判担任。",
     "主裁判,主裁,执法,判罚", "入门"),
    ("第一助理裁判", "第一助理裁判做什么?", "边裁|AR1",
     "第一助理裁判负责一侧边线，协助判罚越位、球出界及犯规方向。",
     "与第二助理裁判分守两条边线。",
     "助理裁判,边裁,越位,边线", "入门"),
    ("第二助理裁判", "第二助理裁判做什么?", "边裁|AR2",
     "第二助理裁判负责另一侧边线，职责与第一助理裁判相同。",
     "举旗示意越位与出界，主裁可最终采纳或更改。",
     "助理裁判,边裁,越位,协助", "入门"),
    ("第四官员", "第四官员的职责是什么?", "Fourth Official",
     "第四官员管理换人、补时举牌、替补席纪律并协助主裁维持场边秩序。",
     "主裁无法继续执法时可由第四官员替补。",
     "第四官员,换人,补时,场边", "入门"),
    ("VAR", "裁判如何使用VAR?", "视频助理裁判|Video Review",
     "VAR在视频室复核进球、点球、红牌及认错身份四类清晰严重错漏，建议主裁改判或维持。",
     "主裁可到场边监视器亲自查看。",
     "VAR,视频裁判,复核,改判", "入门"),
    ("AVAR", "AVAR在裁判组中做什么?", "助理VAR",
     "AVAR协助VAR操作回放、沟通并建议复核类别，不直接在场内执法。",
     "与VAR共同在视频操作室工作。",
     "AVAR,视频裁判,助理,复核", "进阶"),
    ("有利原则", "裁判何时适用有利原则?", "advantage|play on",
     "犯规后若进攻方仍保有明显进攻优势，裁判可延迟吹哨并口头示意比赛继续。",
     "事后仍可向犯规球员补发卡牌。",
     "有利原则,advantage,延迟,进攻", "进阶"),
    ("间接任意球示意", "裁判单臂上举是什么意思?", "间接任意球|单臂上举",
     "裁判单臂上举表示间接任意球，须保持至球进入球门或出界/换死球。",
     "若直接射入且未触及其他球员，判球门球或界外球。",
     "间接任意球,单臂上举,示意,规则", "入门"),
    ("点球判罚手势", "裁判判点球时的手势?", "指点球点|penalty signal",
     "裁判指向点球点，表示禁区内犯规或手球等应判点球。",
     "点球判罚后通常仍可能出牌。",
     "点球,手势,判罚,禁区", "入门"),
    ("黄牌出示", "裁判如何出示黄牌?", "yellow card|警告",
     "裁判从口袋取出黄牌举过头顶，向违纪球员口头说明并记录。",
     "同一球员第二张黄牌将导致罚下。",
     "黄牌,警告,出示,纪律", "入门"),
    ("红牌出示", "裁判如何出示红牌?", "red card|罚下",
     "裁判出示红牌，球员须立即离场且不得替补补位。",
     "可直接红牌或由两黄变一红。",
     "红牌,罚下,出示,退场", "入门"),
    ("两黄变一红", "两黄变一红的程序?", "second yellow|黄加黄",
     "裁判先出示第二张黄牌，再出示红牌，球员被罚下。",
     "两黄可来自不同性质违纪。",
     "两黄变一红,黄牌,红牌,程序", "入门"),
    ("越位旗示", "边裁举旗示越位怎么做?", "越位旗|offside flag",
     "助理裁判在传球瞬间认定越位后举旗，主裁吹停并判间接任意球。",
     "世界杯现辅以半自动越位技术辅助。",
     "越位,边裁,举旗,助理裁判", "入门"),
    ("犯规方向", "边裁旗示犯规方向?", "方向旗|foul direction",
     "助理裁判旗指向进攻方向表示哪方获得任意球或界外球。",
     "主裁可能未看清时参考边裁示意。",
     "犯规方向,边裁,旗语,任意球", "入门"),
    ("界外球指示", "裁判如何指示界外球?", "throw-in direction",
     "裁判手臂斜指方向，表示由哪队掷界外球。",
     "最后触球方判定归属。",
     "界外球,指示,边线,裁判", "入门"),
    ("角球指示", "裁判如何指示角球?", "corner kick signal",
     "裁判指向角球区，表示攻方获得角球。",
     "守方最后触球越过门线且未进球。",
     "角球,指示,角球区,裁判", "入门"),
    ("球门球指示", "裁判如何指示球门球?", "goal kick signal",
     "裁判手臂指向球门区，表示守方开球门球。",
     "攻方最后触球越过门线且未进球。",
     "球门球,指示,球门区,裁判", "入门"),
    ("补时举牌", "第四官员如何示补时?", "added time board",
     "第四官员在场边电子牌或手牌显示上下半场补时分钟数。",
     "实际补时可能略长于所示数字。",
     "补时,举牌,第四官员,时间", "入门"),
    ("换人管理", "裁判如何管理换人?", "substitution procedure",
     "第四官员检查替补与下场球员，主裁在死球时允许替补从边线进入。",
     "世界杯正赛换人名额依赛事规程执行。",
     "换人,替补,第四官员,程序", "入门"),
    ("队长沟通", "裁判为何找队长沟通?", "captain talk",
     "主裁通过队长传达纪律要求、控制比赛节奏并减少球员围堵。",
     "队长应代表球队与裁判理性沟通。",
     "队长,沟通,纪律,主裁", "入门"),
    ("口头警告", "裁判口头警告是什么?", "verbal warning",
     "对轻微违纪先口头警告，再犯或严重时可正式出牌。",
     "拖延时间、抗议判罚常先获口头警告。",
     "口头警告,警告,纪律,裁判", "入门"),
    ("9.15米距离", "裁判如何管理任意球距离?", "ten yards|9.15米",
     "裁判确保防守球员距球至少9.15米，可用喷雾标记或步量。",
     "提前移动或未退距可被黄牌。",
     "9.15米,任意球,距离,人墙", "入门"),
    ("喷雾标记", "裁判喷雾是做什么的?", "vanishing spray|任意球喷雾",
     "裁判用泡沫喷雾标记球位置与人墙线，10秒左右消失。",
     "2014世界杯起广泛使用，减少距离争议。",
     "喷雾,任意球,标记,人墙", "入门"),
    ("视频复核", "VAR视频复核流程?", "on-field review|OFR",
     "主裁可到场边监视器观看回放，结合VAR建议作出最终决定。",
     "重大判罚常采用现场复核。",
     "视频复核,OFR,VAR,监视器", "进阶"),
    ("静默复核", "静默复核是什么?", "silent check|VAR静默",
     "VAR在后台静默检查进球、点球等，若无明显错漏不中断比赛节奏。",
     "进球后常先静默复核再庆祝确认。",
     "静默复核,VAR,进球,复核", "进阶"),
    ("半自动越位", "半自动越位技术是什么?", "SAOT|半自动越位",
     "通过球与球员追踪，辅助裁判更快判定越位，世界杯2022起使用。",
     "可生成3D动画辅助转播解释。",
     "半自动越位,SAOT,越位,技术", "进阶"),
    ("越位划线", "转播越位划线怎么看?", "offside line|划线",
     "转播回放显示传球瞬间进攻球员与倒数第二名防守球员相对位置。",
     "体毛级越位常引发讨论。",
     "越位划线,回放,VAR,判定", "进阶"),
    ("进球复核", "VAR如何复核进球?", "goal check",
     "复核进球前是否有犯规、手球、越位或球未完全过线。",
     "确认后主裁可做出进球有效手势。",
     "进球复核,VAR,有效,越位", "入门"),
    ("点球复核", "VAR如何复核点球?", "penalty check",
     "复核禁区内是否犯规、是否手球及犯规地点是否在禁区内。",
     "漏判点球可由VAR建议补判。",
     "点球复核,VAR,禁区,犯规", "进阶"),
    ("红牌复核", "VAR如何复核红牌?", "red card review",
     "复核暴力行为、严重犯规或错认身份是否应直红。",
     "错牌可改判或撤销。",
     "红牌复核,VAR,暴力,改判", "进阶"),
    ("认错身份", "VAR认错身份是什么?", "mistaken identity",
     "当裁判向错误球员出牌时，VAR可提示纠正身份。",
     "为VAR四类复核情形之一。",
     "认错身份,VAR,出牌,纠正", "进阶"),
    ("手球判罚", "裁判如何判手球?", "handball decision",
     "考虑是否故意、是否扩大身体面积、是否得分或创造明显机会。",
     "2019年后规则对手球判罚有更细化说明。",
     "手球,判罚,手臂,规则", "进阶"),
    ("严重犯规", "严重犯规如何认定?", "serious foul play",
     "使用过度力量或危及对手安全的动作，通常直红并判直接任意球或点球。",
     "铲球、蹬踏、暴力冲撞常属此类。",
     "严重犯规,红牌,暴力,判罚", "进阶"),
    ("暴力行为", "暴力行为如何处罚?", "violent conduct",
     "无球状态下攻击对手或他人，或严重暴力动作，通常直红。",
     "可追加赛后停赛处罚。",
     "暴力行为,红牌,停赛,纪律", "进阶"),
    ("侮辱裁判", "侮辱裁判怎么罚?", "dissent|disrespect",
     "公然侮辱、威胁或围堵裁判，可黄牌；严重侮辱可直红。",
     "多人围堵裁判可能多张黄牌。",
     "侮辱裁判,黄牌,纪律,抗议", "入门"),
    ("拖延时间", "裁判如何处罚拖延时间?", "time wasting",
     "门将长时间持球、慢开球、换人不迅速等，可口头警告后黄牌。",
     "补时会相应增加。",
     "拖延时间,黄牌,补时,警告", "入门"),
    ("替补席违纪", "替补席违纪怎么罚?", "bench misconduct",
     "替补或教练在场边违纪，裁判可出示黄牌或红牌并报告赛事机构。",
     "红牌对象无法被换下但须离场。",
     "替补席,违纪,黄牌,教练", "进阶"),
    ("技术区", "技术区规则是什么?", "technical area",
     "教练与替补须在指定技术区内，不得擅自进入场地或过度抗议。",
     "越界可能被警告或驱逐。",
     "技术区,教练,场边,规则", "进阶"),
    ("电子换人牌", "电子换人牌是什么?", "substitution board",
     "第四官员举牌显示上下场球员号码，便于转播与记录。",
     "世界杯采用统一换人程序。",
     "换人牌,电子牌,第四官员,换人", "入门"),
    ("国际级裁判", "FIFA国际级裁判是什么?", "FIFA referee",
     "经FIFA认证可执法国际赛事包括世界杯的裁判等级。",
     "主裁、助理、VAR均须达到相应标准。",
     "国际级裁判,FIFA,世界杯,认证", "进阶"),
    ("裁判组", "世界杯裁判组如何组成?", "referee team",
     "通常包括主裁、两名助理裁判、第四官员及VAR团队。",
     "同组裁判常来自同一足协或区域。",
     "裁判组,助理,VAR,世界杯", "进阶"),
    ("回避原则", "裁判回避原则是什么?", "referee neutrality",
     "裁判通常不执法本国球队比赛，避免利益冲突与质疑。",
     "世界杯由中立国家裁判执法。",
     "回避,中立,裁判,公平", "进阶"),
    ("公平竞赛", "公平竞赛奖与裁判关系?", "Fair Play",
     "裁判通过一致执法维护公平竞赛；球队纪律影响公平竞赛奖评选。",
     "世界杯设公平竞赛奖表彰纪律最佳球队。",
     "公平竞赛,纪律,裁判,奖项", "入门"),
    ("点球大战裁判", "点球大战裁判做什么?", "shootout referee",
     "主裁监督轮流点球程序、门将站位、球员进入禁区等规则。",
     "助理裁判协助确认门将线与球员顺序。",
     "点球大战,裁判,十二码,程序", "进阶"),
    ("开球权", "裁判如何决定开球方?", "kick-off choice",
     "赛前抛币，胜者选开球或半场方向，负者获剩余选择。",
     "加时赛重新抛币。",
     "开球权,抛币,开球,赛前", "入门"),
    ("比赛中止", "裁判何时中止比赛?", "suspend match",
     "严重骚乱、场地不安全或极端天气等，裁判可中止或终止比赛。",
     "世界杯极少发生，但有应急预案。",
     "中止比赛,终止,裁判,安全", "专业"),
    ("额外球员", "额外球员进场如何判罚?", "outside agent",
     "非场上球员或已换下球员擅自进场干扰比赛，裁判可暂停并依规则处罚。",
     "VAR可协助发现干扰进球情况。",
     "额外球员,进场,干扰,判罚", "进阶"),
    ("赛后报告", "裁判赛后报告写什么?", "match report",
     "裁判向赛事机构提交红黄牌、冲突、VAR介入等书面报告。",
     "纪律委员会依据报告追加处罚。",
     "赛后报告,纪律,裁判,FIFA", "专业"),
    ("裁判沟通耳机", "裁判耳机通信做什么?", "referee communication",
     "主裁与助理裁判、第四官员通过耳机实时沟通越位与犯规。",
     "提高判罚一致性与反应速度。",
     "耳机,沟通,助理裁判,协作", "进阶"),
    ("进球有效手势", "裁判确认进球的手势?", "goal signal",
     "主裁跑向中圈并手臂指向中圈，示意进球有效、比赛从中圈重启。",
     "VAR确认后常做此手势。",
     "进球有效,手势,主裁,开球", "入门"),
]


def row(seq: int, entry: tuple) -> dict[str, str]:
    l3, q, aliases, short, detail, kw, diff = entry
    return {
        "id": f"WC-GLOS-{seq:05d}",
        "category_l1": "术语与百科",
        "category_l2": "裁判术语",
        "category_l3": l3,
        "scope": "both",
        "priority": "4",
        "question": q,
        "question_aliases": aliases,
        "answer_short": short,
        "answer_detail": detail,
        "answer_format": "definition",
        "keywords": kw,
        "tags": "裁判术语,术语",
        "entities": "",
        "related_ids": "",
        "difficulty": diff,
        "era_start": "",
        "era_end": "",
        "region": "全球",
        "language": "zh-CN",
        "fact_type": "term",
        "confidence": "official",
        "source_type": "IFAB",
        "source_ref": "IFAB Laws of the Game 2024/25; FIFA Refereeing Guidelines",
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
