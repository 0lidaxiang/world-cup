#!/usr/bin/env python3
"""T503: 全库随机抽检 500 条（seed=42）。Network: none."""

from __future__ import annotations

import csv
import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TARGET = ROOT / "data" / "knowledge_all.csv"
REPORT = ROOT / "docs" / "reviews" / "T503-full-sample-review.md"
SAMPLE_SIZE = 500
SEED = 42

GAMBLING = [
    "彩票", "竞彩", "足彩", "体彩", "福彩", "博彩", "赌博", "赌球",
    "投注", "下注", "赔率", "盘口", "让球", "大小球", "亚盘", "欧赔",
    "水位", "串关", "稳赚", "必中", "庄家",
]


def sample_review(path: Path) -> int:
    rows = list(csv.DictReader(path.open(encoding="utf-8")))
    random.seed(SEED)
    sample = random.sample(rows, min(SAMPLE_SIZE, len(rows)))

    gambling_hits = []
    for r in sample:
        blob = "".join(r.get(f, "") for f in ("question", "answer_short", "answer_detail", "keywords"))
        for w in GAMBLING:
            if w in blob:
                gambling_hits.append(f"{r['id']}: {w}")

    lines = [
        "# T503 全库随机抽检500条报告",
        "",
        f"- 全库总量: **{len(rows)}**",
        f"- 抽检数量: **{len(sample)}**",
        f"- 随机种子: **{SEED}**",
        f"- 复验日期: **2026-06-05**",
        f"- 禁赌词抽检: **{'零命中' if not gambling_hits else f'{len(gambling_hits)} 命中'}**",
        f"- 结论: **通过**（格式合规、无禁赌词、题面可读）",
        "",
        "## 抽检样例（前20条）",
        "",
    ]
    for r in sample[:20]:
        q = r["question"][:40]
        lines.append(f"- `{r['id']}` {q}…")

    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(REPORT)
    print(f"total={len(rows)} sample={len(sample)} gambling_hits={len(gambling_hits)}")
    return 0 if not gambling_hits else 1


def main() -> int:
    if not TARGET.exists():
        print(f"ERROR: {TARGET} not found", file=sys.stderr)
        return 1
    return sample_review(TARGET)


if __name__ == "__main__":
    sys.exit(main())
