#!/usr/bin/env python3
"""Generate T064: 50 World Cup draw pots & seeding entries (append).

Network: none (local structured data). Outbound HTTP must use fetch_utils.RateLimitedFetcher (>=1s/request); see docs/data-collection-policy.md and .cursor/rules/world-cup-data-collection.mdc."""

from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUTPUT = ROOT / "data" / "knowledge_tournament_format.csv"
START_ID = 201

COLUMNS = [
    "id", "category_l1", "category_l2", "category_l3", "scope", "priority",
    "question", "question_aliases", "answer_short", "answer_detail", "answer_format",
    "keywords", "tags", "entities", "related_ids", "difficulty",
    "era_start", "era_end", "region", "language", "fact_type", "confidence",
    "source_type", "source_ref", "content_flags", "updated_at",
]

ENTRIES = [
    ("决赛圈抽签", "世界杯决赛圈抽签做什么?", "finals draw",
     "将晋级球队分入小组并确定小组赛程与淘汰赛 bracket 位置。",
     "在决赛圈开始前公开举行。",
     "抽签,小组,赛程,bracket", "入门", "world_cup"),
    ("分档原则", "抽签分档依据什么?", "pot seeding",
     "通常按FIFA排名与近期成绩将球队划入一至四档或更多档。",
     "分档表赛前由FIFA公布。",
     "分档,排名,种子,FIFA", "入门", "world_cup"),
    ("一档种子", "一档通常有哪些队?", "pot 1",
     "东道主与排名最高的若干队在一档，避免过早相遇。",
     "具体数量随参赛队数调整。",
     "一档,东道主,种子,排名", "入门", "world_cup"),
    ("二档", "二档球队怎么定?", "pot 2",
     "次高排名球队进入二档，抽签时各组分配一档+二档等。",
     "保证实力分散。",
     "二档,排名,分配,分散", "入门", "world_cup"),
    ("三档四档", "三档四档作用?", "pots 3-4",
     "较低排名球队分入三、四档，仍遵守洲际回避等规则。",
     "新晋级球队可能在四档。",
     "三档,四档,回避,新军", "入门", "world_cup"),
    ("洲际回避", "抽签回避同洲?", "confederation avoid",
     "同一大洲球队尽量不集中在同一小组（除欧洲特殊配额）。",
     "细则在抽签程序附件。",
     "回避,同洲,欧洲,小组", "入门", "world_cup"),
    ("欧洲上限", "每组欧洲队上限?", "UEFA cap per group",
     "因欧洲队多，规程常限每组最多两支欧洲球队。",
     "防止欧洲内战占满小组。",
     "欧洲,上限,两组,规程", "入门", "world_cup"),
    ("东道主档位", "东道主在第几档?", "host in pot 1",
     "东道主通常固定在一档并优先确定小组座位。",
     "多国主办时各国均可能在一档。",
     "东道主,一档,座位,优先", "入门", "world_cup"),
    ("抽签仪式", "抽签仪式谁主持?", "draw ceremony",
     "FIFA官员、特邀嘉宾与球队代表出席，电视全球直播。",
     "仪式本身不产生竞技结果。",
     "仪式,直播,嘉宾,FIFA", "入门", "world_cup"),
    ("球与碗", "抽签用球机制?", "draw balls",
     "球队名放入球或胶囊，按顺序抽取组别与位置。",
     "过程受公证监督。",
     "球,胶囊,抽取,公证", "入门", "world_cup"),
    ("计算机辅助", "抽签用电脑吗?", "computer draw",
     "部分步骤可用计算机生成随机序列，仍公开透明。",
     "预选赛抽签亦可能使用。",
     "计算机,随机,透明,预选", "进阶", "world_cup"),
    ("赛程生成", "抽签后如何排赛程?", "fixture schedule",
     "组委会依模板填充球队代号，确定开球日期与球场。",
     "末轮同组同时开球防默契球。",
     "赛程,模板,末轮,球场", "入门", "world_cup"),
    ("淘汰赛路径", "淘汰赛 bracket 何时定?", "KO bracket",
     "小组位置决定16强潜在对阵路径，抽签结束时 bracket 框架已现。",
     "具体对手待小组赛后确定。",
     "bracket,16强,路径,框架", "入门", "world_cup"),
    ("A组第一", "A组第一去哪?", "winner path",
     "各组第一、第二在抽签时已对应到 bracket 特定槽位。",
     "如A1对B2等依当届表。",
     "A1,对阵,槽位,第二", "入门", "world_cup"),
    ("同组回避淘汰", "淘汰赛避开同组?", "group avoid KO",
     "16强对阵设计使同组前两名淘汰赛首轮不相遇。",
     "8强后可能碰面。",
     "同组,16强,回避,8强", "入门", "world_cup"),
    ("预选赛抽签", "世预赛也抽签吗?", "qualifier draw",
     "各大洲预选赛启动前举行抽签分档分组。",
     "分档依据排名与近期赛果。",
     "世预赛,抽签,分档,分组", "入门", "world_cup"),
    ("附加赛抽签", "洲际附加赛抽签?", "playoff draw",
     "洲际附加赛对阵由抽签或预定配对决定主客顺序。",
     "单场或双回合依规程。",
     "附加赛,抽签,主客,对阵", "入门", "world_cup"),
    ("排名依据", "分档用哪版排名?", "ranking snapshot",
     "FIFA在抽签前指定截止日期排名快照作为分档依据。",
     "截止日期后友谊赛不计入分档。",
     "排名,快照,截止,分档", "入门", "world_cup"),
    ("未晋级队", "未出线队参与抽签吗?", "only qualified",
     "仅已晋级决赛圈球队参加决赛圈抽签。",
     "预选赛出局队不参与。",
     "晋级,决赛圈,不参与,出局", "入门", "world_cup"),
    ("抽签争议", "抽签不公能申诉吗?", "draw protest",
     "程序错误可在时限内申诉，结果极少推翻重抽。",
     "技术故障有应急预案。",
     "申诉,程序,重抽,故障", "进阶", "world_cup"),
    ("政治回避", "抽签政治回避?", "political avoid",
     "敏感政治对阵可能被规程回避（如特殊安全情形）。",
     "个案依FIFA安全评估。",
     "政治,回避,安全,评估", "进阶", "world_cup"),
    ("种子队好处", "种子队有何优势?", "seeding benefit",
     "种子避免小组赛过早碰其他强队，并可能获更有利淘汰赛路径。",
     "非保证出线。",
     "种子,优势,路径,非保证", "入门", "world_cup"),
    ("死亡之组", "什么是死亡之组?", "group of death",
     "媒体对多支强队同组的称呼，非官方术语。",
     "仍须按积分规则出线。",
     "死亡之组,媒体,强队,积分", "入门", "world_cup"),
    ("最弱小组", "有最弱小组吗?", "weak group",
     "分档旨在均衡，但随机性可能导致某组整体排名较低。",
     "竞技结果仍不确定。",
     "最弱,随机,分档,不确定", "入门", "world_cup"),
    ("抽签权重", "抽签完全随机吗?", "weighted draw",
     "在回避规则约束下随机，非纯均匀概率。",
     "计算机抽签满足约束条件。",
     "随机,约束,回避,计算机", "进阶", "world_cup"),
    ("嘉宾抽签", "名人协助抽签?", "celebrity draw",
     "特邀前球星或名宿抽取球号增加观赏性。",
     "正式结果由竞赛部门记录。",
     "嘉宾,名宿,观赏性,记录", "入门", "world_cup"),
    ("球队代表", "抽签谁出席?", "team delegation",
     "各国足协主席或队长出席领取组别信息。",
     "未出席不影响资格。",
     "代表,足协,队长,出席", "入门", "world_cup"),
    ("媒体区", "抽签媒体规则?", "media draw",
     "全球媒体转播抽签，采访球队即时反应。",
     "与竞赛规则无关。",
     "媒体,转播,采访,反应", "入门", "world_cup"),
    ("抽签时间", "抽签何时举行?", "draw date",
     "通常在决赛圈前数月，留出备战与热身赛时间。",
     "日期由FIFA公告。",
     "日期,数月前,备战,公告", "入门", "world_cup"),
    ("48队抽签", "2026抽签有何不同?", "draw 48 teams",
     "12组结构将使分档与回避规则相对32队时代调整。",
     "以当届抽签程序为准。",
     "2026,12组,分档,调整", "入门", "world_cup", "rule_change_2026"),
    ("更多种子", "48队需要更多档?", "more pots",
     "参赛队增加可能增加分档数量或每档球队数。",
     "官方程序赛前发布。",
     "48队,分档,数量,程序", "进阶", "world_cup", "rule_change_2026"),
    ("三国东道主", "三东道主抽签座位?", "three hosts draw",
     "美加墨可能各占一档并分入不同小组。",
     "具体座位依抽签结果。",
     "三国,东道主,小组,座位", "入门", "world_cup", "time_sensitive"),
    ("小组赛程冲突", "抽签避俱乐部冲突?", "club conflict",
     "赛程组尽量错开同联赛球员过多的开球时间。",
     "非硬性竞赛规则。",
     "赛程,俱乐部,错开,联赛", "进阶", "world_cup"),
    ("电视偏好", "抽签考虑转播?", "TV scheduling",
     "关键对阵开球时间考虑全球收视，由组委会决定。",
     "球队可申请调整有限。",
     "转播,开球,收视,调整", "进阶", "world_cup"),
    ("历史手球", "1986抽签手球?", "Hand of God draw",
     "1986年墨西哥世界杯抽签曾用“上帝之手”梗，属历史轶事。",
     "与现代程序无关。",
     "1986,轶事,历史,抽签", "进阶", "world_cup", "history"),
    ("2018抽签", "2018抽签在哪?", "Moscow 2018 draw",
     "2018年抽签在莫斯科举行，32队分8组。",
     "东道主俄罗斯在一档。",
     "2018,莫斯科,8组,俄罗斯", "入门", "world_cup", "history"),
    ("2022抽签", "2022抽签特点?", "Doha 2022 draw",
     "2022年抽签在多哈举行，32队，冬季赛期随后公布。",
     "东道主卡塔尔在一档。",
     "2022,多哈,卡塔尔,冬季", "入门", "world_cup", "history"),
    ("洲际附加抽签", "附加赛主客抽签?", "home away draw",
     "双回合附加赛主客顺序由抽签决定。",
     "单场则中立或主客预定。",
     "主客,附加赛,顺序,单场", "入门", "world_cup"),
    ("女子世界杯抽签", "女子赛抽签?", "women draw",
     "女子世界杯独立举行抽签，分档规则类似但队伍数不同。",
     "规程单独公布。",
     "女子,抽签,独立,分档", "入门", "both"),
    ("U20抽签", "青年赛抽签?", "youth draw",
     "U20世界杯等青年赛事有独立抽签，与男子决赛圈无关。",
     "年龄组规程分开。",
     "U20,青年,独立,无关", "入门", "both"),
    ("练习抽签", "有彩排抽签吗?", "dress rehearsal",
     "组委会可能内部彩排流程，不公布结果。",
     "正式抽签一次有效。",
     "彩排,内部,流程,正式", "进阶", "world_cup"),
    ("抽签后友谊赛", "抽签后热身?", "friendlies post-draw",
     "球队在决赛圈前安排友谊赛演练战术。",
     "对手选择避开同组强队泄密。",
     "热身,友谊赛,战术,同组", "入门", "world_cup"),
    ("球衣发布", "抽签后发布球衣?", "kit launch",
     "不少球队在抽签后发布世界杯球衣，属商业活动。",
     "与分档无关。",
     "球衣,发布,商业,球队", "入门", "world_cup"),
    ("球迷旅行", "抽签后订票?", "fan travel planning",
     "球迷依据小组城市规划行程，属观赛安排。",
     "FIFA提供官方旅行信息。",
     "球迷,行程,城市,订票", "入门", "world_cup"),
    ("博彩误解", "能否预测抽签结果?", "no prediction service",
     "知识库不提供任何结果预测或胜负建议，仅说明程序规则。",
     "抽签结果赛前未知。",
     "预测,不提供,程序,未知", "入门", "world_cup"),
    ("抽签公平", "如何保证公平?", "integrity measures",
     "公证人、媒体监督与公开直播确保程序可信。",
     "违规将纪律调查。",
     "公平,公证,监督,纪律", "入门", "world_cup"),
    ("重抽案例", "历史上重抽过吗?", "re-draw rare",
     "极少数因程序错误宣布无效后重抽，案例罕见。",
     "以官方记录为准。",
     "重抽,罕见,程序错误,记录", "进阶", "world_cup", "history"),
    ("抽签符号", "为何用动物 mascot?", "draw icons",
     "仪式视觉设计使用图标或吉祥物增加辨识度。",
     "不影响分组逻辑。",
     "视觉,吉祥物,仪式,分组", "入门", "world_cup"),
    ("数据发布", "抽签后数据?", "data release",
     "FIFA官网同步发布小组名单、赛程与 bracket 图。",
     "供媒体与球迷使用。",
     "官网,赛程,bracket,数据", "入门", "world_cup"),
    ("AI分档讨论", "AI能否代抽签?", "AI not used",
     "正式抽签由FIFA规定程序执行，不委托商业AI预测分组。",
     "技术分析仅供内部筹备参考。",
     "AI,抽签,程序,FIFA", "进阶", "world_cup"),
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
        "category_l2": "抽签与分档",
        "category_l3": l3,
        "scope": scope,
        "priority": "5",
        "question": q,
        "question_aliases": aliases,
        "answer_short": short,
        "answer_detail": detail,
        "answer_format": "definition",
        "keywords": kw,
        "tags": "赛制,抽签",
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
