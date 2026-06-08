# 世界杯常识知识库

面向世界杯与足球常识的结构化问答知识库，配合 **Cursor Agent Skill** 使用。在 Cursor 中打开本仓库后，Agent 会检索本地 CSV，给出准确、合规的中文回答。

**当前版本**：v1.0.2 · **知识条目**：10,910 条 · **实体索引**：449 条

---

## 能做什么

| 能力 | 说明 |
|------|------|
| **规则与裁判** | 越位、VAR、点球、黄牌、手球、换人等 |
| **赛制与积分** | 小组赛计分、抽签分档、扩军、预选赛 |
| **历届世界杯** | 各届冠军、名场面、主办国、赛制变化 |
| **球队与球员** | 国家队、球星、教练、俱乐部与联赛背景 |
| **术语与观赛** | 足球黑话、观赛礼仪、场地科技、女足世界杯等 |
| **赌博拒答** | 涉及赔率、盘口、投注、稳赚预测时友好拒答 |

---

## 快速开始

### 环境

- [Cursor](https://cursor.com/) 编辑器（支持 Agent 与项目级 Skill）
- Python 3 仅在你需要自行校验数据时才需要；日常问答不必运行脚本

### 使用步骤

```bash
git clone https://github.com/0lidaxiang/world-cup.git
cd world-cup
```

用 Cursor 打开该文件夹。Skill 位于 `.cursor/skills/world-cup/SKILL.md`，Agent 会自动加载。在 **Agent 对话**中用自然中文提问即可。

**示例问题：**

```
越位怎么判？
2022 年世界杯冠军是谁？
世界杯小组赛怎么算积分？
2026 世界杯有多少支球队？
```

### 复制 Skill 到其他项目（可选）

```bash
mkdir -p ~/.cursor/skills/world-cup
cp -r .cursor/skills/world-cup/* ~/.cursor/skills/world-cup/
```

个人 Skill 仍需能访问本仓库的 `data/` 目录；建议在已打开的本项目中对话，或 @ 引用相关 CSV。

---

## 仓库结构（用户向）

```
world-cup/
├── .cursor/skills/world-cup/SKILL.md   # Agent 工作流（核心）
├── data/
│   ├── knowledge_all.csv               # 全库合并
│   ├── knowledge_*.csv                 # 分类知识库
│   ├── entities.csv                    # 实体索引
│   └── refusal_policy.csv              # 赌博类拒答策略
├── docs/
│   ├── examples.md                     # FAQ 示例
│   └── compliance.md                   # 使用限制与合规说明
├── NOTICE                              # 第三方来源与商标边界
├── LICENSE                             # Apache 2.0
└── CHANGELOG.md                        # 版本更新（用户向）
```

数据维护、采集脚本与内部文档见 [`docs/maintainers/`](docs/maintainers/README.md)（Contributor / Agent 用，非必读）。

---

## 使用限制

- 仅供**非商业参考**与足球文化/常识科普
- **不得**用于赌博、投注、赔率分析或相关决策
- **不得**作为医疗诊断、处方或康复依据（健康类回答含免责声明）
- 不表示与 FIFA、各足协或任何第三方的官方授权或背书
- 涉及时效规则请以 FIFA/IFAB 官方公布为准

本库**不包含**赌博、彩票、赔率、盘口、投注内容；相关提问会被 Skill 拒答。

完整说明：[`docs/compliance.md`](docs/compliance.md) · [`NOTICE`](NOTICE)

---

## 更多资料

- FAQ 示例：[`docs/examples.md`](docs/examples.md)
- 版本记录：[`CHANGELOG.md`](CHANGELOG.md)
- 参与维护：[`docs/maintainers/README.md`](docs/maintainers/README.md)

---

## 许可证

[Apache License 2.0](LICENSE) · 第三方数据来源见 [NOTICE](NOTICE)
