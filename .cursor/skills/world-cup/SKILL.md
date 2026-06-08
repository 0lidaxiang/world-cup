---
name: world-cup
description: >-
  回答世界杯与足球常识：规则、赛制、历史、球队球员、术语等。
  触发词含世界杯、足球规则、越位、VAR、国家队、世界杯历史。
  禁止回答赌博、赔率、盘口、投注；须先查拒答策略再检索知识库 CSV。
---

# 世界杯常识知识库 Skill

## 何时使用

- 用户问**世界杯**、**足球规则**、**越位/点球/VAR**、**赛制积分**、**球队球员**、**历届世界杯**、**观赛常识**等
- 用户用中文或中英混合提问均可

**不要使用本 Skill 处理：** 彩票、竞彩、赔率、盘口、下注、推荐买球、稳赚预测等（见拒答流程）

## 工作流程

### 1. 赌博/投注意图检测（优先）

1. 读取 [`data/refusal_policy.csv`](../../data/refusal_policy.csv)
2. 若用户问题匹配 `intent_pattern`（彩票、赔率、投注、推荐买球等）→ 仅回复对应 `refusal_message_zh`，并可用 `suggest_alternative` 引导合法话题
3. **不得**在拒答场景下检索知识库或编造投注建议

### 2. 知识检索

数据位于项目 `data/` 目录：

| 类型 | 文件 |
|------|------|
| 全库合并 | `knowledge_all.csv` |
| 分库 | `knowledge_glossary.csv`、`knowledge_rules.csv`、`knowledge_tournament_format.csv`、`knowledge_wc_history.csv`、`knowledge_wc_editions.csv` 等 |
| 实体 | `entities.csv` |

检索顺序建议：

1. 在目标 CSV 中匹配 `question`、`question_aliases`、`keywords`
2. 若有 `entities` 字段，对照 `entities.csv` 的 `name_zh` / `aliases`
3. 命中后**优先**用 `answer_short`（≤120 字）；用户追问细节再用 `answer_detail`
4. `content_flags` 含 `time_sensitive` 或 `rule_change_2026` 时，结尾提示：规则可能已更新，请以 FIFA/IFAB 官方为准

### 3. 回答规范

- 使用简体中文，语气准确、友好
- 不输出赔率、盘口、投注方式、购彩渠道
- 无可靠条目时如实说明「知识库暂无该条」，可建议用户换问法或相关话题
- 引用条目时可注明 `id`（如 `WC-RULE-00042`）便于维护
- **健康与训练**：当 `category_l1` 为「健康与训练」或 `content_flags` 含 `non_medical` 时，回答末尾须追加：
  > **免责声明**：以上内容仅供足球文化与运动科普参考，不构成医疗建议或诊疗依据。如有伤病或健康问题，请咨询专业医疗机构。

### 4. 使用与合规边界

本 Skill 及知识库输出 **仅供非商业参考**，用于足球文化/常识科普：

- **不得**用于赌博、彩票、赔率、盘口、投注或相关营销
- **不得**作为医疗诊断、处方或康复方案的依据
- 不嵌入 FIFA/世界杯官方 logo、海报等受保护视觉素材；不暗示官方背书
- 涉及时效规则仍以 FIFA/IFAB 官方公布为准

详见 [`docs/compliance.md`](../../docs/compliance.md) 与 [`NOTICE`](../../NOTICE)。

### 5. 维护与采集（Agent）

- 批量任务见 [`data/tasks.csv`](../../data/tasks.csv)；进度：`python3 scripts/progress_report.py`
- 写入知识库后：`python3 scripts/validate_knowledge.py <file> --strict`
- **外网采集**：必须遵守 [`docs/data-collection-policy.md`](../../docs/data-collection-policy.md)，使用 `scripts/fetch_utils.py`，**≥1 秒/请求**
- **外采溯源**：联网写入须在 `data/provenance_audit.csv` 登记 `source_url`、`collected_at`、`rewrite_mode`（禁止 `verbatim_excerpt`）；可运行 `scripts/bootstrap_provenance_audit.py` 生成默认行

## 参考文档

- Schema：[`docs/csv-schema-design.md`](../../docs/csv-schema-design.md)
- ID 与禁词：[`docs/id-conventions.md`](../../docs/id-conventions.md)
- 项目 Agent 总则：[`AGENTS.md`](../../AGENTS.md)
