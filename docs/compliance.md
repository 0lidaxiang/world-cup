# 合规与法律风险说明

> 版本：v1.0 · 面向维护者与 Skill 使用者 · **非法律意见**

本文档汇总本知识库的常见合规边界与可执行加强措施，与 [`NOTICE`](../NOTICE)、[`data-collection-policy.md`](data-collection-policy.md) 配套使用。

---

## 一、风险分级（摘要）

| 级别 | 领域 | 说明 |
|------|------|------|
| **高** | 版权归属与授权边界 | `source_ref` 指向 FIFA/IFAB 等官方资料是常见做法；若**逐字复写**或保留大量原文而非事实重述，仍可能触及著作权或数据库权争议。 |
| **中** | 商标/品牌边界 | 当前为事实描述，未嵌入 logo/海报/图像；须避免误导性使用 FIFA、World Cup 标识或视觉素材。 |
| **中** | 外网抓取合规 | 文档已设限速；实际执行若并发/绕过源站限制，可能面临访问规则争议或平台处罚。 |
| **中低** | 健康建议边界 | 健康训练条目为科普；若被当作医疗/诊疗建议使用，存在误导风险，须加注免责声明。 |
| **低** | 数据质量误导 | 错误事实本身未必构成侵权，但在敏感场景可能触发监管或名誉风险。 |

---

## 二、使用限制（Skill / 下游应用）

**本知识库及 Skill 输出仅供：**

- 非商业参考与足球文化/常识科普
- 个人或内部学习、问答辅助

**不得用于：**

- 赌博、彩票、赔率、盘口、投注决策或相关营销
- 医疗诊断、处方、康复方案替代专业医师意见
- 暗示与 FIFA、各足协、球员/俱乐部的官方背书或商业授权

Skill 层已在 [`refusal_policy.csv`](../data/refusal_policy.csv) 对赌博类意图拒答；健康类命中 `content_flags` 含 `non_medical` 或 `category_l1=健康与训练` 时须追加免责声明（见 Skill 文档）。

---

## 三、外采条目溯源（不改主表 26 列）

主表保持 [`csv-schema-design.md`](csv-schema-design.md) 定义不变。凡通过外网抓取或引用特定 URL 的条目，**额外**在旁路表 `data/provenance_audit.csv` 登记：

| 列名 | 必填 | 说明 |
|------|:----:|------|
| `knowledge_id` | ✓ | 对应主表 `id`，如 `WC-RULE-00042` |
| `source_url` | | 采集时访问的 URL（无 URL 则留空并填 `notes`） |
| `collected_at` | ✓ | 采集日期 ISO `YYYY-MM-DD` |
| `rewrite_mode` | ✓ | `local_structured` / `fact_restated` / `verbatim_excerpt`（**禁止**将 `verbatim_excerpt` 写入生产库） |
| `fetch_method` | | `none` / `rate_limited_script` / `agent_manual` |
| `notes` | | 人工备注，如「IFAB 2024/25 Law 11 事实重述」 |

### 约定

- 当前 v1 批次生成脚本为**本地结构化写入**（`fetch_method=none`，`rewrite_mode=local_structured`），可通过 `scripts/bootstrap_provenance_audit.py` 批量生成默认溯源行。
- **今后**任何联网写入必须在合并前补全对应 `provenance_audit` 行，且 `rewrite_mode` 不得为 `verbatim_excerpt`。
- 主表 `content_flags` 可叠加 `external_fetch`、`fact_restated` 便于 Skill 与校验识别。

---

## 四、健康类免责声明（统一文案）

回答健康与训练类问题时，在正文末尾追加（Skill 自动或人工一致使用）：

> **免责声明**：以上内容仅供足球文化与运动科普参考，不构成医疗建议或诊疗依据。如有伤病或健康问题，请咨询专业医疗机构。

主表健康条目应带 `content_flags=non_medical`（可与其它 flag 逗号并列）。

---

## 五、商标与视觉素材

- 不在 CSV 或 Skill 回答中嵌入 FIFA/世界杯官方 logo、吉祥物官方美术、赛事海报等受保护视觉素材。
- 文字中可客观提及「FIFA 世界杯」「IFAB 规则」等名称作事实描述，不暗示官方合作或授权。

---

## 六、外网抓取抽检（robots.txt 快照）

定期（建议每月或大规模采集前）运行：

```bash
python3 scripts/audit_fetch_compliance.py
```

脚本将：

1. 对常见数据源域名串行请求 `robots.txt`（间隔 ≥ 1 秒，使用 `RateLimitedFetcher`）
2. 将快照写入 `logs/compliance/robots_snapshot_<timestamp>.txt`
3. 在 stdout 输出摘要，便于人工判断是否允许公开抓取路径

详见 [`data-collection-policy.md`](data-collection-policy.md)。

---

## 七、相关文件

| 文件 | 用途 |
|------|------|
| [`NOTICE`](../NOTICE) | Apache 2.0 第三方来源与使用限制声明 |
| [`LICENSE`](../LICENSE) | Apache License 2.0 |
| [`data/provenance_audit.csv`](../data/provenance_audit.csv) | 外采/溯源旁路表 |
| [`scripts/audit_fetch_compliance.py`](../scripts/audit_fetch_compliance.py) | robots.txt 抽检 |
| [`scripts/bootstrap_provenance_audit.py`](../scripts/bootstrap_provenance_audit.py) | 从主库生成默认溯源行 |
| [`.cursor/skills/world-cup/SKILL.md`](../.cursor/skills/world-cup/SKILL.md) | 回答层合规流程 |
