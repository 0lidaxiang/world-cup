# Changelog

## v1.0.1 — 2026-06-05

### 修复

- 补全 Phase 10 战术缺额：`knowledge_tactics.csv` 新增 T232 补遗战术 50 条（WC-TACT-00551–00600），总量 **600** 条，T231 review PASS
- 全库合并条目更新为 **10,910** 条（+50）
- `validate_knowledge.py --all` 改为仅验 `knowledge_all.csv`；新增 `--batches` 验分文件（排除合并库，避免 duplicate id 误报）
- 同步 `tasks.csv`：`actual_rows` 与 CSV 实计对齐（T148/T149 列错位、T232/T256 补遗批次、T500=10910）
- `progress_report.py` 知识进度仅统计分文件 `data` 任务，排除 `knowledge_all.csv` 合并任务重复计数

### 复验（2026-06-05）

- **T503**：`scripts/review_t503.py`（seed=42）对 `knowledge_all.csv` 抽检 500 条，全库 **10,910** 条，禁赌词零命中，报告见 `docs/reviews/T503-full-sample-review.md`
- **T404**：Skill 端到端复验通过，全库 **10,910** 条、`entities.csv` **449** 条，报告见 `docs/reviews/T404-skill-e2e-test.md`

### 质量提质（2026-06-05）

- 新增 `scripts/quality_debt_seeds.py`、`scripts/fix_quality_debt.py`、`scripts/cleanup_question_suffixes.py`
- 批量改写 culture/discipline/health/records/venues/womens/wc_history 占位题 **~2,600** 条为真实 FAQ，占位比例由 **21%** 降至 **<0.1%**
- 报告见 `docs/reviews/quality-debt-report.md`

## v1.0.0 — 2026-06-05

### 发布说明

世界杯足球常识知识库 v1.0.0 正式发布。

- 全库合并条目：**10,860** 条（目标 ≥10,000）
- 新增 Phase 1 实体扩展（T016–T018）
- 新增 Phase 10–16 知识批次：战术、纪录统计、裁判纪律、场地科技、女足、文化观赛、健康训练
- 全库 strict 校验零 error
- 禁赌词扫描零命中

### 数据文件

| Phase | 文件 | 条数 |
|-------|------|-----:|
| 战术与位置 | knowledge_tactics.csv | 600 |
| 纪录与统计 | knowledge_records_stats.csv | 800 |
| 裁判与纪律 | knowledge_discipline.csv | 300 |
| 场地装备与科技 | knowledge_venues_tech.csv | 400 |
| 女子世界杯 | knowledge_womens_wc.csv | 400 |
| 足球文化与观赛 | knowledge_culture.csv | 300 |
| 健康与训练 | knowledge_health_training.csv | 200 |

