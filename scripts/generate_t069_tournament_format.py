#!/usr/bin/env python3
"""Generate T069: 50 World Cup vs club calendar conflict entries (append).

Network: none (local structured data). Outbound HTTP must use fetch_utils.RateLimitedFetcher (>=1s/request); see docs/data-collection-policy.md and .cursor/rules/world-cup-data-collection.mdc."""

from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUTPUT = ROOT / "data" / "knowledge_tournament_format.csv"
START_ID = 451

COLUMNS = [
    "id", "category_l1", "category_l2", "category_l3", "scope", "priority",
    "question", "question_aliases", "answer_short", "answer_detail", "answer_format",
    "keywords", "tags", "entities", "related_ids", "difficulty",
    "era_start", "era_end", "region", "language", "fact_type", "confidence",
    "source_type", "source_ref", "content_flags", "updated_at",
]

ENTRIES = [
    ("国际比赛日", "世界杯与联赛如何协调?", "international match calendar",
     "FIFA国际比赛日历为世界杯预选赛与决赛圈预留窗口。",
     "各大洲联赛通常在该窗口暂停或调整赛程。",
     "国际比赛日,日历,窗口,联赛", "入门", "both"),
    ("俱乐部放行", "俱乐部必须放人吗?", "club release obligation",
     "FIFA规定俱乐部须在指定日期前释放被国家队征召球员。",
     "拒绝放行可能面临纪律处罚。",
     "放行,征召,义务,纪律", "入门", "both", "rule"),
    ("2022冬赛", "2022为何冲击联赛?", "2022 winter impact",
     "卡塔尔11-12月举办，与欧洲五大联赛赛季中期重叠。",
     "各联赛安排冬歇或额外停赛周。",
     "2022,冬季,联赛,重叠", "入门", "both"),
    ("英超冬歇", "英超2022怎么调整?", "Premier League 2022",
     "英超2022-23赛季设世界杯前特殊停赛周释放球员。",
     "为史上罕见赛季中段长期停赛。",
     "英超,冬歇,2022,停赛", "入门", "both"),
    ("西甲调整", "西甲2022赛程?", "La Liga 2022",
     "西甲同样暂停联赛并调整第17轮前后赛程。",
     "西班牙国家队球员多来自西甲。",
     "西甲,暂停,西班牙,赛程", "入门", "both"),
    ("德甲冬歇", "德甲本有冬歇吗?", "Bundesliga winter break",
     "德甲传统1月冬歇，2022年提前至11月配合世界杯。",
     "德国为2022小组赛出局国之一。",
     "德甲,冬歇,11月,德国", "入门", "both"),
    ("意甲赛程", "意甲2022调整?", "Serie A 2022",
     "意甲压缩赛前赛程并在世界杯期间停摆。",
     "意甲球员在2022世界杯分布广泛。",
     "意甲,停摆,压缩,2022", "入门", "both"),
    ("法甲安排", "法甲2022如何?", "Ligue 1 2022",
     "法甲与多数欧洲联赛同步暂停配合2022世界杯。",
     "法国为卫冕冠军。",
     "法甲,暂停,法国,2022", "入门", "both"),
    ("南美联赛", "南美联赛与世界杯?", "South America calendar",
     "南美部分联赛赛季跨年，与6-7月世界杯冲突较小。",
     "2022冬赛仍影响南美球员在欧洲俱乐部。",
     "南美,跨年,6月,欧洲", "入门", "both"),
    ("MLS赛程", "MLS与2026世界杯?", "MLS 2026 schedule",
     "2026美加墨世界杯期间MLS可能暂停或改赛程。",
     "美国联赛与世界杯同国举办协调更复杂。",
     "MLS,2026,暂停,美国", "入门", "both"),
    ("墨西哥联赛", "墨西哥联赛与世界杯?", "Liga MX conflict",
     "墨西哥联赛夏季赛历与6-7月世界杯常重叠。",
     "2026主场作战协调至关重要。",
     "墨西哥,夏季,重叠,2026", "入门", "both"),
    ("欧冠赛季", "欧冠与世界杯?", "Champions League WC",
     "世界杯年欧冠赛季前段正常进行，淘汰赛在联赛恢复后继续。",
     "2022欧冠决赛在世界杯前完成。",
     "欧冠,赛季,2022,决赛", "入门", "both"),
    ("欧联欧协", "欧联与世界杯?", "Europa League WC",
     "欧联与欧协联与欧冠类似，世界杯窗口暂停欧洲俱乐部赛。",
     "球员归队后接续剩余赛事。",
     "欧联,欧协,暂停,归队", "入门", "both"),
    ("解放者杯", "解放者杯与世界杯?", "Libertadores WC",
     "南美解放者杯与6月世界杯冲突，常调整轮次日期。",
     "CONMEBOL与FIFA协调赛程。",
     "解放者杯,南美,调整,CONMEBOL", "入门", "both"),
    ("亚冠联赛", "亚冠与世界杯?", "AFC Champions League",
     "亚洲俱乐部赛事在世界杯窗口暂停或改期。",
     "亚洲球员多在欧洲中东俱乐部效力。",
     "亚冠,亚洲,暂停,改期", "入门", "both"),
    ("球员疲劳", "世界杯后球员疲劳?", "post-WC fatigue",
     "世界杯球员归队后可能缺乏 preseason 休息。",
     "2022冬赛使赛季中段无缓冲。",
     "疲劳,归队,休息,2022", "入门", "both"),
    ("伤病风险", "世界杯增加伤病风险?", "injury risk WC",
     "高强度世界杯后俱乐部赛季继续，伤病管理成焦点。",
     "俱乐部与国家队医疗数据需共享。",
     "伤病,风险,医疗,管理", "入门", "both"),
    ("Release day", "Release day是什么?", "release day rule",
     "FIFA规定世界杯前固定日期俱乐部须释放球员至国家队。",
     "具体日期在当届 circular 公布。",
     "Release day,释放,日期,circular", "入门", "both", "rule"),
    ("归队时间", "世界杯后何时归队?", "return to club",
     "被淘汰球员可提前归队，冠军成员决赛后数日内返回。",
     "俱乐部可给予额外休息。",
     "归队,淘汰,冠军,休息", "入门", "both"),
    ("转会窗", "世界杯与转会窗?", "transfer window WC",
     "世界杯年夏季转会窗常围绕赛前赛后调整。",
     "出色世界杯表现可能影响转会。",
     "转会窗,夏季,表现,转会", "入门", "both"),
    ("合同年", "世界杯年合同到期?", "contract expiry WC",
     "合同年球员世界杯表现影响续约与转会谈判。",
     "与竞赛规则无直接关系。",
     "合同,到期,续约,谈判", "入门", "both"),
    ("俱乐部拒绝", "俱乐部能否拒绝放人?", "club refusal",
     "仅在FIFA明确例外（如伤病未恢复）下可讨论，一般必须放行。",
     "历史争议个案依纪律程序处理。",
     "拒绝,例外,伤病,纪律", "进阶", "both", "rule"),
    ("友谊赛冲突", "俱乐部赛与友谊赛?", "friendly conflict",
     "国家队友谊赛也占用国际比赛日，俱乐部同样须放行。",
     "世界杯预选赛优先级高于友谊赛。",
     "友谊赛,国际比赛日,放行,预选赛", "入门", "both"),
    ("预选赛窗口", "预选赛占用联赛?", "qualifier windows",
     "世界杯预选赛分散在多个国际比赛日，联赛多次暂停。",
     "2026扩军预选赛周期更长。",
     "预选赛,窗口,暂停,2026", "入门", "both"),
    ("2026北美", "2026俱乐部协调?", "2026 club coordination",
     "2026美加墨世界杯期间北美与全球联赛须与FIFA协调停赛。",
     "三国联赛、MLS与墨西哥联赛同步规划。",
     "2026,北美,协调,停赛", "入门", "both"),
    ("夏季传统", "传统夏季世界杯优势?", "summer WC advantage",
     "6-7月世界杯与北半球联赛休赛期重合，冲突最小。",
     "2022与部分南半球联赛仍有摩擦。",
     "夏季,休赛期,6月,冲突小", "入门", "both"),
    ("澳大利亚联赛", "澳超与世界杯?", "A-League WC",
     "澳超赛季与北半球不同，与6月世界杯重叠程度因年而异。",
     "澳大利亚2022未进决赛圈。",
     "澳超,赛季,澳大利亚,重叠", "入门", "both"),
    ("日本J联赛", "J联赛与世界杯?", "J League WC",
     "J联赛通常夏季进行，与6-7月世界杯直接冲突。",
     "联赛在世界杯期间暂停。",
     "J联赛,夏季,暂停,日本", "入门", "both"),
    ("韩国K联赛", "K联赛调整?", "K League WC",
     "K联赛与J联赛类似，世界杯月暂停联赛。",
     "2022韩国进16强。",
     "K联赛,暂停,韩国,2022", "入门", "both"),
    ("中超赛程", "中超与世界杯?", "CSL WC",
     "中超赛季历多次调整，世界杯年通常避开决赛圈月份。",
     "中国队未进2022决赛圈。",
     "中超,调整,赛季,中国", "入门", "both"),
    ("沙特联赛", "沙特联赛与2022?", "Saudi league 2022",
     "2022世界杯在卡塔尔举行，海湾联赛冬季赛程与杯赛冲突。",
     "沙特该届爆冷阿根廷。",
     "沙特,海湾,2022,联赛", "入门", "both"),
    ("球员归属", "世界杯期间算哪队?", "player status WC",
     "世界杯期间球员代表国家队，俱乐部合同暂停执行比赛义务。",
     "薪资依合同与各国劳动法。",
     "归属,国家队,合同,薪资", "入门", "both"),
    ("Insurance", "世界杯伤病谁赔?", "injury insurance WC",
     "FIFA为世界杯注册球员提供伤病补偿计划覆盖俱乐部。",
     "具体金额依FIFA俱乐部保护计划。",
     "伤病,补偿,FIFA,保险", "进阶", "both", "rule"),
    ("FIFA CPP", "俱乐部 Protection Plan?", "Club Protection Programme",
     "FIFA俱乐部保护计划补偿世界杯期间球员伤缺俱乐部的日薪。",
     "需俱乐部与球员符合注册条件。",
     "CPP,保护,日薪,注册", "进阶", "both", "rule"),
    ("替补征召", "俱乐部替补被征召?", "late call-up",
     "伤病递补征召同样须俱乐部立即放行。",
     "2022多起赛前递补案例。",
     "递补,征召,伤病,放行", "入门", "both"),
    ("U23球员", "俱乐部U23与世界杯?", "U23 WC conflict",
     "U23球员若入选成年国家队同样须放行。",
     "奥运男足与世界杯规则独立。",
     "U23,成年队,放行,奥运", "入门", "both"),
    ("女足世界杯", "女足与俱乐部?", "Women WC clubs",
     "女子世界杯同样占用国际比赛日历，俱乐部须放行。",
     "女足俱乐部赛程协调日增。",
     "女足,俱乐部,日历,放行", "入门", "both"),
    ("世俱杯冲突", "世俱杯与世界杯?", "Club World Cup WC",
     "世俱杯与世界杯不同年或错开，避免直接冲突。",
     "2025扩军世俱杯另议赛程。",
     "世俱杯,错开,扩军,赛程", "进阶", "both"),
    ("欧洲杯同年", "欧洲杯与世界杯?", "Euro same year",
     "欧洲杯与世界杯错开两年，避免同年双重冲突。",
     "2020欧洲杯因疫情顺延至2021。",
     "欧洲杯,错开,两年,2021", "入门", "both"),
    ("美洲杯", "美洲杯与世界杯?", "Copa America WC",
     "美洲杯通常与世界杯错开，2021曾特殊年份举办。",
     "南美球员夏季赛事密集。",
     "美洲杯,错开,2021,南美", "入门", "both"),
    ("非洲杯", "非洲杯与世界杯?", "AFCON WC",
     "非洲杯常于1-2月举行，与6月世界杯间隔数月。",
     "2023非洲杯时间调整曾影响俱乐部。",
     "非洲杯,1月,间隔,2023", "入门", "both"),
    ("俱乐部杯赛", "国内杯赛怎么办?", "domestic cup pause",
     "各国国内杯赛在世界杯窗口通常暂停或改期。",
     "避免与国家队抢球员。",
     "国内杯,暂停,改期,球员", "入门", "both"),
    ("电视转播", "转播权与停赛?", "broadcast pause",
     "联赛停赛期间转播商改播世界杯或重播。",
     "商业合同预先含世界杯条款。",
     "转播,停赛,商业,合同", "入门", "both"),
    ("Fantasy联赛", " fantasy 足球暂停?", "fantasy football pause",
     "主流 fantasy 英超等在世界杯期间暂停计分。",
     "世界杯期间另设 fantasy 世界杯游戏。",
     "fantasy,暂停,计分,游戏", "入门", "both"),
    ("训练基地", "俱乐部基地与国家队?", "training base conflict",
     "国家队世界杯前常另设集训基地，球员暂离俱乐部训练。",
     "Release day前俱乐部仍负责日常训练。",
     "集训,基地,Release,训练", "入门", "both"),
    ("2026跨度", "2026联赛停多久?", "2026 pause length",
     "2026世界杯约39天，北美联赛预计停赛5至6周。",
     "具体以各联盟官方公告为准。",
     "2026,停赛,5周,北美", "入门", "both"),
    ("全球协调", "FIFA如何全球协调?", "global coordination FIFA",
     "FIFA理事会与国际联赛论坛发布日历，要求主要联赛配合。",
     "2022证明非常规赛期需提前多年规划。",
     "全球,协调,日历,论坛", "入门", "both"),
    ("球员意愿", "球员可拒绝国家队吗?", "player refusal NT",
     "FIFA Release day规则下俱乐部不能阻止，球员个人拒服通常受足协纪律。",
     "与俱乐部合同无关。",
     "意愿,拒服,足协,纪律", "进阶", "both", "rule"),
    ("赛程优先", "冲突时谁优先?", "WC priority",
     "世界杯决赛圈在国际比赛日历中优先级高于俱乐部赛事。",
     "FIFA Statutes与Release day规则保障。",
     "优先,世界杯,Statutes,Release", "入门", "both", "rule"),
    ("2022教训", "2022给联赛何教训?", "2022 lessons",
     "2022证明非夏季世界杯需联赛提前3至4年调整赛历。",
     "2026虽在夏季但三国联办仍须协调。",
     "2022,教训,赛历,2026", "入门", "both"),
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
        "category_l2": "俱乐部赛事冲突",
        "category_l3": l3,
        "scope": scope,
        "priority": "5",
        "question": q,
        "question_aliases": aliases,
        "answer_short": short,
        "answer_detail": detail,
        "answer_format": "definition",
        "keywords": kw,
        "tags": "赛制,俱乐部",
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
