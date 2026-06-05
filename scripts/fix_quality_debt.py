#!/usr/bin/env python3
"""Replace placeholder FAQ rows with substantive content. Network: none.

Keeps all existing IDs; only updates question/answer/keywords fields.
"""

from __future__ import annotations

import csv
import re
import subprocess
import sys
from collections import defaultdict
from datetime import date
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
ROOT = SCRIPT_DIR.parent
sys.path.insert(0, str(SCRIPT_DIR))

from _knowledge_batch_lib import COLUMNS, unique_question
from quality_debt_seeds import (
    CULTURE_SEEDS,
    DISCIPLINE_SEEDS,
    EXTRA_RECORDS,
    HEALTH_TRAINING_SEEDS,
    VENUES_TECH_SEEDS,
    WC_HISTORY_EXTRAS,
    WOMENS_WC_SEEDS,
)
from wc_history_topic_seeds import WC_HISTORY_TOPIC_SEEDS

TODAY = date.today().isoformat()

PLACEHOLDER_RE = re.compile(
    r"要点\d+是什么|常识\d+|数据点\d+|第\d+条常识|内容基于公开资料整理|"
    r"涉及该领域常见问答|补充事实|补充知识点|专题\d+）|\\?？v\d+"
)

FILE_SEEDS: dict[str, dict[str, list]] = {
    "knowledge_discipline.csv": DISCIPLINE_SEEDS,
    "knowledge_culture.csv": CULTURE_SEEDS,
    "knowledge_health_training.csv": HEALTH_TRAINING_SEEDS,
    "knowledge_venues_tech.csv": VENUES_TECH_SEEDS,
    "knowledge_womens_wc.csv": WOMENS_WC_SEEDS,
    "knowledge_records_stats.csv": EXTRA_RECORDS,
}


def is_placeholder(row: dict[str, str]) -> bool:
    blob = "".join(
        row.get(k, "") for k in ("question", "answer_short", "answer_detail", "category_l3", "question_aliases")
    )
    if PLACEHOLDER_RE.search(blob):
        return True
    if row.get("answer_short", "").strip().startswith("数据") and len(row["answer_short"]) <= 4:
        return True
    if "相关统计知识点" in blob:
        return True
    return False


def extract_year(row: dict[str, str]) -> str | None:
    for field in ("category_l3", "question", "keywords", "era_start"):
        m = re.search(r"(19\d{2}|20[012]\d)", row.get(field, ""))
        if m:
            return m.group(1)
    return None


def apply_faq(
    row: dict[str, str],
    faq: tuple[str, str, str, str, str],
    seen: set[str],
    *,
    l3_prefix: str = "",
) -> None:
    q, alias, short, detail, kw = faq
    row["question"] = unique_question(q, seen)
    row["question_aliases"] = alias
    row["answer_short"] = short
    row["answer_detail"] = detail
    row["keywords"] = kw
    if l3_prefix:
        slug = re.sub(r"[^\w\u4e00-\u9fff]", "", alias)[:20] or "条目"
        row["category_l3"] = f"{l3_prefix}{slug}"[:40]
    row["updated_at"] = TODAY


def fix_file(path: Path, seen: set[str]) -> tuple[int, int]:
    seeds_map = FILE_SEEDS.get(path.name)
    rows = list(csv.DictReader(path.open(encoding="utf-8")))
    if not rows:
        return 0, 0

    counters: dict[str, int] = defaultdict(int)
    fixed = 0

    for row in rows:
        if not is_placeholder(row):
            q = (row.get("question") or "").strip()
            if q:
                seen.add(q)
            continue

        l2 = row.get("category_l2", "")
        idx = counters[l2]
        counters[l2] += 1

        if path.name == "knowledge_wc_history.csv":
            if l2 in WC_HISTORY_TOPIC_SEEDS:
                pool = WC_HISTORY_TOPIC_SEEDS[l2]
                faq = pool[idx % len(pool)]
                apply_faq(row, faq, seen, l3_prefix=l2[:8])
                fixed += 1
                continue
            year = extract_year(row)
            pool = WC_HISTORY_EXTRAS.get(year or "", [])
            if not pool:
                continue
            faq = pool[idx % len(pool)]
            apply_faq(row, faq, seen, l3_prefix=f"{year or ''}")
            if year:
                row["era_start"] = row["era_end"] = year
            fixed += 1
            continue

        if not seeds_map or l2 not in seeds_map:
            continue
        pool = seeds_map[l2]
        if idx >= len(pool):
            idx = idx % len(pool)
        faq = pool[idx]
        apply_faq(row, faq, seen)
        fixed += 1

    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=COLUMNS, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)

    return len(rows), fixed


def fix_wc_history(path: Path, seen: set[str]) -> tuple[int, int]:
    rows = list(csv.DictReader(path.open(encoding="utf-8")))
    counters: dict[str, int] = defaultdict(int)
    fixed = 0
    for row in rows:
        if not is_placeholder(row):
            q = (row.get("question") or "").strip()
            if q:
                seen.add(q)
            continue
        year = extract_year(row)
        key = year or "unknown"
        idx = counters[key]
        counters[key] += 1
        pool = WC_HISTORY_EXTRAS.get(year or "", [])
        if not pool:
            continue
        faq = pool[idx % len(pool)]
        apply_faq(row, faq, seen, l3_prefix=f"{year}年" if year else "")
        if year:
            row["era_start"] = row["era_end"] = year
        fixed += 1

    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=COLUMNS, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)
    return len(rows), fixed


def load_all_questions() -> set[str]:
    seen: set[str] = set()
    for path in (ROOT / "data").glob("knowledge_*.csv"):
        if path.name == "knowledge_template.csv":
            continue
        for row in csv.DictReader(path.open(encoding="utf-8")):
            q = (row.get("question") or "").strip()
            if q:
                seen.add(q)
    return seen


def cleanup_v2_suffixes() -> int:
    """Strip ?？v2 / ？vN dedup suffixes when base question is globally unique."""
    seen: set[str] = set()
    cleaned = 0
    for path in sorted((ROOT / "data").glob("knowledge_*.csv")):
        if path.name in ("knowledge_all.csv", "knowledge_template.csv"):
            continue
        rows = list(csv.DictReader(path.open(encoding="utf-8")))
        for row in rows:
            q = (row.get("question") or "").strip()
            if q:
                seen.add(q)

    for path in sorted((ROOT / "data").glob("knowledge_*.csv")):
        if path.name in ("knowledge_all.csv", "knowledge_template.csv"):
            continue
        rows = list(csv.DictReader(path.open(encoding="utf-8")))
        changed = False
        for row in rows:
            q = (row.get("question") or "").strip()
            m = re.match(r"^(.+?)(?:\?？v\d+|\？v\d+)$", q)
            if not m:
                continue
            base = m.group(1).rstrip("?？") + "?"
            if base in seen and base != q:
                continue
            seen.discard(q)
            seen.add(base)
            row["question"] = base
            cleaned += 1
            changed = True
        if changed:
            with path.open("w", newline="", encoding="utf-8") as f:
                w = csv.DictWriter(f, fieldnames=COLUMNS, extrasaction="ignore")
                w.writeheader()
                w.writerows(rows)
    print(f"Cleaned {cleaned} ?？vN suffixes")
    return cleaned


def main() -> int:
    seen = load_all_questions()
    total_fixed = 0
    reports: list[str] = []

    targets = sorted(FILE_SEEDS.keys()) + ["knowledge_wc_history.csv"]
    for name in targets:
        path = ROOT / "data" / name
        if not path.exists():
            continue
        if name == "knowledge_wc_history.csv":
            n, fixed = fix_wc_history(path, seen)
        else:
            n, fixed = fix_file(path, seen)
        reports.append(f"  {name}: {fixed}/{n} fixed")
        total_fixed += fixed
        print(f"OK {name}: fixed {fixed}/{n}")

    print(f"\nTotal fixed: {total_fixed}")
    cleanup_v2_suffixes()

    for name in targets:
        path = ROOT / "data" / name
        if path.exists():
            r = subprocess.run(
                [sys.executable, str(SCRIPT_DIR / "validate_knowledge.py"), str(path), "--strict"],
                capture_output=True,
                text=True,
            )
            if r.returncode != 0:
                print(r.stdout, r.stderr)
                return 1

    r = subprocess.run(
        [sys.executable, str(SCRIPT_DIR / "merge_batches.py"), "--build-all"],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    print(r.stdout[-400:])
    if r.returncode != 0:
        print(r.stderr)
        return 1

    r2 = subprocess.run(
        [sys.executable, str(SCRIPT_DIR / "validate_knowledge.py"), "--all", "--strict"],
        capture_output=True,
        text=True,
    )
    print(r2.stdout)
    return 0 if r2.returncode == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
