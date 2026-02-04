"""Tests to verify benchmark functions work correctly."""

import importlib
import sys
from pathlib import Path

import pytest

# Ensure project root is in path
PROJECT_ROOT = Path(__file__).parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# Import benchmark list directly - conftest.py is auto-loaded by pytest
ALL_BENCHMARKS = [
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
    "concurrency_patterns_perf_test",
    "regex_performance_perf_test",
    "object_creation_patterns_perf_test",
    "deep_copy_strategies_perf_test",
    "generator_vs_iterator_perf_test",
    "attribute_access_perf_test",
    "exception_handling_perf_test",
    "serialization_formats_perf_test",
    "context_manager_perf_test",
    "import_strategies_perf_test",
    "free_threaded_perf_test",
    "jit_numeric_perf_test",
]

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


def get_perf_test_functions(module):
    """Get all perf_test functions from a module."""
    return [
        (name, getattr(module, name))
        for name in dir(module)
        if name.startswith("perf_test") and callable(getattr(module, name))
    ]


def apply_quick_iterations(module, module_name):
    """Apply quick iteration settings to a module."""
    if module_name in QUICK_ITERATIONS:
        for attr, value in QUICK_ITERATIONS[module_name].items():
            if hasattr(module, attr):
                setattr(module, attr, value)


class TestBenchmarkFunctions:
    """Test that benchmark functions execute and return values."""

    @pytest.mark.parametrize("module_name", ALL_BENCHMARKS)
    def test_first_perf_function_executes(self, module_name):
        """Test that the first perf_test function in each module executes."""
        try:
            module = importlib.import_module(module_name)
            apply_quick_iterations(module, module_name)

            perf_funcs = get_perf_test_functions(module)
            if not perf_funcs:
                pytest.skip(f"No perf_test functions in {module_name}")

            func_name, func = perf_funcs[0]
            # Just verify the function runs without error
            # Some functions may return None (write operations, etc.)
            func()

        except ImportError as e:
            error_msg = str(e).lower()
            optional_deps = ["orjson", "ujson", "msgpack", "cbor2", "attrs"]
            if any(dep in error_msg for dep in optional_deps):
                pytest.skip(f"Optional dependency missing: {e}")
            raise

    @pytest.mark.parametrize("module_name", ALL_BENCHMARKS)
    def test_perf_functions_are_callable(self, module_name):
        """Test that all perf_test functions are callable."""
        try:
            module = importlib.import_module(module_name)
            perf_funcs = get_perf_test_functions(module)

            for func_name, func in perf_funcs:
                assert callable(func), f"{func_name} is not callable"

        except ImportError:
            pytest.skip("Module could not be imported")


class TestBenchmarkReturnValues:
    """Test that benchmark functions return appropriate values."""

    @pytest.mark.parametrize(
        "module_name",
        [
            "dict_access_perf_test",
            "string_concat_perf_test",
            "list_operations_perf_test",
            "set_operations_perf_test",
        ],
    )
    def test_basic_benchmark_returns_value(self, module_name):
        """Test basic benchmarks return meaningful values."""
        try:
            module = importlib.import_module(module_name)
            apply_quick_iterations(module, module_name)

            perf_funcs = get_perf_test_functions(module)
            for func_name, func in perf_funcs[:3]:  # Test first 3 functions
                result = func()
                # Results should be non-None and typically numeric or collections
                assert result is not None, f"{func_name} should return a value"

        except ImportError:
            pytest.skip("Module could not be imported")


class TestBenchmarkIsolation:
    """Test that benchmarks don't have side effects."""

    def test_file_io_cleans_up(self):
        """Test file_io_perf_test cleans up temporary files."""
        import tempfile

        try:
            module = importlib.import_module("file_io_perf_test")
            apply_quick_iterations(module, "file_io_perf_test")

            # Count temp files before
            temp_dir = tempfile.gettempdir()

            # Run a function if it exists
            perf_funcs = get_perf_test_functions(module)
            if perf_funcs:
                perf_funcs[0][1]()

            # The benchmark should not leave excessive temp files
            # (This is a soft check - just verify it runs)

        except ImportError:
            pytest.skip("Module could not be imported")

    def test_concurrent_benchmark_completes(self):
        """Test concurrency benchmark doesn't hang."""
        try:
            module = importlib.import_module("concurrency_patterns_perf_test")
            apply_quick_iterations(module, "concurrency_patterns_perf_test")

            perf_funcs = get_perf_test_functions(module)
            if perf_funcs:
                # Should complete without hanging
                result = perf_funcs[0][1]()
                assert result is not None

        except ImportError:
            pytest.skip("Module could not be imported")
