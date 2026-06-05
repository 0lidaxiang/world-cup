#!/usr/bin/env python3
"""Generate T026 glossary batch: 50 transfer market terms, non-gambling (append).

Network: none (local structured data). Outbound HTTP must use fetch_utils.RateLimitedFetcher (>=1s/request); see docs/data-collection-policy.md and .cursor/rules/world-cup-data-collection.mdc."""

from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUTPUT = ROOT / "data" / "knowledge_glossary.csv"
START_ID = 301

COLUMNS = [
    "id", "category_l1", "category_l2", "category_l3", "scope", "priority",
    "question", "question_aliases", "answer_short", "answer_detail", "answer_format",
    "keywords", "tags", "entities", "related_ids", "difficulty",
    "era_start", "era_end", "region", "language", "fact_type", "confidence",
    "source_type", "source_ref", "content_flags", "updated_at",
]

ENTRIES = [
    ("转会", "足球转会是什么意思?", "球员转会|transfer",
     "转会指球员与一家俱乐部合同终止或到期后，与另一家俱乐部签约并注册效力。",
     "须符合FIFA与联赛转会窗及注册规则。",
     "转会,球员,俱乐部,注册", "入门"),
    ("转会窗", "转会窗是什么?", "转会期|transfer window",
     "转会窗是联赛允许俱乐部完成球员注册变更的特定时间段。",
     "欧洲主流联赛有夏季窗与冬季窗。",
     "转会窗,注册,夏窗,冬窗", "入门"),
    ("夏窗", "夏季转会窗是什么?", "夏窗|summer window",
     "赛季间歇期主要转会期，多数大额转会发生在夏窗。",
     "世界杯后夏窗常出现国脚流动。",
     "夏窗,夏季,转会窗,转会", "入门"),
    ("冬窗", "冬季转会窗是什么?", "冬窗|winter window",
     "赛季中期较短转会期，用于补强或外租锻炼球员。",
     "各联赛起止日期不同。",
     "冬窗,冬季,转会窗,补强", "入门"),
    ("租借", "球员租借是什么意思?", "loan|外租",
     "球员短期效力另一俱乐部，所有权通常仍归原俱乐部。",
     "可含买断条款或强制买断。",
     "租借,外租,loan,效力", "入门"),
    ("买断", "租借买断是什么?", "买断条款|buy option",
     "租借合同到期后，效力俱乐部可按约定费用永久签下球员。",
     "可选买断与强制买断条款不同。",
     "买断,租借,条款,永久转会", "进阶"),
    ("自由转会", "自由转会是什么意思?", "自由身|free transfer",
     "合同到期后无需支付转会费即可与新俱乐部签约。",
     "球员可获签字费与更高薪资谈判空间。",
     "自由转会,自由身,合同到期,免签", "入门"),
    ("转会费", "转会费是什么?", "transfer fee|转会价格",
     "俱乐部之间为获得球员注册权而支付的费用。",
     "与球员工资、经纪人佣金等为不同概念。",
     "转会费,费用,俱乐部,交易", "入门"),
    ("解约金", "解约金条款是什么?", "违约金|release clause",
     "合同中约定对方俱乐部支付特定金额即可与球员解约并签约。",
     "并非所有合同都含解约金。",
     "解约金,违约金,合同,条款", "进阶"),
    ("续约", "球员续约是什么意思?", "合同续约|contract extension",
     "在原俱乐部延长合同期限，可能调整薪资与角色。",
     "世界杯表现常影响续约谈判。",
     "续约,合同,留队,薪资", "入门"),
    ("经纪人", "足球经纪人做什么?", "球员经纪人|agent",
     "代表球员或俱乐部谈判合同、转会与商业事务，须持牌合规。",
     "FIFA对经纪人监管规则持续更新。",
     "经纪人,agent,谈判,转会", "入门"),
    ("体检", "转会体检是什么?", "medical|体检关",
     "加盟前俱乐部安排体检评估伤病与体能，未通过可能导致转会取消。",
     "大额转会通常体检公开受关注。",
     "体检,medical,转会,加盟", "入门"),
    ("官宣", "俱乐部官宣是什么意思?", "official announcement",
     "俱乐部正式公告球员加盟、续约或离队，标志转会程序公开完成。",
     "此前可能有媒体报道但以官宣为准。",
     "官宣,公告,俱乐部,转会", "入门"),
    ("压哨转会", "压哨转会是什么?", "deadline day|关窗日",
     "在转会窗关闭前最后时刻完成的交易。",
     "关窗日常出现集中官宣。",
     "压哨转会,关窗,转会窗,截止", "入门"),
    ("标王", "转会标王是什么意思?", "转会纪录|record signing",
     "某一转会窗或时期转会费最高的签约，常引发媒体关注。",
     "标王身份与场上表现无必然联系。",
     "标王,转会费,纪录,签约", "入门"),
    ("身价", "球员身价是什么意思?", "市场价值|valuation",
     "指球员在转会市场上的评估价值，受年龄、表现、合同年限等影响。",
     "身价用于转会谈判参考，与竞技表现相关但非官方数据。",
     "身价,市场价值,评估,转会", "入门"),
    ("浮动条款", "转会浮动条款是什么?", "add-on fee|bonus clause",
     "转会费中随球员出场次数、进球或球队成绩触发的追加付款。",
     "用于分摊风险并激励表现。",
     "浮动条款,追加,转会费,条款", "进阶"),
    ("二次转会分成", "二次转会分成是什么?", "sell-on clause|未来转会分成",
     "球员未来再次被出售时，原出售俱乐部按约定比例获得分成。",
     "青训俱乐部常通过此条款获得收益。",
     "二次转会,分成,sell-on,青训", "进阶"),
    ("优先回购", "优先回购权是什么?", "buy-back clause",
     "球员被出售后，原俱乐部有权在特定条件下优先签回。",
     "常见于年轻外租球员合同。",
     "优先回购,回购权,条款,青训", "进阶"),
    ("回避条款", "租借回避条款是什么?", "loan clause vs parent club",
     "外租球员对阵母队时不得出场，避免利益冲突。",
     "各联赛对回避条款执行细则不同。",
     "回避条款,租借,母队,出场", "进阶"),
    ("球员交换", "球员交换转会是什么?", "swap deal|互换",
     "两家俱乐部以球员互换方式完成交易，可附带差额补偿。",
     "名义上可能显示为双向转会。",
     "球员交换,互换,转会,交易", "进阶"),
    ("免签", "免签加盟是什么意思?", "free signing|bosman",
     "无需向原俱乐部支付转会费即可签约，通常因合同到期。",
     "博斯曼法案后自由转会流动增加。",
     "免签,自由身,免费,签约", "入门"),
    ("注册", "球员注册是什么意思?", "registration|联赛注册",
     "球员须在联赛与足协完成注册方可代表俱乐部出场。",
     "转会窗关闭后注册名单通常锁定。",
     "注册,联赛,出场,名单", "入门"),
    ("报名名单", "联赛报名名单是什么?", "squad list|注册名单",
     "俱乐部向足协提交的当季可出场球员名单，有人数上限。",
     "与世界杯国家队名单概念类似但规则不同。",
     "报名名单,注册,联赛,球员", "入门"),
    ("周薪", "球员周薪是什么?", "weekly wage|工资",
     "职业球员与俱乐部合同约定的周期性薪酬，常以周薪报道。",
     "与转会费、奖金为不同收入组成。",
     "周薪,工资,合同,薪酬", "入门"),
    ("签字费", "签字费是什么?", "signing bonus|签约奖金",
     "球员签约时一次性获得的奖金，自由转会时较常见。",
     "与基本薪资、绩效奖金分开计算。",
     "签字费,签约,奖金,合同", "进阶"),
    ("合同年限", "球员合同一般签几年?", "合同期限|contract length",
     "常见3至5年，含可选延长条款；合同期内转会需对方俱乐部同意。",
     "剩余合同年限影响转会谈判筹码。",
     "合同年限,期限,合同,转会", "入门"),
    ("肖像权", "球员肖像权是什么?", "image rights",
     "球员姓名、形象用于商业推广的权利，可在合同中单独约定分成。",
     "国家队与俱乐部商业使用需分别授权。",
     "肖像权,商业,合同,推广", "进阶"),
    ("离队", "球员离队有哪些方式?", "离开俱乐部|exit",
     "包括转会、租借、合同到期、解约协商及极少数退役等形式。",
     "世界杯前离队可能影响国家队选材。",
     "离队,转会,解约,合同", "入门"),
    ("协商解约", "协商解约是什么?", "mutual termination",
     "俱乐部与球员协商一致提前终止合同，球员可自由寻找下家。",
     "有时涉及补偿金安排。",
     "协商解约,解约,合同,离队", "进阶"),
    ("TMS", "FIFA转会匹配系统是什么?", "Transfer Matching System",
     "FIFA TMS用于国际转会电子申报与合规审核，职业转会须录入系统。",
     "提高转会透明度与支付追踪。",
     "TMS,FIFA,转会系统,国际转会", "专业"),
    ("国际转会证明", "ITC是什么?", "International Transfer Certificate",
     "球员跨国转会时原协会签发的国际转会证明，新协会据此注册。",
     "无ITC通常无法完成国际注册。",
     "ITC,国际转会证明,注册,FIFA", "专业"),
    ("青训补偿", "青训补偿是什么?", "training compensation",
     "球员首次职业合同或转会时，培养其的青训俱乐部可获得补偿。",
     "旨在激励青训投入。",
     "青训补偿,青训,培养,补偿", "进阶"),
    ("联合培养", "联合培养分成是什么?", "solidarity mechanism",
     "球员转会时，其青少年时期效力过的俱乐部可按比例获得团结机制分成。",
     "FIFA团结机制规则适用。",
     "联合培养,团结机制,青训,分成", "专业"),
    ("外租锻炼", "外租锻炼目的是什么?", "loan for development",
     "年轻球员外租至其他联赛获得更多出场时间与发展空间。",
     "世界杯年外租表现可能影响国家队位置。",
     "外租锻炼,年轻球员,出场,发展", "入门"),
    ("豪门求购", "豪门求购是什么意思?", "big club interest",
     "大型俱乐部对球员表达引进兴趣，转会谈判可能持续数周。",
     "媒体报道不等于正式报价。",
     "豪门,求购,转会,兴趣", "入门"),
    ("报价", "俱乐部报价是什么?", "bid|offer",
     "一家俱乐部向另一家就球员转会提出的正式或口头金额方案。",
     "卖方俱乐部可接受、拒绝或还价。",
     "报价,bid,转会,谈判", "入门"),
    ("还价", "转会还价是什么?", "counter offer",
     "卖方对买方报价不满意时提出更高要价或不同条款。",
     "多轮谈判后可能达成协议。",
     "还价,谈判,转会,报价", "入门"),
    ("体检失败", "体检失败转会会怎样?", "failed medical",
     "球员未通过体检，俱乐部可取消交易或重新谈判条款。",
     "大额转会风险环节之一。",
     "体检失败,medical,取消,转会", "进阶"),
    ("合同到期", "合同到期后球员归属?", "contract expiry",
     "合同到期球员成为自由球员，可与任意俱乐部谈判。",
     "世界杯前合同年球员常受关注。",
     "合同到期,自由身,续约,转会", "入门"),
    ("降薪留队", "降薪留队是什么?", "pay cut to stay",
     "球员为留队接受薪资下调，多见于俱乐部财务调整期。",
     "与转会离队为不同选择。",
     "降薪,留队,薪资,合同", "进阶"),
    ("转会传闻", "转会传闻可信吗?", "transfer rumor|流言",
     "媒体报道的潜在转会，在俱乐部官宣前均非正式确认。",
     "应以官方公告为准。",
     "转会传闻,流言,媒体,官宣", "入门"),
    ("世界杯年转会", "世界杯年转会有何特点?", "World Cup year transfer",
     "世界杯后球员表现可能推高转会价值；赛前大转会或影响备战。",
     "俱乐部与国家队需协调球员状态。",
     "世界杯年,转会,国脚,状态", "进阶"),
    ("放行国脚", "俱乐部为何放行国脚?", "release for national team",
     "根据FIFA国际比赛日规定，俱乐部须放行被征召国脚参加国家队赛事。",
     "世界杯期间球员归属国家队征召。",
     "放行,国脚,国家队,征召", "入门"),
    ("转会禁令", "转会禁令是什么?", "transfer ban",
     "因违反注册或财务规则，俱乐部在特定期间被禁止注册新球员。",
     "仍可与球员签约但须待禁令解除后注册。",
     "转会禁令,注册,处罚,FIFA", "进阶"),
    ("财务公平", "财务公平规则是什么?", "FFP|Financial Fair Play",
     "欧足联等要求俱乐部收支平衡，限制过度烧钱引援。",
     "违规可能面临罚款或欧战限制。",
     "财务公平,FFP,欧足联,引援", "进阶"),
    ("工资结构", "俱乐部工资结构是什么?", "wage structure",
     "球队总薪资预算及球员间薪酬层级，影响引援与续约空间。",
     "与转会费共同构成俱乐部成本。",
     "工资结构,薪资,预算,俱乐部", "进阶"),
    ("替补门将规则", "转会与第三门将?", "third goalkeeper rule",
     "世界杯允许每队报名含三名门将在内的26人，转会窗门将补强常见。",
     "伤病时可能紧急签替补门将。",
     "门将,报名,世界杯,补强", "进阶"),
    ("队医通过", "转会还需要什么程序?", "paperwork completion",
     "除体检与合同外，须完成足协注册、工作许可（如适用）及TMS申报。",
     "国际转会程序较国内更复杂。",
     "注册,工作许可,程序,国际转会", "进阶"),
    ("关窗日", "转会关窗日是什么?", "deadline day|转会截止",
     "转会窗最后一天，俱乐部须在此日前完成注册手续，否则须待下一窗期。",
     "欧洲关窗日常出现集中官宣与压哨交易。",
     "关窗日,截止,转会窗,注册", "入门"),
]


def row(seq: int, entry: tuple) -> dict[str, str]:
    l3, q, aliases, short, detail, kw, diff = entry
    return {
        "id": f"WC-GLOS-{seq:05d}",
        "category_l1": "术语与百科",
        "category_l2": "转会市场",
        "category_l3": l3,
        "scope": "football_general",
        "priority": "2",
        "question": q,
        "question_aliases": aliases,
        "answer_short": short,
        "answer_detail": detail,
        "answer_format": "definition",
        "keywords": kw,
        "tags": "转会市场,术语",
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
        "source_ref": "FIFA Regulations on the Status and Transfer of Players",
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
