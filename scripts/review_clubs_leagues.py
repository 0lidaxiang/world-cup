#!/usr/bin/env python3
"""Review knowledge_clubs_leagues.csv quality (T213).

Network: none (local structured data only)."""

from __future__ import annotations

import csv
import subprocess
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TARGET = ROOT / "data" / "knowledge_clubs_leagues.csv"
REPORT = ROOT / "docs" / "reviews" / "T213-clubs-leagues-review.md"
EXPECTED_ROWS = 650
SAMPLE_SIZE = 50
ID_PREFIX = "WC-CLUB-"

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
    bad_prefix = [i for i in ids if not i.startswith(ID_PREFIX)]
    if bad_prefix:
        issues.append(f"bad id prefix: {bad_prefix[:3]}")

    nums = sorted(int(i.rsplit("-", 1)[-1]) for i in ids)
    seq_ok = (
        len(rows) == EXPECTED_ROWS
        and nums
        and nums[0] == 1
        and nums[-1] == EXPECTED_ROWS
        and len(nums) == len(set(nums))
    )
    if len(rows) != EXPECTED_ROWS:
        issues.append(f"expected {EXPECTED_ROWS} rows, got {len(rows)}")
    if nums and not seq_ok:
        issues.append(f"id sequence issue: first={nums[0]}, last={nums[-1]}")

    dup_q = [q for q, c in Counter(r["question"].strip() for r in rows).items() if c > 1]
    if dup_q:
        issues.append(f"duplicate questions: {dup_q[:5]}")

    bad_l1 = [r["id"] for r in rows if r.get("category_l1") != "俱乐部与联赛"]
    if bad_l1:
        issues.append(f"bad category_l1: {bad_l1[:3]}")

    for r in rows:
        if len(r.get("answer_short", "")) > 120:
            issues.append(f"{r['id']} answer_short too long")
        kw = [k.strip() for k in r.get("keywords", "").split(",") if k.strip()]
        if len(kw) < 3:
            issues.append(f"{r['id']} keywords < 3")
        blob = "".join(r.get(f, "") for f in ("question", "answer_short", "answer_detail", "keywords"))
        for w in GAMBLING:
            if w in blob:
                issues.append(f"{r['id']} gambling: {w}")

    by_l2: dict[str, list[dict[str, str]]] = defaultdict(list)
    for r in rows:
        by_l2[r["category_l2"]].append(r)

    odd = {k: len(v) for k, v in by_l2.items() if len(v) != 50}
    if odd:
        issues.append(f"non-50 batch sizes: {list(odd.items())[:5]}")

    validate = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "validate_knowledge.py"), str(TARGET), "--strict"],
        capture_output=True,
        text=True,
    )

    step = max(1, len(rows) // SAMPLE_SIZE)
    sample = [rows[i] for i in range(0, len(rows), step)][:SAMPLE_SIZE]

    sample_lines: list[str] = []
    for r in sample:
        sample_lines.append(
            f"- `{r['id']}` [{r['category_l2']}] {r['question'][:36]}… → {r['answer_short'][:48]}"
        )

    lines = [
        "# T213 俱乐部与联赛质量抽检报告",
        "",
        f"- 文件: `data/knowledge_clubs_leagues.csv`",
        f"- 总行数: **{len(rows)}**（目标 {EXPECTED_ROWS}）",
        f"- category_l2 批次数: **{len(by_l2)}**",
        f"- 全量校验: **{'PASS' if validate.returncode == 0 else 'FAIL'}**",
        f"- 等距抽检: **{len(sample)}** 条（约 {100 * len(sample) / max(len(rows), 1):.1f}%）",
        "",
        "| 检查项 | 结果 |",
        "|--------|------|",
        f"| validate_knowledge --strict | {'PASS' if validate.returncode == 0 else 'FAIL'} |",
        f"| ID 唯一 {ID_PREFIX} | {'PASS' if not bad_prefix and len(ids) == len(set(ids)) else 'FAIL'} |",
        f"| ID 连续 00001–{EXPECTED_ROWS:05d} | {'PASS' if seq_ok else 'FAIL'} |",
        f"| category_l1 俱乐部与联赛 | {'PASS' if not bad_l1 else 'FAIL'} |",
        f"| 问题去重 | {'PASS' if not dup_q else 'FAIL'} |",
        f"| 禁赌词扫描 | {'PASS' if not any('gambling' in i for i in issues) else 'FAIL'} |",
        "",
        "## category_l2 分布",
        "",
        "| category_l2 | 条数 |",
        "|-------------|:----:|",
    ]
    for k, v in sorted(by_l2.items(), key=lambda x: x[0]):
        lines.append(f"| {k} | {len(v)} |")

    lines.extend(["", "## 等距抽检样例", ""])
    lines.extend(sample_lines)
    lines.extend(["", "## 结论", ""])

    ok = not issues and validate.returncode == 0 and len(rows) == EXPECTED_ROWS
    if ok:
        lines.append("**通过**：全量校验零 error，650 条俱乐部与联赛知识可标 T213 done。")
        code = 0
    else:
        lines.append("**未通过**")
        for i in issues[:40]:
            lines.append(f"- {i}")
        if validate.returncode != 0:
            lines.append(f"- validate 输出:\n```\n{validate.stdout[-800:]}\n```")
        code = 1

    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(REPORT)
    return code


if __name__ == "__main__":
    sys.exit(main())
