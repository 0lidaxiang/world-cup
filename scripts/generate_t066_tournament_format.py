#!/usr/bin/env python3
"""Generate T066: 50 World Cup schedule & rest-day entries (append).

Network: none (local structured data). Outbound HTTP must use fetch_utils.RateLimitedFetcher (>=1s/request); see docs/data-collection-policy.md and .cursor/rules/world-cup-data-collection.mdc."""

from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUTPUT = ROOT / "data" / "knowledge_tournament_format.csv"
START_ID = 301

COLUMNS = [
    "id", "category_l1", "category_l2", "category_l3", "scope", "priority",
    "question", "question_aliases", "answer_short", "answer_detail", "answer_format",
    "keywords", "tags", "entities", "related_ids", "difficulty",
    "era_start", "era_end", "region", "language", "fact_type", "confidence",
    "source_type", "source_ref", "content_flags", "updated_at",
]

ENTRIES = [
    ("决赛圈赛期", "世界杯决赛圈一般多长?", "finals duration",
     "32队时代决赛圈约32天，含小组赛与淘汰赛全程。",
     "48队时代总场次增加，赛期相应延长。",
     "决赛圈,赛期,天数,32天", "入门", "world_cup"),
    ("48队赛期", "2026世界杯赛期多长?", "2026 duration",
     "美加墨2026预计约39天，覆盖6月中旬至7月中旬。",
     "三国联办跨度大，具体以官方赛程为准。",
     "2026,39天,赛期,美加墨", "入门", "world_cup"),
    ("小组赛轮次", "小组赛踢几轮?", "group rounds",
     "4队小组踢3轮各1场，共6场小组赛后决出前两名。",
     "末轮同组两场须同时开球。",
     "小组赛,三轮,同开,轮次", "入门", "world_cup"),
    ("末轮同开", "小组赛末轮为何同开?", "simultaneous kickoffs",
     "防止先赛球队知晓赛果后影响后赛战术，保证公平。",
     "FIFA规程要求同组最后两场开球时间一致。",
     "末轮,同开,公平,小组赛", "入门", "world_cup"),
    ("两场间隔", "相邻两场最少隔几天?", "minimum rest days",
     "FIFA要求相邻比赛至少间隔48小时（2个完整自然日）。",
     "48队时代48组阶段同样适用该休息下限。",
     "48小时,间隔,休息,两场", "入门", "world_cup"),
    ("淘汰赛间隔", "淘汰赛休息比小组赛长吗?", "knockout rest",
     "16强至决赛各阶段通常间隔3至4天，多于小组赛最低48小时。",
     "具体间隔依当届官方赛程表。",
     "淘汰赛,间隔,16强,休息", "入门", "world_cup"),
    ("揭幕战", "揭幕战一般何时?", "opening match timing",
     "东道主或FIFA指定对阵承办开幕式与揭幕战，常于赛期首日。",
     "2022卡塔尔揭幕战为11月20日。",
     "揭幕战,开幕式,首日,东道主", "入门", "world_cup"),
    ("决赛日期", "决赛一般何时?", "final match timing",
     "决赛常安排在赛期最后一日或倒数第二日傍晚。",
     "冠军在决赛当场产生，无附加赛。",
     "决赛,最后,冠军,日期", "入门", "world_cup"),
    ("三四名赛", "季军战与决赛间隔?", "third place timing",
     "三四名决赛通常在决赛前一日或前两日进行。",
     "半决赛负者获得额外休息后再赛。",
     "季军战,间隔,半决赛,休息", "入门", "world_cup"),
    ("每日场次", "一天最多踢几场?", "matches per day",
     "赛期中段常安排3至4场/日，开幕与收官阶段场次可能减少。",
     "48队时代小组赛阶段每日场次更多。",
     "每日,场次,密度,赛程", "入门", "world_cup"),
    ("晚场开球", "为何有晚场?", "evening kickoffs",
     "适应当地气温与全球转播黄金时段，晚场利于球员与观众。",
     "中东与夏季主办国晚场更常见。",
     "晚场,开球,气温,转播", "入门", "world_cup"),
    ("中场休息", "中场休息多久?", "half-time break",
     "中场休息不超过15分钟，裁判可酌情缩短。",
     "加时赛前另有15分钟休息。",
     "中场,15分钟,休息,规则", "入门", "both", "rule"),
    ("加时休息", "加时赛前休息多久?", "extra time break",
     "90分钟平局后加时前休息不超过15分钟。",
     "点球大战前再休息不超过1分钟。",
     "加时,休息,15分钟,点球", "入门", "world_cup", "rule"),
    ("补水暂停", "高温能否补水暂停?", "cooling breaks",
     "裁判可因高温在上下半场各设一次官方补水暂停。",
     "卡塔尔2022多场比赛启用该措施。",
     "补水,高温,暂停,裁判", "入门", "world_cup", "rule"),
    ("无赛日", "决赛圈有无赛日?", "rest days no match",
     "赛期中会安排无赛日供球队恢复与转场。",
     "淘汰赛阶段无赛日常多于小组赛末段。",
     "无赛日,恢复,转场,休息", "入门", "world_cup"),
    ("16强间隔", "16强与8强隔几天?", "R16 to QF gap",
     "16强赛后通常休息3至4天再踢8强。",
     "具体日期见当届赛程PDF。",
     "16强,8强,间隔,休息", "入门", "world_cup"),
    ("半决赛间隔", "半决赛后休息多久?", "semi to final rest",
     "决赛球队半决赛后通常有6至7天休息。",
     "长于小组赛阶段的最低48小时要求。",
     "半决赛,决赛,休息,间隔", "入门", "world_cup"),
    ("连续作战", "能否三天踢两场?", "three-day turnaround",
     "决赛圈相邻两场须间隔至少48小时，禁止过密赛程。",
     "预选赛阶段安排可能更紧，决赛圈更严格。",
     "连续,48小时,禁止,过密", "入门", "world_cup"),
    ("冬赛期", "2022为何11月踢?", "winter scheduling",
     "卡塔尔夏季高温不适比赛，改在11-12月举办。",
     "为史上首次北半球冬季世界杯决赛圈。",
     "2022,冬季,卡塔尔,11月", "入门", "world_cup"),
    ("夏赛传统", "世界杯传统赛期?", "summer tradition",
     "多数届次在6-7月北半球夏季举行，与联赛休赛期重叠。",
     "2022与2026因主办国气候有所调整。",
     "夏季,6月,7月,传统", "入门", "world_cup"),
    ("2026跨度", "2026赛程跨几国?", "tri-nation travel",
     "美加墨三国联办，球队可能跨国飞行，赛程考虑转场时间。",
     "同组比赛尽量集中区域以减少旅途。",
     "2026,跨国,飞行,联办", "进阶", "world_cup"),
    ("时区安排", "赛程如何兼顾时区?", "time zone scheduling",
     "开球时间兼顾主办国本地、欧洲与美洲转播市场。",
     "三国联办时同一比赛日可能跨多个时区。",
     "时区,转播,开球,市场", "入门", "world_cup"),
    ("训练日", "比赛日前能否训练?", "training day",
     "球队可在比赛日前一日官方训练，时长与媒体开放依规程。",
     "赛前24小时起对手可观摩一次训练。",
     "训练,赛前,官方,媒体", "入门", "world_cup"),
    ("官方酒店", "球队住官方酒店吗?", "team hotels",
     "各队通常入住组委会指定基地酒店，减少通勤。",
     "训练基地与酒店距离影响休息质量。",
     "酒店,基地,通勤,休息", "入门", "world_cup"),
    ("封闭期", "赛前是否封闭?", "pre-match lockdown",
     "关键淘汰赛前球队常减少公开活动以专注备战。",
     "非强制规则，由各队自主管理。",
     "封闭,备战,淘汰赛,管理", "入门", "world_cup"),
    ("媒体日", "赛前媒体活动?", "media day",
     "赛前须出席新闻发布会，队长与主教练参加。",
     "时间安排在规程规定的媒体窗口内。",
     "媒体,发布会,队长,赛前", "入门", "world_cup"),
    ("48队96场", "48队小组赛多少场?", "48-team group matches",
     "12组×4队共72场小组赛，加上32场淘汰赛共104场。",
     "较32队64场显著增加。",
     "48队,104场,小组赛,72场", "入门", "world_cup"),
    ("32队64场", "32队时代总场次?", "32-team total matches",
     "8组48场小组赛加16场淘汰赛共64场。",
     "1998至2022年沿用该结构。",
     "32队,64场,8组,淘汰赛", "入门", "world_cup"),
    ("同组赛程", "同组四队如何对阵?", "group fixture order",
     "每队与同组另三队各赛一场，三轮后按积分排名。",
     "末轮两场须同时开球。",
     "同组,对阵,三轮,积分", "入门", "world_cup"),
    ("48组12轮", "48队小组如何分组赛?", "12 groups schedule",
     "12个小组各6场，赛期前两周密集完成大部分小组赛。",
     "具体轮次分配以2026官方赛程为准。",
     "12组,48队,密集,前两轮", "入门", "world_cup"),
    ("新32强", "48队如何进32强?", "round of 32",
     "各组前二加8个最佳第三共32队进入淘汰赛。",
     "第三排名规则在规程中列明。",
     "32强,第三,最佳,晋级", "入门", "world_cup"),
    ("淘汰赛单场", "淘汰赛踢几场?", "knockout single leg",
     "决赛圈淘汰赛均为单场定胜负，无主客场双回合。",
     "平局进加时，仍平则点球。",
     "淘汰赛,单场,加时,点球", "入门", "world_cup"),
    ("点球大战", "点球何时进行?", "penalty timing",
     "淘汰赛加时仍平局后进行点球大战决胜负。",
     "小组赛平局不踢点球。",
     "点球,淘汰赛,加时,小组赛", "入门", "world_cup", "rule"),
    ("长途飞行", "跨国比赛影响休息吗?", "long-haul travel",
     "赛程设计尽量避免短时间跨洲飞行，给予转场日。",
     "2026三国联办对飞行距离尤为关注。",
     "飞行,转场,休息,2026", "进阶", "world_cup"),
    ("气候适应", "球队如何适应气候?", "climate acclimatization",
     "提前抵达主办国集训以适应温度、湿度与海拔。",
     "冬赛或高原主办国适应期更长。",
     "气候,适应,集训,海拔", "入门", "world_cup"),
    ("高原比赛", "高原举办影响赛程吗?", "altitude scheduling",
     "墨西哥等高原城市比赛时赛程会考虑体能恢复。",
     "2010南非部分赛场海拔较高。",
     "高原,墨西哥,体能,恢复", "进阶", "world_cup"),
    ("脑震荡观察", "脑震荡换人影响阵容?", "concussion sub rest",
     "额外脑震荡换人名额不计入常规5换，利于保护球员。",
     "被换下的球员须完成评估流程。",
     "脑震荡,换人,观察,评估", "进阶", "world_cup", "rule"),
    ("五换人", "五换人如何影响体能?", "five subs stamina",
     "允许5次换人3个窗口，教练可更频繁刷新阵容。",
     "2022卡塔尔起正式采用5换人。",
     "五换人,体能,窗口,2022", "入门", "world_cup", "rule"),
    ("加时换人", "加时还能换人吗?", "extra time subs",
     "部分届次规程允许加时额外换人名额。",
     "具体以当届FIFA World Cup Regulations为准。",
     "加时,换人,额外,规程", "进阶", "world_cup", "rule"),
    ("赛后恢复", "赛后恢复时间?", "post-match recovery",
     "高强度淘汰赛后球队依赖48小时以上间隔恢复。",
     "医疗团队负责冷却、按摩与睡眠管理。",
     "恢复,医疗,间隔,淘汰", "入门", "world_cup"),
    ("裁判休息", "裁判也有休息要求吗?", "referee rest",
     "裁判组同样遵循场次间隔，避免连续执法。",
     "VAR团队与助理裁判一并轮换。",
     "裁判,间隔,轮换,VAR", "入门", "world_cup"),
    ("开球时间", "开球时间如何公布?", "kickoff announcement",
     "全部开球时间在赛前数周由FIFA与组委会联合发布。",
     "末轮同组场次同时公布。",
     "开球,公布,赛程,FIFA", "入门", "world_cup"),
    ("延期比赛", "比赛能否延期?", "postponement",
     "极端天气或安全原因下FIFA可改期，尽量不影响48小时规则。",
     "2020年代疫情曾影响全球赛程范例。",
     "延期,改期,天气,安全", "进阶", "world_cup"),
    ("双赛日", "同一球队双赛日?", "double matchday",
     "决赛圈不存在同一球队同日两场，间隔至少48小时。",
     "青年赛或俱乐部赛规则不同。",
     "双赛,48小时,禁止,决赛圈", "入门", "world_cup"),
    ("预选赛窗口", "预选赛国际比赛日?", "qualifier windows",
     "预选赛使用FIFA国际比赛日历窗口，与联赛协调。",
     "与决赛圈集中赛期不同。",
     "预选赛,国际比赛日,窗口,联赛", "入门", "both"),
    ("赛后解散", "淘汰后何时离队?", "elimination departure",
     "被淘汰球队通常24至48小时内离村，不再占用官方资源。",
     "个别球员可能留队参加颁奖活动。",
     "淘汰,离村,解散,离队", "入门", "world_cup"),
    ("冠军行程", "冠军赛后还有比赛吗?", "champion schedule end",
     "决赛即为最后一场，冠军赛后参加颁奖与庆祝。",
     "无季后附加赛。",
     "冠军,决赛,最后,颁奖", "入门", "world_cup"),
    ("赛会村", "球队住赛会村吗?", "team base camp",
     "各队选择官方认证基地而非统一奥运村式住宿。",
     "基地至赛场通勤时间纳入赛程考量。",
     "基地,赛会,通勤,认证", "入门", "world_cup"),
    ("2022密度", "2022赛程密度如何?", "Qatar 2022 density",
     "28天完成64场，因冬赛压缩但仍满足48小时间隔。",
     "为32队时代较短赛期之一。",
     "2022,28天,密度,卡塔尔", "入门", "world_cup"),
    ("官方赛程", "哪里查官方赛程?", "official schedule source",
     "FIFA官网与当届组委会发布权威赛程与开球时间。",
     "第三方App仅供参考，以官方为准。",
     "官方,赛程,FIFA,开球", "入门", "world_cup"),
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
        "category_l2": "赛程与休息",
        "category_l3": l3,
        "scope": scope,
        "priority": "5",
        "question": q,
        "question_aliases": aliases,
        "answer_short": short,
        "answer_detail": detail,
        "answer_format": "definition",
        "keywords": kw,
        "tags": "赛制,赛程",
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
