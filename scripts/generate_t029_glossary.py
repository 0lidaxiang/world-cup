#!/usr/bin/env python3
"""Generate T029 glossary batch: 50 World Cup-specific terms (append).

Network: none (local structured data). Outbound HTTP must use fetch_utils.RateLimitedFetcher (>=1s/request); see docs/data-collection-policy.md and .cursor/rules/world-cup-data-collection.mdc."""

from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUTPUT = ROOT / "data" / "knowledge_glossary.csv"
START_ID = 451

COLUMNS = [
    "id", "category_l1", "category_l2", "category_l3", "scope", "priority",
    "question", "question_aliases", "answer_short", "answer_detail", "answer_format",
    "keywords", "tags", "entities", "related_ids", "difficulty",
    "era_start", "era_end", "region", "language", "fact_type", "confidence",
    "source_type", "source_ref", "content_flags", "updated_at",
]

ENTRIES = [
    ("大力神杯", "大力神杯是什么?", "世界杯奖杯|FIFA World Cup Trophy",
     "大力神杯是世界杯冠军奖杯，由18K金制成，冠军球队赛后需归还由FIFA保管。",
     "1974年起使用，取代雷米特杯。",
     "大力神杯,奖杯,冠军,世界杯", "入门"),
    ("雷米特杯", "雷米特杯是什么?", "旧世界杯奖杯|Jules Rimet",
     "1930至1970年使用的世界杯奖杯，巴西三冠后永久保留原件。",
     "现用大力神杯替代。",
     "雷米特杯,奖杯,历史,巴西", "进阶"),
    ("FIFA世界杯", "FIFA世界杯是什么?", "World Cup|世界杯赛",
     "FIFA主办的国家队最高水平赛事，每四年一届，全球影响力最大的单项体育赛之一。",
     "男子世界杯自1930年首届乌拉圭举办。",
     "FIFA,世界杯,国家队,四年一届", "入门"),
    ("小组赛", "世界杯小组赛怎么踢?", "group stage|小组阶段",
     "正赛首轮各队分小组循环赛，积分排名决定出线或淘汰。",
     "2022为8组每组4队，2026扩军后赛制将调整。",
     "小组赛,出线,积分,赛制", "入门"),
    ("淘汰赛", "世界杯淘汰赛规则?", "knockout stage|单场淘汰",
     "小组出线后进入单场决胜，平局则加时与点球大战直至分出胜负。",
     "从16强至决赛均为淘汰赛。",
     "淘汰赛,单场,加时,点球", "入门"),
    ("32强", "世界杯32强是什么?", "正赛32队|32支球队",
     "指世界杯正赛阶段32支参赛队，2022卡塔尔沿用此规模。",
     "2026将扩军至48队。",
     "32强,正赛,参赛队,扩军", "入门"),
    ("48强", "2026世界杯48队什么意思?", "扩军48队|48支球队",
     "2026美加墨世界杯将首次有48队参赛，赛制与分组方式相应调整。",
     "FIFA已公布新赛制框架。",
     "48强,2026,扩军,赛制", "入门"),
    ("开幕战", "世界杯开幕战是什么?", "揭幕战|opening match",
     "赛事首场或象征性开幕比赛，常由东道主之一参与。",
     "全球转播关注度极高。",
     "开幕战,揭幕战,首场,东道主", "入门"),
    ("决赛", "世界杯决赛是什么?", "final|冠军战",
     "两支胜者争夺大力神杯的单场决赛，全球收视峰值常出现在此。",
     "决赛于赛事末周举行。",
     "决赛,冠军,大力神杯,单场", "入门"),
    ("季军战", "世界杯季军战是什么?", "third place play-off|三四名",
     "半决赛负者之间的比赛，决出第三、第四名。",
     "部分球员视其为荣誉战，部分球队大幅轮换。",
     "季军战,三四名,半决赛,荣誉", "入门"),
    ("金靴奖", "世界杯金靴奖是什么?", "Golden Boot|最佳射手",
     "授予决赛阶段进球最多的球员，进球相同则比较助攻等。",
     "克洛泽以16球保持世界杯历史总进球纪录。",
     "金靴,最佳射手,进球,奖项", "入门"),
    ("金球奖", "世界杯金球奖是什么?", "Golden Ball|最佳球员",
     "授予决赛阶段表现最突出的球员，由媒体投票产生。",
     "与法国《France Football》杂志评选的金球奖为不同奖项。",
     "金球,最佳球员,奖项,世界杯", "入门"),
    ("金手套", "世界杯金手套是什么?", "Golden Glove|最佳门将",
     "授予决赛阶段表现最佳的门将。",
     "2010起正式设立该奖项。",
     "金手套,最佳门将,门将,奖项", "入门"),
    ("最佳年轻球员", "世界杯最佳年轻球员?", "Best Young Player|最佳新人",
     "授予21岁及以下（具体以赛事规程为准）表现突出球员。",
     "姆巴佩2018年获此奖。",
     "最佳年轻球员,新人,奖项,21岁", "入门"),
    ("公平竞赛奖", "世界杯公平竞赛奖?", "Fair Play Award|公平竞赛",
     "授予赛事期间纪律表现最佳、球迷行为等综合评分高的球队。",
     "黄牌更少、体育精神更佳为参考因素。",
     "公平竞赛,纪律,奖项,球队", "入门"),
    ("最佳进球奖", "世界杯最佳进球奖?", "Goal of the Tournament",
     "由FIFA或球迷投票选出赛事最精彩进球。",
     "2018起较受关注。",
     "最佳进球,奖项,精彩,投票", "入门"),
    ("抽签", "世界杯抽签是什么?", "draw|分组抽签",
     "正赛前公开仪式将球队分入小组并确定赛程，按分档与地理规则回避。",
     "全球媒体直播抽签结果。",
     "抽签,分组,赛程,仪式", "入门"),
    ("分档", "世界杯分档是什么?", "pot seeding|种子分档",
     "按世界排名或过往成绩将球队分为若干档，抽签时各档均衡分布。",
     "东道主通常锁定一档。",
     "分档,种子,排名,抽签", "进阶"),
    ("种子队", "世界杯种子队是什么?", "seeded team|一档",
     "分档中排名较高球队，抽签时避免小组赛过早相遇。",
     "一档通常含东道主与排名前列球队。",
     "种子队,一档,排名,抽签", "入门"),
    ("死亡之组", "死亡之组是什么意思?", "group of death|强组",
     "指小组赛汇聚多支强队、出线竞争异常激烈的小组，非官方术语。",
     "媒体常用形容吸引眼球的分组。",
     "死亡之组,小组赛,强队,出线", "入门"),
    ("东道主", "世界杯东道主有什么特权?", "host nation|主办国",
     "主办国自动获得正赛席位，并常参与开幕战，享有主场支持。",
     "2002日韩、2022卡塔尔等为亚洲东道主。",
     "东道主,主办国,自动晋级,开幕", "入门"),
    ("联合举办", "世界杯联合举办是什么?", "co-host|多国主办",
     "一届赛事由两个或更多国家共同主办，如2002日韩、2026美加墨。",
     "赛程与后勤协调更复杂。",
     "联合举办,多国,2026,主办", "入门"),
    ("世界杯吉祥物", "世界杯吉祥物是什么?", "mascot|官方吉祥物",
     "每届设计的官方形象，用于推广与周边，如2018扎比瓦卡、2022拉伊卜。",
     "体现主办国文化元素。",
     "吉祥物,mascot,推广,文化", "入门"),
    ("主题曲", "世界杯主题曲是什么?", "official song|主题歌",
     "赛事官方或合作推广歌曲，如2010 Waka Waka、2014 We Are One等。",
     "与开幕式表演常相关联。",
     "主题曲,歌曲,推广,开幕式", "入门"),
    ("官方用球", "世界杯官方用球?", "World Cup ball|比赛用球",
     "FIFA与赞助商为当届赛事发布的专用足球，具独特设计与命名。",
     "阿迪达斯长期为世界杯供应用球。",
     "官方用球,足球,阿迪达斯,装备", "入门"),
    ("卫冕冠军", "卫冕冠军是什么意思?", "defending champion|上届冠军",
     "上一届世界杯冠军球队，下届以卫冕冠军身份参赛。",
     "1966起无球队成功卫冕世界杯。",
     "卫冕冠军,上届冠军,魔咒,球队", "入门"),
    ("卫冕魔咒", "世界杯卫冕魔咒是什么?", "no repeat champion",
     "自1966英格兰后尚无球队成功卫冕世界杯冠军，被媒体称为魔咒。",
     "竞技强度与赛程因素常被讨论。",
     "卫冕,魔咒,冠军,历史", "入门"),
    ("东道主魔咒", "东道主表现规律?", "host nation performance",
     "东道主常小组赛出线且偶有夺冠，但非必然；表现因队实力而异。",
     "1930乌拉圭、1966英格兰、1998法国等东道主夺冠。",
     "东道主,主场,出线,冠军", "进阶"),
    ("洲际名额", "世界杯各大洲名额?", "qualification slots|名额分配",
     "FIFA按各大洲分配正赛席位，通过预选赛决出，名额随扩军调整。",
     "欧洲、南美、亚洲等配额不同。",
     "名额,洲际,预选赛,分配", "进阶"),
    ("预选赛", "世界杯预选赛是什么?", "World Cup qualification|世预赛",
     "正赛前的洲际或区域系列赛，球队争夺有限世界杯席位。",
     "周期长达数年。",
     "预选赛,世预赛,出线,席位", "入门"),
    ("洲际附加赛", "世界杯附加赛是什么?", "intercontinental playoff",
     "部分大洲球队通过附加赛争夺最后席位，常跨洲对阵。",
     "单场或两回合形式依规程而定。",
     "附加赛,洲际,席位,出线", "进阶"),
    ("26人大名单", "世界杯26人大名单?", "squad size|报名名单",
     "2022卡塔尔起正赛报名扩至26人，比赛日可换人数相应增加。",
     "此前长期为23人。",
     "26人,大名单,报名,2022", "入门"),
    ("比赛日名单", "世界杯比赛日名单?", "matchday squad|每场名单",
     "每场可从26人中选特定人数进入替补席，具体上限依当届规程。",
     "教练根据战术与伤病调整。",
     "比赛日,替补席,名单,每场", "进阶"),
    ("国籍资格", "世界杯球员国籍规则?", "eligibility|代表资格",
     "球员须持有该国国籍并满足FIFA国家队变更规则方可代表该国。",
     "归化球员须符合居住或血统条件。",
     "国籍,资格,代表,规则", "进阶"),
    ("世界杯周期", "世界杯周期是什么?", "four-year cycle|四年周期",
     "相邻两届正赛间隔约四年，含预选赛、洲际赛与俱乐部赛季交错。",
     "2022至2026因卡塔尔改期略有调整。",
     "周期,四年,预选赛,赛程", "入门"),
    ("冬世界杯", "2022冬世界杯为何特殊?", "winter World Cup|冬季举办",
     "卡塔尔2022因夏季高温改在11–12月举办，打破北半球夏季惯例。",
     "欧洲联赛赛季中途暂停配合。",
     "冬世界杯,2022,卡塔尔,赛程", "入门"),
    ("官方合作伙伴", "世界杯赞助商是什么?", "FIFA partner|合作伙伴",
     "FIFA全球合作伙伴与赛事赞助商，球场广告与转播露出受其约束。",
     "与国家队装备赞助商可能不同。",
     "赞助商,合作伙伴,FIFA,商业", "进阶"),
    ("比赛官员", "世界杯裁判如何选派?", "match officials|裁判组",
     "FIFA从全球国际级裁判中选派主裁、助理与VAR团队执法世界杯。",
     "同组裁判通常来自同一足协体系。",
     "裁判,官员,选派,FIFA", "进阶"),
    ("VAR世界杯", "世界杯VAR何时启用?", "VAR at World Cup",
     "2018俄罗斯世界杯首次在正赛全面使用VAR，2022继续并升级半自动越位。",
     "重大判罚透明度提高。",
     "VAR,2018,视频裁判,世界杯", "入门"),
    ("半自动越位", "2022半自动越位是什么?", "SAOT|世界杯越位",
     "2022卡塔尔世界杯使用半自动越位辅助，加快判罚并生成3D动画。",
     "与VAR流程结合。",
     "半自动越位,2022,SAOT,技术", "进阶"),
    ("官方海报", "世界杯官方海报?", "poster|宣传海报",
     "每届发布的官方视觉形象，用于全球推广。",
     "设计风格体现主办国文化。",
     "海报,官方,推广,设计", "入门"),
    ("Fan Festival", "世界杯球迷节是什么?", "fan zone|球迷区",
     "主办城市设立的官方球迷观赛与活动区，未购票者也可参与氛围。",
     "2022卡塔尔设多个官方球迷区。",
     "球迷节,fan zone,观赛,活动", "入门"),
    ("世足最高舞台", "为何称世界杯最高舞台?", "biggest stage|顶级赛事",
     "全球曝光、国家队荣誉与四年等待使世界杯成为多数球员生涯最高目标。",
     "与俱乐部欧冠为不同维度荣誉。",
     "最高舞台,荣誉,国家队,目标", "入门"),
    ("世界杯停办", "世界杯曾停办吗?", "World War hiatus|停办",
     "1942与1946因二战未举办，1950恢复后每四年一届延续至今。",
     "1930首届后仅两次中断。",
     "停办,二战,历史,1942", "进阶"),
    ("首届世界杯", "首届世界杯在哪办?", "1930 Uruguay|第一届",
     "1930年乌拉圭举办首届世界杯，13队参赛，东道主乌拉圭夺冠。",
     "雷米特杯时期开始。",
     "首届,1930,乌拉圭,历史", "入门"),
    ("扩军历史", "世界杯扩军历程?", "expansion history|参赛队增加",
     "从1930年13队到1998年32队，2026将增至48队，反映全球足球发展。",
     "扩军影响赛制与预选赛配额。",
     "扩军,历史,48队,赛制", "进阶"),
    ("点球大战", "世界杯点球大战规则?", "shootout in World Cup",
     "淘汰赛加时仍平局则点球决胜，世界杯史上多届决赛曾进入点球大战。",
     "1994、2006、2022决赛均有点球大战。",
     "点球大战,淘汰赛,决胜,决赛", "入门"),
    ("世界杯纪录", "世界杯有哪些著名纪录?", "World Cup records|纪录",
     "包括总进球、出场次数、连胜、最年轻进球等，由FIFA与媒体统计。",
     "克洛泽16球为历史射手王。",
     "纪录,历史,进球,统计", "入门"),
    ("全进球球员", "世界杯全进球球员?", "scored in every game|每场进球",
     "指在当届决赛阶段每场比赛均有进球的球员，极罕见成就。",
     "媒体统计术语非官方奖项。",
     "全进球,纪录,罕见,射手", "专业"),
    ("世界杯口号", "世界杯宣传口号?", "tagline|slogan",
     "每届赛事官方推广语，如2022“Now is All”等，用于全球营销。",
     "与吉祥物、海报共同构成视觉体系。",
     "口号,slogan,推广,营销", "入门"),
]


def row(seq: int, entry: tuple) -> dict[str, str]:
    l3, q, aliases, short, detail, kw, diff = entry
    return {
        "id": f"WC-GLOS-{seq:05d}",
        "category_l1": "术语与百科",
        "category_l2": "世界杯专属",
        "category_l3": l3,
        "scope": "world_cup",
        "priority": "5",
        "question": q,
        "question_aliases": aliases,
        "answer_short": short,
        "answer_detail": detail,
        "answer_format": "definition",
        "keywords": kw,
        "tags": "世界杯专属,术语",
        "entities": "",
        "related_ids": "",
        "difficulty": diff,
        "era_start": "",
        "era_end": "",
        "region": "全球",
        "language": "zh-CN",
        "fact_type": "term",
        "confidence": "official",
        "source_type": "FIFA",
        "source_ref": "FIFA World Cup Regulations & official publications",
        "content_flags": "time_sensitive",
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
