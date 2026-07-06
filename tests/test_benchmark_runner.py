"""Tests for run_all_tests.py benchmark runner."""

import json
import subprocess
import sys
import types
from pathlib import Path

import pytest

from benchmark_manifest import BenchmarkSpec, OptionalDependency, all_benchmark_modules

PROJECT_ROOT = Path(__file__).parent.parent


class TestBenchmarkRunnerCLI:
    """Tests for CLI interface of run_all_tests.py."""

    def test_help_option(self):
        """Test --help option displays usage information."""
        result = subprocess.run(
            [sys.executable, "run_all_tests.py", "--help"],
            capture_output=True,
            text=True,
            cwd=PROJECT_ROOT,
        )
        assert result.returncode == 0
        assert "Run Python performance benchmarks" in result.stdout
        assert "--all" in result.stdout
        assert "--category" in result.stdout
        assert "--quick" in result.stdout
        assert "--list" in result.stdout
        assert "--format" in result.stdout
        assert "--output" in result.stdout

    def test_list_option(self):
        """Test --list option displays all benchmarks."""
        result = subprocess.run(
            [sys.executable, "run_all_tests.py", "--list"],
            capture_output=True,
            text=True,
            cwd=PROJECT_ROOT,
        )
        assert result.returncode == 0
        assert "Available Benchmarks" in result.stdout
        assert "BASIC" in result.stdout
        assert "ADVANCED" in result.stdout
        assert "EXPERT" in result.stdout
        assert "iterate_2d_array_perf_test" in result.stdout
        assert "dict_access_perf_test" in result.stdout
        assert "concurrency_patterns_perf_test" in result.stdout
        assert "attribute_access_perf_test" in result.stdout

    def test_no_args_shows_help(self):
        """Test running without arguments shows help."""
        result = subprocess.run(
            [sys.executable, "run_all_tests.py"],
            capture_output=True,
            text=True,
            cwd=PROJECT_ROOT,
        )
        assert result.returncode == 1
        assert "--all" in result.stdout


class TestBenchmarkRunnerModule:
    """Tests for run_all_tests.py module functionality."""

    def test_module_import(self):
        """Test that run_all_tests can be imported."""
        import run_all_tests

        assert hasattr(run_all_tests, "BENCHMARKS")
        assert hasattr(run_all_tests, "QUICK_ITERATIONS")
        assert hasattr(run_all_tests, "run_benchmark")
        assert hasattr(run_all_tests, "build_payload")
        assert hasattr(run_all_tests, "list_benchmarks")
        assert hasattr(run_all_tests, "main")

    def test_benchmarks_dict_structure(self):
        """Test BENCHMARKS dict has expected structure."""
        import run_all_tests

        assert "basic" in run_all_tests.BENCHMARKS
        assert "advanced" in run_all_tests.BENCHMARKS
        assert "expert" in run_all_tests.BENCHMARKS
        assert len(run_all_tests.BENCHMARKS["basic"]) >= 10
        assert len(run_all_tests.BENCHMARKS["advanced"]) >= 5
        assert len(run_all_tests.BENCHMARKS["expert"]) >= 5

    def test_quick_iterations_coverage(self):
        """Test QUICK_ITERATIONS covers all benchmarks."""
        import run_all_tests

        for benchmark in all_benchmark_modules():
            assert benchmark in run_all_tests.QUICK_ITERATIONS, f"Benchmark {benchmark} missing from QUICK_ITERATIONS"

    def test_required_dependency_failures_are_not_passes(self):
        """Test missing required deps fail benchmark results."""
        import run_all_tests

        spec = BenchmarkSpec(
            module="dict_access_perf_test",
            title="Synthetic missing dependency",
            category="basic",
            required_dependencies=("definitely_missing_required_dependency_xyz",),
            quick_overrides={"PERF_ITERATIONS": 1},
        )
        result = run_all_tests.run_benchmark(spec, quick=True, emit_text=False)
        assert result["status"] == "failed"
        assert result["errors"][0]["type"] == "missing_required_dependency"

    def test_optional_dependency_skips_are_explicit(self):
        """Test missing optional deps skip matching cases without failing."""
        import run_all_tests

        module_name = "synthetic_optional_benchmark"
        module = types.ModuleType(module_name)

        def perf_test1_fake_optional():
            """fake optional case."""
            return 1

        perf_test1_fake_optional.__module__ = module_name
        module.perf_test1_fake_optional = perf_test1_fake_optional
        sys.modules[module_name] = module
        try:
            spec = BenchmarkSpec(
                module=module_name,
                title="Synthetic optional dependency",
                category="basic",
                optional_dependencies=(
                    OptionalDependency(
                        import_name="definitely_missing_optional_dependency_xyz",
                        markers=("fake",),
                    ),
                ),
                quick_overrides={"ITERATIONS": 1},
            )
            result = run_all_tests.run_benchmark(spec, quick=True, emit_text=False)
        finally:
            del sys.modules[module_name]

        assert result["status"] == "skipped"
        assert result["cases"][0]["status"] == "skipped"
        assert result["skips"][0]["dependency"] == "definitely_missing_optional_dependency_xyz"

    def test_quick_mode_overrides_apply_before_execution(self):
        """Test quick-mode overrides are recorded and applied."""
        import dict_access_perf_test
        import run_all_tests

        result = run_all_tests.run_benchmark("dict_access_perf_test", quick=True, runs=1, emit_text=False)
        assert result["status"] == "passed"
        assert result["quick_overrides"]["DICTIONARY_SIZE"] == 100
        assert dict_access_perf_test.DICTIONARY_SIZE == 100

    def test_json_payload_contains_environment_metadata(self):
        """Test structured payload contains environment, summary, and benchmarks."""
        import run_all_tests
        from benchmark_manifest import get_benchmark_spec

        payload = run_all_tests.build_payload(
            [get_benchmark_spec("dict_access_perf_test")], quick=True, emit_text=False
        )
        encoded = json.dumps(payload)
        decoded = json.loads(encoded)

        assert "environment" in decoded
        assert "summary" in decoded
        assert "benchmarks" in decoded
        assert decoded["environment"]["python_version"]
        assert decoded["environment"]["quick"] is True
        assert decoded["benchmarks"][0]["cases"]


class TestBenchmarkExecution:
    """Tests for actual benchmark execution."""

    @pytest.mark.slow
    def test_quick_run_basic_category(self):
        """Test running basic benchmarks in quick mode."""
        result = subprocess.run(
            [sys.executable, "run_all_tests.py", "--category", "basic", "--quick"],
            capture_output=True,
            text=True,
            cwd=PROJECT_ROOT,
            timeout=300,
        )
        assert "SUMMARY" in result.stdout
        assert "Total:" in result.stdout

    def test_json_output_file(self, tmp_path):
        """Test JSON output can be written to a file."""
        output_path = tmp_path / "results.json"
        result = subprocess.run(
            [
                sys.executable,
                "run_all_tests.py",
                "--category",
                "basic",
                "--quick",
                "--format",
                "json",
                "--output",
                str(output_path),
            ],
            capture_output=True,
            text=True,
            cwd=PROJECT_ROOT,
            timeout=300,
        )
        if (
            result.returncode != 0
            and output_path.exists()
            and "Required dependency not installed" in output_path.read_text()
        ):
            pytest.skip("Required benchmark dependencies are not installed locally")

        assert result.returncode == 0
        payload = json.loads(output_path.read_text())
        assert "environment" in payload
        assert "summary" in payload
        assert "benchmarks" in payload
