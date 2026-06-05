#!/usr/bin/env python3
"""Generate T221: 位置职责 (append). Network: none."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))

from _knowledge_batch_lib import append_batch, load_all_questions
from _remaining_batches import ALL_GENERATORS, ALL_BATCHES

TASK_ID = "T221"


def main() -> None:
    batch = next(b for b in ALL_BATCHES if b.task_id == TASK_ID)
    gen = ALL_GENERATORS[TASK_ID]
    entries = gen()
    n = append_batch(
        ROOT / "data" / batch.output,
        entries,
        start_id=batch.start_id,
        id_prefix=batch.id_prefix,
        category_l1=batch.category_l1,
        category_l2=batch.category_l2,
        tags=batch.tags,
        priority=batch.priority,
        default_fact_type=batch.default_fact_type,
        source_ref=batch.source_ref,
        global_questions=load_all_questions(),
    )
    print(f"{TASK_ID}: wrote {n} rows to {batch.output}")


if __name__ == "__main__":
    main()
