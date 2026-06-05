#!/usr/bin/env python3
"""Generate T060: 50 World Cup founding & FIFA relationship entries (append).

Network: none (local structured data). Outbound HTTP must use fetch_utils.RateLimitedFetcher (>=1s/request); see docs/data-collection-policy.md and .cursor/rules/world-cup-data-collection.mdc."""

from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUTPUT = ROOT / "data" / "knowledge_tournament_format.csv"
START_ID = 1

COLUMNS = [
    "id", "category_l1", "category_l2", "category_l3", "scope", "priority",
    "question", "question_aliases", "answer_short", "answer_detail", "answer_format",
    "keywords", "tags", "entities", "related_ids", "difficulty",
    "era_start", "era_end", "region", "language", "fact_type", "confidence",
    "source_type", "source_ref", "content_flags", "updated_at",
]

ENTRIES = [
    ("FIFA成立", "国际足联哪年成立?", "FIFA founding",
     "国际足联1904年5月21日在巴黎成立。",
     "全称国际足球联合会，总部现设瑞士苏黎世。",
     "FIFA,1904,巴黎,成立", "入门", "both", "history"),
    ("世界杯创设", "世界杯是谁倡议的?", "Rimet World Cup",
     "法国人朱尔·雷米特推动设立世界杯，1928年大会通过。",
     "旨在促进各国国家队交流与世界足球普及。",
     "雷米特,创设,1928,世界杯", "入门", "world_cup", "history"),
    ("首届世界杯", "首届世界杯何时何地?", "1930 Uruguay",
     "1930年7月在乌拉圭蒙得维的亚举行，13队参赛。",
     "乌拉圭作为1928奥运足球冠军与百年独立庆典主办。",
     "1930,首届,乌拉圭,13队", "入门", "world_cup", "history"),
    ("二战停办", "世界杯因二战停办吗?", "WWII cancellation",
     "1942年与1946年两届因二战取消，1946年大会决定恢复。",
     "1950年巴西恢复举办为第四届。",
     "二战,停办,1942,1946", "入门", "world_cup", "history"),
    ("FIFA与世界杯", "世界杯归谁组织?", "FIFA organizes WC",
     "世界杯由国际足联独家主办并制定当届竞赛规程。",
     "各大洲足联协助预选赛，决赛圈由FIFA统一运营。",
     "FIFA,主办,规程,决赛圈", "入门", "world_cup", "history"),
    ("正式名称", "世界杯英文官方名?", "FIFA World Cup",
     "英文正式名称为FIFA World Cup，中文常称国际足联世界杯。",
     "与俱乐部赛事、区域杯赛名称不可混用。",
     "FIFA World Cup,名称,官方,英文", "入门", "both", "history"),
    ("雷米特杯", "早期冠军奖杯叫什么?", "Jules Rimet Trophy",
     "1930至1970年冠军获雷米特杯，巴西三冠后永久保留。",
     "1974年起改用大力神杯体系。",
     "雷米特杯,奖杯,1970,巴西", "入门", "world_cup", "history"),
    ("大力神杯", "现行世界杯奖杯?", "FIFA World Cup Trophy",
     "1974年起冠军获大力神杯复制品，真品由FIFA保管。",
     "原杯不再随队永久持有。",
     "大力神杯,1974,奖杯,FIFA", "入门", "world_cup", "history"),
    ("与奥运关系", "世界杯与奥运足球?", "WC vs Olympic",
     "世界杯为FIFA独立旗舰赛；奥运男足有年龄限制且规程不同。",
     "二者赛程、名额与注册规则均不互相替代。",
     "奥运,区别,年龄,独立", "入门", "both", "history"),
    ("四年周期", "世界杯几年一届?", "four-year cycle",
     "自1930年起（二战除外）每四年一届，由FIFA理事会确定赛历。",
     "预选赛与决赛圈贯穿整个周期。",
     "四年,一届,周期,FIFA", "入门", "world_cup", "history"),
    ("1950赛制", "1950年世界杯赛制?", "1950 final group",
     "1950年无单场决赛，四队末轮循环定冠军，乌拉圭夺冠。",
     "属特殊历史赛制，此后恢复淘汰赛决赛。",
     "1950,循环,决赛,乌拉圭", "进阶", "world_cup", "history"),
    ("扩军16队", "何时扩至16队?", "expand to 16",
     "1954年瑞士世界杯起决赛圈为16队，直至1982年前维持。",
     "扩军反映全球参赛国增多。",
     "16队,1954,扩军,决赛圈", "入门", "world_cup", "history"),
    ("扩军24队", "何时扩至24队?", "expand to 24",
     "1982年西班牙世界杯起决赛圈扩至24队。",
     "小组赛结构随之调整。",
     "24队,1982,西班牙,扩军", "入门", "world_cup", "history"),
    ("扩军32队", "何时扩至32队?", "expand to 32",
     "1998年法国世界杯起决赛圈为32队，持续至2022年。",
     "8组×4队为经典结构。",
     "32队,1998,法国,扩军", "入门", "world_cup", "history"),
    ("会员国基础", "谁能参加世界杯?", "FIFA members",
     "仅限国际足联正式会员协会派国家队参赛。",
     "非会员或被停权协会不得参赛。",
     "会员国,协会,国家队,资格", "入门", "both", "history"),
    ("赛事定位", "世界杯在足球地位?", "flagship event",
     "世界杯是男子国家队层面最高荣誉赛事之一。",
     "与各大洲国家杯、洲际俱乐部赛层级不同。",
     "旗舰,国家队,荣誉,地位", "入门", "world_cup", "history"),
    ("女子世界杯", "女子世界杯何时创办?", "Women World Cup",
     "女子世界杯1991年创办，规程与男子赛历独立。",
     "同属FIFA主办但文件与名额体系分开。",
     "女子,1991,独立,规程", "入门", "both", "history"),
    ("联合会杯", "联合会杯与世界杯?", "Confederations Cup",
     "联合会杯曾为世界杯前哨赛，2017年后停办。",
     "不再作为世界杯主办国测试赛固定环节。",
     "联合会杯,停办,前哨,历史", "进阶", "world_cup", "history"),
    ("洲际归属", "世界杯与六大洲?", "six confederations",
     "预选赛按亚足联、非足联、中北美、南美、大洋洲、欧足联划分。",
     "名额分配由FIFA理事会决议。",
     "六大洲,预选赛,名额,分配", "入门", "both", "history"),
    ("商标权属", "世界杯标志归谁?", "WC trademarks",
     "世界杯名称、会徽等知识产权归国际足联所有。",
     "主办国组委会依授权使用视觉系统。",
     "商标,FIFA,会徽,知识产权", "入门", "world_cup", "history"),
    ("收入用途", "世界杯收入去向?", "FIFA revenue",
     "赛事收入主要用于全球足球发展、青训与足协支持项目。",
     "具体分配依FIFA财务与治理规则。",
     "收入,发展,青训,FIFA", "进阶", "world_cup", "history"),
    ("第22届", "2022年是第几届?", "Qatar 2022 edition",
     "卡塔尔2022年为男子世界杯第22届。",
     "因主办国在11-12月举办亦称冬赛届。",
     "第22届,2022,卡塔尔,届次", "入门", "world_cup", "history"),
    ("第23届", "2026年是第几届?", "2026 edition number",
     "美加墨2026年为男子世界杯第23届。",
     "首次48队、三国联合主办。",
     "第23届,2026,48队,联合主办", "入门", "world_cup", "history"),
    ("抵制历史", "世界杯有抵制参赛吗?", "boycott history",
     "历史上部分届次出现退赛或抵制，影响参赛队数与分组。",
     "具体届次以当届报名名单为准。",
     "抵制,退赛,历史,参赛", "进阶", "world_cup", "history"),
    ("政治影响", "世界杯与政治?", "politics and WC",
     "FIFA章程强调政治非干预，但主办与外交仍常引发讨论。",
     "竞赛规程本身不处理双边关系。",
     "政治,主办,外交,章程", "进阶", "world_cup", "history"),
    ("业余时代", "早期世界杯职业化?", "amateur to pro",
     "早期对职业球员有限制，1950年代后职业球员全面参赛。",
     "标志现代足球与世界杯商业化发展。",
     "职业化,早期,限制,历史", "进阶", "world_cup", "history"),
    ("转播开端", "世界杯何时全球转播?", "TV history",
     "1954年起电视转播扩大，推动赛事全球影响力。",
     "媒体权现为FIFA核心商业资产之一。",
     "转播,电视,1954,媒体", "入门", "world_cup", "history"),
    ("吉祥物传统", "世界杯吉祥物何时起?", "mascot tradition",
     "1966年英格兰世界杯推出威利，形成长期营销传统。",
     "吉祥物属品牌活动，非竞赛规则。",
     "吉祥物,1966,品牌,传统", "入门", "world_cup", "history"),
    ("官方用球", "世界杯官方用球传统?", "match ball tradition",
     "每届发布官方比赛用球，名称与设计成为文化符号。",
     "用球须符合国际足球协会理事会标准。",
     "用球,官方,每届,传统", "入门", "world_cup", "history"),
    ("与俱乐部赛", "世界杯是俱乐部赛吗?", "not club competition",
     "世界杯是国家队赛事，球员代表所属足协出战。",
     "与欧冠等俱乐部赛事组织主体不同。",
     "国家队,俱乐部,区别,足协", "入门", "both", "history"),
    ("规程文件", "世界杯最高规则文件?", "WC Regulations",
     "当届《FIFA World Cup Regulations》为赛事最高竞赛文件。",
     "与《足球竞赛规则》并行适用。",
     "规程,Regulations,FIFA,当届", "入门", "world_cup", "rule"),
    ("章程关系", "FIFA章程与世界杯?", "FIFA Statutes",
     "FIFA章程规定世界杯主办权、会员义务与治理结构。",
     "具体赛制细节在当届规程中展开。",
     "章程,Statutes,主办权,治理", "进阶", "both", "history"),
    ("发展计划", "世界杯与足球发展?", "development programmes",
     "FIFA通过世界杯周期资金支援基层、女足与裁判培养。",
     "与场上积分规则无直接关联。",
     "发展,基层,女足,裁判", "入门", "world_cup", "history"),
    ("公平竞赛", "公平竞赛奖何时设立?", "Fair Play award",
     "公平竞赛奖鼓励纪律优良球队，评选依当届纪律数据。",
     "属荣誉奖项，非积分规则。",
     "公平竞赛,奖项,纪律,荣誉", "入门", "world_cup", "history"),
    ("金球金靴", "世界杯个人奖项?", "Golden awards",
     "金球、金靴等奖项在赛事结束后由技术团队评选。",
     "评选标准在当届技术报告中说明。",
     "金球,金靴,评选,奖项", "入门", "both", "history"),
    ("东道主传统", "东道主自动晋级?", "host auto qualify",
     "主办国通常自动获得当届决赛圈席位，细则写入当届规程。",
     "联合主办时各国席位安排依大会决议。",
     "东道主,自动,席位,晋级", "入门", "world_cup", "rule"),
    ("揭幕战", "揭幕战传统?", "opening match",
     "东道主或FIFA指定对阵常承办开幕式与揭幕战。",
     "赛程由组委会与FIFA联合公布。",
     "揭幕战,开幕式,东道主,赛程", "入门", "world_cup", "history"),
    ("三四名赛", "季军战历史?", "third place match",
     "多数届次半决赛负者进行三四名决赛，部分届次曾取消。",
     "是否举办以当届赛程为准。",
     "季军战,三四名,半决赛,历史", "入门", "world_cup", "history"),
    ("点球大战", "世界杯点球大战史?", "penalty shootout history",
     "淘汰赛平局后点球决胜，规则与IFAB一致。",
     "1982年后在世界杯淘汰赛广泛采用。",
     "点球,淘汰赛,IFAB,历史", "入门", "world_cup", "rule"),
    ("加时历史", "世界杯加时规则史?", "extra time history",
     "淘汰赛90分钟平进入加时，仍平则点球大战。",
     "小组赛历史上均不踢加时。",
     "加时,淘汰赛,小组赛,规则", "入门", "world_cup", "rule"),
    ("VAR历史", "世界杯何时用VAR?", "VAR at WC",
     "2018年俄罗斯世界杯决赛圈全面启用VAR。",
     "2022年起增加半自动越位辅助。",
     "VAR,2018,半自动,历史", "入门", "world_cup", "history"),
    ("换人演变", "世界杯换人名额演变?", "substitution history",
     "历史上从0到3再到5名替补出场，依当届规程执行。",
     "脑震荡换人协议近年纳入。",
     "换人,名额,演变,规程", "进阶", "world_cup", "rule"),
    ("非洲首办", "非洲何时首办世界杯?", "2010 South Africa",
     "2010年南非为非洲大陆首次主办男子世界杯。",
     "推动当地基建与足球普及项目。",
     "2010,南非,非洲,首办", "入门", "world_cup", "history"),
    ("亚洲首办", "亚洲何时首办世界杯?", "2002 Korea Japan",
     "2002年韩日合办为亚洲首次主办，亦为多东道主先例。",
     "赛程跨两国协调。",
     "2002,韩日,亚洲,合办", "入门", "world_cup", "history"),
    ("中东首办", "中东何时首办世界杯?", "2022 Qatar",
     "2022年卡塔尔为中东首次主办，赛期安排在11-12月。",
     "气候与赛程调整写入主办协议。",
     "2022,卡塔尔,中东,赛期", "入门", "world_cup", "history"),
    ("南美垄断早期", "早期世界杯谁夺冠多?", "early dominance",
     "1930至1962年冠军多由南美球队获得，欧洲后来崛起。",
     "反映足球传播与竞技格局演变。",
     "南美,欧洲,冠军,早期", "入门", "world_cup", "history"),
    ("巴西五冠", "哪队世界杯冠军最多?", "Brazil five titles",
     "巴西队五次夺冠为历史最多，意大利、德国各四次。",
     "统计截至最近一届决赛。",
     "巴西,五冠,纪录,冠军", "入门", "world_cup", "history"),
    ("新军参赛", "世界杯新面孔?", "debutants",
     "每届扩军或预选赛结果可能带来首次晋级决赛圈球队。",
     "具体名单以当届官方报名为准。",
     "新军,首秀,决赛圈,晋级", "入门", "world_cup", "history"),
    ("遗产项目", "世界杯遗产计划?", "legacy programme",
     "主办国常设场馆改造、社区足球与可持续遗产评估。",
     "属赛后社会遗产，非竞赛积分规则。",
     "遗产,场馆,社区,主办", "入门", "world_cup", "history"),
    ("未来届次", "下届世界杯哪里办?", "future hosts",
     "2026美加墨后，2030、2034等主办国由FIFA大会投票确定。",
     "具体赛制以当届公布规程为准。",
     "未来,主办,投票,FIFA", "入门", "world_cup", "history"),
]


def row(seq: int, entry: tuple) -> dict[str, str]:
    l3, q, aliases, short, detail, kw, diff = entry[:7]
    scope, fact_type, flags = "world_cup", "history", ""
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
        "category_l2": "创立与归属",
        "category_l3": l3,
        "scope": scope,
        "priority": "5",
        "question": q,
        "question_aliases": aliases,
        "answer_short": short,
        "answer_detail": detail,
        "answer_format": "definition",
        "keywords": kw,
        "tags": "赛制,创立",
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
