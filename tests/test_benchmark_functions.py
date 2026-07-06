"""Tests to verify benchmark functions work correctly."""

import importlib
from pathlib import Path

import pytest

from benchmark_manifest import BENCHMARK_SPECS, all_benchmark_modules, get_benchmark_spec
from run_all_tests import collect_benchmark_cases, missing_dependencies

PROJECT_ROOT = Path(__file__).parent.parent


ALL_BENCHMARKS = all_benchmark_modules()


def import_or_skip_missing_required(module_name):
    """Import a benchmark module or skip when required deps are absent locally."""
    spec = get_benchmark_spec(module_name)
    missing_required = missing_dependencies(spec.required_dependencies)
    if missing_required:
        pytest.skip(f"Required dependencies missing locally: {', '.join(missing_required)}")
    return importlib.import_module(module_name)


def apply_quick_iterations(module, module_name):
    """Apply quick iteration settings to a module."""
    spec = get_benchmark_spec(module_name)
    for attr, value in spec.quick_overrides.items():
        if hasattr(module, attr):
            setattr(module, attr, value)
    reset_func = getattr(module, "reset_benchmark_data", None)
    if callable(reset_func):
        reset_func()


class TestBenchmarkFunctions:
    """Test that benchmark functions execute and return values."""

    @pytest.mark.parametrize("module_name", ALL_BENCHMARKS)
    def test_first_perf_function_executes(self, module_name):
        """Test that the first perf_test function in each module executes."""
        module = import_or_skip_missing_required(module_name)
        apply_quick_iterations(module, module_name)

        perf_funcs = collect_benchmark_cases(module)
        assert perf_funcs, f"No perf_test functions in {module_name}"

        perf_funcs[0]()

    @pytest.mark.parametrize("module_name", ALL_BENCHMARKS)
    def test_perf_functions_are_callable(self, module_name):
        """Test that all perf_test functions are callable."""
        module = import_or_skip_missing_required(module_name)
        for func in collect_benchmark_cases(module):
            assert callable(func), f"{func.__name__} is not callable"

    def test_case_discovery_uses_source_order(self):
        """Test runner case discovery avoids lexicographic perf_test10 ordering."""
        module = import_or_skip_missing_required("attribute_access_perf_test")
        case_names = [func.__name__ for func in collect_benchmark_cases(module)]
        assert case_names[0] == "perf_test1_read_normal"
        assert case_names.index("perf_test10_write_normal") > case_names.index("perf_test9_read_descriptor")


class TestBenchmarkReturnValues:
    """Test that representative benchmark functions return meaningful values."""

    @pytest.mark.parametrize(
        "module_name",
        [
            "dict_access_perf_test",
            "string_concat_perf_test",
            "list_operations_perf_test",
            "set_operations_perf_test",
            "data_structure_lookup_perf_test",
        ],
    )
    def test_basic_benchmark_returns_value(self, module_name):
        """Test basic benchmarks return meaningful values."""
        module = import_or_skip_missing_required(module_name)
        apply_quick_iterations(module, module_name)

        for func in collect_benchmark_cases(module)[:3]:
            result = func()
            assert result is not None, f"{func.__name__} should return a value"


class TestBenchmarkIsolation:
    """Test that benchmarks don't have disruptive side effects."""

    def test_file_io_cleans_up(self):
        """Test file_io_perf_test creates temp files lazily and cleans them up."""
        module = import_or_skip_missing_required("file_io_perf_test")
        apply_quick_iterations(module, "file_io_perf_test")

        assert module.TEST_FILE is None
        collect_benchmark_cases(module)[0]()
        assert module.TEST_FILE is not None
        module.cleanup_test_file()
        assert module.TEST_FILE is None

    def test_all_manifest_specs_have_quick_overrides(self):
        """Test every benchmark has quick-mode settings in the manifest."""
        missing = [spec.module for spec in BENCHMARK_SPECS if not spec.quick_overrides]
        assert not missing
