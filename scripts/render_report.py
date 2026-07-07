#!/usr/bin/env python3
"""Render benchmark runner JSON into a compact Markdown report."""

from __future__ import annotations

import argparse
import json
from collections.abc import Iterable
from pathlib import Path
from typing import Any


def _format_seconds(value: Any) -> str:
    """Format a duration in seconds for human-readable Markdown tables."""
    if value is None:
        return "n/a"
    seconds = float(value)
    if seconds < 0.000001:
        return f"{seconds * 1_000_000_000:.1f} ns"
    if seconds < 0.001:
        return f"{seconds * 1_000_000:.1f} us"
    if seconds < 1:
        return f"{seconds * 1000:.3f} ms"
    return f"{seconds:.3f} s"


def _count_cases(cases: Iterable[dict[str, Any]], status: str) -> int:
    """Count cases with one status."""
    return sum(1 for case in cases if case.get("status") == status)


def _median_range(cases: list[dict[str, Any]]) -> str:
    """Return min and max median duration across passed cases."""
    medians = [
        float(case["seconds_median"])
        for case in cases
        if case.get("status") == "passed" and case.get("seconds_median") is not None
    ]
    if not medians:
        return "n/a"
    return f"{_format_seconds(min(medians))} - {_format_seconds(max(medians))}"


def render_markdown(payload: dict[str, Any]) -> str:
    """Render a benchmark JSON payload to Markdown."""
    environment = payload.get("environment", {})
    summary = payload.get("summary", {})
    benchmarks = payload.get("benchmarks", [])

    lines = [
        "# Python Practical Benchmarks Report",
        "",
        "> Machine-specific benchmark evidence. Use it to verify reproducibility, not as a universal ranking.",
        "",
        "## Environment",
        "",
        "| Field | Value |",
        "| --- | --- |",
        f"| Timestamp UTC | {environment.get('timestamp_utc', 'unknown')} |",
        f"| Python | {environment.get('python_implementation', 'Python')} {environment.get('python_version', 'unknown')} |",
        f"| Platform | {environment.get('platform', 'unknown')} |",
        f"| Machine | {environment.get('machine', 'unknown')} |",
        f"| CPU count | {environment.get('cpu_count', 'unknown')} |",
        f"| Git SHA | {environment.get('git_sha', 'unknown')} |",
        f"| Quick mode | {environment.get('quick', 'unknown')} |",
        f"| Runs / warmups | {environment.get('runs', 'unknown')} / {environment.get('warmups', 'unknown')} |",
        "",
        "## Summary",
        "",
        "| Metric | Count |",
        "| --- | ---: |",
        f"| Benchmarks total | {summary.get('total', 0)} |",
        f"| Benchmarks passed | {summary.get('passed', 0)} |",
        f"| Benchmarks failed | {summary.get('failed', 0)} |",
        f"| Benchmarks skipped | {summary.get('skipped', 0)} |",
        f"| Cases total | {summary.get('cases_total', 0)} |",
        f"| Cases passed | {summary.get('cases_passed', 0)} |",
        f"| Cases failed | {summary.get('cases_failed', 0)} |",
        f"| Cases skipped | {summary.get('cases_skipped', 0)} |",
        "",
        "## Benchmark Summary",
        "",
        "| Benchmark | Category | Status | Cases passed | Cases skipped | Cases failed | Median range |",
        "| --- | --- | --- | ---: | ---: | ---: | ---: |",
    ]

    skipped_cases = []
    failed_cases = []
    for benchmark in benchmarks:
        cases = list(benchmark.get("cases", []))
        module = benchmark.get("module", "unknown")
        lines.append(
            "| "
            f"`{module}` | "
            f"{benchmark.get('category', 'unknown')} | "
            f"{benchmark.get('status', 'unknown')} | "
            f"{_count_cases(cases, 'passed')} | "
            f"{_count_cases(cases, 'skipped')} | "
            f"{_count_cases(cases, 'failed')} | "
            f"{_median_range(cases)} |"
        )
        for case in cases:
            if case.get("status") == "skipped":
                skipped_cases.append((module, case))
            elif case.get("status") == "failed":
                failed_cases.append((module, case))

    if skipped_cases:
        lines.extend(["", "## Explicit Skips", ""])
        for module, case in skipped_cases:
            lines.append(f"- `{module}.{case.get('name', 'unknown')}`: {case.get('reason', 'no reason provided')}")

    if failed_cases:
        lines.extend(["", "## Failed Cases", ""])
        for module, case in failed_cases:
            lines.append(f"- `{module}.{case.get('name', 'unknown')}`: {case.get('error', 'no error provided')}")

    errors = [
        (benchmark.get("module", "unknown"), error) for benchmark in benchmarks for error in benchmark.get("errors", [])
    ]
    if errors:
        lines.extend(["", "## Benchmark Errors", ""])
        for module, error in errors:
            lines.append(f"- `{module}`: {error.get('message', 'no error message')}")

    lines.append("")
    return "\n".join(lines)


def build_parser() -> argparse.ArgumentParser:
    """Build the report renderer CLI parser."""
    parser = argparse.ArgumentParser(description="Render benchmark JSON as Markdown")
    parser.add_argument("input", help="Path to run_all_tests.py JSON output")
    parser.add_argument("--output", help="Write Markdown report to this path")
    return parser


def main() -> int:
    """Run the report renderer CLI."""
    args = build_parser().parse_args()
    payload = json.loads(Path(args.input).read_text(encoding="utf-8"))
    report = render_markdown(payload)

    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(report, encoding="utf-8")
    else:
        print(report)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
