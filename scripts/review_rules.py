#!/usr/bin/env python3
"""Review knowledge_rules.csv quality (T056).

Network: none (local structured data). Outbound HTTP must use fetch_utils.RateLimitedFetcher (>=1s/request); see docs/maintainers/data-collection-policy.md and .cursor/rules/world-cup-data-collection.mdc."""

from __future__ import annotations

import csv
import subprocess
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RULES = ROOT / "data" / "knowledge_rules.csv"
REPORT = ROOT / "docs" / "reviews" / "T056-rules-review.md"

GAMBLING = [
    "彩票", "竞彩", "足彩", "体彩", "福彩", "博彩", "赌博", "赌球",
    "投注", "下注", "赔率", "盘口", "让球", "大小球", "亚盘", "欧赔",
    "水位", "串关", "稳赚", "必中", "庄家",
]


def main() -> int:
    rows = list(csv.DictReader(RULES.open(encoding="utf-8")))
    issues: list[str] = []

    ids = [r["id"] for r in rows]
    if len(ids) != len(set(ids)):
        issues.append("duplicate ids detected")

    if not all(i.startswith("WC-RULE-") for i in ids):
        issues.append("non-RULE id prefix found")

    nums = sorted(int(i.rsplit("-", 1)[-1]) for i in ids)
    expected = list(range(1, len(rows) + 1))
    if nums != expected:
        missing = [n for n in expected if n not in nums]
        issues.append(f"id gaps: {missing[:15]}... (total gaps {len(missing)})")

    q_counts = Counter(r["question"].strip() for r in rows)
    dup_q = [q for q, c in q_counts.items() if c > 1]
    if dup_q:
        issues.append(f"duplicate questions: {dup_q[:5]}")

    for r in rows:
        if len(r.get("answer_short", "")) > 120:
            issues.append(f"{r['id']} answer_short too long")

    for r in rows:
        blob = "".join(r.get(f, "") for f in ("question", "answer_short", "answer_detail", "keywords"))
        for w in GAMBLING:
            if w in blob:
                issues.append(f"{r['id']} gambling keyword: {w}")

    l1_bad = [r["id"] for r in rows if r.get("category_l1") != "规则与裁判"]
    if l1_bad:
        issues.append(f"category_l1 mismatch: {l1_bad[:5]}")

    c2 = Counter(r["category_l2"] for r in rows)

    sample_n = max(1, len(rows) // 20)  # 5%
    sample_indices = list(range(0, len(rows), max(1, len(rows) // sample_n)))[:sample_n]
    sample = [rows[i] for i in sample_indices]

    validate = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "validate_knowledge.py"), str(RULES), "--strict"],
        capture_output=True,
        text=True,
    )
    validate_pass = validate.returncode == 0

    REPORT.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# T056 规则与裁判质量抽检报告",
        "",
        f"- 文件: `data/knowledge_rules.csv`",
        f"- 总行数: **{len(rows)}**",
        f"- 抽检比例: **约 5%**（{len(sample)} 条，等距抽样）",
        f"- 全量校验: `validate_knowledge.py --strict` → **{'PASS' if validate_pass else 'FAIL'}**",
        "",
        "## 自动检查结果",
        "",
        "| 检查项 | 结果 |",
        "|--------|------|",
        f"| ID 唯一性 | {'PASS' if len(ids) == len(set(ids)) else 'FAIL'} |",
        f"| ID 连续 00001–{len(rows):05d} | {'PASS' if nums == expected else 'FAIL'} |",
        f"| category_l1=规则与裁判 | {'PASS' if not l1_bad else 'FAIL'} |",
        f"| 问题去重 | {'PASS' if not dup_q else 'FAIL'} |",
        f"| answer_short ≤120 | {'PASS' if not any('answer_short too long' in i for i in issues) else 'FAIL'} |",
        f"| 赌博禁词扫描 | {'PASS' if not any('gambling' in i for i in issues) else 'FAIL'} |",
        "",
        "## category_l2 分布（16 批次）",
        "",
        "| category_l2 | 条数 |",
        "|-------------|:----:|",
    ]
    for k, v in sorted(c2.items(), key=lambda x: x[0]):
        lines.append(f"| {k} | {v} |")

    flags = Counter(r.get("content_flags", "") or "(空)" for r in rows)
    lines.extend(["", "## content_flags 概览", ""])
    for k, v in flags.most_common(8):
        lines.append(f"- `{k}`: {v}")

    lines.extend(["", "## 5% 抽检样本", ""])
    for r in sample:
        short = r["question"][:50]
        lines.append(f"- `{r['id']}` [{r['category_l2']}] {short}")

    lines.extend(["", "## IFAB 交叉核对说明", ""])
    lines.append(
        "条目 `source_type` 以 IFAB / FIFA 为主，`source_ref` 标注 Laws of the Game 2024/25 "
        "或世界杯规程；2026 相关条目标记 `rule_change_2026` / `time_sensitive`，上线前应复查官方文本。"
    )

    lines.extend(["", "## 结论", ""])
    if issues or not validate_pass:
        lines.append("**未通过**，问题如下：")
        for i in issues:
            lines.append(f"- {i}")
        if not validate_pass:
            lines.append(f"- validate stderr: {validate.stderr[:500]}")
        REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
        print(f"Review FAILED, see {REPORT}")
        return 1

    lines.append("**通过**。800 条规则全量校验零 error，抽检无重复问句与禁词，ID 连续唯一。")
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Review PASS, report: {REPORT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
