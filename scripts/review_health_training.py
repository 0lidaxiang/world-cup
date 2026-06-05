#!/usr/bin/env python3
"""Review knowledge_health_training.csv quality (T304). Network: none."""
from __future__ import annotations
import csv, subprocess, sys
from collections import Counter, defaultdict
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
TARGET = ROOT / "data" / "knowledge_health_training.csv"
REPORT = ROOT / "docs" / "reviews" / "T304-health-training-review.md"
EXPECTED_ROWS = 200
SAMPLE_SIZE = 50
ID_PREFIX = "WC-HLTH"
CATEGORY_L1 = "健康与训练"
GAMBLING = ['彩票', '竞彩', '足彩', '体彩', '福彩', '博彩', '赌博', '赌球', '投注', '下注', '赔率', '盘口', '让球', '大小球', '亚盘', '欧赔', '水位', '串关', '稳赚', '必中', '庄家']

def main() -> int:
    rows = list(csv.DictReader(TARGET.open(encoding="utf-8")))
    issues = []
    ids = [r["id"] for r in rows]
    if len(ids) != len(set(ids)): issues.append("duplicate ids")
    if len(rows) != EXPECTED_ROWS: issues.append(f"expected {EXPECTED_ROWS}, got {len(rows)}")
    dup_q = [q for q,c in Counter(r["question"].strip() for r in rows).items() if c>1]
    if dup_q: issues.append(f"dup questions: {dup_q[:3]}")
    bad_l1 = [r["id"] for r in rows if r.get("category_l1") != CATEGORY_L1]
    if bad_l1: issues.append("bad category_l1")
    for r in rows:
        if len(r.get("answer_short","")) > 120: issues.append(f"{r['id']} short too long")
        blob = "".join(r.get(f,"") for f in ("question","answer_short","answer_detail","keywords"))
        for w in GAMBLING:
            if w in blob: issues.append(f"{r['id']} gambling {w}")
    by_l2 = defaultdict(list)
    for r in rows: by_l2[r["category_l2"]].append(r)
    validate = subprocess.run([sys.executable, str(ROOT/"scripts"/"validate_knowledge.py"), str(TARGET), "--strict"], capture_output=True, text=True)
    step = max(1, len(rows)//SAMPLE_SIZE)
    sample = [rows[i] for i in range(0,len(rows),step)][:SAMPLE_SIZE]
    lines = ["# T304 质量抽检报告", "", f"- 总行数: **{len(rows)}**", f"- 校验: **{'PASS' if validate.returncode==0 else 'FAIL'}**", ""]
    if issues: lines.append("## 问题"); lines.extend(f"- {i}" for i in issues[:30])
    else: lines.append("**通过**")
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text("\n".join(lines)+"\n", encoding="utf-8")
    print(REPORT)
    return 0 if not issues and validate.returncode==0 else 1

if __name__ == "__main__": sys.exit(main())
