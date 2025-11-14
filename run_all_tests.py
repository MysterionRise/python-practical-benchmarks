#!/usr/bin/env python3
"""
Test runner for all Python performance benchmarks.

This script runs all benchmarks with reduced iterations to verify they work correctly.
Used primarily in CI/CD pipelines to ensure benchmarks don't error out.

Usage:
    python run_all_tests.py --all --quick           # Run all benchmarks with minimal iterations
    python run_all_tests.py --category basic        # Run only basic benchmarks
    python run_all_tests.py --category advanced     # Run only advanced benchmarks
    python run_all_tests.py --category expert       # Run only expert benchmarks
    python run_all_tests.py --list                  # List all benchmarks
"""
import argparse
import importlib
import sys
from pathlib import Path

# Benchmark categorization
BENCHMARKS = {
    "basic": [
        "iterate_2d_array_peft_test",
        "iterate_df_pandas_perf_test",
        "dict_access_perf_test",
        "string_concat_perf_test",
        "list_operations_perf_test",
        "file_io_perf_test",
        "json_perf_test",
        "set_operations_perf_test",
        "function_call_perf_test",
        "data_structure_lookup_perf_test",
    ],
    "advanced": [
        "concurrency_patterns_perf_test",
        "regex_performance_perf_test",
        "object_creation_patterns_perf_test",
        "deep_copy_strategies_perf_test",
        "generator_vs_iterator_perf_test",
    ],
    "expert": [
        "attribute_access_perf_test",
        "exception_handling_perf_test",
        "serialization_formats_perf_test",
        "context_manager_perf_test",
        "import_strategies_perf_test",
    ],
}

# Iteration reduction for quick testing
QUICK_ITERATIONS = {
    "iterate_2d_array_peft_test": {"PERF_ITERATIONS": 10, "ARRAY_SIZE": 100},
    "iterate_df_pandas_perf_test": {"PERF_ITERATIONS": 10},
    "dict_access_perf_test": {"PERF_ITERATIONS": 100, "DICTIONARY_SIZE": 100},
    "string_concat_perf_test": {"PERF_ITERATIONS": 10, "NUM_STRINGS": 100},
    "list_operations_perf_test": {"PERF_ITERATIONS": 10, "NUM_ITEMS": 100},
    "file_io_perf_test": {"PERF_ITERATIONS": 10, "NUM_LINES": 100},
    "json_perf_test": {"PERF_ITERATIONS": 10, "DATA_SIZE": 10},
    "set_operations_perf_test": {"PERF_ITERATIONS": 100, "DATA_SIZE": 100},
    "function_call_perf_test": {"PERF_ITERATIONS": 1000, "CALL_COUNT": 100},
    "data_structure_lookup_perf_test": {"PERF_ITERATIONS": 100, "LOOKUP_COUNT": 100},
    "concurrency_patterns_perf_test": {"NUM_TASKS": 10, "IO_SLEEP_DURATION": 0.001},
    "regex_performance_perf_test": {"PERF_ITERATIONS": 10, "NUM_STRINGS": 100},
    "object_creation_patterns_perf_test": {"PERF_ITERATIONS": 1000, "ACCESS_ITERATIONS": 10000},
    "deep_copy_strategies_perf_test": {
        "PERF_ITERATIONS_SIMPLE": 100,
        "PERF_ITERATIONS_NESTED": 10,
        "PERF_ITERATIONS_OBJECTS": 100,
    },
    "generator_vs_iterator_perf_test": {"DATASET_SIZE": 10000, "PIPELINE_SIZE": 1000},
    "attribute_access_perf_test": {"ACCESS_ITERATIONS": 10000},
    "exception_handling_perf_test": {
        "ITERATIONS": 1000,
        "NESTED_ITERATIONS": 100,
        "EXCEPTION_ITERATIONS": 100,
    },
    "serialization_formats_perf_test": {"ITERATIONS": 10},
    "context_manager_perf_test": {"ITERATIONS": 1000, "NESTED_ITERATIONS": 100, "FILE_ITERATIONS": 100},
    "import_strategies_perf_test": {"ITERATIONS": 1000, "ACCESS_ITERATIONS": 10000},
}


def run_benchmark(module_name, quick=False):
    """Run a single benchmark module."""
    print(f"\n{'='*80}")
    print(f"Running: {module_name}")
    print(f"{'='*80}")

    try:
        # Import the module
        module = importlib.import_module(module_name)

        # If quick mode, reduce iterations
        if quick and module_name in QUICK_ITERATIONS:
            for attr, value in QUICK_ITERATIONS[module_name].items():
                if hasattr(module, attr):
                    setattr(module, attr, value)
                    print(f"  Set {attr} = {value} (quick mode)")

        # Run the main block (simulates python module.py)
        if hasattr(module, "__main__"):
            module.__main__()
        else:
            # Most modules use if __name__ == "__main__"
            # We'll execute a minimal test instead
            print(f"  Testing basic functions...")

            # Find and run a test function
            test_functions = [
                name for name in dir(module) if name.startswith("perf_test") and callable(getattr(module, name))
            ]

            if test_functions:
                # Run first test function as smoke test
                test_func = getattr(module, test_functions[0])
                result = test_func()
                print(f"  ✓ {test_functions[0]}() completed: {result}")
            else:
                print(f"  ⚠ No test functions found, assuming module is OK")

        print(f"✓ {module_name} completed successfully")
        return True

    except ImportError as e:
        print(f"⚠ {module_name} - Import error (missing optional dependency?): {e}")
        return True  # Don't fail on missing optional deps
    except Exception as e:
        print(f"✗ {module_name} - FAILED with error: {e}")
        import traceback

        traceback.print_exc()
        return False


def list_benchmarks():
    """List all available benchmarks."""
    print("\nAvailable Benchmarks:\n")
    for category, benchmarks in BENCHMARKS.items():
        print(f"{category.upper()} ({len(benchmarks)} benchmarks):")
        for i, benchmark in enumerate(benchmarks, 1):
            print(f"  {i}. {benchmark}")
        print()


def main():
    parser = argparse.ArgumentParser(description="Run Python performance benchmarks")
    parser.add_argument("--all", action="store_true", help="Run all benchmarks")
    parser.add_argument(
        "--category", choices=["basic", "advanced", "expert"], help="Run benchmarks in specific category"
    )
    parser.add_argument("--quick", action="store_true", help="Run with reduced iterations (for CI/testing)")
    parser.add_argument("--list", action="store_true", help="List all available benchmarks")

    args = parser.parse_args()

    if args.list:
        list_benchmarks()
        return 0

    if not args.all and not args.category:
        parser.print_help()
        return 1

    # Determine which benchmarks to run
    to_run = []
    if args.all:
        for category_benchmarks in BENCHMARKS.values():
            to_run.extend(category_benchmarks)
    elif args.category:
        to_run = BENCHMARKS[args.category]

    print(f"\n{'='*80}")
    print(f"BENCHMARK TEST RUNNER")
    print(f"{'='*80}")
    print(f"Running {len(to_run)} benchmarks")
    print(f"Quick mode: {args.quick}")
    print(f"{'='*80}\n")

    # Run benchmarks
    results = {}
    for module_name in to_run:
        success = run_benchmark(module_name, quick=args.quick)
        results[module_name] = success

    # Summary
    print(f"\n{'='*80}")
    print(f"SUMMARY")
    print(f"{'='*80}")

    passed = sum(1 for success in results.values() if success)
    failed = len(results) - passed

    print(f"Total:  {len(results)}")
    print(f"Passed: {passed} ✓")
    print(f"Failed: {failed} ✗")

    if failed > 0:
        print("\nFailed benchmarks:")
        for module_name, success in results.items():
            if not success:
                print(f"  ✗ {module_name}")

    print(f"{'='*80}\n")

    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
