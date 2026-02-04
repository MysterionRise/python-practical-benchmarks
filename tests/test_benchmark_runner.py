"""Tests for run_all_tests.py benchmark runner."""

import subprocess
import sys
from pathlib import Path

import pytest

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
        # Check for some specific benchmarks
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
        # Should show help when no arguments provided
        assert "--all" in result.stdout or "usage" in result.stdout.lower()


class TestBenchmarkRunnerModule:
    """Tests for run_all_tests.py module functionality."""

    def test_module_import(self):
        """Test that run_all_tests can be imported."""
        import run_all_tests

        assert hasattr(run_all_tests, "BENCHMARKS")
        assert hasattr(run_all_tests, "QUICK_ITERATIONS")
        assert hasattr(run_all_tests, "run_benchmark")
        assert hasattr(run_all_tests, "list_benchmarks")
        assert hasattr(run_all_tests, "main")

    def test_benchmarks_dict_structure(self):
        """Test BENCHMARKS dict has expected structure."""
        import run_all_tests

        assert "basic" in run_all_tests.BENCHMARKS
        assert "advanced" in run_all_tests.BENCHMARKS
        assert "expert" in run_all_tests.BENCHMARKS

        # Each category should have benchmarks
        assert len(run_all_tests.BENCHMARKS["basic"]) >= 10
        assert len(run_all_tests.BENCHMARKS["advanced"]) >= 5
        assert len(run_all_tests.BENCHMARKS["expert"]) >= 5

    def test_quick_iterations_coverage(self):
        """Test QUICK_ITERATIONS covers all benchmarks."""
        import run_all_tests

        all_benchmarks = []
        for benchmarks in run_all_tests.BENCHMARKS.values():
            all_benchmarks.extend(benchmarks)

        for benchmark in all_benchmarks:
            assert benchmark in run_all_tests.QUICK_ITERATIONS, f"Benchmark {benchmark} missing from QUICK_ITERATIONS"

    def test_list_benchmarks_output(self, capsys):
        """Test list_benchmarks function output."""
        import run_all_tests

        run_all_tests.list_benchmarks()
        captured = capsys.readouterr()

        assert "Available Benchmarks" in captured.out
        assert "BASIC" in captured.out
        assert "ADVANCED" in captured.out
        assert "EXPERT" in captured.out


class TestBenchmarkExecution:
    """Tests for actual benchmark execution (smoke tests)."""

    @pytest.mark.slow
    def test_quick_run_basic_category(self):
        """Test running basic benchmarks in quick mode."""
        result = subprocess.run(
            [sys.executable, "run_all_tests.py", "--category", "basic", "--quick"],
            capture_output=True,
            text=True,
            cwd=PROJECT_ROOT,
            timeout=300,  # 5 minute timeout
        )
        # Allow for some failures due to missing optional dependencies
        # but the runner itself should complete
        assert "SUMMARY" in result.stdout
        assert "Total:" in result.stdout
