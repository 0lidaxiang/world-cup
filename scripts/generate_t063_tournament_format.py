#!/usr/bin/env python3
"""Generate T063: 50 World Cup 2026 48-team expansion format entries (append).

Network: none (local structured data). Outbound HTTP must use fetch_utils.RateLimitedFetcher (>=1s/request); see docs/maintainers/data-collection-policy.md and .cursor/rules/world-cup-data-collection.mdc."""

from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUTPUT = ROOT / "data" / "knowledge_tournament_format.csv"
START_ID = 151

COLUMNS = [
    "id", "category_l1", "category_l2", "category_l3", "scope", "priority",
    "question", "question_aliases", "answer_short", "answer_detail", "answer_format",
    "keywords", "tags", "entities", "related_ids", "difficulty",
    "era_start", "era_end", "region", "language", "fact_type", "confidence",
    "source_type", "source_ref", "content_flags", "updated_at",
]

ENTRIES = [
    ("扩军48队", "2026世界杯几队参赛?", "48 teams 2026",
     "2026年美加墨世界杯决赛圈扩军至48支球队。",
     "为1930年以来最大规模决赛圈。",
     "2026,48队,扩军,决赛圈", "入门", "world_cup", "rule_change_2026"),
    ("主办三国", "2026世界杯哪里办?", "USA Canada Mexico",
     "由美国、加拿大、墨西哥联合主办，三国共享赛事。",
     "墨西哥第三次主办，加拿大首次。",
     "2026,美加墨,主办,联合", "入门", "world_cup", "time_sensitive"),
    ("新小组结构", "48队如何分组?", "12 groups of 4",
     "计划分为12个小组，每组4队，前两名出线共24队。",
     "具体以当届公布的最终规程为准。",
     "12组,4队,出线,24队", "入门", "world_cup", "rule_change_2026"),
    ("小组赛场次", "48队小组赛多少场?", "group match count",
     "每组6场、12组共72场小组赛（4队双循环）。",
     "较32队时代增加24场小组赛场次。",
     "72场,小组赛,双循环,增加", "入门", "world_cup", "rule_change_2026"),
    ("淘汰赛32强", "24队出线后怎么踢?", "round of 32",
     "24队出线后进入32强淘汰赛，需8队附加或轮空机制依规程。",
     "FIFA公布的bracket设计以官方文件为准。",
     "32强,24队,淘汰,bracket", "进阶", "world_cup", "rule_change_2026"),
    ("名额增加", "2026各洲名额变化?", "quota increase 2026",
     "扩军后亚洲、非洲、中北美等名额普遍上调。",
     "精确数字以FIFA理事会当届决议为准。",
     "名额,亚洲,非洲,上调", "入门", "world_cup", "rule_change_2026"),
    ("赛程长度", "2026赛事是否更长?", "longer tournament",
     "参赛队与场次增加，总赛程预计长于32队时代。",
     "具体天数见组委会赛历。",
     "赛程,天数,场次,更长", "入门", "world_cup", "time_sensitive"),
    ("场馆分布", "2026场馆跨三国?", "venues three countries",
     "比赛分布在三国多座城市，跨境旅行依签证与交通规划。",
     "组委会协调统一竞赛标准。",
     "场馆,三国,城市,签证", "入门", "world_cup", "time_sensitive"),
    ("时区挑战", "2026跨时区开球?", "time zones",
     "北美多时差，开球时间兼顾全球转播与本地 prime time。",
     "球员休息与旅行时间纳入赛程设计。",
     "时区,开球,转播,休息", "进阶", "world_cup", "time_sensitive"),
    ("夏季赛历", "2026仍在夏季吗?", "June July schedule",
     "2026年预计6-7月举行，与俱乐部赛季窗口协调。",
     "最终日期以FIFA公告为准。",
     "夏季,6月,7月,赛历", "入门", "world_cup", "time_sensitive"),
    ("东道主席位", "2026三个东道主都晋级吗?", "three hosts qualify",
     "美加墨均自动获得决赛圈席位，细则写入当届规程。",
     "不占本洲附加名额或依决议执行。",
     "东道主,自动,三国,席位", "入门", "world_cup", "rule_change_2026"),
    ("抽签变化", "48队抽签有何不同?", "draw changes",
     "抽签分档与回避规则将随队数增加调整。",
     "正式流程在决赛圈前公布。",
     "抽签,分档,回避,48队", "入门", "world_cup", "rule_change_2026"),
    ("同组第三", "小组第三能否出线?", "third place 2026",
     "现行48队方案为每组前二出线，第三不出线。",
     "若规程修订以官方文本为准。",
     "小组第三,不出线,前二,方案", "入门", "world_cup", "rule_change_2026"),
    ("最佳第三名", "是否恢复最佳第三名?", "best third place",
     "1998年前曾用最佳第三名，2026方案以FIFA公布为准。",
     "知识库不预设未公布规则。",
     "最佳第三,历史,公布,方案", "进阶", "world_cup", "rule_change_2026"),
    ("淘汰赛64?", "会有64强吗?", "no round of 64",
     "48队结构下从24或32强阶段进入淘汰，非64队锦标赛。",
     "避免与俱乐部赛混淆。",
     "64强,误解,淘汰,48队", "入门", "world_cup", "rule_change_2026"),
    ("冠军场次", "2026夺冠最多几场?", "matches to win",
     "若仍为3场小组+4场淘汰，冠军最多7场，与32队制相同。",
     "若增加附加轮次则场次上调。",
     "7场,冠军,小组,淘汰", "入门", "world_cup", "rule_change_2026"),
    ("换人规则", "2026换人名额?", "subs 2026",
     "预计延续每场5次换人及脑震荡协议，以当届规程为准。",
     "IFAB全球规则同步更新。",
     "换人,5次,脑震荡,规程", "入门", "world_cup", "time_sensitive"),
    ("VAR", "2026 VAR技术?", "VAR 2026",
     "预计继续使用VAR与半自动越位，可能升级版本。",
     "技术方案赛前认证。",
     "VAR,半自动,2026,升级", "入门", "world_cup", "time_sensitive"),
    ("气候场馆", "2026是否全在空调场?", "climate venues",
     "北美部分球场为露天，高温场次可能设补水暂停。",
     "不像2022全部可封闭空调场。",
     "气候,露天,补水,北美", "入门", "world_cup", "time_sensitive"),
    ("旅行距离", "球员旅行负担?", "travel load",
     "三国主办导致部分球队跨境飞行增多。",
     "赛程组尽量缩短淘汰赛旅行。",
     "旅行,跨境,负担,赛程", "进阶", "world_cup", "time_sensitive"),
    ("球迷签证", "跨国观赛签证?", "fan visas",
     "观赛球迷可能需多国签证，组委会提供指引。",
     "与竞赛规则无关但影响观赛。",
     "签证,观赛,跨国,指引", "入门", "world_cup", "time_sensitive"),
    ("票务", "2026门票销售?", "ticketing 2026",
     "票务由FIFA与主办联合体销售，分阶段放票。",
     "实名制依当地法规。",
     "门票,销售,FIFA,实名", "入门", "world_cup", "time_sensitive"),
    ("legacy", "2026遗产目标?", "legacy 2026",
     "强调基层足球、女足发展与可持续场馆利用。",
     "赛后评估依FIFA报告。",
     "遗产,基层,女足,可持续", "入门", "world_cup", "time_sensitive"),
    ("预选赛已调", "世预赛已按48队调整?", "qualifiers adjusted",
     "2022周期后的世预赛名额已按扩军方案分配。",
     "各洲末轮赛制相应延长或增加。",
     "世预赛,名额,调整,各洲", "入门", "world_cup", "rule_change_2026"),
    ("新军机会", "扩军利好哪些队?", "more debutants",
     "名额增加使中小足球协会更有机会晋级决赛圈。",
     "实际结果取决于预选赛。",
     "新军,中小协会,名额,机会", "入门", "world_cup", "rule_change_2026"),
    ("竞争激烈", "扩军会降低质量吗?", "quality debate",
     "FIFA认为可提升全球参与，竞技强度仍由预选赛筛选。",
     "讨论属观点，规程只规定席位。",
     "质量,参与,预选赛,观点", "进阶", "world_cup", "rule_change_2026"),
    ("商业收入", "48队商业影响?", "commercial impact",
     "更多场次可能增加媒体与赞助曝光，分配依FIFA财务规则。",
     "与场上规则无直接关系。",
     "商业,赞助,场次,媒体", "进阶", "world_cup", "time_sensitive"),
    ("转播", "2026转播安排?", "broadcast 2026",
     "全球媒体权由FIFA出售，三国信号制作协调。",
     "开球时间影响亚洲观众。",
     "转播,媒体权,全球,亚洲", "入门", "world_cup", "time_sensitive"),
    ("吉祥物", "2026吉祥物?", "mascot 2026",
     "官方吉祥物与视觉识别将赛前发布。",
     "属品牌活动。",
     "吉祥物,2026,品牌,发布", "入门", "world_cup", "time_sensitive"),
    ("官方用球", "2026比赛用球?", "ball 2026",
     "将发布专用官方用球，须通过IFAB认证。",
     "名称赛前揭晓。",
     "用球,官方,2026,认证", "入门", "world_cup", "time_sensitive"),
    ("主题曲", "2026主题曲?", "song 2026",
     "赛事音乐活动依组委会文化计划公布。",
     "非竞赛规程内容。",
     "主题曲,文化,2026,活动", "入门", "world_cup", "time_sensitive"),
    ("志愿者", "2026志愿者招募?", "volunteers 2026",
     "三国将招募大量志愿者协助运营。",
     "培训标准统一依FIFA手册。",
     "志愿者,招募,运营,手册", "入门", "world_cup", "time_sensitive"),
    ("安保", "2026安保协调?", "security 2026",
     "跨国安保由各国政府与组委会合作。",
     "球场准入依当地法规。",
     "安保,政府,准入,合作", "入门", "world_cup", "time_sensitive"),
    ("反歧视", "2026反歧视计划?", "anti-discrimination",
     "延续FIFA反歧视与公平竞赛活动，赛场零容忍。",
     "球员教育赛前完成。",
     "反歧视,公平竞赛,教育,零容忍", "入门", "world_cup", "time_sensitive"),
    ("可持续性", "2026碳足迹目标?", "sustainability",
     "主办承诺减少碳足迹、推广公共交通与绿色场馆。",
     "指标在可持续报告中披露。",
     "可持续,碳足迹,绿色,交通", "进阶", "world_cup", "time_sensitive"),
    ("与2022对比", "2026与2022赛制差?", "vs Qatar 2022",
     "2022为32队冬赛单国；2026为48队夏赛三国。",
     "规程文件分别适用当届。",
     "2022,对比,32队,单国", "入门", "world_cup", "rule_change_2026"),
    ("俱乐部影响", "扩军俱乐部放人更久?", "club release longer",
     "决赛圈场次增加可能延长国家队征召总天数。",
     "国际足联与职业联赛协商日历。",
     "俱乐部,放人,日历,协商", "进阶", "both", "rule_change_2026"),
    ("伤病风险", "赛程密会增加伤病?", "injury risk",
     "密集赛程是医学关注重点，轮换与休息依队医管理。",
     "规程尽量保证淘汰赛休息天数。",
     "伤病,密集,休息,轮换", "进阶", "world_cup", "time_sensitive"),
    ("女子赛事", "2026不影响女子赛?", "women separate",
     "女子世界杯赛历独立，2026扩军不改变女子规程。",
     "女子2027等届次单独公布。",
     "女子,独立,赛历,规程", "入门", "both", "rule_change_2026"),
    ("青少队", "2026与U20关系?", "youth separate",
     "U20世界杯等青年赛事与男子48队决赛圈无关。",
     "年龄组别规程分开。",
     "U20,青年,无关,分开", "入门", "both"),
    ("规则试验", "2026会试验新规则吗?", "trial laws",
     "世界杯通常不试验IFAB临时规则，除非全球已采纳。",
     "以赛前IFAB版本为准。",
     "规则,试验,IFAB,采纳", "进阶", "both", "time_sensitive"),
    ("半自动越位", "2026半自动越位?", "SAOT 2026",
     "预计延续半自动越位辅助，提升判罚一致性。",
     "设备赛前测试认证。",
     "半自动,越位,2026,SAOT", "入门", "world_cup", "time_sensitive"),
    ("点球新规", "2026点球规则变吗?", "penalties 2026",
     "点球大战程序依当时有效的IFAB规则。",
     "无世界杯单独点球规则。",
     "点球,IFAB,程序,一致", "入门", "both", "time_sensitive"),
    ("加时", "2026加时规则?", "extra time 2026",
     "淘汰赛预计仍为30分钟加时后点球。",
     "小组赛无加时。",
     "加时,淘汰,小组,点球", "入门", "world_cup", "rule_change_2026"),
    ("三四名", "2026还有季军战吗?", "third place 2026",
     "预计保留三四名决赛，除非当届规程另定。",
     "以FIFA赛历公告为准。",
     "季军战,三四名,保留,赛历", "入门", "world_cup", "time_sensitive"),
    ("揭幕战", "2026揭幕战在哪?", "opening match",
     "揭幕战城市与对阵由组委会与FIFA赛前公布。",
     "通常由美国或墨西哥主要场馆承办。",
     "揭幕战,开幕,城市,公布", "入门", "world_cup", "time_sensitive"),
    ("决赛场地", "2026决赛在哪踢?", "final venue",
     "决赛预计在美国大型场馆举行，具体球场待确认。",
     "官方确认后更新知识库。",
     "决赛,场地,美国,待确认", "入门", "world_cup", "time_sensitive"),
    ("积分APP", "如何查2026积分榜?", "live standings",
     "FIFA官方应用与网站提供实时积分与出线形势。",
     "数据以官方记录为准。",
     "积分榜,官方,应用,实时", "入门", "world_cup", "time_sensitive"),
    ("FAQ更新", "2026规则会变吗?", "regulations may update",
     "在决赛圈前FIFA可能微调规程，以最新公布文本为准。",
     "本库条目标注rule_change_2026或time_sensitive。",
     "微调,公布,最新,标注", "入门", "world_cup", "rule_change_2026"),
    ("历史意义", "48队扩军历史意义?", "historic expansion",
     "标志世界杯进入新的全球参与规模阶段。",
     "赛制细节需随官方文件迭代。",
     "48队,历史,参与,规模", "入门", "world_cup", "history"),
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
        "category_l2": "2026扩军",
        "category_l3": l3,
        "scope": scope,
        "priority": "5",
        "question": q,
        "question_aliases": aliases,
        "answer_short": short,
        "answer_detail": detail,
        "answer_format": "definition",
        "keywords": kw,
        "tags": "赛制,2026",
        "entities": "",
        "related_ids": "",
        "difficulty": diff,
        "era_start": "2026",
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
