#!/usr/bin/env python3
"""Generate T065: 50 World Cup bidding & host selection entries (append).

Network: none (local structured data). Outbound HTTP must use fetch_utils.RateLimitedFetcher (>=1s/request); see docs/maintainers/data-collection-policy.md and .cursor/rules/world-cup-data-collection.mdc."""

from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUTPUT = ROOT / "data" / "knowledge_tournament_format.csv"
START_ID = 251

COLUMNS = [
    "id", "category_l1", "category_l2", "category_l3", "scope", "priority",
    "question", "question_aliases", "answer_short", "answer_detail", "answer_format",
    "keywords", "tags", "entities", "related_ids", "difficulty",
    "era_start", "era_end", "region", "language", "fact_type", "confidence",
    "source_type", "source_ref", "content_flags", "updated_at",
]

ENTRIES = [
    ("申办流程", "世界杯主办国怎么选?", "host selection",
     "由国际足联会员大会投票选定主办国或联合主办体。",
     "申办前须提交候选文件并通过合规审查。",
     "申办,投票,大会,主办国", "入门", "world_cup"),
    ("申办文件", "申办文件包含什么?", "bid book",
     "涵盖场馆、交通、住宿、安保、医疗、遗产与可持续性计划。",
     "FIFA评估团现场考察后打分。",
     "申办文件,场馆,评估,遗产", "入门", "world_cup"),
    ("评估团", "FIFA评估团做什么?", "inspection team",
     "考察候选城市设施、政府支持与风险，发布公开技术报告。",
     "报告供会员投票参考。",
     "评估团,考察,技术报告,投票", "入门", "world_cup"),
    ("投票规则", "主办国投票规则?", "voting procedure",
     "多数票当选，多轮淘汰得票最少候选，程序依FIFA治理规则。",
     "投票保密或公开程度依大会规定。",
     "投票,多数,淘汰,治理", "进阶", "world_cup"),
    ("联合主办", "可以多国联合主办吗?", "co-hosting",
     "2026美加墨为联合主办先例，分摊场馆与赛程责任。",
     "须FIFA理事会批准框架协议。",
     "联合主办,2026,美加墨,协议", "入门", "world_cup"),
    ("单国主办", "单国主办优势?", "single host",
     "单国主办便于统一签证、交通与组委会治理。",
     "历史上多数届次为单国。",
     "单国,签证,交通,治理", "入门", "world_cup"),
    ("场馆标准", "申办需要哪些场馆?", "stadium requirements",
     "须满足容量、媒体、更衣室、安全与草坪标准，决赛球场要求更高。",
     "可新建或改造现有球场。",
     "场馆,容量,标准,改造", "入门", "world_cup"),
    ("训练基地", "训练基地要求?", "team base camps",
     "各队训练基地需符合距离、设施与安保标准，赛前申报。",
     "组委会协调预订。",
     "训练基地,安保,设施,申报", "入门", "world_cup"),
    ("主办协议", "主办国与FIFA签什么?", "host agreement",
     "签署主办协议明确权利义务、商业、安保与竞赛运营分工。",
     "具有法律约束力。",
     "主办协议,权利义务,法律,运营", "进阶", "world_cup"),
    ("LOC", "本地组委会角色?", "local organising committee",
     "本地组委会负责落地运营，FIFA保留赛事品牌与竞赛监督。",
     "赛后组委会解散或转型。",
     "LOC,组委会,运营,品牌", "入门", "world_cup"),
    ("政府保证", "政府保证函?", "government guarantees",
     "申办国政府承诺签证、安保、税收与劳动等支持。",
     "为投票必要条件之一。",
     "政府保证,签证,税收,安保", "进阶", "world_cup"),
    ("人权标准", "申办与人权标准?", "human rights",
     "FIFA加强申办与人权、劳工标准审查，纳入评估维度。",
     "具体指标在治理政策中更新。",
     "人权,劳工,审查,治理", "进阶", "world_cup"),
    ("可持续性", "申办可持续性要求?", "sustainability bid",
     "候选文件须说明碳管理、交通与场馆赛后利用。",
     "赛后遗产为评分项。",
     "可持续,碳管理,遗产,评分", "入门", "world_cup"),
    ("2030申办", "2030世界杯申办进展?", "2030 bid status",
     "2030主办权由会员大会投票确定，候选来自多洲联合方案。",
     "结果以FIFA官方公告为准。",
     "2030,申办,投票,公告", "入门", "world_cup", "time_sensitive"),
    ("2034申办", "2034世界杯申办?", "2034 bid",
     "2034主办权竞争依FIFA时间表进行，细则陆续公布。",
     "知识库随官方更新。",
     "2034,申办,时间表,公布", "入门", "world_cup", "time_sensitive"),
    ("轮换原则", "主办权大洲轮换?", "rotation policy",
     "FIFA曾考虑大洲轮换，现已更灵活但仍避免连续同洲主办。",
     "具体限制见当届招标指引。",
     "轮换,大洲,灵活,招标", "进阶", "world_cup"),
    ("首次主办", "首次主办意义?", "first time host",
     "首次主办国常借世界杯推动基建与足球普及。",
     "如2010南非、2022卡塔尔。",
     "首次,主办,基建,普及", "入门", "world_cup", "history"),
    ("重复主办", "哪些国家多次主办?", "repeat hosts",
     "墨西哥、意大利、法国、德国、巴西等多次主办。",
     "2026墨西哥第三次主办。",
     "多次,墨西哥,巴西,德国", "入门", "world_cup", "history"),
    ("撤回申办", "申办能否撤回?", "withdraw bid",
     "候选可在投票前撤回，影响剩余候选竞争格局。",
     "已发生多次历史案例。",
     "撤回,申办,候选,案例", "进阶", "world_cup", "history"),
    ("贿赂调查", "申办腐败调查?", "ethics investigations",
     "FIFA伦理委员会曾调查申办腐败，推动治理改革。",
     "现行合规程序更严格。",
     "伦理,腐败,改革,合规", "进阶", "world_cup", "history"),
    ("世界杯收益", "主办国经济收益?", "economic impact",
     "旅游、就业与基建带动效益评估争议大，依独立研究。",
     "非竞赛规则内容。",
     "经济,旅游,基建,评估", "进阶", "world_cup"),
    ("场馆白象", "赛后场馆闲置?", "white elephants",
     "部分主办国面临场馆利用率不足，遗产计划旨在缓解。",
     "申办文件要求赛后用途。",
     "场馆,闲置,遗产,利用率", "进阶", "world_cup"),
    ("气候选址", "主办国气候考量?", "climate selection",
     "极端气候可能影响赛期，如2022改冬季、2026北美夏季。",
     "候选文件须说明应对方案。",
     "气候,赛期,冬季,应对", "入门", "world_cup"),
    ("时区", "主办国时区影响?", "time zone impact",
     "开球时间服务全球转播，主办国本地观众亦需兼顾。",
     "赛程组与FIFA协调。",
     "时区,开球,转播,本地", "入门", "world_cup"),
    ("签证政策", "世界杯球迷签证?", "fan visas",
     "主办国常设短期观赛签证或入境便利，依双边协议。",
     "2026三国可能需多次签证。",
     "签证,球迷,入境,2026", "入门", "world_cup", "time_sensitive"),
    ("安保成本", "主办安保谁买单?", "security costs",
     "主办国政府承担主要安保，FIFA协调国际标准。",
     "预算在申办文件中列明。",
     "安保,政府,成本,预算", "进阶", "world_cup"),
    ("免税", "参赛物资免税?", "tax exemptions",
     "主办国通常对赛事进口设备与球队物资给予临时免税。",
     "细节在主办协议。",
     "免税,进口,物资,协议", "进阶", "world_cup"),
    ("劳动权益", "场馆建设劳工?", "construction labour",
     "申办评估关注建筑工人权益与安全标准。",
     "2022后标准更受重视。",
     "劳工,建设,权益,安全", "进阶", "world_cup"),
    ("媒体中心", "国际媒体中心?", "IMC",
     "主办城市设国际媒体中心，提供转播与新闻设施。",
     "容量依预计注册记者数。",
     "媒体中心,转播,记者,设施", "入门", "world_cup"),
    ("官方酒店", "球队官方酒店?", "team hotels",
     "组委会认证酒店满足星级、安保与交通要求。",
     "球队自选在认证名单内。",
     "酒店,认证,安保,球队", "入门", "world_cup"),
    ("交通规划", "城市间交通?", "transport plan",
     "申办文件包括机场、铁路与公路扩容方案。",
     "赛时可能实行交通管制。",
     "交通,机场,铁路,管制", "入门", "world_cup"),
    ("环保", "主办环保承诺?", "green hosting",
     "减少一次性塑料、推广公共交通与绿色建筑认证。",
     "指标写入可持续报告。",
     "环保,塑料,绿色,报告", "入门", "world_cup"),
    ("遗产基金", "世界杯遗产基金?", "legacy fund",
     "部分收入投入基层足球与社区项目。",
     "由FIFA与主办联合体管理。",
     "遗产基金,基层,社区,FIFA", "入门", "world_cup"),
    ("取消主办", "能否取消主办权?", "strip hosting",
     "严重违约或不可抗力下FIFA可重新分配或中止。",
     "极罕见，需理事会决议。",
     "取消,违约,重新分配,罕见", "进阶", "world_cup"),
    ("备用主办", "有备用主办国吗?", "backup host",
     "招标有时要求备用方案，具体依当届文件。",
     "非每届公开备用国。",
     "备用,方案,招标,文件", "进阶", "world_cup"),
    ("女子主办", "女子世界杯主办选择?", "women hosting",
     "女子世界杯主办国亦由FIFA大会投票，流程类似但规模较小。",
     "独立候选文件。",
     "女子,主办,投票,独立", "入门", "both"),
    ("青少主办", "U20世界杯主办?", "youth hosting",
     "青年世界杯主办选择流程简化，由理事会或大会确定。",
     "与男子旗舰赛分开。",
     "U20,青年,主办,分开", "入门", "both"),
    ("2018俄罗斯", "2018主办国?", "Russia 2018",
     "2018年由俄罗斯主办，11座城市承办，32队赛制。",
     "揭幕战在莫斯科。",
     "2018,俄罗斯,11城,32队", "入门", "world_cup", "history"),
    ("2022卡塔尔", "2022主办特点?", "Qatar 2022 host",
     "2022卡塔尔首次中东主办，赛期11-12月，8座球场。",
     "揭幕战在多哈。",
     "2022,卡塔尔,冬季,8座", "入门", "world_cup", "history"),
    ("2026准备", "2026筹备状态?", "2026 preparation",
     "美加墨联合组委会推进场馆改造与赛程规划。",
     "细节随官方新闻更新。",
     "2026,筹备,场馆,联合", "入门", "world_cup", "time_sensitive"),
    ("招标时间线", "申办时间线多长?", "bid timeline",
     "从启动招标到投票通常数年，含考察与公关阶段。",
     "具体日期见FIFA日历。",
     "时间线,招标,考察,投票", "入门", "world_cup"),
    ("民间申办", "民间能申办吗?", "national federation only",
     "仅会员协会代表国家向FIFA提交申办，非民间公司单独申办。",
     "政府与足协合作。",
     "会员协会,申办,政府,合作", "入门", "world_cup"),
    ("成本分担", "联合主办如何分担?", "cost sharing",
     "联合主办协议划分场馆、安保与营销成本。",
     "收入分成亦在协议约定。",
     "成本,分担,收入,协议", "进阶", "world_cup"),
    ("法律框架", "主办国特殊立法?", "event legislation",
     "部分国家通过世界杯特别法保障知识产权与安保。",
     "赛后法律状态依各国。",
     "特别法,知识产权,安保,立法", "进阶", "world_cup"),
    ("赞助商", "主办城市赞助商?", "sponsorship",
     "FIFA全球赞助商与主办国本地赞助商层级分开。",
     "防止市场冲突。",
     "赞助商,全球,本地,层级", "入门", "world_cup"),
    ("票务收入", "门票收入归谁?", "ticket revenue",
     "收入分配在FIFA与本地组委会协议中约定。",
     "定价策略考虑本地购买力。",
     "门票,收入,分配,定价", "入门", "world_cup"),
    ("志愿者法", "志愿者法律地位?", "volunteer legal",
     "志愿者签署协议明确保险、工时与行为准则。",
     "不替代有偿员工核心岗位。",
     "志愿者,保险,协议,准则", "入门", "world_cup"),
    ("反腐败", "主办反腐败措施?", "anti-corruption host",
     "招标与采购须遵守FIFA诚信合规与审计要求。",
     "违规可向伦理委员会举报。",
     "反腐败,合规,审计,举报", "进阶", "world_cup"),
    ("赛后评估", "主办赛后评估?", "post-tournament review",
     "FIFA与组委会发布赛后报告评估目标达成与遗产。",
     "影响下届招标标准。",
     "赛后,评估,报告,遗产", "入门", "world_cup"),
    ("转播基建", "申办国转播设施要求?", "broadcast infrastructure",
     "申办文件须说明国际转播中心、光纤与卫星上行能力。",
     "赛时由FIFA媒体团队协调全球信号制作。",
     "转播,光纤,卫星,媒体", "入门", "world_cup"),
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
        "category_l2": "主办国与申办",
        "category_l3": l3,
        "scope": scope,
        "priority": "5",
        "question": q,
        "question_aliases": aliases,
        "answer_short": short,
        "answer_detail": detail,
        "answer_format": "definition",
        "keywords": kw,
        "tags": "赛制,申办",
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
