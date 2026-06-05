#!/usr/bin/env python3
"""Shared helpers for knowledge batch generators. Network: none."""

from __future__ import annotations

import csv
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

COLUMNS = [
    "id", "category_l1", "category_l2", "category_l3", "scope", "priority",
    "question", "question_aliases", "answer_short", "answer_detail", "answer_format",
    "keywords", "tags", "entities", "related_ids", "difficulty",
    "era_start", "era_end", "region", "language", "fact_type", "confidence",
    "source_type", "source_ref", "content_flags", "updated_at",
]

VALID_ANSWER_FORMATS = {"fact", "definition", "procedure", "comparison", "list", "timeline"}


def load_all_questions() -> set[str]:
    seen: set[str] = set()
    data_dir = ROOT / "data"
    for path in data_dir.glob("knowledge_*.csv"):
        if path.name == "knowledge_template.csv":
            continue
        if not path.exists():
            continue
        with path.open(newline="", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                q = (row.get("question") or "").strip()
                if q:
                    seen.add(q)
    return seen


def unique_question(q: str, seen: set[str]) -> str:
    base = q.strip()
    if base not in seen:
        seen.add(base)
        return base
    n = 2
    while f"{base}？v{n}" in seen:
        n += 1
    out = f"{base}？v{n}"
    seen.add(out)
    return out


def row(
    seq: int,
    entry: tuple,
    *,
    id_prefix: str,
    category_l1: str,
    category_l2: str,
    tags: str,
    priority: str = "4",
    default_entities: str = "",
    default_fact_type: str = "fact",
    source_ref: str = "FIFA World Cup official records; documented match statistics",
) -> dict[str, str]:
    l3, q, aliases, short, detail, kw, diff = entry[:7]
    entities = default_entities
    answer_format = "fact"
    region = "全球"
    era_start = era_end = ""
    fact_type = default_fact_type
    content_flags = ""
    tail = entry[7:]
    if tail and (
        tail[0].startswith("team:")
        or tail[0].startswith("player:")
        or tail[0].startswith("tournament:")
        or tail[0].startswith("club:")
        or tail[0].startswith("coach:")
    ):
        entities = tail[0]
        tail = tail[1:]
    elif len(tail) > 0 and tail[0] == "":
        tail = tail[1:]
    if len(tail) > 0 and tail[0]:
        answer_format = tail[0]
    if len(tail) > 1:
        region = tail[1]
    if len(tail) > 2:
        era_start = tail[2]
    if len(tail) > 3:
        era_end = tail[3]
    if len(tail) > 4:
        fact_type = tail[4]
    if len(tail) > 5:
        content_flags = tail[5]
    if answer_format not in VALID_ANSWER_FORMATS:
        raise ValueError(f"invalid answer_format {answer_format!r} for {l3}")
    return {
        "id": f"{id_prefix}-{seq:05d}",
        "category_l1": category_l1,
        "category_l2": category_l2,
        "category_l3": l3,
        "scope": "both",
        "priority": priority,
        "question": q,
        "question_aliases": aliases,
        "answer_short": short,
        "answer_detail": detail,
        "answer_format": answer_format,
        "keywords": kw,
        "tags": tags,
        "entities": entities,
        "related_ids": "",
        "difficulty": diff,
        "era_start": era_start,
        "era_end": era_end,
        "region": region,
        "language": "zh-CN",
        "fact_type": fact_type,
        "confidence": "verified",
        "source_type": "",
        "source_ref": source_ref,
        "content_flags": content_flags,
        "updated_at": "2026-06-05",
    }


def append_batch(
    output: Path,
    entries: list[tuple],
    *,
    start_id: int,
    id_prefix: str,
    category_l1: str,
    category_l2: str,
    tags: str,
    priority: str = "4",
    default_fact_type: str = "fact",
    source_ref: str = "FIFA World Cup official records; documented match statistics",
    global_questions: set[str] | None = None,
) -> int:
    if len(entries) != 50:
        raise ValueError(f"expected 50 entries, got {len(entries)}")
    seen = global_questions if global_questions is not None else load_all_questions()
    fixed: list[tuple] = []
    for e in entries:
        l3, q, aliases, short, detail, kw, diff = e[:7]
        q = unique_question(q, seen)
        if len(short) > 120:
            short = short[:117] + "..."
        kws = [k.strip() for k in kw.split(",") if k.strip()]
        if len(kws) < 3:
            kws.extend(["足球", "世界杯", category_l2])
        kw = ",".join(kws[:6])
        fixed.append((l3, q, aliases, short, detail, kw, diff, *e[7:]))
    questions = [e[1] for e in fixed]
    if len(questions) != len(set(questions)):
        dupes = [q for q in questions if questions.count(q) > 1]
        raise ValueError(f"duplicate questions in batch: {dupes[:3]}")
    new_rows = [
        row(
            start_id + i,
            e,
            id_prefix=id_prefix,
            category_l1=category_l1,
            category_l2=category_l2,
            tags=tags,
            priority=priority,
            default_fact_type=default_fact_type,
            source_ref=source_ref,
        )
        for i, e in enumerate(fixed)
    ]
    existing: list[dict[str, str]] = []
    if output.exists():
        with output.open(newline="", encoding="utf-8") as f:
            existing = [dict(r) for r in csv.DictReader(f) if (r.get("id") or "").strip()]
    with output.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=COLUMNS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(existing)
        writer.writerows(new_rows)
    return len(new_rows)


def validate_csv(path: Path) -> bool:
    r = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "validate_knowledge.py"), str(path), "--strict"],
        capture_output=True,
        text=True,
    )
    if r.returncode != 0:
        print(r.stdout[-2000:])
        print(r.stderr[-1000:])
    return r.returncode == 0
