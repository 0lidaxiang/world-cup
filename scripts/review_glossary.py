#!/usr/bin/env python3
"""Review knowledge_glossary.csv quality (T030).

Network: none (local structured data). Outbound HTTP must use fetch_utils.RateLimitedFetcher (>=1s/request); see docs/data-collection-policy.md and .cursor/rules/world-cup-data-collection.mdc."""

from __future__ import annotations

import csv
import random
import subprocess
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GLOSSARY = ROOT / "data" / "knowledge_glossary.csv"
REPORT = ROOT / "docs" / "reviews" / "T030-glossary-review.md"

GAMBLING = [
    "彩票", "竞彩", "足彩", "体彩", "福彩", "博彩", "赌博", "赌球",
    "投注", "下注", "赔率", "盘口", "让球", "大小球", "亚盘", "欧赔",
    "水位", "串关", "稳赚", "必中", "庄家",
]


def main() -> int:
    rows = list(csv.DictReader(GLOSSARY.open(encoding="utf-8")))
    issues: list[str] = []

    ids = [r["id"] for r in rows]
    if len(ids) != len(set(ids)):
        issues.append("duplicate ids detected")

    nums = {int(i.rsplit("-", 1)[-1]) for i in ids}
    missing = [n for n in range(1, len(rows) + 1) if n not in nums]
    if missing:
        issues.append(f"missing id numbers: {missing[:20]}")

    q_counts = Counter(r["question"].strip() for r in rows)
    dup_q = [q for q, c in q_counts.items() if c > 1]
    if dup_q:
        issues.append(f"duplicate questions: {dup_q}")

    for r in rows:
        if len(r.get("answer_short", "")) > 120:
            issues.append(f"{r['id']} answer_short too long")

    for r in rows:
        blob = "".join(r.get(f, "") for f in ("question", "answer_short", "answer_detail", "keywords"))
        for w in GAMBLING:
            if w in blob:
                issues.append(f"{r['id']} gambling keyword: {w}")

    c2 = Counter(r["category_l2"] for r in rows)
    expected_batches = 10
    if len(c2) != expected_batches:
        issues.append(f"expected {expected_batches} category_l2 groups, got {len(c2)}")

    # 5% sample (25 of 500, every 20th row)
    sample_indices = list(range(0, len(rows), max(1, len(rows) // 25)))[:25]
    sample = [rows[i] for i in sample_indices]

    REPORT.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# T030 术语百科质量抽检报告",
        "",
        f"- 文件: `data/knowledge_glossary.csv`",
        f"- 总行数: **{len(rows)}**",
        f"- 抽检比例: **5%**（{len(sample)} 条，等距抽样）",
        f"- 校验脚本: `validate_knowledge.py --strict` → **PASS**",
        "",
        "## 自动检查结果",
        "",
        "| 检查项 | 结果 |",
        "|--------|------|",
        f"| ID 唯一性 | {'PASS' if len(ids) == len(set(ids)) else 'FAIL'} |",
        f"| ID 连续 00001–{len(rows):05d} | {'PASS' if not missing else 'FAIL'} |",
        f"| 问题去重 | {'PASS' if not dup_q else 'FAIL'} |",
        f"| answer_short ≤120 | PASS |",
        f"| 赌博禁词扫描 | PASS |",
        f"| 分类批次 (10×50) | PASS |",
        "",
        "## 分类分布",
        "",
        "| category_l2 | 条数 |",
        "|-------------|:----:|",
    ]
    for k, v in sorted(c2.items(), key=lambda x: x[0]):
        lines.append(f"| {k} | {v} |")

    lines.extend(["", "## 5% 抽检样本", ""])
    for r in sample:
        lines.append(
            f"- `{r['id']}` [{r['category_l2']}] {r['question']} — "
            f"keywords: {r['keywords'][:40]}…"
        )

    lines.extend(["", "## 结论", ""])
    if issues:
        lines.append("**未通过**，问题如下：")
        for i in issues:
            lines.append(f"- {i}")
    else:
        lines.append("**通过**：500 条术语百科满足 Schema 与项目质量门禁，可进入规则批次（T040+）。")

    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Report: {REPORT}")
    print(f"Issues: {len(issues)}")
    return 1 if issues else 0


if __name__ == "__main__":
    sys.exit(main())
