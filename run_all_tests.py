#!/usr/bin/env python3
"""Run Python performance benchmarks with structured, repeatable reporting."""

from __future__ import annotations

import argparse
import asyncio
import importlib
import importlib.util
import inspect
import json
import os
import platform
import statistics
import subprocess
import sys
import time
import traceback
from datetime import datetime, timezone
from pathlib import Path
from shutil import which
from types import ModuleType
from typing import Any, Callable, Optional, Union

from benchmark_manifest import (
    BENCHMARK_SPECS,
    CATEGORIES,
    BenchmarkSpec,
    OptionalDependency,
    benchmarks_by_category,
    get_benchmark_spec,
    quick_iterations,
)

BENCHMARKS = benchmarks_by_category()
QUICK_ITERATIONS = quick_iterations()
MEASUREMENT_RUNS = 3
WARMUP_RUNS = 1


def dependency_available(import_name: str) -> bool:
    """Return whether an import name can be resolved."""
    return importlib.util.find_spec(import_name) is not None


def missing_dependencies(import_names: tuple[str, ...]) -> list[str]:
    """Return missing dependencies from a tuple of import names."""
    return [import_name for import_name in import_names if not dependency_available(import_name)]


def missing_optional_dependencies(dependencies: tuple[OptionalDependency, ...]) -> list[OptionalDependency]:
    """Return optional dependencies that are not importable."""
    return [dependency for dependency in dependencies if not dependency_available(dependency.import_name)]


def apply_quick_overrides(module: ModuleType, spec: BenchmarkSpec, quick: bool) -> dict[str, Any]:
    """Apply quick-mode constants to a benchmark module."""
    applied: dict[str, Any] = {}
    if not quick:
        return applied

    for attr, value in spec.quick_overrides.items():
        if hasattr(module, attr):
            setattr(module, attr, value)
            applied[attr] = value

    reset_func = getattr(module, "reset_benchmark_data", None)
    if callable(reset_func):
        reset_func()

    return applied


def collect_benchmark_cases(module: ModuleType) -> list[Callable[[], Any]]:
    """Collect top-level perf_test functions in source order."""
    cases = []
    seen_ids = set()
    for name, value in inspect.getmembers(module, inspect.isfunction):
        if name.startswith("perf_test") and value.__module__ == module.__name__ and id(value) not in seen_ids:
            cases.append(value)
            seen_ids.add(id(value))
    return sorted(cases, key=lambda func: func.__code__.co_firstlineno)


def case_text(func: Callable[[], Any]) -> str:
    """Return searchable text for optional dependency case matching."""
    return f"{func.__name__} {inspect.getdoc(func) or ''}".lower()


def optional_skip_dependency(
    func: Callable[[], Any],
    missing_optional: list[OptionalDependency],
) -> Optional[OptionalDependency]:
    """Return the missing optional dependency that controls this case, if any."""
    searchable = case_text(func)
    for dependency in missing_optional:
        if any(marker.lower() in searchable for marker in dependency.markers):
            return dependency
    return None


def execute_case(func: Callable[[], Any]) -> Any:
    """Execute sync or async benchmark case once."""
    if inspect.iscoroutinefunction(func):
        return asyncio.run(func())
    return func()


def preview_result(result: Any) -> str | None:
    """Return a compact preview without dumping large benchmark data."""
    if result is None:
        return None
    if isinstance(result, str):
        return f"str(len={len(result)}, preview={result[:120]!r})"
    if isinstance(result, bytes):
        return f"bytes(len={len(result)}, preview={result[:40]!r})"
    if isinstance(result, (list, tuple, set, dict)):
        return f"{type(result).__name__}(len={len(result)})"

    preview = repr(result)
    if len(preview) > 160:
        preview = f"{preview[:157]}..."
    return preview


def measure_case(
    func: Callable[[], Any],
    runs: int = MEASUREMENT_RUNS,
    warmups: int = WARMUP_RUNS,
) -> dict[str, Any]:
    """Warm up and measure one benchmark case."""
    result = None
    for _ in range(warmups):
        result = execute_case(func)

    timings = []
    for _ in range(runs):
        start = time.perf_counter()
        result = execute_case(func)
        timings.append(time.perf_counter() - start)

    return {
        "name": func.__name__,
        "status": "passed",
        "seconds_min": min(timings),
        "seconds_median": statistics.median(timings),
        "seconds_mean": statistics.mean(timings),
        "seconds_stdev": statistics.stdev(timings) if len(timings) > 1 else 0.0,
        "runs": runs,
        "warmups": warmups,
        "result_preview": preview_result(result),
    }


def skipped_case(func: Callable[[], Any], dependency: OptionalDependency) -> dict[str, Any]:
    """Build a structured skipped-case result."""
    return {
        "name": func.__name__,
        "status": "skipped",
        "seconds_min": None,
        "seconds_median": None,
        "seconds_mean": None,
        "seconds_stdev": None,
        "runs": 0,
        "warmups": 0,
        "result_preview": None,
        "reason": f"optional dependency not installed: {dependency.import_name}",
    }


def environment_skipped_case(func: Callable[[], Any], reason: str) -> dict[str, Any]:
    """Build a structured skipped-case result for environment limitations."""
    return {
        "name": func.__name__,
        "status": "skipped",
        "seconds_min": None,
        "seconds_median": None,
        "seconds_mean": None,
        "seconds_stdev": None,
        "runs": 0,
        "warmups": 0,
        "result_preview": None,
        "reason": reason,
    }


def failed_case(func: Callable[[], Any], exc: BaseException) -> dict[str, Any]:
    """Build a structured failed-case result."""
    return {
        "name": func.__name__,
        "status": "failed",
        "seconds_min": None,
        "seconds_median": None,
        "seconds_mean": None,
        "seconds_stdev": None,
        "runs": 0,
        "warmups": 0,
        "result_preview": None,
        "error": f"{type(exc).__name__}: {exc}",
    }


def run_benchmark(
    benchmark: Union[BenchmarkSpec, str],
    quick: bool = False,
    runs: int = MEASUREMENT_RUNS,
    warmups: int = WARMUP_RUNS,
    emit_text: bool = True,
) -> dict[str, Any]:
    """Run one benchmark module and return structured results."""
    spec = get_benchmark_spec(benchmark) if isinstance(benchmark, str) else benchmark
    result: dict[str, Any] = {
        "module": spec.module,
        "title": spec.title,
        "category": spec.category,
        "status": "passed",
        "cases": [],
        "skips": [],
        "errors": [],
        "quick_overrides": {},
    }

    if emit_text:
        print(f"\n{'=' * 80}")
        print(f"Running: {spec.module} ({spec.title})")
        print(f"{'=' * 80}")

    missing_required = missing_dependencies(spec.required_dependencies)
    if missing_required:
        result["status"] = "failed"
        for dependency in missing_required:
            error = {
                "type": "missing_required_dependency",
                "dependency": dependency,
                "message": f"Required dependency not installed: {dependency}",
            }
            result["errors"].append(error)
            if emit_text:
                print(f"  FAILED missing required dependency: {dependency}")
        return result

    try:
        module = importlib.import_module(spec.module)
        applied_overrides = apply_quick_overrides(module, spec, quick)
        result["quick_overrides"] = applied_overrides
        for attr, value in applied_overrides.items():
            if emit_text:
                print(f"  Set {attr} = {value} (quick mode)")

        cases = collect_benchmark_cases(module)
        if not cases:
            result["status"] = "failed"
            error = {"type": "no_cases", "message": "No top-level perf_test* functions found"}
            result["errors"].append(error)
            if emit_text:
                print("  FAILED no top-level perf_test* functions found")
            return result

        missing_optional = missing_optional_dependencies(spec.optional_dependencies)
        for func in cases:
            skipped_dependency = optional_skip_dependency(func, missing_optional)
            if skipped_dependency:
                case_result = skipped_case(func, skipped_dependency)
                result["cases"].append(case_result)
                result["skips"].append(
                    {
                        "case": func.__name__,
                        "dependency": skipped_dependency.import_name,
                        "reason": case_result["reason"],
                    }
                )
                if emit_text:
                    print(f"  SKIP {func.__name__}: {case_result['reason']}")
                continue

            try:
                case_result = measure_case(func, runs=runs, warmups=warmups)
                result["cases"].append(case_result)
                if emit_text:
                    print(
                        f"  OK   {func.__name__}: "
                        f"median={case_result['seconds_median']:.6f}s "
                        f"min={case_result['seconds_min']:.6f}s "
                        f"runs={case_result['runs']}"
                    )
            except PermissionError as exc:
                searchable = case_text(func)
                if "multiprocessing" in searchable or "processpool" in searchable:
                    reason = f"environment denied process creation: {exc}"
                    case_result = environment_skipped_case(func, reason)
                    result["cases"].append(case_result)
                    result["skips"].append({"case": func.__name__, "dependency": None, "reason": reason})
                    if emit_text:
                        print(f"  SKIP {func.__name__}: {reason}")
                    continue
                case_result = failed_case(func, exc)
                result["cases"].append(case_result)
                result["errors"].append(
                    {
                        "type": "case_failure",
                        "case": func.__name__,
                        "message": case_result["error"],
                        "traceback": traceback.format_exc(),
                    }
                )
                if emit_text:
                    print(f"  FAIL {func.__name__}: {case_result['error']}")
            except Exception as exc:  # noqa: BLE001 - runner must report all benchmark failures.
                case_result = failed_case(func, exc)
                result["cases"].append(case_result)
                result["errors"].append(
                    {
                        "type": "case_failure",
                        "case": func.__name__,
                        "message": case_result["error"],
                        "traceback": traceback.format_exc(),
                    }
                )
                if emit_text:
                    print(f"  FAIL {func.__name__}: {case_result['error']}")

    except Exception as exc:  # noqa: BLE001 - runner must report import and setup failures.
        result["errors"].append(
            {
                "type": "benchmark_failure",
                "message": f"{type(exc).__name__}: {exc}",
                "traceback": traceback.format_exc(),
            }
        )

    if result["errors"]:
        result["status"] = "failed"
    elif result["cases"] and all(case["status"] == "skipped" for case in result["cases"]):
        result["status"] = "skipped"
    else:
        result["status"] = "passed"

    if emit_text:
        print(f"  Result: {result['status'].upper()}")

    return result


def selected_benchmarks(run_all: bool, category: Optional[str]) -> list[BenchmarkSpec]:
    """Return benchmark specs selected by CLI arguments."""
    if run_all:
        return list(BENCHMARK_SPECS)
    if category:
        return [spec for spec in BENCHMARK_SPECS if spec.category == category]
    return []


def git_sha() -> Optional[str]:
    """Return the current git SHA if available."""
    git_path = which("git")
    if not git_path:
        return None
    try:
        completed = subprocess.run(
            [git_path, "rev-parse", "--short", "HEAD"],
            capture_output=True,
            check=False,
            text=True,
        )
    except OSError:
        return None
    if completed.returncode != 0:
        return None
    return completed.stdout.strip()


def environment_metadata(quick: bool, runs: int, warmups: int) -> dict[str, Any]:
    """Return environment metadata for structured benchmark output."""
    return {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "python_version": platform.python_version(),
        "python_implementation": platform.python_implementation(),
        "platform": platform.platform(),
        "machine": platform.machine(),
        "processor": platform.processor(),
        "cpu_count": os.cpu_count(),
        "git_sha": git_sha(),
        "quick": quick,
        "runs": runs,
        "warmups": warmups,
    }


def build_summary(benchmark_results: list[dict[str, Any]]) -> dict[str, int]:
    """Build benchmark-level and case-level summary counts."""
    case_results = [case for benchmark in benchmark_results for case in benchmark["cases"]]
    return {
        "total": len(benchmark_results),
        "passed": sum(1 for benchmark in benchmark_results if benchmark["status"] == "passed"),
        "failed": sum(1 for benchmark in benchmark_results if benchmark["status"] == "failed"),
        "skipped": sum(1 for benchmark in benchmark_results if benchmark["status"] == "skipped"),
        "cases_total": len(case_results),
        "cases_passed": sum(1 for case in case_results if case["status"] == "passed"),
        "cases_failed": sum(1 for case in case_results if case["status"] == "failed"),
        "cases_skipped": sum(1 for case in case_results if case["status"] == "skipped"),
    }


def build_payload(
    specs: list[BenchmarkSpec],
    quick: bool,
    emit_text: bool,
    runs: int = MEASUREMENT_RUNS,
    warmups: int = WARMUP_RUNS,
) -> dict[str, Any]:
    """Run selected benchmarks and build the complete result payload."""
    benchmark_results = [
        run_benchmark(spec, quick=quick, runs=runs, warmups=warmups, emit_text=emit_text) for spec in specs
    ]
    return {
        "environment": environment_metadata(quick=quick, runs=runs, warmups=warmups),
        "summary": build_summary(benchmark_results),
        "benchmarks": benchmark_results,
    }


def print_text_summary(payload: dict[str, Any]) -> None:
    """Print text summary for human-oriented runs."""
    summary = payload["summary"]
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"Total:        {summary['total']}")
    print(f"Passed:       {summary['passed']}")
    print(f"Failed:       {summary['failed']}")
    print(f"Skipped:      {summary['skipped']}")
    print(f"Cases total:  {summary['cases_total']}")
    print(f"Cases passed: {summary['cases_passed']}")
    print(f"Cases failed: {summary['cases_failed']}")
    print(f"Cases skipped:{summary['cases_skipped']}")

    failed = [benchmark for benchmark in payload["benchmarks"] if benchmark["status"] == "failed"]
    if failed:
        print("\nFailed benchmarks:")
        for benchmark in failed:
            print(f"  - {benchmark['module']}")
            for error in benchmark["errors"]:
                print(f"    {error['message']}")

    print("=" * 80 + "\n")


def write_json_output(output_path: str, payload: dict[str, Any]) -> None:
    """Write structured JSON results to a path."""
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")


def list_benchmarks() -> None:
    """List all available benchmarks."""
    print("\nAvailable Benchmarks:\n")
    for category in CATEGORIES:
        specs = [spec for spec in BENCHMARK_SPECS if spec.category == category]
        print(f"{category.upper()} ({len(specs)} benchmarks):")
        for index, spec in enumerate(specs, 1):
            print(f"  {index}. {spec.module} - {spec.title}")
        print()


def positive_int(value: str) -> int:
    """Parse a positive integer CLI value."""
    parsed = int(value)
    if parsed < 1:
        raise argparse.ArgumentTypeError("must be >= 1")
    return parsed


def non_negative_int(value: str) -> int:
    """Parse a non-negative integer CLI value."""
    parsed = int(value)
    if parsed < 0:
        raise argparse.ArgumentTypeError("must be >= 0")
    return parsed


def build_parser() -> argparse.ArgumentParser:
    """Build CLI parser."""
    parser = argparse.ArgumentParser(description="Run Python performance benchmarks")
    parser.add_argument("--all", action="store_true", help="Run all benchmarks")
    parser.add_argument("--category", choices=list(CATEGORIES), help="Run benchmarks in a specific category")
    parser.add_argument("--quick", action="store_true", help="Run with reduced iterations (for CI/testing)")
    parser.add_argument("--list", action="store_true", help="List all available benchmarks")
    parser.add_argument("--format", choices=["text", "json"], default="text", help="Output format")
    parser.add_argument("--output", help="Write structured JSON results to this path")
    parser.add_argument("--runs", type=positive_int, default=MEASUREMENT_RUNS, help="Measured runs per case")
    parser.add_argument("--warmups", type=non_negative_int, default=WARMUP_RUNS, help="Warmup executions per case")
    return parser


def parse_args() -> argparse.Namespace:
    """Parse CLI arguments."""
    parser = build_parser()
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    if args.list:
        list_benchmarks()
        return 0

    if not args.all and not args.category:
        build_parser().print_help()
        return 1

    specs = selected_benchmarks(args.all, args.category)
    emit_text = args.format == "text"

    if emit_text:
        print("\n" + "=" * 80)
        print("BENCHMARK TEST RUNNER")
        print("=" * 80)
        print(f"Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
        print(f"Running {len(specs)} benchmarks")
        print(f"Quick mode: {args.quick}")
        print(f"Measured runs per case: {args.runs}")
        print(f"Warmups per case: {args.warmups}")
        print(f"{'=' * 80}\n")

    payload = build_payload(specs, quick=args.quick, emit_text=emit_text, runs=args.runs, warmups=args.warmups)

    if args.output:
        write_json_output(args.output, payload)

    if args.format == "json" and not args.output:
        print(json.dumps(payload, indent=2, sort_keys=True))
    elif emit_text:
        print_text_summary(payload)

    return 0 if payload["summary"]["failed"] == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
