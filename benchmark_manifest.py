"""Benchmark catalog and quick-mode configuration."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

CATEGORIES = ("basic", "advanced", "expert")


@dataclass(frozen=True)
class OptionalDependency:
    """Optional dependency that controls one or more benchmark cases."""

    import_name: str
    markers: tuple[str, ...]


@dataclass(frozen=True)
class BenchmarkSpec:
    """Metadata needed to import, run, and report one benchmark module."""

    module: str
    title: str
    category: str
    required_dependencies: tuple[str, ...] = ()
    optional_dependencies: tuple[OptionalDependency, ...] = ()
    quick_overrides: dict[str, Any] = field(default_factory=dict)


BENCHMARK_SPECS: tuple[BenchmarkSpec, ...] = (
    BenchmarkSpec(
        module="iterate_2d_array_perf_test",
        title="2D Array Iteration",
        category="basic",
        required_dependencies=("numpy",),
        quick_overrides={"PERF_ITERATIONS": 10, "ARRAY_SIZE": 100},
    ),
    BenchmarkSpec(
        module="iterate_df_pandas_perf_test",
        title="Pandas DataFrame Iteration",
        category="basic",
        required_dependencies=("pandas",),
        quick_overrides={"PERF_ITERATIONS": 10},
    ),
    BenchmarkSpec(
        module="dict_access_perf_test",
        title="Dictionary Access",
        category="basic",
        quick_overrides={"PERF_ITERATIONS": 100, "DICTIONARY_SIZE": 100},
    ),
    BenchmarkSpec(
        module="string_concat_perf_test",
        title="String Concatenation",
        category="basic",
        quick_overrides={"PERF_ITERATIONS": 10, "NUM_STRINGS": 100},
    ),
    BenchmarkSpec(
        module="list_operations_perf_test",
        title="List Operations",
        category="basic",
        quick_overrides={"PERF_ITERATIONS": 10, "NUM_ITEMS": 100},
    ),
    BenchmarkSpec(
        module="file_io_perf_test",
        title="File I/O Operations",
        category="basic",
        quick_overrides={"PERF_ITERATIONS": 10, "NUM_LINES": 100},
    ),
    BenchmarkSpec(
        module="json_perf_test",
        title="JSON Serialization/Deserialization",
        category="basic",
        optional_dependencies=(
            OptionalDependency(import_name="ujson", markers=("ujson",)),
            OptionalDependency(import_name="orjson", markers=("orjson",)),
        ),
        quick_overrides={"PERF_ITERATIONS": 10, "DATA_SIZE": 10},
    ),
    BenchmarkSpec(
        module="set_operations_perf_test",
        title="Set Operations",
        category="basic",
        quick_overrides={"PERF_ITERATIONS": 100, "DATA_SIZE": 100},
    ),
    BenchmarkSpec(
        module="function_call_perf_test",
        title="Function Call Overhead",
        category="basic",
        quick_overrides={"PERF_ITERATIONS": 1000, "CALL_COUNT": 100},
    ),
    BenchmarkSpec(
        module="data_structure_lookup_perf_test",
        title="Data Structure Lookups",
        category="basic",
        required_dependencies=("numpy",),
        quick_overrides={"PERF_ITERATIONS": 100, "LOOKUP_COUNT": 100, "DATASET_SIZE": 100},
    ),
    BenchmarkSpec(
        module="concurrency_patterns_perf_test",
        title="Concurrency Patterns",
        category="advanced",
        quick_overrides={"NUM_TASKS": 10, "IO_SLEEP_DURATION": 0.001},
    ),
    BenchmarkSpec(
        module="regex_performance_perf_test",
        title="Regex Performance",
        category="advanced",
        quick_overrides={"PERF_ITERATIONS": 10, "NUM_STRINGS": 100},
    ),
    BenchmarkSpec(
        module="object_creation_patterns_perf_test",
        title="Object Creation Patterns",
        category="advanced",
        optional_dependencies=(OptionalDependency(import_name="attr", markers=("attrs",)),),
        quick_overrides={"PERF_ITERATIONS": 1000, "ACCESS_ITERATIONS": 10000},
    ),
    BenchmarkSpec(
        module="deep_copy_strategies_perf_test",
        title="Deep Copy Strategies",
        category="advanced",
        quick_overrides={
            "PERF_ITERATIONS_SIMPLE": 100,
            "PERF_ITERATIONS_NESTED": 10,
            "PERF_ITERATIONS_OBJECTS": 100,
        },
    ),
    BenchmarkSpec(
        module="generator_vs_iterator_perf_test",
        title="Generator vs Iterator Patterns",
        category="advanced",
        quick_overrides={"DATASET_SIZE": 10000, "PIPELINE_SIZE": 1000},
    ),
    BenchmarkSpec(
        module="attribute_access_perf_test",
        title="Attribute Access & Descriptors",
        category="expert",
        quick_overrides={"ACCESS_ITERATIONS": 10000},
    ),
    BenchmarkSpec(
        module="exception_handling_perf_test",
        title="Exception Handling",
        category="expert",
        quick_overrides={"ITERATIONS": 1000, "NESTED_ITERATIONS": 100, "EXCEPTION_ITERATIONS": 100},
    ),
    BenchmarkSpec(
        module="serialization_formats_perf_test",
        title="Serialization Formats",
        category="expert",
        required_dependencies=("numpy",),
        optional_dependencies=(
            OptionalDependency(import_name="orjson", markers=("orjson",)),
            OptionalDependency(import_name="msgpack", markers=("msgpack",)),
        ),
        quick_overrides={"ITERATIONS": 10},
    ),
    BenchmarkSpec(
        module="context_manager_perf_test",
        title="Context Manager Overhead",
        category="expert",
        quick_overrides={"ITERATIONS": 1000, "NESTED_ITERATIONS": 100, "FILE_ITERATIONS": 100},
    ),
    BenchmarkSpec(
        module="import_strategies_perf_test",
        title="Import Strategies",
        category="expert",
        quick_overrides={"ITERATIONS": 1000, "ACCESS_ITERATIONS": 10000},
    ),
    BenchmarkSpec(
        module="free_threaded_perf_test",
        title="Free-Threaded Python",
        category="expert",
        quick_overrides={"NUM_WORKERS": 2, "WORK_ITERATIONS": 10000},
    ),
    BenchmarkSpec(
        module="jit_numeric_perf_test",
        title="JIT Compiler Performance",
        category="expert",
        quick_overrides={"PERF_ITERATIONS": 2, "NUMERIC_ITERATIONS": 10000, "MANDELBROT_SIZE": 50},
    ),
)


def benchmarks_by_category() -> dict[str, list[str]]:
    """Return benchmark module names grouped by category."""
    return {category: [spec.module for spec in BENCHMARK_SPECS if spec.category == category] for category in CATEGORIES}


def quick_iterations() -> dict[str, dict[str, Any]]:
    """Return quick-mode overrides keyed by module name."""
    return {spec.module: dict(spec.quick_overrides) for spec in BENCHMARK_SPECS}


def all_benchmark_modules() -> list[str]:
    """Return all benchmark module names in manifest order."""
    return [spec.module for spec in BENCHMARK_SPECS]


def get_benchmark_spec(module_name: str) -> BenchmarkSpec:
    """Return metadata for one benchmark module."""
    for spec in BENCHMARK_SPECS:
        if spec.module == module_name:
            return spec
    raise KeyError(f"Unknown benchmark module: {module_name}")
