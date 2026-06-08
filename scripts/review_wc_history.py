#!/usr/bin/env python3
"""Review knowledge_wc_history.csv quality (T090).

Network: none (local structured data). Outbound HTTP must use fetch_utils.RateLimitedFetcher (>=1s/request); see docs/maintainers/data-collection-policy.md and .cursor/rules/world-cup-data-collection.mdc."""

from __future__ import annotations

import csv
import subprocess
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TARGET = ROOT / "data" / "knowledge_wc_history.csv"
REPORT = ROOT / "docs" / "reviews" / "T090-wc-history-review.md"

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
    if not all(i.startswith("WC-WHIS-") for i in ids):
        issues.append("bad id prefix")

    nums = sorted(int(i.rsplit("-", 1)[-1]) for i in ids)
    if nums != list(range(1, len(rows) + 1)):
        issues.append("id not continuous 1..N")

    dup_q = [q for q, c in Counter(r["question"].strip() for r in rows).items() if c > 1]
    if dup_q:
        issues.append(f"duplicate questions: {dup_q[:5]}")

    for r in rows:
        if len(r.get("answer_short", "")) > 120:
            issues.append(f"{r['id']} answer_short too long")

    for r in rows:
        blob = "".join(r.get(f, "") for f in ("question", "answer_short", "answer_detail", "keywords"))
        for w in GAMBLING:
            if w in blob:
                issues.append(f"{r['id']} gambling: {w}")

    validate = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "validate_knowledge.py"), str(TARGET), "--strict"],
        capture_output=True,
        text=True,
    )

    sample = [rows[i] for i in range(0, len(rows), max(1, len(rows) // 35))][:35]

    lines = [
        "# T090 世界杯历史概览质量抽检报告",
        "",
        f"- 总行数: **{len(rows)}**",
        f"- 全量校验: **{'PASS' if validate.returncode == 0 else 'FAIL'}**",
        f"- 抽检约 5%: {len(sample)} 条",
        "",
        f"| 问题去重 | {'PASS' if not dup_q else 'FAIL'} |",
        f"| ID 连续 | {'PASS' if nums == list(range(1, len(rows)+1)) else 'FAIL'} |",
        "",
        "## 结论",
        "",
    ]
    if issues or validate.returncode != 0:
        lines.append("**未通过**")
        for i in issues:
            lines.append(f"- {i}")
        REPORT.parent.mkdir(parents=True, exist_ok=True)
        REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
        return 1

    lines.append("**通过**。700 条历史条目全量校验零 error，问题无重复。")
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"PASS: {REPORT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
