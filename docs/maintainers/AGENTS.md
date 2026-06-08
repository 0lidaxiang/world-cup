# World Cup 常识知识库 — Agent 指南

本仓库由 Cursor Agent 执行 `docs/maintainers/tasks.csv` 中的采集与验收任务。以下原则 **必须** 遵守。

## 1. 外网请求限速（最高优先级之一）

- 所有脚本与 Agent 联网行为：**相邻请求间隔 ≥ 1 秒**，宁可慢、不可高频。
- Python 实现：仅通过 [`scripts/fetch_utils.py`](../scripts/fetch_utils.py) 的 `RateLimitedFetcher`（禁止 `min_interval_sec < 1.0`）。
- 细则：[`data-collection-policy.md`](data-collection-policy.md)
- Cursor 规则：`.cursor/rules/world-cup-data-collection.mdc`（`alwaysApply: true`）

## 2. 内容合规

- 禁止采集/生成赌博、彩票、赔率、盘口、投注相关内容（见 [`id-conventions.md`](id-conventions.md) §7.3）。
- 健康与训练条目须带 `content_flags=non_medical`；Skill 回答追加非医疗免责声明。
- 外网采集条目须在 [`provenance_audit.csv`](provenance_audit.csv) 登记 URL、采集时间与 `rewrite_mode`（见 [`../compliance.md`](../compliance.md)）。
- 使用前阅读 [`NOTICE`](../../NOTICE) 与 [`../compliance.md`](../compliance.md)：非商业参考、禁博彩、禁作诊疗依据。

## 3. 数据质量门禁

- **日常门禁**：单文件 `validate_knowledge.py data/knowledge_*.csv --strict`（增量批次）。
- **全库门禁**：合并后 `validate_knowledge.py data/knowledge_all.csv --strict` 或 `validate_knowledge.py --all --strict`（仅验 `knowledge_all.csv`，不与分文件重复验 ID）。
- **分文件全扫**：`validate_knowledge.py --batches --strict`（验各 `knowledge_*.csv`，排除 `knowledge_all.csv`）。
- 零 error 后方可标任务 `done`；不修改已 `done` 任务的合法 ID；不删除已有合法数据。

## 4. 任务执行

- 进度：`python3 scripts/progress_report.py --next 10`
- 完成后更新 `docs/maintainers/tasks.csv` 的 `status` 与 `actual_rows`。

## 5. 脚本目录

`scripts/` 下全部现有与未来脚本均受第 1 条约束；纯本地 `generate_*.py` 也须在 docstring 标明是否访问外网。
