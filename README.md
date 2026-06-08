# 世界杯常识知识库

面向世界杯与足球常识的结构化问答知识库，配合 **Cursor Agent Skill** 使用。Agent 会先检索本地 CSV，再给出准确、合规的中文回答。

**当前版本**：v1.0.1 · **知识条目**：10,910 条 · **实体索引**：449 条

---

## 它有什么效果

安装并在 Cursor 中打开本仓库后，你可以像问真人球迷一样提问，Agent 会按固定流程作答：

| 能力 | 说明 |
|------|------|
| **规则与裁判** | 越位、VAR、点球、黄牌、手球、换人等 |
| **赛制与积分** | 小组赛计分、抽签分档、扩军、预选赛 |
| **历届世界杯** | 各届冠军、名场面、主办国、赛制变化 |
| **球队与球员** | 国家队、球星、教练、俱乐部与联赛背景 |
| **术语与观赛** | 足球黑话、观赛礼仪、场地科技、女足世界杯等 |
| **赌博拒答** | 涉及赔率、盘口、投注、稳赚预测时友好拒答，不查知识库 |

**工作方式（Agent 自动执行）**：

1. **拒答检测** — 先读 `data/refusal_policy.csv`，命中赌博类意图则直接返回拒答话术
2. **知识检索** — 在 `data/knowledge_*.csv` 中匹配 `question`、`keywords`、`entities`
3. **组装回答** — 优先 `answer_short`（≤120 字），追问时用 `answer_detail`；涉及时效规则会提示以 FIFA/IFAB 官方为准

**实测效果**（T404 端到端测试 PASS）：

- 合法问题示例：「越位怎么判？」「2022 年世界杯冠军是谁？」→ 命中知识库，回答准确
- 拒答示例：「巴西对法国赔率多少？」→ 不给出赔率或投注建议
- 全库 `validate_knowledge.py --all --strict` 零 error，禁赌词扫描零命中

---

## 如何使用

### 环境要求

- [Cursor](https://cursor.com/) 编辑器（支持 Agent 与项目级 Skill）
- Python 3（仅维护/校验数据时需要，日常问答不必运行脚本）

### 方式一：克隆仓库后在 Cursor 中打开（推荐）

```bash
git clone https://github.com/0lidaxiang/world-cup.git
cd world-cup
```

用 Cursor 打开该文件夹。项目内已包含 Skill 定义：

```
.cursor/skills/world-cup/SKILL.md
```

Cursor Agent 会自动发现该 Skill。在 **Agent 对话**中直接提问即可，无需额外配置。

### 方式二：复制 Skill 到个人目录（多项目通用）

若希望在任意项目里都能问世界杯问题，可将 Skill 复制到个人技能目录：

```bash
mkdir -p ~/.cursor/skills/world-cup
cp -r .cursor/skills/world-cup/* ~/.cursor/skills/world-cup/
```

注意：个人 Skill 需能访问本仓库的 `data/` 目录；建议仍将本仓库克隆到本地，并在提问时 @ 引用相关 CSV，或始终在已打开的本项目中对话。

### 怎么提问

用自然中文即可，例如：

```
越位怎么判？
2022 年世界杯冠军是谁？
世界杯小组赛怎么算积分？
德国队英文叫什么？
2026 世界杯有多少支球队？
```

涉及时效或规则变更（如 2026 扩军）时，回答会标注「以官方最新公布为准」。

**不要期待它回答**：彩票、竞彩、赔率、盘口、下注推荐等——这类问题会被拒答。

---

## 仓库结构

```
world-cup/
├── .cursor/skills/world-cup/SKILL.md   # Agent 工作流说明（核心）
├── data/
│   ├── knowledge_all.csv               # 全库合并（10,910 条）
│   ├── knowledge_rules.csv             # 规则与裁判
│   ├── knowledge_glossary.csv          # 术语
│   ├── knowledge_wc_editions.csv       # 历届世界杯
│   ├── entities.csv                    # 球队/赛事等实体
│   └── refusal_policy.csv              # 赌博类拒答策略
├── docs/
│   ├── examples.md                     # 50 组 FAQ 示例
│   ├── skill-retrieval-guide.md        # 检索逻辑说明
│   └── csv-schema-design.md            # 数据字段设计
├── scripts/                            # 校验与维护脚本
├── AGENTS.md                           # 数据采集 Agent 规范
└── CHANGELOG.md                        # 版本记录
```

---

## 维护者常用命令

```bash
# 查看采集进度
python3 scripts/progress_report.py

# 校验全库（发布前）
python3 scripts/validate_knowledge.py --all --strict

# 校验各分库
python3 scripts/validate_knowledge.py --batches --strict
```

外网采集须遵守 `docs/data-collection-policy.md`，脚本联网间隔 ≥ 1 秒。

---

## 内容合规

本知识库 **不包含** 赌博、彩票、赔率、盘口、投注相关内容。Skill 层对相应用户意图单独拒答。详见 `docs/id-conventions.md`。

---

## 许可证

见 [LICENSE](LICENSE)。

## 相关链接

- 检索参考：`docs/skill-retrieval-guide.md`
- FAQ 示例：`docs/examples.md`
- 拒答测试用例：`docs/refusal-testcases.md`
