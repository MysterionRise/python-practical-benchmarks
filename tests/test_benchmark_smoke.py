"""Smoke tests to verify benchmark modules and manifest structure."""

import ast
import importlib
from pathlib import Path

import pytest

from benchmark_manifest import BENCHMARK_SPECS, all_benchmark_modules
from run_all_tests import collect_benchmark_cases, missing_dependencies

PROJECT_ROOT = Path(__file__).parent.parent


ALL_BENCHMARKS = all_benchmark_modules()


def import_or_skip_missing_required(module_name):
    """Import a benchmark module or skip when required deps are absent locally."""
    spec = next(spec for spec in BENCHMARK_SPECS if spec.module == module_name)
    missing_required = missing_dependencies(spec.required_dependencies)
    if missing_required:
        pytest.skip(f"Required dependencies missing locally: {', '.join(missing_required)}")
    return importlib.import_module(module_name)


def call_name(func_node):
    """Return a dotted call name for simple call expressions."""
    if isinstance(func_node, ast.Name):
        return func_node.id
    if isinstance(func_node, ast.Attribute):
        parts = []
        current = func_node
        while isinstance(current, ast.Attribute):
            parts.append(current.attr)
            current = current.value
        if isinstance(current, ast.Name):
            parts.append(current.id)
        return ".".join(reversed(parts))
    return ""


def is_main_guard(node):
    """Return True for if __name__ == '__main__' guards."""
    if not isinstance(node, ast.If):
        return False
    test = node.test
    return (
        isinstance(test, ast.Compare)
        and isinstance(test.left, ast.Name)
        and test.left.id == "__name__"
        and any(
            isinstance(comparator, ast.Constant) and comparator.value == "__main__" for comparator in test.comparators
        )
    )


class TestBenchmarkImports:
    """Test that all benchmark modules can be imported."""

    @pytest.mark.parametrize("module_name", ALL_BENCHMARKS)
    def test_benchmark_import(self, module_name):
        """Test that each benchmark module can be imported without errors."""
        module = import_or_skip_missing_required(module_name)
        assert module is not None

    @pytest.mark.parametrize("module_name", ALL_BENCHMARKS)
    def test_benchmark_has_docstring(self, module_name):
        """Test that each benchmark module has a useful module docstring."""
        module = import_or_skip_missing_required(module_name)
        assert module.__doc__ is not None, f"{module_name} missing docstring"
        assert len(module.__doc__) > 50, f"{module_name} docstring too short"


class TestBenchmarkStructure:
    """Test that benchmark modules follow the expected structure."""

    def test_manifest_covers_every_benchmark_file(self):
        """Test that every benchmark file is declared in the manifest."""
        benchmark_files = sorted(path.stem for path in PROJECT_ROOT.glob("*_perf_test.py"))
        assert sorted(ALL_BENCHMARKS) == benchmark_files

    @pytest.mark.parametrize("module_name", ALL_BENCHMARKS)
    def test_benchmark_has_top_level_perf_cases(self, module_name):
        """Test that each benchmark exposes top-level perf_test functions."""
        module = import_or_skip_missing_required(module_name)
        assert collect_benchmark_cases(module), f"{module_name} has no top-level perf_test functions"

    @pytest.mark.parametrize("module_name", ALL_BENCHMARKS)
    def test_benchmark_has_configuration_constants(self, module_name):
        """Test that benchmarks have numeric configuration constants."""
        module = import_or_skip_missing_required(module_name)
        constants = [
            name
            for name in dir(module)
            if name.isupper() and not name.startswith("_") and isinstance(getattr(module, name), (int, float))
        ]
        assert constants, f"{module_name} has no numeric configuration constants"

    @pytest.mark.parametrize("module_name", ALL_BENCHMARKS)
    def test_no_import_time_timing_or_printing(self, module_name):
        """Test that benchmark modules do not time or print at import time."""
        path = PROJECT_ROOT / f"{module_name}.py"
        tree = ast.parse(path.read_text())
        forbidden_calls = []
        for node in tree.body:
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)) or is_main_guard(node):
                continue
            for child in ast.walk(node):
                if isinstance(child, ast.Call) and call_name(child.func) in {"print", "timeit.timeit"}:
                    forbidden_calls.append((child.lineno, call_name(child.func)))

        assert not forbidden_calls, f"{module_name} has import-time calls: {forbidden_calls}"
