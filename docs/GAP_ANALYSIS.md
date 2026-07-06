# Portfolio Quality Gap Analysis

This document tracks the work needed to make `python-practical-benchmarks` credible as a senior engineering portfolio project. The goal is honest reproducibility and maintainability, not unsupported "enterprise-grade" claims.

## Current State

| Area | Current Position | Status |
|------|------------------|--------|
| Benchmark catalog | 22 benchmarks across basic, advanced, and expert categories | Implemented |
| Benchmark metadata | Central manifest for categories, dependencies, titles, and quick-mode settings | Implemented |
| Runner | Text and JSON output with repeated measurements and environment metadata | Implemented |
| Tests | Import, manifest, runner, and representative execution checks | Implemented |
| Coverage | Coverage reporting for runner-oriented tests; no hard project-wide threshold | Intentional |
| Tooling | Ruff, mypy, pytest, pre-commit, Dependabot, security workflows | Implemented |
| Benchmark methodology | Repeat timing, warmup, structured output, and dependency-aware skip/fail behavior | Improving |

## Completed Improvements

- Replaced duplicated benchmark lists with `benchmark_manifest.py`.
- Made benchmark discovery source-order based instead of lexicographic `dir()` order.
- Added structured JSON output with environment metadata, benchmark summaries, case timings, skips, and errors.
- Changed missing required dependencies from false passes to benchmark failures.
- Changed missing optional dependencies into explicit skipped cases.
- Removed import-time timing and printing from benchmark modules.
- Fixed the 2D array benchmark filename typo so it follows the `*_perf_test.py` convention.
- Updated documentation to avoid stale 80% coverage-threshold claims.

## Remaining Gaps

- Benchmark result tables in README are still representative examples; they should eventually be generated from checked-in JSON artifacts.
- Some modules still build sizable data at import time. They are import-safe from a timing/printing perspective, but not fully lazy.
- The project has coverage reporting, but not a meaningful coverage gate yet.
- Statistical rigor is basic. A future iteration should add configurable repeats, warmup counts, confidence intervals, and regression comparison against previous result files.
- Optional dependency coverage depends on the local or CI install profile. A dedicated optional-dependency job should assert all optional cases execute.

## Verification Commands

```bash
ruff check .
ruff format --check .
mypy .
pytest tests/ -v
python run_all_tests.py --list
python run_all_tests.py --all --quick
python run_all_tests.py --all --quick --format json --output /tmp/python-practical-benchmarks-results.json
```

## Next Portfolio Milestone

The next highest-signal improvement is to publish generated benchmark result artifacts per Python version and platform, then make the README consume or link to those artifacts. That would turn the project from a benchmark runner into an auditable performance reference.
