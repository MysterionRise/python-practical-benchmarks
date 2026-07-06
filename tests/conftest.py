"""Shared pytest fixtures for benchmark tests."""

import importlib
from pathlib import Path

import pytest

from benchmark_manifest import all_benchmark_modules, benchmarks_by_category, get_benchmark_spec

PROJECT_ROOT = Path(__file__).parent.parent


ALL_BENCHMARKS = all_benchmark_modules()
BENCHMARKS = benchmarks_by_category()


@pytest.fixture
def benchmark_loader():
    """Fixture to load benchmark modules with quick iterations."""

    def load(module_name):
        """Load a benchmark module and apply quick iteration settings."""
        module = importlib.import_module(module_name)
        spec = get_benchmark_spec(module_name)
        for attr, value in spec.quick_overrides.items():
            if hasattr(module, attr):
                setattr(module, attr, value)
        reset_func = getattr(module, "reset_benchmark_data", None)
        if callable(reset_func):
            reset_func()
        return module

    return load


@pytest.fixture
def all_benchmark_names():
    """Return list of all benchmark module names."""
    return ALL_BENCHMARKS.copy()


@pytest.fixture
def benchmark_categories():
    """Return benchmark categories dictionary."""
    return {category: benchmarks.copy() for category, benchmarks in BENCHMARKS.items()}
