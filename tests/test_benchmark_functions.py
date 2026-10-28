"""Tests to verify benchmark functions work correctly."""

import importlib
from pathlib import Path

import pytest

from benchmark_manifest import BENCHMARK_SPECS, all_benchmark_modules, get_benchmark_spec
from run_all_tests import (
    case_text,
    collect_benchmark_cases,
    execute_case,
    missing_dependencies,
    missing_optional_dependencies,
    optional_skip_dependency,
)

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

    @pytest.mark.parametrize("module_name", ALL_BENCHMARKS)
    def test_every_case_returns_value(self, module_name):
        """Test every runnable case returns a value, so results can be sanity-checked."""
        module = import_or_skip_missing_required(module_name)
        apply_quick_iterations(module, module_name)
        missing_optional = missing_optional_dependencies(get_benchmark_spec(module_name).optional_dependencies)

        returned_none = []
        for func in collect_benchmark_cases(module):
            if optional_skip_dependency(func, missing_optional):
                continue
            try:
                result = execute_case(func)
            except PermissionError:
                if "multiprocessing" not in case_text(func) and "processpool" not in case_text(func):
                    raise
                continue  # sandboxes may forbid process creation; the runner reports these as skips
            if result is None:
                returned_none.append(func.__name__)

        assert not returned_none, f"{module_name} cases returned None: {returned_none}"


# Cases within each group compute the same thing in different ways, so a fair comparison needs equal results.
EQUIVALENT_CASES = [
    ("iterate_2d_array_perf_test", ("perf_test", "perf_test2", "perf_test3", "perf_test4", "perf_test5")),
    (
        "dict_access_perf_test",
        ("perf_test1_dict_key", "perf_test2_dict_get", "perf_test3_dict_setdefault", "perf_test4_defaultdict"),
    ),
    ("list_operations_perf_test", tuple(f"perf_test{n}" for n in range(1, 8))),
    (
        "generator_vs_iterator_perf_test",
        ("perf_test6_list_pipeline", "perf_test7_generator_pipeline", "perf_test8_itertools_pipeline"),
    ),
    ("exception_handling_perf_test", ("perf_test9_type_lbyl", "perf_test10_type_eafp")),
    (
        "deep_copy_strategies_perf_test",
        ("perf_test9_nested_manual", "perf_test10_nested_deepcopy", "perf_test11_nested_json"),
    ),
]


def normalized(result):
    """Flatten nested lists and NumPy arrays so equivalent results compare equal."""
    if hasattr(result, "tolist"):
        result = result.tolist()
    if isinstance(result, list) and result and isinstance(result[0], list):
        return [value for row in result for value in row]
    return result


class TestBenchmarkEquivalence:
    """Test that compared cases do the same work, so their timings are comparable."""

    @pytest.mark.parametrize(("module_name", "case_names"), EQUIVALENT_CASES)
    def test_compared_cases_compute_the_same_result(self, module_name, case_names):
        """Test that each group of compared cases returns equal results under quick settings."""
        module = import_or_skip_missing_required(module_name)
        apply_quick_iterations(module, module_name)
        results = {name: normalized(getattr(module, name)()) for name in case_names}
        reference = results[case_names[0]]
        different = [name for name, result in results.items() if result != reference]
        assert not different, f"{module_name}: {different} differ from {case_names[0]}"


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
