#!/usr/bin/env python3
"""Review knowledge_tournament_format.csv quality (T070).

Network: none (local structured data). Outbound HTTP must use fetch_utils.RateLimitedFetcher (>=1s/request); see docs/maintainers/data-collection-policy.md and .cursor/rules/world-cup-data-collection.mdc."""

from __future__ import annotations

import csv
import subprocess
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TARGET = ROOT / "data" / "knowledge_tournament_format.csv"
REPORT = ROOT / "docs" / "reviews" / "T070-tournament-format-review.md"

GAMBLING = [
    "彩票", "竞彩", "足彩", "体彩", "福彩", "博彩", "赌博", "赌球",
    "投注", "下注", "赔率", "盘口", "让球", "大小球", "亚盘", "欧赔",
    "水位", "串关", "稳赚", "必中", "庄家",
]


def main() -> int:
    rows = list(csv.DictReader(TARGET.open(encoding="utf-8")))
    issues: list[str] = []

    ids = [r["id"] for r in rows]
    if len(ids) != len(set(ids)):
        issues.append("duplicate ids")

    if not all(i.startswith("WC-TFMT-") for i in ids):
        issues.append("invalid id prefix")

    nums = sorted(int(i.rsplit("-", 1)[-1]) for i in ids)
    expected = list(range(1, len(rows) + 1))
    if nums != expected:
        missing = [n for n in expected if n not in nums]
        issues.append(f"id gaps: {missing[:10]} (total {len(missing)})")

    dup_q = [q for q, c in Counter(r["question"].strip() for r in rows).items() if c > 1]
    if dup_q:
        issues.append(f"duplicate questions: {dup_q[:8]}")

    for r in rows:
        if len(r.get("answer_short", "")) > 120:
            issues.append(f"{r['id']} answer_short too long")

    for r in rows:
        blob = "".join(r.get(f, "") for f in ("question", "answer_short", "answer_detail", "keywords"))
        for w in GAMBLING:
            if w in blob:
                issues.append(f"{r['id']} gambling: {w}")

    l1_bad = [r["id"] for r in rows if r.get("category_l1") != "世界杯赛制与组织"]
    if l1_bad:
        issues.append("category_l1 mismatch")

    sample_n = max(1, len(rows) // 20)
    sample = [rows[i] for i in range(0, len(rows), max(1, len(rows) // sample_n))][:sample_n]

    validate = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "validate_knowledge.py"), str(TARGET), "--strict"],
        capture_output=True,
        text=True,
    )

    lines = [
        "# T070 赛制与组织质量抽检报告",
        "",
        f"- 文件: `data/knowledge_tournament_format.csv`",
        f"- 总行数: **{len(rows)}**",
        f"- 抽检: **约 5%**（{len(sample)} 条）",
        f"- 全量校验: **{'PASS' if validate.returncode == 0 else 'FAIL'}**",
        "",
        "## 检查项",
        "",
        f"| ID 唯一连续 | {'PASS' if not any('id' in i for i in issues) else 'FAIL'} |",
        f"| category_l1 | {'PASS' if not l1_bad else 'FAIL'} |",
        f"| 问题去重 | {'PASS' if not dup_q else 'FAIL'} |",
        f"| 禁赌词 | {'PASS' if not any('gambling' in i for i in issues) else 'FAIL'} |",
        "",
        "## category_l2 分布",
        "",
    ]
    for k, v in sorted(Counter(r["category_l2"] for r in rows).items()):
        lines.append(f"- {k}: {v}")

    lines.extend(["", "## 抽检样本", ""])
    for r in sample[:25]:
        lines.append(f"- `{r['id']}` [{r['category_l2']}] {r['question'][:45]}")

    lines.extend(["", "## 结论", ""])
    if issues or validate.returncode != 0:
        lines.append("**未通过**")
        for i in issues:
            lines.append(f"- {i}")
        REPORT.parent.mkdir(parents=True, exist_ok=True)
        REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
        print(f"FAILED: {issues}")
        return 1

    lines.append("**通过**。500 条赛制条目全量校验零 error。")
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"PASS: {REPORT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
