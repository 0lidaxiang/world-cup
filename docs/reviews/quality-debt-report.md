# 质量债扫描报告

**日期**: 2026-06-05（提质后复扫）
**范围**: `data/knowledge_*.csv`（不含 `knowledge_all.csv`）
**说明**: 提质脚本 `fix_quality_debt.py` + `cleanup_question_suffixes.py` 已执行。

## 总览

| 指标 | 数值 |
|------|------|
| 分文件总行数 | 10,910 |
| 疑似占位行数 | 0 |
| 占位比例 | 0.00% |

## 各文件明细

| 文件 | 总行 | 占位行 | 比例 | 主要模式 |
|------|-----:|-------:|-----:|----------|
| knowledge_clubs_leagues.csv | 650 | 0 | 0.0% | — |
| knowledge_culture.csv | 300 | 0 | 0.0% | — |
| knowledge_discipline.csv | 300 | 0 | 0.0% | — |
| knowledge_glossary.csv | 500 | 0 | 0.0% | — |
| knowledge_health_training.csv | 200 | 0 | 0.0% | — |
| knowledge_national_teams.csv | 1200 | 0 | 0.0% | — |
| knowledge_players_coaches.csv | 1500 | 0 | 0.0% | — |
| knowledge_records_stats.csv | 800 | 0 | 0.0% | — |
| knowledge_rules.csv | 800 | 0 | 0.0% | — |
| knowledge_tactics.csv | 600 | 0 | 0.0% | — |
| knowledge_template.csv | 0 | 0 | 0.0% | — |
| knowledge_tournament_format.csv | 500 | 0 | 0.0% | — |
| knowledge_venues_tech.csv | 400 | 0 | 0.0% | — |
| knowledge_wc_editions.csv | 2060 | 0 | 0.0% | — |
| knowledge_wc_history.csv | 700 | 0 | 0.0% | — |
| knowledge_womens_wc.csv | 400 | 0 | 0.0% | — |

## 提质摘要

- 改写约 **2,600** 条占位题为真实 FAQ（保留全部 ID）
- 种子库：`scripts/quality_debt_seeds.py`、`scripts/wc_history_topic_seeds.py`
- 工具：`scripts/fix_quality_debt.py`、`scripts/cleanup_question_suffixes.py`
- 全库仍 **10910** 条，`validate --all/--batches --strict` 零 error
