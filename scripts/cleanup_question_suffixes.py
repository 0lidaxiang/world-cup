#!/usr/bin/env python3
"""Remove or rephrase ?？vN dedup suffixes. Network: none."""

from __future__ import annotations

import csv
import re
import subprocess
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
ROOT = SCRIPT_DIR.parent
sys.path.insert(0, str(SCRIPT_DIR))
from _knowledge_batch_lib import COLUMNS, unique_question

SUFFIX_RE = re.compile(r"^(.+?)(?:\?？v\d+|\？v\d+)$")


def alt_question(row: dict[str, str], base: str, seen: set[str]) -> str:
    alias = (row.get("question_aliases") or "").strip()
    short = (row.get("answer_short") or "").strip()
    l3 = (row.get("category_l3") or "").strip()
    year_m = re.search(r"(19\d{2}|20[012]\d)", base + short + l3)
    year = year_m.group(1) if year_m else ""

    candidates = []
    if alias and alias not in ("常识1", "数据1") and len(alias) >= 2:
        candidates.append(f"{alias}是什么?" if not alias.endswith("?") else alias)
    if year and "世界杯" in base:
        topic = re.sub(r"\d{4}年?", "", base).replace("是谁", "").replace("是什么", "").strip("?？ ")
        if topic:
            candidates.append(f"{year}年{topic}详情?")
    if short and len(short) <= 40:
        candidates.append(f"{short}?" if not short.endswith("?") else short)
    if l3 and len(l3) >= 3:
        candidates.append(f"世界杯{l3}相关问答?")

    for c in candidates:
        q = c if c.endswith("?") else c + "?"
        if len(q) <= 80:
            return unique_question(q, seen)
    return unique_question(f"{base.rstrip('?？')}（补充）?", seen)


def main() -> int:
    seen: set[str] = set()
    for path in sorted((ROOT / "data").glob("knowledge_*.csv")):
        if path.name in ("knowledge_all.csv", "knowledge_template.csv"):
            continue
        for row in csv.DictReader(path.open(encoding="utf-8")):
            q = (row.get("question") or "").strip()
            if q and SUFFIX_RE.match(q) is None:
                seen.add(q)

    cleaned = 0
    for path in sorted((ROOT / "data").glob("knowledge_*.csv")):
        if path.name in ("knowledge_all.csv", "knowledge_template.csv"):
            continue
        rows = list(csv.DictReader(path.open(encoding="utf-8")))
        changed = False
        for row in rows:
            q = (row.get("question") or "").strip()
            m = SUFFIX_RE.match(q)
            if not m:
                continue
            base = m.group(1).rstrip("?？") + "?"
            if base not in seen:
                seen.discard(q)
                seen.add(base)
                row["question"] = base
            else:
                new_q = alt_question(row, base, seen)
                seen.discard(q)
                row["question"] = new_q
            cleaned += 1
            changed = True
        if changed:
            with path.open("w", newline="", encoding="utf-8") as f:
                w = csv.DictWriter(f, fieldnames=COLUMNS, extrasaction="ignore")
                w.writeheader()
                w.writerows(rows)

    print(f"Cleaned {cleaned} suffix rows")
    subprocess.run(
        [sys.executable, str(SCRIPT_DIR / "merge_batches.py"), "--build-all"],
        cwd=ROOT, check=True,
    )
    r = subprocess.run(
        [sys.executable, str(SCRIPT_DIR / "validate_knowledge.py"), "--all", "--strict"],
        capture_output=True, text=True,
    )
    print(r.stdout)
    return r.returncode


if __name__ == "__main__":
    sys.exit(main())
