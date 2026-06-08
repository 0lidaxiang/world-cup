#!/usr/bin/env python3
"""
Spot-check robots.txt for common World Cup knowledge source domains.

Writes a timestamped snapshot under logs/compliance/ and prints a summary.
Uses RateLimitedFetcher (>=1s between requests).

Network: yes (robots.txt only, serial).
"""

from __future__ import annotations

import argparse
import sys
from datetime import datetime, timezone
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from fetch_utils import RateLimitedFetcher

ROOT = Path(__file__).resolve().parent.parent

# Domains commonly referenced in source_ref; extend as needed.
DEFAULT_DOMAINS = [
    "www.fifa.com",
    "www.theifab.com",
    "en.wikipedia.org",
    "www.uefa.com",
]


def fetch_robots(fetcher: RateLimitedFetcher, domain: str) -> tuple[int | None, str, str | None]:
    url = f"https://{domain}/robots.txt"
    try:
        body = fetcher.get_text(url)
        return 200, body, None
    except Exception as e:  # noqa: BLE001 — CLI summary tool
        return None, "", str(e)


def summarize_robots(body: str) -> list[str]:
    lines: list[str] = []
    user_agent = "*"
    for raw in body.splitlines()[:200]:
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        lower = line.lower()
        if lower.startswith("user-agent:"):
            user_agent = line.split(":", 1)[1].strip()
        elif lower.startswith("disallow:"):
            path = line.split(":", 1)[1].strip() or "/"
            if user_agent == "*":
                lines.append(f"  Disallow ({user_agent}): {path}")
    return lines[:15]


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit robots.txt for source domains")
    parser.add_argument(
        "--domains",
        nargs="*",
        default=DEFAULT_DOMAINS,
        help="Hostnames to check (default: FIFA, IFAB, Wikipedia, UEFA)",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=ROOT / "logs" / "compliance",
        help="Directory for snapshot files",
    )
    args = parser.parse_args()

    fetcher = RateLimitedFetcher()
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    args.output_dir.mkdir(parents=True, exist_ok=True)
    snapshot_path = args.output_dir / f"robots_snapshot_{ts}.txt"

    sections: list[str] = [
        f"# robots.txt compliance snapshot",
        f"# generated_at_utc: {ts}",
        f"# fetcher: RateLimitedFetcher min_interval={fetcher.min_interval_sec}s",
        "",
    ]

    print(f"Checking {len(args.domains)} domain(s)...")
    for domain in args.domains:
        status, body, err = fetch_robots(fetcher, domain)
        sections.append(f"## {domain}")
        sections.append(f"url: https://{domain}/robots.txt")
        if err:
            sections.append(f"status: ERROR")
            sections.append(f"error: {err}")
            print(f"  {domain}: ERROR — {err}")
        else:
            sections.append(f"status: {status}")
            sections.append(f"bytes: {len(body.encode('utf-8', errors='replace'))}")
            preview = summarize_robots(body)
            if preview:
                sections.append("highlights:")
                sections.extend(preview)
            else:
                sections.append("(no Disallow rules in first 200 lines or empty body)")
            print(f"  {domain}: OK ({len(body)} chars)")
        sections.append("")

    text = "\n".join(sections)
    snapshot_path.write_text(text, encoding="utf-8")
    print(f"\nSnapshot written: {snapshot_path}")
    print("Review Disallow rules before large-scale fetching. See docs/compliance.md.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
