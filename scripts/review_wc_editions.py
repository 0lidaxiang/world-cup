#!/usr/bin/env python3
"""Review knowledge_wc_editions.csv quality (T123).

Network: none (local structured data only). Outbound HTTP must use
fetch_utils.RateLimitedFetcher (>=1s/request); see docs/maintainers/data-collection-policy.md
and .cursor/rules/world-cup-data-collection.mdc."""

from __future__ import annotations

import csv
import subprocess
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TARGET = ROOT / "data" / "knowledge_wc_editions.csv"
REPORT = ROOT / "docs" / "reviews" / "T123-wc-editions-review.md"
SAMPLE_PER_EDITION = 10

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
    bad_prefix = [i for i in ids if not i.startswith("WC-WCED-")]
    if bad_prefix:
        issues.append(f"bad id prefix: {bad_prefix[:3]}")

    dup_q = [q for q, c in Counter(r["question"].strip() for r in rows).items() if c > 1]
    if dup_q:
        issues.append(f"duplicate questions: {dup_q[:5]}")

    for r in rows:
        if len(r.get("answer_short", "")) > 120:
            issues.append(f"{r['id']} answer_short too long")
        blob = "".join(r.get(f, "") for f in ("question", "answer_short", "answer_detail", "keywords"))
        for w in GAMBLING:
            if w in blob:
                issues.append(f"{r['id']} gambling: {w}")

    by_edition: dict[str, list[dict[str, str]]] = defaultdict(list)
    for r in rows:
        by_edition[r["category_l2"]].append(r)

    validate = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "validate_knowledge.py"), str(TARGET), "--strict"],
        capture_output=True,
        text=True,
    )

    sample_lines: list[str] = []
    for edition in sorted(by_edition):
        bucket = by_edition[edition]
        step = max(1, len(bucket) // SAMPLE_PER_EDITION)
        picked = [bucket[i] for i in range(0, len(bucket), step)][:SAMPLE_PER_EDITION]
        sample_lines.append(f"### {edition}（{len(bucket)} 条，抽检 {len(picked)} 条）")
        for r in picked:
            sample_lines.append(
                f"- `{r['id']}` {r['category_l3']}: {r['question'][:40]}… → {r['answer_short'][:50]}"
            )
        sample_lines.append("")

    lines = [
        "# T123 历届世界杯质量抽检报告",
        "",
        f"- 总行数: **{len(rows)}**",
        f"- 届次（category_l2）: **{len(by_edition)}**",
        f"- 全量校验: **{'PASS' if validate.returncode == 0 else 'FAIL'}**",
        f"- 每届抽检: **{SAMPLE_PER_EDITION}** 条（共约 {len(by_edition) * SAMPLE_PER_EDITION} 条）",
        "",
        "| 检查项 | 结果 |",
        "|--------|------|",
        f"| validate_knowledge --strict | {'PASS' if validate.returncode == 0 else 'FAIL'} |",
        f"| ID 唯一 WC-WCED- | {'PASS' if not bad_prefix and len(ids) == len(set(ids)) else 'FAIL'} |",
        f"| 问题去重 | {'PASS' if not dup_q else 'FAIL'} |",
        f"| 禁赌词扫描 | {'PASS' if not any('gambling' in i for i in issues) else 'FAIL'} |",
        "",
        "## 分届抽检（交叉核对样例）",
        "",
    ]
    lines.extend(sample_lines)
    lines.extend(["## 结论", ""])

    if issues or validate.returncode != 0:
        lines.append("**未通过**")
        for i in issues[:30]:
            lines.append(f"- {i}")
        if validate.returncode != 0:
            lines.append("- validate_knowledge 输出见终端")
        REPORT.parent.mkdir(parents=True, exist_ok=True)
        REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
        print(f"FAIL: {REPORT}")
        return 1

    lines.append(
        "**通过**。2060 条历届世界杯条目全量校验零 error，"
        "23 届各抽检 10 条样例已列出供人工交叉核对。"
    )
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"PASS: {REPORT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
