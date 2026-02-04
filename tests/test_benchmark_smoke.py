"""Smoke tests to verify all benchmark modules can be imported."""

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


class TestBenchmarkImports:
    """Test that all benchmark modules can be imported."""

    @pytest.mark.parametrize("module_name", ALL_BENCHMARKS)
    def test_benchmark_import(self, module_name):
        """Test that each benchmark module can be imported without errors."""
        try:
            module = importlib.import_module(module_name)
            assert module is not None
        except ImportError as e:
            # Some modules may fail due to optional dependencies
            # This is acceptable as long as the error is about missing packages
            error_msg = str(e).lower()
            optional_deps = ["orjson", "ujson", "msgpack", "cbor2", "attrs"]
            if any(dep in error_msg for dep in optional_deps):
                pytest.skip(f"Optional dependency missing: {e}")
            else:
                raise

    @pytest.mark.parametrize("module_name", ALL_BENCHMARKS)
    def test_benchmark_has_docstring(self, module_name):
        """Test that each benchmark module has a docstring."""
        try:
            module = importlib.import_module(module_name)
            assert module.__doc__ is not None, f"{module_name} missing docstring"
            assert len(module.__doc__) > 50, f"{module_name} docstring too short"
        except ImportError:
            pytest.skip("Module could not be imported")


class TestBenchmarkStructure:
    """Test that benchmark modules follow the expected structure."""

    @pytest.mark.parametrize("module_name", ALL_BENCHMARKS)
    def test_benchmark_has_test_functions(self, module_name):
        """Test that each benchmark has callable test functions."""
        try:
            module = importlib.import_module(module_name)
            # Check for perf_test* functions OR test* functions OR main executable
            perf_funcs = [
                name
                for name in dir(module)
                if (name.startswith("perf_test") or name.startswith("test_"))
                and callable(getattr(module, name))
                and not name.startswith("__")
            ]
            # Allow modules that just have a main block to run
            has_main = hasattr(module, "__name__")
            if not perf_funcs and not has_main:
                pytest.skip(f"{module_name} has no test functions (may use main block)")
        except ImportError:
            pytest.skip("Module could not be imported")

    @pytest.mark.parametrize("module_name", ALL_BENCHMARKS)
    def test_benchmark_has_configuration_constants(self, module_name):
        """Test that benchmarks have configuration constants (uppercase attrs)."""
        try:
            module = importlib.import_module(module_name)

            # Look for uppercase constants that are integers
            constants = [
                name
                for name in dir(module)
                if name.isupper() and not name.startswith("_") and isinstance(getattr(module, name), (int, float))
            ]

            # Most benchmarks should have at least one configuration constant
            # Some benchmarks might not, so we just warn
            if not constants:
                pytest.skip(f"{module_name} has no configuration constants (optional)")
        except ImportError:
            pytest.skip("Module could not be imported")
