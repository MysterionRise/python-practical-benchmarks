"""Shared pytest fixtures for benchmark tests."""

import importlib
import sys
from pathlib import Path

import pytest

# Add project root to path for imports
PROJECT_ROOT = Path(__file__).parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


# Benchmark categories from run_all_tests.py
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
        "free_threaded_perf_test",
        "jit_numeric_perf_test",
    ],
}

ALL_BENCHMARKS = []
for benchmarks in BENCHMARKS.values():
    ALL_BENCHMARKS.extend(benchmarks)


# Quick iteration settings to reduce test time
QUICK_ITERATIONS = {
    "iterate_2d_array_peft_test": {"PERF_ITERATIONS": 2, "ARRAY_SIZE": 10},
    "iterate_df_pandas_perf_test": {"PERF_ITERATIONS": 2},
    "dict_access_perf_test": {"PERF_ITERATIONS": 10, "DICTIONARY_SIZE": 10},
    "string_concat_perf_test": {"PERF_ITERATIONS": 2, "NUM_STRINGS": 10},
    "list_operations_perf_test": {"PERF_ITERATIONS": 2, "NUM_ITEMS": 10},
    "file_io_perf_test": {"PERF_ITERATIONS": 2, "NUM_LINES": 10},
    "json_perf_test": {"PERF_ITERATIONS": 2, "DATA_SIZE": 2},
    "set_operations_perf_test": {"PERF_ITERATIONS": 10, "DATA_SIZE": 10},
    "function_call_perf_test": {"PERF_ITERATIONS": 100, "CALL_COUNT": 10},
    "data_structure_lookup_perf_test": {"PERF_ITERATIONS": 10, "LOOKUP_COUNT": 10},
    "concurrency_patterns_perf_test": {"NUM_TASKS": 2, "IO_SLEEP_DURATION": 0.001},
    "regex_performance_perf_test": {"PERF_ITERATIONS": 2, "NUM_STRINGS": 10},
    "object_creation_patterns_perf_test": {"PERF_ITERATIONS": 100, "ACCESS_ITERATIONS": 100},
    "deep_copy_strategies_perf_test": {
        "PERF_ITERATIONS_SIMPLE": 10,
        "PERF_ITERATIONS_NESTED": 2,
        "PERF_ITERATIONS_OBJECTS": 10,
    },
    "generator_vs_iterator_perf_test": {"DATASET_SIZE": 100, "PIPELINE_SIZE": 10},
    "attribute_access_perf_test": {"ACCESS_ITERATIONS": 100},
    "exception_handling_perf_test": {
        "ITERATIONS": 100,
        "NESTED_ITERATIONS": 10,
        "EXCEPTION_ITERATIONS": 10,
    },
    "serialization_formats_perf_test": {"ITERATIONS": 2},
    "context_manager_perf_test": {"ITERATIONS": 100, "NESTED_ITERATIONS": 10, "FILE_ITERATIONS": 10},
    "import_strategies_perf_test": {"ITERATIONS": 100, "ACCESS_ITERATIONS": 100},
    "free_threaded_perf_test": {"NUM_WORKERS": 2, "WORK_ITERATIONS": 100},
    "jit_numeric_perf_test": {"PERF_ITERATIONS": 1, "NUMERIC_ITERATIONS": 100, "MANDELBROT_SIZE": 10},
}


@pytest.fixture
def benchmark_loader():
    """Fixture to load benchmark modules with quick iterations."""

    def load(module_name):
        """Load a benchmark module and apply quick iteration settings."""
        module = importlib.import_module(module_name)

        # Apply quick iteration settings
        if module_name in QUICK_ITERATIONS:
            for attr, value in QUICK_ITERATIONS[module_name].items():
                if hasattr(module, attr):
                    setattr(module, attr, value)

        return module

    return load


@pytest.fixture
def all_benchmark_names():
    """Return list of all benchmark module names."""
    return ALL_BENCHMARKS.copy()


@pytest.fixture
def benchmark_categories():
    """Return benchmark categories dictionary."""
    return BENCHMARKS.copy()
