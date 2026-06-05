#!/usr/bin/env python3
"""Generate quality_debt_seeds.py with 2655+ substantive FAQs. Network: none."""

from __future__ import annotations

import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
OUT = SCRIPT_DIR / "quality_debt_seeds.py"
sys.path.insert(0, str(SCRIPT_DIR))

from _seed_banks import (  # noqa: E402
    build_culture,
    build_discipline,
    build_extra_records,
    build_health,
    build_history_extras,
    build_venues,
    build_womens,
)

HEADER = '''#!/usr/bin/env python3
"""Quality seed FAQs for knowledge-base debt remediation.

Provides substantive FAQ tuples to replace placeholder generators in
_remaining_batches.py and orchestrate_remaining_73.py.

Network: none.
"""

from __future__ import annotations

FAQ = tuple[str, str, str, str, str]
"""(question, alias, answer_short, answer_detail, keywords)"""


def _short(text: str, limit: int = 120) -> str:
    t = text.strip()
    if len(t) <= limit:
        return t
    return t[: limit - 1] + "…"


def _faq(q: str, alias: str, short: str, detail: str, keywords: str) -> FAQ:
    return (q.strip(), alias.strip(), _short(short), detail.strip(), keywords.strip())


GAMBLING_TERMS = frozenset({
    "彩票", "竞彩", "足彩", "体彩", "福彩", "博彩", "赌博", "赌球",
    "投注", "下注", "赔率", "盘口", "让球", "大小球", "亚盘", "欧赔",
    "水位", "串关", "稳赚", "必中", "庄家",
})


'''


def emit_dict(name: str, data: dict) -> str:
    lines = [f"{name}: dict[str, list[FAQ]] = {{"]
    for cat, faqs in data.items():
        lines.append(f'    "{cat}": [')
        for f in faqs:
            q, a, s, d, k = f
            lines.append(f"        _faq({q!r}, {a!r}, {s!r}, {d!r}, {k!r}),")
        lines.append("    ],")
    lines.append("}")
    return "\n".join(lines)


def emit_history(name: str, data: dict) -> str:
    lines = [f"{name}: dict[str, list[FAQ]] = {{"]
    for year, faqs in data.items():
        lines.append(f'    "{year}": [')
        for f in faqs:
            q, a, s, d, k = f
            lines.append(f"        _faq({q!r}, {a!r}, {s!r}, {d!r}, {k!r}),")
        lines.append("    ],")
    lines.append("}")
    return "\n".join(lines)


VALIDATOR = Path(__file__).resolve().parent.joinpath("quality_debt_seeds.py").read_text(encoding="utf-8")
VALIDATOR = "def _check_no_gambling" + VALIDATOR.split("def _check_no_gambling", 1)[1]


def main() -> None:
    facts = {
        "DISCIPLINE_SEEDS": build_discipline(),
        "CULTURE_SEEDS": build_culture(),
        "HEALTH_TRAINING_SEEDS": build_health(),
        "VENUES_TECH_SEEDS": build_venues(),
        "WOMENS_WC_SEEDS": build_womens(),
        "EXTRA_RECORDS": build_extra_records(),
        "WC_HISTORY_EXTRAS": build_history_extras(),
    }
    parts = [HEADER]
    parts.append(emit_dict("DISCIPLINE_SEEDS", facts["DISCIPLINE_SEEDS"]))
    parts.append("")
    parts.append(emit_dict("CULTURE_SEEDS", facts["CULTURE_SEEDS"]))
    parts.append("")
    parts.append(emit_dict("HEALTH_TRAINING_SEEDS", facts["HEALTH_TRAINING_SEEDS"]))
    parts.append("")
    parts.append(emit_dict("VENUES_TECH_SEEDS", facts["VENUES_TECH_SEEDS"]))
    parts.append("")
    parts.append(emit_dict("WOMENS_WC_SEEDS", facts["WOMENS_WC_SEEDS"]))
    parts.append("")
    parts.append(emit_dict("EXTRA_RECORDS", facts["EXTRA_RECORDS"]))
    parts.append("")
    parts.append(emit_history("WC_HISTORY_EXTRAS", facts["WC_HISTORY_EXTRAS"]))
    parts.append("")
    parts.append(VALIDATOR.rstrip())
    OUT.write_text("\n".join(parts) + "\n", encoding="utf-8")
    print(f"Wrote {OUT} ({OUT.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()
