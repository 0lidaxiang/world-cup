#!/usr/bin/env python3
"""Generate T061: 50 World Cup continental qualifier system entries (append).

Network: none (local structured data). Outbound HTTP must use fetch_utils.RateLimitedFetcher (>=1s/request); see docs/data-collection-policy.md and .cursor/rules/world-cup-data-collection.mdc."""

from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUTPUT = ROOT / "data" / "knowledge_tournament_format.csv"
START_ID = 51

COLUMNS = [
    "id", "category_l1", "category_l2", "category_l3", "scope", "priority",
    "question", "question_aliases", "answer_short", "answer_detail", "answer_format",
    "keywords", "tags", "entities", "related_ids", "difficulty",
    "era_start", "era_end", "region", "language", "fact_type", "confidence",
    "source_type", "source_ref", "content_flags", "updated_at",
]

ENTRIES = [
    ("预选赛总述", "世界杯预选赛怎么组织?", "qualifiers overview",
     "由六大洲足联依FIFA分配名额各自组织，胜者晋级决赛圈。",
     "东道主通常自动晋级，不占洲内名额或依决议执行。",
     "预选赛,六大洲,名额,晋级", "入门", "world_cup"),
    ("名额分配", "决赛圈名额如何分配?", "slot allocation",
     "国际足联理事会依各大洲实力与参赛规模分配洲际名额。",
     "每周期可能微调，以当届决议为准。",
     "名额,分配,理事会,洲际", "入门", "world_cup"),
    ("欧洲区", "欧洲区预选赛赛制?", "UEFA qualifiers",
     "欧足联组织多轮小组赛或联赛制，头名及部分次名晋级。",
     "欧洲名额通常最多，赛制随周期调整。",
     "欧洲,UEFA,小组赛,晋级", "入门", "world_cup"),
    ("南美区", "南美区预选赛赛制?", "CONMEBOL qualifiers",
     "南美足联常采用全员主客循环积分制，前几名直接晋级。",
     "竞争集中，赛程密集。",
     "南美,CONMEBOL,循环,积分", "入门", "world_cup"),
    ("亚洲区", "亚洲区预选赛赛制?", "AFC qualifiers",
     "亚足联分阶段：外围、小组、决赛圈，名额较少竞争激烈。",
     "近年常含第四阶段决出直接出线队。",
     "亚洲,AFC,分阶段,出线", "入门", "world_cup"),
    ("非洲区", "非洲区预选赛赛制?", "CAF qualifiers",
     "非足联多轮淘汰或小组后进入决赛阶段决出出线队。",
     "参赛队数量多，轮次较长。",
     "非洲,CAF,淘汰,小组", "入门", "world_cup"),
    ("中北美区", "中北美加勒比预选赛?", "CONCACAF qualifiers",
     "中北美及加勒比足联分阶段筛选，末段常含六强循环。",
     "2026主办三国或影响当周期安排。",
     "中北美,CONCACAF,六强,循环", "入门", "world_cup"),
    ("大洋洲区", "大洋洲预选赛赛制?", "OFC qualifiers",
     "大洋洲足联先决区域冠军，再与其他洲进行洲际附加赛。",
     "直接出线名额通常最少。",
     "大洋洲,OFC,附加赛,冠军", "入门", "world_cup"),
    ("洲际附加赛", "洲际附加赛是什么?", "inter-confed playoff",
     "部分名额由不同洲球队主客或单场决胜争夺最后席位。",
     "对阵组合由FIFA抽签或规程预定。",
     "附加赛,洲际,名额,决胜", "入门", "world_cup"),
    ("东道主名额", "东道主占预选赛名额吗?", "host quota",
     "主办国自动晋级时一般不消耗本洲出线名额，依当届FIFA决议。",
     "多国主办时各国席位单独规定。",
     "东道主,自动,名额,不占", "入门", "world_cup"),
    ("注册期限", "预选赛球员注册?", "player registration",
     "各队须在FIFA规定窗口提交预选赛名单并符合国籍规则。",
     "与决赛圈大名单规则衔接。",
     "注册,名单,国籍,窗口", "进阶", "world_cup"),
    ("同组回避", "预选赛同组回避?", "draw restrictions",
     "抽签时通常回避同足联过高密度同组，细则依当届手册。",
     "政治敏感对阵亦可能被回避。",
     "抽签,回避,同组,手册", "进阶", "world_cup"),
    ("积分规则", "预选赛积分怎么算?", "qualifier points",
     "胜3平1负0为常规积分，同分依净胜球、进球等顺序比较。",
     "与决赛圈小组赛原则类似。",
     "积分,净胜球,胜平负,比较", "入门", "world_cup"),
    ("中立场地", "预选赛可用中立场地吗?", "neutral venue",
     "因安全、制裁或足协协议可申请中立场地，须FIFA批准。",
     "非常规安排，个案处理。",
     "中立场地,批准,安全,个案", "进阶", "world_cup"),
    ("弃赛处理", "预选赛弃赛怎么判?", "walkover",
     "未出场或退出可能判0-3负并罚款，依纪律与竞赛条款。",
     "影响后续轮次排名。",
     "弃赛,0-3,罚款,纪律", "进阶", "world_cup"),
    ("重赛规则", "预选赛能否重赛?", "replay rules",
     "场地事故、秩序混乱等极端情形由FIFA纪律与竞赛机构裁决。",
     "极少见，以官方公告为准。",
     "重赛,裁决,FIFA,极端", "进阶", "world_cup"),
    ("视频辅助", "预选赛用VAR吗?", "VAR in qualifiers",
     "是否启用VAR由足联与FIFA协议决定，不如决赛圈统一。",
     "关键场次逐步推广。",
     "VAR,预选赛,协议,推广", "进阶", "both"),
    ("赛程国际日", "预选赛何时踢?", "FIFA windows",
     "主要在FIFA国际比赛日进行，减少与俱乐部冲突。",
     "俱乐部须放行国家队球员。",
     "国际日,赛程,俱乐部,放行", "入门", "both"),
    ("俱乐部放人", "俱乐部必须放人吗?", "release obligation",
     "国际足联规定俱乐部须放行注册国家队球员参加世预赛。",
     "有补偿与伤病保护条款。",
     "放人,俱乐部,义务,补偿", "进阶", "both"),
    ("黄牌累积", "预选赛黄牌停赛?", "booking suspension",
     "预选赛黄牌累积规则依各大洲足联细则，可能带入决赛圈。",
     "决赛圈前常部分清零，依规程。",
     "黄牌,累积,停赛,清零", "进阶", "world_cup"),
    ("年龄限制", "世预赛有年龄限制吗?", "no age cap",
     "男子世界杯预选赛为成年国家队，无奥运式U23上限。",
     "青年队参加青年世锦赛，非世界杯。",
     "成年,无年龄,奥运,区别", "入门", "both"),
    ("归化球员", "预选赛归化球员规则?", "naturalized players",
     "须符合FIFA国籍与转会协会变更年限等规定方可代表。",
     "违规使用将被纪律处罚。",
     "归化,国籍,FIFA,资格", "进阶", "both"),
    ("双国籍", "双国籍球员选哪队?", "dual nationality",
     "球员在符合.tie-break规则下可选择代表一国，绑定后变更受限。",
     "具体以FIFA国籍条例为准。",
     "双国籍,代表,绑定,条例", "进阶", "both"),
    ("种子队", "预选赛分档种子?", "seeding qualifiers",
     "抽签按FIFA排名或近期成绩分档，避免强队过早相遇。",
     "分档表赛前公布。",
     "种子,分档,排名,抽签", "入门", "world_cup"),
    ("财务补贴", "预选赛差旅补贴?", "travel support",
     "FIFA对部分足协提供预选赛差旅与组织补贴。",
     "金额与项目依发展计划。",
     "补贴,差旅,足协,发展", "进阶", "world_cup"),
    ("女子预选赛", "女子世界杯预选赛?", "women qualifiers",
     "女子世界杯预选赛由各洲足联独立组织，名额体系与男子不同。",
     "规程单独公布。",
     "女子,预选赛,独立,名额", "入门", "both"),
    ("2026名额", "2026世预赛名额变化?", "2026 quota",
     "2026扩军至48队后各洲名额上调，具体数字以FIFA决议为准。",
     "周期末段赛程已按新名额设计。",
     "2026,48队,名额,扩军", "入门", "world_cup", "rule_change_2026"),
    ("欧洲附加", "欧洲是否有附加赛?", "UEFA playoffs",
     "部分周期欧洲次名队通过附加赛争夺剩余席位。",
     "赛制为单场或主客依当届规定。",
     "欧洲,附加赛,次名,席位", "入门", "world_cup"),
    ("亚洲第四阶段", "亚洲预选赛最后阶段?", "AFC final round",
     "亚洲常设末轮小组或循环决出直接出线与附加赛球队。",
     "队数随名额变化。",
     "亚洲,末轮,出线,附加", "入门", "world_cup"),
    ("非洲末轮", "非洲预选赛决赛阶段?", "CAF final round",
     "非洲末轮多为小组双循环或淘汰赛决出世界杯门票。",
     "轮次多、周期长。",
     "非洲,末轮,小组,门票", "入门", "world_cup"),
    ("南美积分", "南美预选赛多少轮?", "CONMEBOL rounds",
     "全员主客双循环，积分最高若干名直接晋级。",
     "无分组阶段，强度大。",
     "南美,双循环,积分,直接", "入门", "world_cup"),
    ("中北美末段", "中北美六强赛?", "hex final round",
     "传统六强循环决定直接出线与中北美附加赛席位。",
     "2026周期因主办国可能有特殊安排。",
     "中北美,六强,循环,出线", "入门", "world_cup"),
    ("大洋洲冠军", "大洋洲冠军怎么走?", "OFC champion path",
     "大洋洲冠军进入洲际附加赛，对手可能来自其他洲。",
     "晋级难度高但提供曝光。",
     "大洋洲,冠军,附加,对手", "入门", "world_cup"),
    ("排名积分", "预选赛影响排名?", "ranking points",
     "世预赛结果计入FIFA国家队排名，影响分档与抽签。",
     "友谊赛权重不同。",
     "排名,积分,FIFA,分档", "入门", "both"),
    ("同分加时", "预选赛淘汰赛加时?", "KO in qualifiers",
     "部分洲淘汰赛平局进入加时与点球，联赛制则不加时。",
     "依当届洲足联规程。",
     "加时,点球,淘汰赛,洲规", "进阶", "world_cup"),
    ("高原主场", "高原主场是否限制?", "altitude rules",
     "FIFA曾对高原比赛设特殊医疗与适应规则，个别协会受限。",
     "安全与公平为考量。",
     "高原,医疗,适应,限制", "进阶", "world_cup"),
    ("气候延期", "预选赛因天气延期?", "weather postponement",
     "极端天气可申请延期，由裁判与竞赛官员决定。",
     "须在后续国际日补赛。",
     "天气,延期,补赛,国际日", "入门", "world_cup"),
    ("裁判选派", "预选赛裁判来源?", "referee appointment",
     "通常由本洲足联裁判委员会选派，关键战可有FIFA观察。",
     "决赛圈裁判名单单独选拔。",
     "裁判,选派,足联,观察", "入门", "world_cup"),
    ("兴奋剂", "预选赛兴奋剂检测?", "anti-doping qualifiers",
     "世预赛同样受世界反兴奋剂条例约束，赛内赛外抽检。",
     "与决赛圈标准一致。",
     "兴奋剂,WADA,检测,世预赛", "进阶", "both"),
    ("转播权", "预选赛转播权归属?", "qualifier media",
     "各大洲足联与FIFA分销预选赛转播权，与决赛圈合同分开。",
     "球迷观看渠道依地区协议。",
     "转播,分销,足联,媒体", "入门", "world_cup"),
    ("票务", "预选赛门票销售?", "qualifier tickets",
     "由主办协会与地方组委会销售，价格与安保依当地法规。",
     "与决赛圈全球票务体系不同。",
     "门票,本地,协会,销售", "入门", "world_cup"),
    ("数据统计", "预选赛数据谁统计?", "match data",
     "FIFA与洲足联记录进球、助攻等，供排名与技术报告使用。",
     "决赛圈球员数据延续累计。",
     "统计,数据,FIFA,技术", "入门", "world_cup"),
    ("晋级公示", "何时公布出线队?", "qualification confirmation",
     "各洲末轮结束后FIFA确认48强名单并启动决赛圈抽签准备。",
     "名单以官方公告为准。",
     "出线,公示,48强,公告", "入门", "world_cup"),
    ("未出线队", "未出线队还能去吗?", "eliminated teams",
     "未晋级球队不参加决赛圈，球员回俱乐部备战。",
     "无候补替补席位。",
     "未出线,淘汰,俱乐部,无候补", "入门", "world_cup"),
    ("友谊赛穿插", "预选赛期友谊赛?", "friendly windows",
     "国际日期间可安排友谊赛保持状态，但世预赛优先。",
     "伤病风险由协会管理。",
     "友谊赛,国际日,状态,协会", "入门", "both"),
    ("教练资格", "预选赛教练执照?", "coach licensing",
     "主教练须持有FIFA/洲足联认可的Pro级或等效执照。",
     "无证可能面临罚款。",
     "教练,执照,Pro,罚款", "进阶", "world_cup"),
    ("装备规定", "预选赛球衣规定?", "equipment qualifiers",
     "球衣颜色、广告与号码依FIFA装备通则，略宽于决赛圈。",
     "冲突时客队更换颜色。",
     "球衣,装备,颜色,通则", "入门", "world_cup"),
    ("Tie-break", "预选赛同分怎么办?", "tie-breakers",
     "依次比较净胜球、进球、相互战绩、公平竞赛等，依规程。",
     "仍无法区分可抽签。",
     "同分,净胜球,相互,抽签", "进阶", "world_cup"),
    ("周期长度", "世预赛持续多久?", "qualifying cycle",
     "通常覆盖三至四年，与世界杯决赛圈间隔衔接。",
     "下周期在决赛圈后重启。",
     "周期,三年,四年,衔接", "入门", "world_cup"),
    ("与洲际杯", "世预赛与美洲杯?", "confed cup relation",
     "洲际锦标赛与世预赛并行但赛事独立，赛程需协调。",
     "球员负荷由协会统筹。",
     "美洲杯,并行,独立,负荷", "入门", "both"),
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
        "category_l2": "预选赛体系",
        "category_l3": l3,
        "scope": scope,
        "priority": "5",
        "question": q,
        "question_aliases": aliases,
        "answer_short": short,
        "answer_detail": detail,
        "answer_format": "definition",
        "keywords": kw,
        "tags": "赛制,预选赛",
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
