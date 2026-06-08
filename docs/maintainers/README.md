# 维护者文档

本目录存放**数据采集、质量验收与 Agent 工作流**相关文档，面向 Contributor 与 Cursor Agent。**普通使用者无需阅读**；请从根目录 [README](../../README.md) 与 [Skill](../../.cursor/skills/world-cup/SKILL.md) 开始。

---

## 目录说明

| 文件 / 目录 | 用途 |
|-------------|------|
| [AGENTS.md](AGENTS.md) | Agent 采集总则与门禁 |
| [tasks.csv](tasks.csv) | 235 项任务台账（status / actual_rows） |
| [task-plan.md](task-plan.md) | 分阶段计划与里程碑 |
| [csv-schema-design.md](csv-schema-design.md) | 知识库 26 列 Schema |
| [id-conventions.md](id-conventions.md) | ID 规则与禁赌词 |
| [data-collection-policy.md](data-collection-policy.md) | 外网限速与抓取 SOP |
| [skill-retrieval-guide.md](skill-retrieval-guide.md) | Skill 检索逻辑详解 |
| [refusal-testcases.md](refusal-testcases.md) | 拒答 QA 用例 |
| [provenance_audit.csv](provenance_audit.csv) | 外采溯源旁路表 |
| [reviews/](reviews/) | 批次抽检与 e2e 测试报告 |
| [batches/archive/](batches/archive/) | 历史批次快照 |
| [CHANGELOG-internal.md](CHANGELOG-internal.md) | 内部详细变更记录 |

---

## 常用命令

```bash
# 任务进度
python3 scripts/progress_report.py --next 10

# 校验单文件 / 全库
python3 scripts/validate_knowledge.py data/knowledge_glossary.csv --strict
python3 scripts/validate_knowledge.py --all --strict

# 合并全库
python3 scripts/merge_batches.py --build-all

# 生成默认溯源行
python3 scripts/bootstrap_provenance_audit.py

# robots.txt 抽检（联网，≥1s/请求）
python3 scripts/audit_fetch_compliance.py
```

脚本目录：[`scripts/`](../../scripts/)（含 `generate_*`、`review_*`、`validate_knowledge.py` 等）。

---

## 对外文档（用户向）

- [README](../../README.md)
- [CHANGELOG](../../CHANGELOG.md)
- [docs/compliance.md](../compliance.md)
- [docs/examples.md](../examples.md)
- [NOTICE](../../NOTICE)
