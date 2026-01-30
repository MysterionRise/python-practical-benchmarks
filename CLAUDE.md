# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A Python performance benchmarking repository with 20 benchmarks organized into three tiers: basic (10), advanced (5), and expert (5). Each benchmark answers a specific performance question with real measurements and actionable decision guides.

## Commands

### Running Benchmarks

```bash
# Run all benchmarks with reduced iterations (CI mode)
python run_all_tests.py --all --quick

# Run by category
python run_all_tests.py --category basic --quick
python run_all_tests.py --category advanced --quick
python run_all_tests.py --category expert --quick

# List all benchmarks
python run_all_tests.py --list

# Run individual benchmark (full iterations)
python dict_access_perf_test.py
```

### Code Quality

```bash
# Format code
black --line-length 120 *.py

# Sort imports
isort --profile black --line-length 120 *.py

# Lint
flake8 *.py --max-line-length=120 --ignore=W605,E203,W503,E501

# Run all pre-commit hooks
pre-commit run --all-files
```

## Architecture

### Benchmark File Structure

Each `*_perf_test.py` file follows a consistent pattern:

1. **Module docstring**: Contains the performance question and results table upfront
2. **Configuration constants**: `PERF_ITERATIONS`, `DATASET_SIZE`, etc. (uppercase, overridable for quick mode)
3. **Test functions**: Named `perf_test1_*`, `perf_test2_*`, etc., each returning a value to prevent optimizer elimination
4. **Decision guide**: WHEN TO USE, BEST PRACTICES, ANTI-PATTERNS sections

### Test Runner Integration

`run_all_tests.py` dynamically imports benchmarks and reduces iteration counts via `QUICK_ITERATIONS` dict. It finds and runs functions starting with `perf_test` as smoke tests.

### Optional Dependencies

Some benchmarks gracefully handle missing optional packages (orjson, ujson, msgpack, cbor2, attrs) using try/except imports.

## Code Style

- **Line length**: 120 characters
- **Formatter**: Black with `--line-length 120`
- **Import sorting**: isort with `--profile black`
- **Constants**: UPPER_CASE for configurable test parameters
- **Commits**: Conventional commits (feat:, fix:, chore:)

## Python Version Support

Python 3.9 through 3.14 (tested in CI).
