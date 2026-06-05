#!/usr/bin/env python3
"""
Report progress for the World Cup knowledge base project from data/tasks.csv.

Usage:
  python scripts/progress_report.py
  python scripts/progress_report.py --json
  python scripts/progress_report.py --next 5
  python scripts/progress_report.py --phase 2

Network: none (local structured data). Outbound HTTP must use fetch_utils.RateLimitedFetcher (>=1s/request); see docs/data-collection-policy.md and .cursor/rules/world-cup-data-collection.mdc."""

from __future__ import annotations

import argparse
import csv
import json
import sys
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from validate_knowledge import discover_knowledge_files, project_root

KNOWLEDGE_GOAL = 10_000
MILESTONES = {
    "M1 MVP": 1_300,
    "M2 世界杯专题": 4_000,
    "M3 人物球队": 6_700,
    "M4 全分类": 10_000,
    "M5 v1.0": 10_000,
}

STATUS_ORDER = ("done", "review", "in_progress", "blocked", "not_started")
DONE_STATUSES = {"done"}
ACTIVE_STATUSES = {"in_progress", "review"}


@dataclass
class TaskRow:
    task_id: str
    phase: int
    phase_name: str
    task_order: int
    task_name: str
    task_type: str
    output_file: str
    target_rows: int
    batch_size: int
    status: str
    priority: str
    depends_on: str
    estimated_hours: float
    actual_rows: int
    notes: str


def knowledge_batch_output_names(data_dir: Path) -> frozenset[str]:
    return frozenset(
        p.name
        for p in data_dir.glob("knowledge_*.csv")
        if p.name not in {"knowledge_template.csv", "knowledge_all.csv"}
    )


def is_knowledge_batch_task(task: TaskRow, batch_outputs: frozenset[str]) -> bool:
    """Data tasks that append rows to per-category knowledge CSVs (not merge output)."""
    if task.task_type != "data":
        return False
    return Path(task.output_file).name in batch_outputs


@dataclass
class ProgressReport:
    generated_at: str
    task_total: int = 0
    task_by_status: dict[str, int] = field(default_factory=dict)
    task_by_phase: list[dict] = field(default_factory=list)
    task_by_priority: dict[str, dict[str, int]] = field(default_factory=dict)
    hours_estimated_total: float = 0.0
    hours_estimated_done: float = 0.0
    hours_estimated_remaining: float = 0.0
    knowledge_target_from_tasks: int = 0
    knowledge_actual_from_tasks: int = 0
    knowledge_rows_in_csv: int = 0
    knowledge_goal: int = KNOWLEDGE_GOAL
    knowledge_gap: int = 0
    knowledge_progress_pct: float = 0.0
    milestones: list[dict] = field(default_factory=list)
    data_tasks: list[dict] = field(default_factory=list)
    next_tasks: list[dict] = field(default_factory=list)
    blocked_tasks: list[dict] = field(default_factory=list)


def parse_int(value: str, default: int = 0) -> int:
    value = (value or "").strip()
    if not value:
        return default
    try:
        return int(value)
    except ValueError:
        return default


def parse_float(value: str, default: float = 0.0) -> float:
    value = (value or "").strip()
    if not value:
        return default
    try:
        return float(value)
    except ValueError:
        return default


def load_tasks(tasks_path: Path) -> list[TaskRow]:
    with tasks_path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        tasks: list[TaskRow] = []
        for row in reader:
            tasks.append(
                TaskRow(
                    task_id=row.get("task_id", "").strip(),
                    phase=parse_int(row.get("phase", "")),
                    phase_name=row.get("phase_name", "").strip(),
                    task_order=parse_int(row.get("task_order", "")),
                    task_name=row.get("task_name", "").strip(),
                    task_type=row.get("task_type", "").strip(),
                    output_file=row.get("output_file", "").strip(),
                    target_rows=parse_int(row.get("target_rows", "")),
                    batch_size=parse_int(row.get("batch_size", "")),
                    status=row.get("status", "not_started").strip() or "not_started",
                    priority=row.get("priority", "").strip(),
                    depends_on=row.get("depends_on", "").strip(),
                    estimated_hours=parse_float(row.get("estimated_hours", "")),
                    actual_rows=parse_int(row.get("actual_rows", "")),
                    notes=(row.get("notes") or "").strip(),
                )
            )
        return tasks


def count_knowledge_csv_rows(data_dir: Path) -> int:
    total = 0
    for path in discover_knowledge_files(data_dir):
        if path.name in {"knowledge_template.csv", "knowledge_all.csv"}:
            continue
        with path.open(newline="", encoding="utf-8") as f:
            reader = csv.reader(f)
            next(reader, None)
            for row in reader:
                if any(cell.strip() for cell in row):
                    total += 1
    return total


def dependencies_met(task: TaskRow, done_ids: set[str]) -> bool:
    if not task.depends_on:
        return True
    deps = [d.strip() for d in task.depends_on.split(";") if d.strip()]
    return all(dep in done_ids for dep in deps)


def build_report(tasks: list[TaskRow], data_dir: Path) -> ProgressReport:
    from datetime import datetime, timezone

    report = ProgressReport(generated_at=datetime.now(timezone.utc).isoformat())
    report.task_total = len(tasks)

    status_counts: dict[str, int] = defaultdict(int)
    for task in tasks:
        status_counts[task.status] += 1
    report.task_by_status = {s: status_counts.get(s, 0) for s in STATUS_ORDER if status_counts.get(s, 0)}

    phase_groups: dict[int, list[TaskRow]] = defaultdict(list)
    for task in tasks:
        phase_groups[task.phase].append(task)

    for phase in sorted(phase_groups):
        group = phase_groups[phase]
        phase_name = group[0].phase_name if group else ""
        done = sum(1 for t in group if t.status in DONE_STATUSES)
        report.task_by_phase.append(
            {
                "phase": phase,
                "phase_name": phase_name,
                "tasks_total": len(group),
                "tasks_done": done,
                "tasks_pct": round(done / len(group) * 100, 1) if group else 0.0,
                "knowledge_target": sum(t.target_rows for t in group if t.task_type == "data"),
                "knowledge_actual": sum(t.actual_rows for t in group if t.task_type == "data"),
            }
        )

    priority_groups: dict[str, list[TaskRow]] = defaultdict(list)
    for task in tasks:
        key = task.priority or "unset"
        priority_groups[key].append(task)

    for priority in sorted(priority_groups):
        group = priority_groups[priority]
        report.task_by_priority[priority] = {
            "total": len(group),
            "done": sum(1 for t in group if t.status in DONE_STATUSES),
            "not_started": sum(1 for t in group if t.status == "not_started"),
        }

    report.hours_estimated_total = sum(t.estimated_hours for t in tasks)
    report.hours_estimated_done = sum(
        t.estimated_hours for t in tasks if t.status in DONE_STATUSES
    )
    report.hours_estimated_remaining = report.hours_estimated_total - report.hours_estimated_done

    data_tasks = [t for t in tasks if t.task_type == "data"]
    batch_outputs = knowledge_batch_output_names(data_dir)
    knowledge_batch_tasks = [t for t in data_tasks if is_knowledge_batch_task(t, batch_outputs)]
    report.knowledge_target_from_tasks = sum(t.target_rows for t in knowledge_batch_tasks)
    report.knowledge_actual_from_tasks = sum(t.actual_rows for t in knowledge_batch_tasks)
    report.knowledge_rows_in_csv = count_knowledge_csv_rows(data_dir)
    report.knowledge_gap = max(0, report.knowledge_goal - report.knowledge_rows_in_csv)
    report.knowledge_progress_pct = round(
        min(report.knowledge_rows_in_csv / report.knowledge_goal * 100, 100.0), 2
    )

    for name, target in MILESTONES.items():
        reached = report.knowledge_rows_in_csv >= target
        report.milestones.append(
            {
                "name": name,
                "target_rows": target,
                "current_rows": report.knowledge_rows_in_csv,
                "reached": reached,
            }
        )

    report.data_tasks = [
        {
            "task_id": t.task_id,
            "task_name": t.task_name,
            "status": t.status,
            "target_rows": t.target_rows,
            "actual_rows": t.actual_rows,
            "gap": max(0, t.target_rows - t.actual_rows),
            "output_file": t.output_file,
        }
        for t in data_tasks
        if t.status != "done" or t.actual_rows < t.target_rows
    ]

    done_ids = {t.task_id for t in tasks if t.status in DONE_STATUSES}
    report.blocked_tasks = [
        {"task_id": t.task_id, "task_name": t.task_name, "notes": t.notes}
        for t in tasks
        if t.status == "blocked"
    ]

    candidates = [
        t
        for t in tasks
        if t.status == "not_started" and dependencies_met(t, done_ids)
    ]
    priority_rank = {"P0": 0, "P1": 1, "P2": 2, "P3": 3, "": 9}
    candidates.sort(
        key=lambda t: (priority_rank.get(t.priority, 9), t.phase, t.task_order, t.task_id)
    )
    report.next_tasks = [
        {
            "task_id": t.task_id,
            "phase_name": t.phase_name,
            "task_name": t.task_name,
            "priority": t.priority,
            "target_rows": t.target_rows,
            "output_file": t.output_file,
        }
        for t in candidates
    ]

    return report


def print_report(report: ProgressReport, phase_filter: int | None, next_n: int) -> None:
    done = report.task_by_status.get("done", 0)
    print("=" * 60)
    print("世界杯常识知识库 — 进度报告")
    print("=" * 60)
    print(f"生成时间: {report.generated_at}")
    print()

    print("【任务总览】")
    print(f"  任务总数: {report.task_total}")
    print(f"  已完成:   {done} ({round(done / report.task_total * 100, 1) if report.task_total else 0}%)")
    for status, count in report.task_by_status.items():
        if status != "done":
            print(f"  {status}: {count}")
    print(
        f"  预估工时: {report.hours_estimated_done:.0f}h / {report.hours_estimated_total:.0f}h "
        f"(剩余 {report.hours_estimated_remaining:.0f}h)"
    )
    print()

    print("【知识条目进度】")
    print(f"  目标:     {report.knowledge_goal:,} 条")
    print(f"  CSV 实计: {report.knowledge_rows_in_csv:,} 条")
    print(f"  任务登记: {report.knowledge_actual_from_tasks:,} 条 (target 合计 {report.knowledge_target_from_tasks:,})")
    print(f"  缺口:     {report.knowledge_gap:,} 条 ({report.knowledge_progress_pct}% 完成)")
    if report.knowledge_actual_from_tasks != report.knowledge_rows_in_csv:
        print(
            "  ⚠ tasks.csv 的 actual_rows 与 CSV 实计不一致，"
            "合并数据后请同步更新 actual_rows"
        )
    print()

    print("【里程碑】")
    for m in report.milestones:
        mark = "✓" if m["reached"] else " "
        print(
            f"  [{mark}] {m['name']}: {m['current_rows']:,} / {m['target_rows']:,}"
        )
    print()

    print("【分阶段进度】")
    for phase in report.task_by_phase:
        if phase_filter is not None and phase["phase"] != phase_filter:
            continue
        print(
            f"  Phase {phase['phase']:>2} {phase['phase_name']:<12} "
            f"任务 {phase['tasks_done']}/{phase['tasks_total']} ({phase['tasks_pct']}%) "
            f"| 知识 {phase['knowledge_actual']}/{phase['knowledge_target']}"
        )
    print()

    if report.blocked_tasks:
        print("【阻塞任务】")
        for t in report.blocked_tasks:
            print(f"  {t['task_id']} {t['task_name']} — {t['notes']}")
        print()

    print(f"【建议下一步】（前 {next_n} 项，依赖已满足）")
    for t in report.next_tasks[:next_n]:
        rows = f", 目标 {t['target_rows']} 条" if t["target_rows"] else ""
        print(f"  {t['task_id']} [{t['priority']}] {t['task_name']}{rows}")
    if not report.next_tasks[:next_n]:
        print("  (无)")
    print()

    incomplete_data = [d for d in report.data_tasks if d["gap"] > 0]
    if incomplete_data:
        top = sorted(incomplete_data, key=lambda x: x["gap"], reverse=True)[:8]
        print("【数据任务缺口 Top】")
        for d in top:
            print(
                f"  {d['task_id']} {d['status']}: "
                f"{d['actual_rows']}/{d['target_rows']} (-{d['gap']}) — {d['task_name']}"
            )
        print()


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Report World Cup knowledge project progress.")
    parser.add_argument(
        "--tasks",
        type=Path,
        default=project_root() / "data" / "tasks.csv",
        help="Path to tasks.csv (default: data/tasks.csv)",
    )
    parser.add_argument("--json", action="store_true", help="Output JSON instead of text")
    parser.add_argument("--phase", type=int, help="Filter phase section to one phase")
    parser.add_argument("--next", type=int, default=5, help="How many next tasks to show (default: 5)")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    root = project_root()
    tasks_path = args.tasks if args.tasks.is_absolute() else root / args.tasks

    if not tasks_path.exists():
        print(f"tasks file not found: {tasks_path}", file=sys.stderr)
        return 1

    tasks = load_tasks(tasks_path)
    report = build_report(tasks, root / "data")

    if args.json:
        print(json.dumps(report.__dict__, ensure_ascii=False, indent=2))
    else:
        print_report(report, args.phase, args.next)

    return 0


if __name__ == "__main__":
    sys.exit(main())
