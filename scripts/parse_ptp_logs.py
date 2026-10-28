
#!/usr/bin/env python3
"""Parse LinuxPTP ptp4l logs and output descriptive statistics."""

from __future__ import annotations

import argparse
import csv
import json
import math
import re
import sys
from pathlib import Path
from statistics import mean, pstdev
from typing import Iterable

# Supports common log entries in the format:
# "master offset ... sN freq ... path delay ..."
LOG_PATTERN = re.compile(
    r"master\s+offset\s+(?P<offset>[+-]?\d+)\s+"
    r"s\d+\s+freq\s+[+-]?\d+\s+"
    r"path\s+delay\s+(?P<delay>[+-]?\d+)",
    re.IGNORECASE,
)


def parse_lines(lines: Iterable[str]) -> tuple[list[dict[str, int]], int]:
    """Return valid records and the number of unmatched non-empty lines."""
    records: list[dict[str, int]] = []
    unmatched = 0

    for line in lines:
        if not line.strip():
            continue

        match = LOG_PATTERN.search(line)
        if not match:
            unmatched += 1
            continue

        records.append(
            {
                "offset_ns": int(match.group("offset")),
                "path_delay_ns": int(match.group("delay")),
            }
        )

    return records, unmatched


def summarize(records: list[dict[str, int]]) -> dict[str, int | float]:
    """Calculate descriptive statistics using population standard deviation."""
    if not records:
        raise ValueError("No valid records available for analysis.")

    offsets = [item["offset_ns"] for item in records]
    delays = [item["path_delay_ns"] for item in records]

    return {
        "sample_count": len(records),
        "mean_offset_ns": mean(offsets),
        "rms_offset_ns": math.sqrt(mean(value * value for value in offsets)),
        "max_abs_offset_ns": max(abs(value) for value in offsets),
        "offset_population_stddev_ns": pstdev(offsets),
        "mean_path_delay_ns": mean(delays),
        "min_path_delay_ns": min(delays),
        "max_path_delay_ns": max(delays),
    }


def write_csv(path: Path, records: list[dict[str, int]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle, fieldnames=["offset_ns", "path_delay_ns"]
        )
        writer.writeheader()
        writer.writerows(records)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Parse clock offset and path delay from ptp4l logs."
    )
    parser.add_argument("log_file", type=Path, help="Input ptp4l log file")
    parser.add_argument("--csv", type=Path, help="Optional output CSV file")
    parser.add_argument(
        "--json", type=Path, help="Optional output JSON summary file"
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()

    try:
        with args.log_file.open(
            "r", encoding="utf-8", errors="replace"
        ) as handle:
            records, unmatched = parse_lines(handle)
    except OSError as exc:
        print(
            f"Error: Unable to read file '{args.log_file}': {exc}",
            file=sys.stderr,
        )
        return 2

    if not records:
        print(
            "Error: No valid ptp4l records found "
            f"(unmatched non-empty lines: {unmatched}).",
            file=sys.stderr,
        )
        return 1

    summary = summarize(records)
    summary["unmatched_nonempty_lines"] = unmatched

    print("PTP Log Analysis Summary")
    print(f"Valid samples: {summary['sample_count']}")
    print(f"Mean offset: {summary['mean_offset_ns']:.3f} ns")
    print(f"RMS offset: {summary['rms_offset_ns']:.3f} ns")
    print(f"Maximum absolute offset: {summary['max_abs_offset_ns']} ns")
    print(
        "Offset population standard deviation: "
        f"{summary['offset_population_stddev_ns']:.3f} ns"
    )
    print(f"Mean path delay: {summary['mean_path_delay_ns']:.3f} ns")
    print(f"Minimum path delay: {summary['min_path_delay_ns']} ns")
    print(f"Maximum path delay: {summary['max_path_delay_ns']} ns")
    print(f"Unmatched non-empty lines: {unmatched}")

    try:
        if args.csv:
            write_csv(args.csv, records)
            print(f"CSV exported to: {args.csv}")

        if args.json:
            args.json.parent.mkdir(parents=True, exist_ok=True)
            args.json.write_text(
                json.dumps(summary, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )
            print(f"JSON exported to: {args.json}")

    except OSError as exc:
        print(
            f"Error: Unable to write output file: {exc}",
            file=sys.stderr,
        )
        return 2

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
