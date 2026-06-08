#!/usr/bin/env python3
"""Generate T028 glossary batch: 50 equipment & pitch terms (append).

Network: none (local structured data). Outbound HTTP must use fetch_utils.RateLimitedFetcher (>=1s/request); see docs/maintainers/data-collection-policy.md and .cursor/rules/world-cup-data-collection.mdc."""

from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUTPUT = ROOT / "data" / "knowledge_glossary.csv"
START_ID = 401

COLUMNS = [
    "id", "category_l1", "category_l2", "category_l3", "scope", "priority",
    "question", "question_aliases", "answer_short", "answer_detail", "answer_format",
    "keywords", "tags", "entities", "related_ids", "difficulty",
    "era_start", "era_end", "region", "language", "fact_type", "confidence",
    "source_type", "source_ref", "content_flags", "updated_at",
]

ENTRIES = [
    ("比赛用球", "世界杯比赛用球规格?", "足球规格|official ball",
     "世界杯用球须符合IFAB与FIFA标准，圆周、重量、气压在规则允许范围内。",
     "每届世界杯阿迪达斯等赞助商发布专属用球。",
     "比赛用球,足球,规格,FIFA", "入门"),
    ("球压", "足球气压多少合适?", "ball pressure|充气",
     "规则要求比赛球气压0.6–1.1大气压（约600–1100克/平方厘米），裁判赛前检查。",
     "气压影响球速与轨迹。",
     "球压,气压,足球,规则", "入门"),
    ("球门", "标准球门尺寸是多少?", "球门规格|goal size",
     "球门宽7.32米、高2.44米，门柱与横梁须同等宽度，白色为主。",
     "尺寸自19世纪规则演变后沿用至今。",
     "球门,尺寸,门柱,横梁", "入门"),
    ("门柱", "门柱和横梁是什么?", "goalpost|crossbar",
     "门柱为两侧直立柱，横梁连接其上形成门框；球须完全越过门线平面才算进球。",
     "2014年起门线技术辅助判定。",
     "门柱,横梁,门框,进球", "入门"),
    ("球网", "球门球网作用?", "goal net|球网",
     "球网在进球后兜住皮球，便于确认进球并加快比赛重启。",
     "世界杯球场球网须符合FIFA安全与外观要求。",
     "球网,球门,进球,装备", "入门"),
    ("天然草", "世界杯为何用天然草?", "natural grass|真草",
     "天然草弹性与球员触感较好，顶级赛事首选，但对气候与维护要求高。",
     "部分场馆采用混合或可切换草皮系统。",
     "天然草,草皮,场地,维护", "入门"),
    ("人工草", "人工草皮是什么?", "artificial turf|人造草",
     "人工草皮由合成纤维制成，耐磨且受天气影响小，多用于训练或部分联赛。",
     "FIFA有人工草质量认证体系。",
     "人工草,人造草,草皮,场地", "入门"),
    ("混合草", "混合草皮是什么?", "hybrid pitch|混草",
     "天然草与人工纤维混合铺设，增强根系稳定与耐用度，世界杯部分场馆采用。",
     "卡塔尔2022部分球场使用混合草技术。",
     "混合草,草皮,世界杯,场地", "进阶"),
    ("护腿板", "护腿板必须戴吗?", "shin guards|护胫",
     "规则要求球员必须佩戴护腿板，由塑胶等材质制成，被袜子完全覆盖。",
     "裁判赛前会检查装备合规。",
     "护腿板,护胫,装备,规则", "入门"),
    ("球鞋", "足球鞋有哪些类型?", "足球鞋|cleats",
     "按场地分FG（天然草）、SG（软长钉）、AG（人工草）、TF（碎钉）、IC（室内）等。",
     "世界杯通常在天然草使用FG或SG。",
     "足球鞋,钉鞋,FG,装备", "入门"),
    ("FG钉鞋", "FG钉鞋是什么?", "Firm Ground|长钉",
     "FG适用于干燥天然草，钉长适中，提供抓地力与转向支撑。",
     "湿软场地可能改用SG更长钉。",
     "FG,钉鞋,天然草,抓地", "入门"),
    ("SG钉鞋", "SG钉鞋何时用?", "Soft Ground|软长钉",
     "SG钉较长，适用于雨后泥泞天然草，增强防滑。",
     "不当场地使用可能增加伤病风险。",
     "SG,钉鞋,湿草,防滑", "进阶"),
    ("门将手套", "门将手套作用?", "goalkeeper gloves|手套",
     "门将手套增大摩擦与保护指关节，便于扑救持球。",
     "不同品牌掌面粘性材料不同。",
     "门将手套,扑救,门将,装备", "入门"),
    ("球衣", "世界杯球衣规则?", "kit|比赛服",
     "两队球衣颜色须可区分，含号码、姓名与赞助商标识，须符合FIFA装备规定。",
     "主队通常选择主色，客队改穿备用色。",
     "球衣,比赛服,号码,世界杯", "入门"),
    ("球袜", "球袜有什么要求?", "socks|袜子",
     "球袜须完全覆盖护腿板，颜色通常与球衣配套。",
     "部分球员习惯拉低或调整球袜长度。",
     "球袜,护腿板,装备,规则", "入门"),
    ("紧身衣", "球员为何穿紧身衣?", "base layer|压缩衣",
     "紧身衣可保暖、排汗并轻微压缩肌肉，属个人偏好装备非强制。",
     "寒冷或雨天比赛更常见。",
     "紧身衣,压缩,保暖,装备", "入门"),
    ("队长袖标", "队长袖标装备规定?", "captain armband|袖标",
     "队长佩戴明显袖标以便裁判识别，须为单一明确标识。",
     "场上仅一名佩戴者被视为队长。",
     "队长袖标,袖标,队长,装备", "入门"),
    ("比赛场地", "标准足球场尺寸?", "pitch size|场地大小",
     "国际比赛场地长100–110米、宽64–75米，世界杯须在规则范围内。",
     "尺寸可在规则区间内调整。",
     "场地,尺寸,球场,规则", "入门"),
    ("中线", "中线的作用?", "halfway line|中线",
     "中线将场分为两半，开球时对方须在中圈内，中圈半径9.15米。",
     "部分庆祝与站位规则涉及中线。",
     "中线,中圈,开球,场地", "入门"),
    ("禁区线", "禁区线如何划定?", "penalty area line|禁区",
     "大禁区与小禁区用白线标出，点球点距门线11米。",
     "线宽不超过12厘米。",
     "禁区,线,点球点,场地", "入门"),
    ("角旗", "角旗是什么?", "corner flag|角旗杆",
     "四角竖立角旗，高度不低于1.5米，不可移除以免危险。",
     "角球须从角球区内开出。",
     "角旗,角球,标志,场地", "入门"),
    ("替补席", "替补席在哪里?", "team bench|替补席",
     "替补席位于场边技术区附近，替补与教练团队在此就座。",
     "世界杯球场替补席有遮阳与座位编号。",
     "替补席,替补,场边,教练", "入门"),
    ("技术区", "技术区范围?", "technical area|教练区",
     "教练与替补须在指定技术区内活动，不得随意进入比赛区域。",
     "越界可能被裁判警告。",
     "技术区,教练,场边,规则", "入门"),
    ("球员通道", "球员通道是什么?", "player tunnel|隧道",
     "连接更衣室与球场的通道，两队出场时在此列队，世界杯常有儿童球童陪同。",
     "决赛通道布置更具仪式感。",
     "球员通道,出场,隧道,仪式", "入门"),
    ("看台", "世界杯看台是什么?", "stands|观众席",
     "球场观众坐席区域，容量因场馆而异，世界杯须满足FIFA容量与安全标准。",
     "2022卡塔尔部分球场容量较常规世界杯偏小。",
     "看台,观众,容量,球场", "入门"),
    ("球场容量", "世界杯球场容量要求?", "stadium capacity|坐席",
     "FIFA对世界杯比赛场馆有最低容量与安全、媒体、VIP区域等要求。",
     "决赛场馆容量通常最大。",
     "容量,球场,世界杯,标准", "进阶"),
    ("封闭球场", "封闭球场是什么?", "closed stadium|无跑道",
     "观众席贴近场边、无田径跑道的专用足球场，观赛体验更沉浸。",
     "现代世界杯场馆多为封闭球场。",
     "封闭球场,专用,足球场,观赛", "入门"),
    ("可伸缩屋顶", "球场屋顶有什么作用?", "retractable roof|屋顶",
     "可开关屋顶控制日照、温度与降水影响，2026部分场馆计划采用。",
     "完全封闭时需注意通风与草皮光照。",
     "屋顶,可伸缩,场馆,天气", "进阶"),
    ("灯光系统", "夜场比赛照明要求?", "floodlights|灯光",
     "职业比赛需均匀照明满足转播与裁判视线，FIFA有照度建议标准。",
     "世界杯小组赛与淘汰赛常安排晚间场。",
     "灯光,夜场,照明,转播", "进阶"),
    ("转播机位", "世界杯转播机位?", "broadcast camera|摄像机",
     "球场预设主机位、战术机位、门后机位及无人机等，服务全球转播。",
     "VAR也依赖多路转播信号。",
     "转播,机位,摄像机,世界杯", "进阶"),
    ("VAR室", "VAR操作室在哪?", "VAR room|视频室",
     "通常位于球场内或附近，VAR与AVAR通过多路镜头复核判罚。",
     "与转播中心信号互联。",
     "VAR室,视频,复核,球场", "进阶"),
    ("医疗室", "球场医疗设施?", "medical room|医疗",
     "世界杯球场须配备医疗室、担架及紧急通道，满足球员急救需求。",
     "脑震荡协议要求场边评估。",
     "医疗,急救,球场,设施", "进阶"),
    ("浇水", "赛前为何浇水?", "pitch watering|洒水",
     "适度浇水可加快传球速度、减少扬尘并保护草皮，由场地管理员执行。",
     "过度浇水可能导致球速异常。",
     "浇水,草皮,维护,场地", "进阶"),
    ("草皮维护", "世界杯草皮如何维护?", "groundkeeping|草坪",
     "赛前修剪、滚压、浇水与补草，确保平整度与弹性符合职业标准。",
     "多场馆共用时会增加维护难度。",
     "草皮,维护,草坪,世界杯", "进阶"),
    ("海拔", "高海拔对比赛影响?", "altitude|高原",
     "高海拔空气稀薄，球员体能与球速受影响，需提前适应。",
     "墨西哥城、基多等场地曾引发讨论。",
     "海拔,高原,体能,环境", "进阶"),
    ("高温", "高温比赛如何应对?", "heat|高温",
     "裁判可设置补水暂停，比赛时间避开正午，球员需注意补水与降温。",
     "卡塔尔2022改为冬季举办，主要因夏季高温不适宜比赛。",
     "高温,补水,气候,世界杯", "进阶"),
    ("降水", "雨天比赛影响?", "rain|雨天",
     "雨天球速加快、场地湿滑，铲球与传球失误可能增多，常换SG钉鞋。",
     "裁判判断场地是否可比赛。",
     "降水,雨天,场地,比赛", "入门"),
    ("世界杯用球命名", "世界杯用球如何命名?", "Al Rihla|Telstar|用球名",
     "赞助商常为每届用球取当地文化相关名称，如2022阿尔里哈、2018电视之星18。",
     "用球设计也服务转播识别。",
     "用球,命名,阿迪达斯,世界杯", "入门"),
    ("备用球", "比赛备用球规则?", "spare ball|备用足球",
     "裁判可准备多颗比赛用球，出界快速时边线附近放置备用球以加快重启。",
     "减少比赛中断时间。",
     "备用球,足球,裁判,比赛", "进阶"),
    ("电子记分", "球场记分牌作用?", "scoreboard|记分",
     "显示比分、时间、补时与换人信息，第四官员补时与记分同步。",
     "现代球场多为LED大屏。",
     "记分牌,比分,补时,球场", "入门"),
    ("广告牌", "场边广告牌是什么?", "LED boards|广告",
     "围绕场边的LED或静态广告，世界杯为FIFA全球合作伙伴保留位。",
     "转播画面常包含场边广告。",
     "广告牌,LED,赞助,场边", "入门"),
    ("球童", "球童做什么?", "ball kid|小球童",
     "儿童球童协助捡球、递球，世界杯出场仪式常伴球员入场。",
     "来自本地足球推广项目。",
     "球童,捡球,仪式,世界杯", "入门"),
    ("装备检查", "赛前装备检查什么?", "equipment check|检查",
     "裁判检查护腿板、钉鞋危险件、球衣颜色冲突与首饰等违规物品。",
     "不符合者可被要求更换或离场。",
     "装备检查,护腿板,裁判,规则", "入门"),
    ("颜色冲突", "球衣颜色冲突怎么办?", "kit clash|颜色相近",
     "两队球衣过于相近时，客队或指定一方改穿备用球衣以保证区分。",
     "裁判赛前与两队确认。",
     "球衣,颜色,备用,区分", "入门"),
    ("训练场", "世界杯训练场是什么?", "training pitch|训练基地",
     "各队驻地附近训练场，草皮与设施尽量接近比赛场标准。",
     "训练场位置影响球队后勤安排。",
     "训练场,训练,基地,世界杯", "入门"),
    ("混合赛区", "世界杯赛区驻地?", "team base camp|大本营",
     "球队选择城市作为大本营，下榻酒店并固定使用当地训练场。",
     "2026美加墨跨度大，旅行距离更长。",
     "大本营,驻地,训练,赛区", "进阶"),
    ("FIFA球场标准", "FIFA球场质量标准?", "FIFA Quality Pro|场地认证",
     "FIFA对职业比赛场地有质量分级与测试，世界杯场馆须达到最高要求。",
     "包括平整度、反弹、滚动等指标。",
     "FIFA,场地标准,认证,质量", "专业"),
    ("门线技术", "门线技术装备?", "GLT sensors|门线",
     "门线附近传感器或摄像系统判断球是否完全过线，结果仅传裁判设备。",
     "2014巴西世界杯起全面使用。",
     "门线技术,GLT,进球,装备", "进阶"),
    ("喷雾泡沫", "任意球泡沫是什么?", "vanishing foam|标记",
     "裁判用可消失泡沫标记球位与人墙线，10秒左右消散。",
     "2014世界杯起普及。",
     "喷雾,泡沫,任意球,裁判", "入门"),
    ("冷天气装备", "寒冷比赛允许什么?", "cold weather|冬装",
     "球员可戴手套、长袖紧身衣等，须仍符合球衣与号码可见规则。",
     "2018俄罗斯部分场次气温较低。",
     "寒冷,保暖,装备,手套", "入门"),
]


def row(seq: int, entry: tuple) -> dict[str, str]:
    l3, q, aliases, short, detail, kw, diff = entry
    return {
        "id": f"WC-GLOS-{seq:05d}",
        "category_l1": "术语与百科",
        "category_l2": "装备与场地",
        "category_l3": l3,
        "scope": "both",
        "priority": "3",
        "question": q,
        "question_aliases": aliases,
        "answer_short": short,
        "answer_detail": detail,
        "answer_format": "definition",
        "keywords": kw,
        "tags": "装备与场地,术语",
        "entities": "",
        "related_ids": "",
        "difficulty": diff,
        "era_start": "",
        "era_end": "",
        "region": "全球",
        "language": "zh-CN",
        "fact_type": "term",
        "confidence": "official",
        "source_type": "IFAB",
        "source_ref": "IFAB Laws of the Game; FIFA Stadium & Equipment Guidelines",
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
