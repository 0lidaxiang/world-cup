#!/usr/bin/env python3
"""Generate T027 glossary batch: 50 youth academy & reserve team terms (append).

Network: none (local structured data). Outbound HTTP must use fetch_utils.RateLimitedFetcher (>=1s/request); see docs/maintainers/data-collection-policy.md and .cursor/rules/world-cup-data-collection.mdc."""

from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUTPUT = ROOT / "data" / "knowledge_glossary.csv"
START_ID = 351

COLUMNS = [
    "id", "category_l1", "category_l2", "category_l3", "scope", "priority",
    "question", "question_aliases", "answer_short", "answer_detail", "answer_format",
    "keywords", "tags", "entities", "related_ids", "difficulty",
    "era_start", "era_end", "region", "language", "fact_type", "confidence",
    "source_type", "source_ref", "content_flags", "updated_at",
]

ENTRIES = [
    ("青训", "足球青训是什么意思?", "青训体系|youth academy",
     "青训是俱乐部或机构对青少年球员进行系统训练与培养的长周期项目。",
     "优秀青训可为一线队与国家队输送人才。",
     "青训,青少年,培养,俱乐部", "入门"),
    ("梯队", "俱乐部梯队是什么?", "梯队体系|youth teams",
     "梯队指俱乐部按年龄或级别划分的各级青年队与预备队，构成人才金字塔。",
     "常见从U12至U23及预备队层级。",
     "梯队,青年队,级别,俱乐部", "入门"),
    ("一线队", "一线队是什么意思?", "成年队|first team",
     "一线队是俱乐部最高级别球队，参加顶级联赛与杯赛，世界杯球员多出自一线队。",
     "青训球员目标通常是进入一线队。",
     "一线队,成年队,顶级联赛,球员", "入门"),
    ("预备队", "预备队是什么?", "B队|reserve team",
     "预备队介于青年队与一线队之间，多为成年替补与年轻球员提供比赛平台。",
     "部分联赛预备队可参加低级别联赛。",
     "预备队,B队,替补,比赛", "入门"),
    ("U23", "U23队是什么?", "Under 23|23岁以下",
     "U23指23岁以下年龄组球队，奥运会男足以U23为主并允许少量超龄球员。",
     "俱乐部U23常参与青年联赛或友谊赛。",
     "U23,23岁以下,青年队,奥运会", "入门"),
    ("U21", "U21队是什么?", "Under 21|21岁以下",
     "U21为21岁以下青年队，欧洲U21锦标赛为该年龄段国家队赛事。",
     "是观察未来国脚的重要窗口。",
     "U21,21岁以下,青年队,欧青赛", "入门"),
    ("U20", "U20世界杯是什么?", "U-20 World Cup|世青赛",
     "FIFA U20世界杯是20岁以下国家队赛事，众多球星曾在此亮相。",
     "与成年世界杯为不同赛事。",
     "U20,世青赛,世界杯,青年", "入门"),
    ("U17", "U17世界杯是什么?", "U-17 World Cup",
     "FIFA U17世界杯是17岁以下国家队赛事，展示各国青训早期成果。",
     "许多球员17岁后进入更高梯队。",
     "U17,世少赛,世界杯,青训", "入门"),
    ("提拔", "青训球员如何提拔一线队?", "升入一线队|promotion",
     "表现突出的青训球员可被教练征召进入一线队训练与比赛名单。",
     "季前集训与热身赛是常见考察期。",
     "提拔,一线队,青训,晋升", "入门"),
    ("青训学院", "青训学院是什么?", "足球学院|academy",
     "俱乐部或独立机构设立的系统化训练与教育设施，集中培养青少年球员。",
     "拉玛西亚、卡斯蒂亚等为知名体系组成部分。",
     "青训学院,学院,训练,培养", "入门"),
    ("拉玛西亚", "拉玛西亚是什么?", "La Masia|巴萨青训",
     "巴塞罗那俱乐部著名青训基地，以传控与技术培养闻名，产出梅西、哈维等球星。",
     "是世界青训标杆之一。",
     "拉玛西亚,巴萨,青训,传控", "进阶"),
    ("本队培养", "本队培养球员是什么?", "homegrown|自家青训",
     "由本俱乐部青训体系培养并升入一线队的球员，常受球迷情感认同。",
     "部分联赛要求报名名单含一定homegrown人数。",
     "本队培养,homegrown,青训,自家", "进阶"),
    ("球探", "青训球探做什么?", "scout|青少年球探",
     "球探负责发掘有潜力的青少年球员，推荐给俱乐部试训与签约。",
     "南美与非洲是重要球探市场。",
     "球探,scout,发掘,试训", "入门"),
    ("试训", "青少年试训是什么?", "trial|训练营选拔",
     "球员短期参与俱乐部训练以评估水平，通过后可获得青训合同。",
     "公开试训与邀请试训形式不同。",
     "试训,trial,选拔,青训", "入门"),
    ("青训合同", "青少年球员合同有什么特点?", "youth contract|学徒合同",
     "未成年球员合同受FIFA与各国劳动法保护，含教育、训练与最低保障条款。",
     "国际转会年龄与保护规则更严格。",
     "青训合同,青少年,保护,规则", "进阶"),
    ("国际转会年龄", "未成年球员国际转会限制?", "minor transfer|18岁",
     "FIFA原则上禁止18岁以下国际转会，例外需满足居住、家庭等严格条件。",
     "旨在保护青少年免受不当流动。",
     "国际转会,未成年,18岁,FIFA", "进阶"),
    ("外租锻炼", "青训球员为何外租?", "loan development|出租锻炼",
     "一线队机会有限时，外租至其他俱乐部获得正式比赛时间。",
     "世界杯前外租表现可能影响国家队入选。",
     "外租,锻炼,出场,青训", "入门"),
    ("青年欧冠", "青年欧冠是什么?", "UEFA Youth League",
     "欧洲顶级俱乐部U19参与的欧足联青年联赛，水平较高的青年赛事。",
     "是欧洲青训质量展示平台。",
     "青年欧冠,U19,欧洲,赛事", "进阶"),
    ("青年联赛", "青年联赛是什么?", "youth league|梯队联赛",
     "各国组织的青少年级别联赛，供梯队球员积累比赛经验。",
     "与成年顶级联赛并行但独立运营。",
     "青年联赛,梯队,比赛,经验", "入门"),
    ("年龄段", "青训如何分年龄段?", "age group|年龄组",
     "通常按出生年份划分U8至U23等组别，规则与场地尺寸随年龄调整。",
     "小年龄段强调趣味与基础技术。",
     "年龄段,年龄组,U系列,分组", "入门"),
    ("小场足球", "青训为何用小场地?", "small-sided games|小场",
     "小场地、少人数比赛增加触球次数，利于技术与人球结合培养。",
     "FIFA推荐低龄段采用小场形式。",
     "小场,触球,技术,青训", "进阶"),
    ("门将青训", "门将如何专项培养?", "goalkeeper academy|门将青训",
     "门将有独立训练模块，包括反应、站位、出击与脚下技术。",
     "优秀门将成才周期常较长。",
     "门将,专项,青训,培养", "进阶"),
    ("青训总监", "青训总监做什么?", "academy director",
     "负责青训战略、教练团队、梯队架构与人才输送一线队。",
     "与一线队教练组保持人才沟通。",
     "青训总监,管理,战略,梯队", "进阶"),
    ("青训教练", "青训教练与一线队教练区别?", "youth coach",
     "青训教练侧重长期技术、战术基础与心理教育，而非短期成绩。",
     "需具备青少年教学资质与耐心。",
     "青训教练,训练,教育,青少年", "入门"),
    ("体能窗口", "青少年发育期训练注意什么?", "growth spurt|发育期",
     "青春期生长突增期需控制负荷，避免过度训练导致伤病。",
     "科学监控身高体重与关节负荷。",
     "发育期,负荷,伤病,科学", "进阶"),
    ("过度训练", "青训过度训练风险?", "overtraining|少年伤病",
     "青少年全年无休、多队并行易导致 burnout 与应力性损伤。",
     "俱乐部与学校、国家队需协调赛程。",
     "过度训练,伤病,青少年,负荷", "进阶"),
    ("双线作战", "青训球员双线作战?", "club and school|学训兼顾",
     "球员同时代表俱乐部梯队与学校或地区代表队，需协调赛程。",
     "部分国家有学训结合政策。",
     "双线,学校,梯队,赛程", "进阶"),
    ("国青队", "国青队是什么?", "national youth team|青年国家队",
     "各年龄段国家队，如U20、U23，是成年国家队的人才库。",
     "世界杯球员多数有国青履历。",
     "国青队,青年国家队,人才库,年龄段", "入门"),
    ("天才少年", "天才少年如何界定?", "wonderkid|新星",
     "媒体对早慧、早进入高级别比赛的青少年球员的称呼，非官方术语。",
     "成长需长期稳定出场与正确引导。",
     "天才少年,wonderkid,新星,青少年", "入门"),
    ("早慧球员", "早慧球员要注意什么?", "early bloomer|早熟",
     "身体或技术早熟者在同龄比赛中占优，但需防止忽视全面发育。",
     "晚熟球员同样可能成大器。",
     "早慧,早熟,发育,青训", "进阶"),
    ("晚熟球员", "晚熟球员还能成才吗?", "late bloomer|大器晚成",
     "身体或战术理解较晚成熟的球员，可能在18岁后快速进步。",
     "青训不应过早淘汰晚熟类型。",
     "晚熟,大器晚成,青训,发育", "进阶"),
    ("青训补偿", "青训俱乐部如何获补偿?", "training compensation",
     "球员首次签职业合同或转会时，培养俱乐部按规则获得经济补偿。",
     "鼓励基层青训持续投入。",
     "青训补偿,培养,补偿,俱乐部", "进阶"),
    ("团结机制", "团结机制分成是什么?", "solidarity mechanism",
     "球员转会时，其12至23岁期间效力过的青训俱乐部可按比例分成。",
     "FIFA全球适用规则。",
     "团结机制,分成,青训,FIFA", "专业"),
    ("校园足球", "校园足球与职业青训关系?", "school football",
     "校园足球侧重普及与教育，与职业俱乐部青训可并行或衔接。",
     "部分球员从校园路径进入职业试训。",
     "校园足球,普及,教育,衔接", "入门"),
    ("体校足球", "体校足球是什么路径?", "sports school|体校",
     "中国特色培养路径之一，结合文化学习与专业足球训练。",
     "仍可向职业俱乐部输送球员。",
     "体校,培养,路径,中国", "进阶"),
    ("世界杯新人", "世界杯新人从哪来?", "young star|新星首秀",
     "多数来自欧洲五大联赛一线队或南美主力俱乐部，青训背景各异。",
     "世界杯是年轻球员成名的顶级舞台。",
     "世界杯,新人,新星,一线队", "入门"),
    ("报名规则", "世界杯青训球员报名?", "World Cup squad youth",
     "世界杯成年队无年龄上限，年轻球员须进入26人名单并满足国籍等资格。",
     "U20/U17赛事为不同年龄组世界杯。",
     "世界杯,报名,成年队,名单", "入门"),
    ("梯队租借", "梯队球员租借规则?", "youth loan",
     "未成年或刚成年球员外租常含出场保证与家长/监护人同意条款。",
     "母队保留所有权与回购选项。",
     "梯队,租借,出场,条款", "进阶"),
    ("二队联赛", "二队参加什么比赛?", "second team league|B队联赛",
     "部分国家允许预备队参加第三级别或独立预备队联赛。",
     "规则各国差异大。",
     "二队,预备队,联赛,比赛", "进阶"),
    ("技术测试", "青训选拔看什么?", "talent identification|选材",
     "综合评估技术、战术理解、身体、心理与比赛智慧，非单一指标。",
     "长期观察优于一次试训定论。",
     "选材,测试,评估,青训", "进阶"),
    ("位置改造", "青训会改位置吗?", "position switch|改位置",
     "教练可能将青少年从边锋改中锋等，以优化长期发展路径。",
     "需考虑身体发育与战术需求。",
     "改位置,改造,青训,发展", "进阶"),
    ("双国籍青训", "双国籍球员青训归属?", "dual nationality youth",
     "可在符合规则下代表一国青年队，成年后可能面临国家队选择。",
     "FIFA国家队变更规则有严格限制。",
     "双国籍,青年队,国家队,选择", "进阶"),
    ("归化球员", "归化与青训有何不同?", "naturalized player|归化",
     "归化是成年球员通过居住或血统获得新国籍代表该国，非本国土青训产品。",
     "世界杯各队归化球员数量常受讨论。",
     "归化,国籍,国家队,青训", "进阶"),
    ("俱乐部DNA", "俱乐部DNA是什么?", "playing identity|风格传承",
     "指俱乐部长期形成的战术风格与价值观，青训需与之衔接。",
     "如巴萨传控、拜仁高位等。",
     "俱乐部DNA,风格,传承,青训", "进阶"),
    ("季前考察", "季前如何考察青训球员?", "pre-season trial",
     "一线队季前热身与集训是教练评估青训球员能否留队或外租的关键期。",
     "表现优异者可获得杯赛或联赛出场。",
     "季前,考察,热身,提拔", "入门"),
    ("杯赛轮换", "杯赛为何用青训?", "cup rotation|轮换练兵",
     "国内杯赛或低优先级比赛，一线队轮换时给青训球员出场机会。",
     "平衡成绩与人才培养。",
     "杯赛,轮换,出场,练兵", "入门"),
    ("长期计划", "青训为何强调长期?", "long-term development",
     "球员成熟常需8至12年培养，短期成绩不应牺牲技术与心理基础。",
     "顶级俱乐部青训强调耐心与连贯的培养计划。",
     "长期,培养,规划,青训", "入门"),
    ("家长角色", "青训阶段家长作用?", "parent support|家庭支持",
     "家庭在交通、心理支持与学业平衡上影响青少年球员稳定性。",
     "俱乐部常提供家长沟通机制。",
     "家长,家庭,支持,青少年", "入门"),
    ("退出青训", "踢不上职业怎么办?", "release from academy",
     "未获职业合同者须规划学业或其他职业路径，俱乐部应提供过渡支持。",
     "绝大多数青训球员不会成为职业球员。",
     "退出,青训,职业,过渡", "入门"),
    ("女足青训", "女足青训与男足有何不同?", "女子青训|女足梯队",
     "女足青训近年快速发展，训练方法与男足相似但资源与曝光度因地区差异较大。",
     "女子世界杯推动各国加大女足青训投入。",
     "女足青训,女子,梯队,世界杯", "入门"),
]


def row(seq: int, entry: tuple) -> dict[str, str]:
    l3, q, aliases, short, detail, kw, diff = entry
    return {
        "id": f"WC-GLOS-{seq:05d}",
        "category_l1": "术语与百科",
        "category_l2": "青训与梯队",
        "category_l3": l3,
        "scope": "both",
        "priority": "3",
        "question": q,
        "question_aliases": aliases,
        "answer_short": short,
        "answer_detail": detail,
        "answer_format": "definition",
        "keywords": kw,
        "tags": "青训与梯队,术语",
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
        "source_ref": "FIFA Youth Football & RSTP guidelines; national academy practices",
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
