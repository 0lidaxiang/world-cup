#!/usr/bin/env python3
"""Generate T067: 50 World Cup individual awards entries (append).

Network: none (local structured data). Outbound HTTP must use fetch_utils.RateLimitedFetcher (>=1s/request); see docs/data-collection-policy.md and .cursor/rules/world-cup-data-collection.mdc."""

from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUTPUT = ROOT / "data" / "knowledge_tournament_format.csv"
START_ID = 351

COLUMNS = [
    "id", "category_l1", "category_l2", "category_l3", "scope", "priority",
    "question", "question_aliases", "answer_short", "answer_detail", "answer_format",
    "keywords", "tags", "entities", "related_ids", "difficulty",
    "era_start", "era_end", "region", "language", "fact_type", "confidence",
    "source_type", "source_ref", "content_flags", "updated_at",
]

ENTRIES = [
    ("金球奖", "世界杯金球奖是什么?", "Golden Ball",
     "授予决赛圈最佳球员，由FIFA技术委员会在赛后评选。",
     "1982年起正式设立，先评10人候选再定冠军。",
     "金球,最佳球员,评选,FIFA", "入门", "world_cup"),
    ("金靴奖", "世界杯金靴怎么算?", "Golden Boot",
     "授予进球最多球员，并列时比助攻少者、出场少者优先。",
     "1982年起沿用现行统计规则。",
     "金靴,进球,助攻,并列", "入门", "world_cup"),
    ("金手套", "世界杯最佳门将奖?", "Golden Glove",
     "授予最佳门将，2010年起称阿迪达斯金手套奖。",
     "综合扑救、失球与球队成绩由技术团队评定。",
     "金手套,门将,2010,扑救", "入门", "world_cup"),
    ("最佳新秀", "世界杯最佳年轻球员?", "Best Young Player",
     "授予21岁以下表现最佳球员，2006年起设立。",
     "年龄以赛事开始时计算。",
     "新秀,21岁,2006,年轻", "入门", "world_cup"),
    ("公平竞赛队", "公平竞赛奖给谁?", "Fair Play team",
     "授予纪律最佳球队，依据黄红牌与积极比赛评分。",
     "1986年墨西哥获首届公平竞赛队奖。",
     "公平竞赛,纪律,黄牌,球队", "入门", "world_cup"),
    ("最佳进球", "世界杯最佳进球奖?", "Goal of the Tournament",
     "FIFA可评当届最佳进球，由球迷或专家投票。",
     "非每届必设，属展示类荣誉。",
     "最佳进球,投票,展示,荣誉", "入门", "world_cup"),
    ("决赛MVP", "决赛有单独MVP吗?", "final MVP",
     "金球奖涵盖整届表现，决赛无单独官方MVP奖项。",
     "媒体常自发评选决赛最佳。",
     "决赛,MVP,金球,媒体", "入门", "world_cup"),
    ("1982设立", "金球金靴何时设立?", "1982 awards start",
     "1982西班牙世界杯起正式设立金球与金靴。",
     "此前仅有非正式最佳球员讨论。",
     "1982,西班牙,设立,历史", "入门", "world_cup", "history"),
    ("梅西金球", "梅西拿过世界杯金球吗?", "Messi Golden Ball",
     "梅西2014年获金球（亚军），2022年率队夺冠并再获金球。",
     "为少数既获金球又夺冠的球员。",
     "梅西,2022,2014,金球", "入门", "world_cup", "history"),
    ("罗纳尔多金靴", "罗纳尔多世界杯金靴?", "Ronaldo Golden Boot",
     "罗纳尔多2002年8球获金靴并率队巴西夺冠。",
     "2006年再进3球。",
     "罗纳尔多,2002,金靴,8球", "入门", "world_cup", "history"),
    ("克洛泽纪录", "世界杯历史射手王?", "Klose record",
     "克洛泽16球为世界杯历史最多，2014年夺冠。",
     "金靴统计仅计当届进球。",
     "克洛泽,16球,射手王,2014", "入门", "world_cup", "history"),
    ("姆巴佩金靴", "姆巴佩2022金靴?", "Mbappe 2022 boot",
     "姆巴佩2022年8球获金靴，决赛上演帽子戏法。",
     "法国获亚军。",
     "姆巴佩,2022,8球,帽子戏法", "入门", "world_cup", "history"),
    ("卡恩金手套", "2002最佳门将?", "Kahn Golden Glove",
     "卡恩2002年获最佳门将，德国获亚军。",
     "为少数非冠军队门将获奖例。",
     "卡恩,2002,门将,德国", "入门", "world_cup", "history"),
    ("诺伊尔2014", "诺伊尔2014奖项?", "Neuer 2014",
     "诺伊尔2014年获金手套，德国夺冠仅失4球。",
     "革新清道夫门将角色。",
     "诺伊尔,2014,金手套,德国", "入门", "world_cup", "history"),
    ("格列兹曼2018", "2018金球谁得?", "Griezmann 2018",
     "2018年法国夺冠，媒体常提格列兹曼表现，官方金球由莫德里奇获得。",
     "克罗地亚获亚军，莫德里奇获金球。",
     "2018,莫德里奇,金球,克罗地亚", "入门", "world_cup", "history"),
    ("齐达内2006", "齐达内2006金球?", "Zidane 2006",
     "齐达内2006年获金球，决赛因头顶犯规被罚下。",
     "法国点球憾负意大利。",
     "齐达内,2006,金球,决赛", "入门", "world_cup", "history"),
    ("罗纳尔多1998", "1998罗纳尔多金球?", "Ronaldo 1998",
     "罗纳尔多1998年获金球，决赛表现受健康问题影响。",
     "巴西0比3负法国。",
     "罗纳尔多,1998,金球,法国", "入门", "world_cup", "history"),
    ("贝利1958", "早期有个人奖项吗?", "early awards",
     "1958贝利崭露头角但尚无现代金球金靴体系。",
     "个人奖项为1982年后制度化。",
     "贝利,1958,早期,历史", "进阶", "world_cup", "history"),
    ("助攻统计", "金靴并列看助攻吗?", "assists tiebreak",
     "进球相同则助攻更少者获奖，仍平则出场分钟更少者优先。",
     "FIFA官方技术报告公布详细数据。",
     "助攻,并列,出场,分钟", "入门", "world_cup"),
    ("乌龙球", "乌龙算金靴吗?", "own goals boot",
     "金靴仅统计球员射入对方球门的进球，乌龙不计。",
     "点球大战进球亦不计入金靴。",
     "乌龙,金靴,点球大战,不计", "入门", "world_cup", "rule"),
    ("点球大战", "点球大战进球算金靴吗?", "penalty shootout goals",
     "点球大战中的进球不计入金靴与射手榜。",
     "仅常规时间与加时进球计入。",
     "点球大战,金靴,加时,射手榜", "入门", "world_cup", "rule"),
    ("评选时间", "奖项何时公布?", "award announcement",
     "金球、金靴、金手套等在决赛后颁奖典礼或官方发布。",
     "技术委员会在决赛前已拟定候选名单。",
     "公布,决赛后,典礼,候选", "入门", "world_cup"),
    ("技术委员会", "谁负责评选?", "technical study group",
     "FIFA技术委员会与专家小组依据当届全部比赛评估。",
     "发布《技术报告》详述数据与评选理由。",
     "技术委员会,专家,报告,评选", "入门", "world_cup"),
    ("候选名单", "金球候选几人?", "Golden Ball shortlist",
     "通常先公布约10名候选，决赛后揭晓得主。",
     "含冠亚军球队核心球员为主。",
     "候选,10人,短名单,揭晓", "入门", "world_cup"),
    ("门将评选", "金手套怎么评?", "GK selection criteria",
     "综合失球数、扑救次数、关键扑救与球队走多远。",
     "冠军队门将往往占优但不绝对。",
     "金手套,失球,扑救,综合", "入门", "world_cup"),
    ("新秀年龄", "最佳新秀年龄线?", "young player age",
     "须在比赛开始日未满22周岁（部分届次为21岁）。",
     "2022规程以21岁为上限。",
     "年龄,22岁,21岁,上限", "入门", "world_cup"),
    ("博格巴2014", "2014最佳新秀?", "Pogba 2014 young",
     "2014最佳年轻球员为保罗·博格巴。",
     "法国该届未进决赛。",
     "博格巴,2014,新秀,法国", "入门", "world_cup", "history"),
    ("穆勒2010", "穆勒2010奖项?", "Muller 2010 awards",
     "穆勒2010年获金靴（5球）与最佳新秀。",
     "德国获季军。",
     "穆勒,2010,金靴,新秀", "入门", "world_cup", "history"),
    ("萨莫拉无关", "金手套与萨莫拉?", "not Zamora",
     "金手套为世界杯奖项，与西甲萨莫拉奖无关。",
     "二者评选体系与赛事不同。",
     "萨莫拉,西甲,无关,区别", "入门", "both"),
    ("欧洲金球", "世界杯金球与欧洲金球?", "Ballon d'Or difference",
     "世界杯金球由FIFA技术委员会评，与《法国足球》金球奖不同。",
     "2010至2015年曾合并为国际足联金球奖。",
     "欧洲金球,FIFA,合并,区别", "进阶", "both", "history"),
    ("全队奖项", "有最佳球队奖吗?", "best team award",
     "冠军即最佳球队，无单独最佳阵容官方奖杯。",
     "技术报告可选最佳11人但非正式奖项。",
     "冠军,最佳11,技术报告,无奖杯", "入门", "world_cup"),
    ("最佳11人", "官方最佳阵容?", "team of tournament",
     "FIFA技术报告常发布赛事最佳阵容11人。",
     "属分析性质，非颁奖礼奖项。",
     "最佳11,技术报告,分析,阵容", "入门", "world_cup"),
    ("教练奖", "世界杯有最佳教练吗?", "best coach award",
     "世界杯无官方最佳教练奖，冠军教练获冠军荣誉。",
     "媒体评选不影响FIFA官方奖项。",
     "教练,无官方,冠军,媒体", "入门", "world_cup"),
    ("队长袖标", "队长有单独奖吗?", "captain award",
     "无最佳队长奖，队长举起大力神杯即为最高荣誉。",
     "袖标队长职责在竞赛规程中规定。",
     "队长,袖标,大力神杯,无奖", "入门", "world_cup"),
    ("替补进球", "替补球员能拿金靴吗?", "substitute Golden Boot",
     "替补与首发一视同仁，进球即可竞争金靴。",
     "2018英格兰凯恩6球获金靴含点球。",
     "替补,金靴,凯恩,点球", "入门", "world_cup"),
    ("小组赛出局", "小组赛出局能拿金球吗?", "group exit Golden Ball",
     "理论上可能但历史金球多来自四强球队。",
     "1990萨维切维奇等为少数例外讨论。",
     "小组赛,金球,四强,历史", "进阶", "world_cup", "history"),
    ("守门员金靴", "门将能拿金靴吗?", "GK Golden Boot",
     "门将若进球（极罕见）可计金靴，如奇拉维特曾进点球。",
     "现代世界杯门将进球实例极少。",
     "门将,金靴,奇拉维特,罕见", "进阶", "world_cup"),
    ("1986莱因克尔", "1986金靴谁得?", "Lineker 1986 boot",
     "1986金靴为英格兰莱因克尔6球，阿根廷马拉多纳获金球。",
     "阿根廷该届夺冠。",
     "莱因克尔,1986,马拉多纳,6球", "入门", "world_cup", "history"),
    ("1990斯基拉奇", "1990最佳新秀?", "Schillaci 1990",
     "1990意大利斯基拉奇6球获金靴，表现惊艳。",
     "意大利获季军。",
     "斯基拉奇,1990,金靴,意大利", "入门", "world_cup", "history"),
    ("2002卡西利亚斯", "2002金手套?", "2002 Golden Glove",
     "2002最佳门将通常记为卡恩，卡西利亚斯该届尚未获金手套。",
     "2010起统一称金手套。",
     "2002,卡恩,卡西,门将", "进阶", "world_cup", "history"),
    ("2014J罗", "2014金靴谁得?", "James 2014 boot",
     "2014金靴为哥伦比亚哈梅斯·罗德里格斯6球。",
     "含对乌拉圭精彩凌空。",
     "J罗,2014,金靴,6球", "入门", "world_cup", "history"),
    ("2022马丁", "2022金手套?", "Martinez 2022 glove",
     "2022金手套为阿根廷马丁内斯，决赛关键扑救助夺冠。",
     "点球大战表现突出。",
     "马丁内斯,2022,金手套,阿根廷", "入门", "world_cup", "history"),
    ("2022恩佐", "2022最佳新秀?", "Enzo 2022 young",
     "2022最佳年轻球员为阿根廷恩佐·费尔南德斯。",
     "该届助阿根廷夺冠。",
     "恩佐,2022,新秀,阿根廷", "入门", "world_cup", "history"),
    ("赞助商名", "奖项有商业冠名吗?", "sponsored awards",
     "金手套等可由阿迪达斯等品牌赞助冠名。",
     "不影响评选标准与FIFA归属。",
     "赞助,阿迪达斯,冠名,品牌", "入门", "world_cup"),
    ("公平竞赛个人", "有个人公平竞赛奖吗?", "individual fair play",
     "世界杯不设个人公平竞赛奖，仅球队奖。",
     "俱乐部赛事偶有个人公平竞赛奖。",
     "个人,公平竞赛,球队,区别", "入门", "world_cup"),
    ("禁赛影响", "禁赛球员能评奖吗?", "suspended player award",
     "被禁赛球员通常无法参与剩余赛事，丧失评奖机会。",
     "评选基于实际出场贡献。",
     "禁赛,评奖,出场,贡献", "入门", "world_cup"),
    ("数据官方", "奖项数据哪里查?", "official stats source",
     "FIFA官网当届技术报告与比赛统计为权威来源。",
     "第三方数据网站仅供参考。",
     "FIFA,技术报告,统计,权威", "入门", "world_cup"),
    ("历史统计", "能否跨届比金靴?", "cross-tournament boots",
     "金靴为当届奖项，历史总进球榜单独统计。",
     "克洛泽16球为生涯世界杯总进球。",
     "跨届,总进球,金靴,克洛泽", "入门", "world_cup"),
    ("女子世界杯", "女足有个人奖项吗?", "Women World Cup awards",
     "女子世界杯同样设金球、金靴、金手套与最佳新秀。",
     "评选流程与男子赛类似。",
     "女足,金球,金靴,平行", "入门", "both"),
    ("奖项性质", "奖项影响积分吗?", "awards vs standings",
     "个人与公平竞赛奖均为荣誉，不计入竞赛积分或排名。",
     "与场上胜负规则完全分离。",
     "荣誉,积分,无关,排名", "入门", "world_cup"),
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
        "category_l2": "奖项设置",
        "category_l3": l3,
        "scope": scope,
        "priority": "5",
        "question": q,
        "question_aliases": aliases,
        "answer_short": short,
        "answer_detail": detail,
        "answer_format": "definition",
        "keywords": kw,
        "tags": "赛制,奖项",
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
