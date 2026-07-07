# Portfolio Case Study

## Problem

Python performance advice is often repeated without local evidence. This project turns common performance questions into runnable benchmarks with documented caveats, structured output, and tests around the benchmark harness itself.

## Current Architecture

The benchmark manifest is the catalog and single source of truth for module name, category, title, dependencies, optional dependency markers, and quick-mode overrides. The runner imports that manifest, applies quick-mode configuration, discovers top-level `perf_test*` functions in source order, and records structured results.

The test suite protects the harness behavior that matters for credibility:

- every benchmark file is declared in the manifest
- benchmark modules import without timing or printing at import time
- missing required dependencies fail benchmark results
- missing optional dependencies create explicit skipped cases
- JSON output includes environment metadata
- quick-mode overrides apply before case execution

## Tradeoffs

The project keeps each benchmark directly runnable as a script while also supporting structured execution through `run_all_tests.py`. That preserves approachability for individual examples and gives reviewers one reproducible command for the full suite.

The runner uses a lightweight `perf_counter()` harness rather than `pyperf`. This keeps the repo simple and dependency-light, but the methodology docs are explicit that these are practical measurements, not isolated laboratory results.

## Proof Points

Reviewer-facing evidence lives in three places:

- `run_all_tests.py --all --quick --format json` for machine-readable benchmark results
- `scripts/render_report.py` for compact Markdown summaries
- GitHub Actions artifacts for CI-generated JSON and Markdown evidence

Together, these show measurement discipline, honest dependency handling, typed/linted code, and regression tests for the benchmark infrastructure.

## What To Inspect

A CTO or senior engineering reviewer should inspect the manifest, runner, tests, methodology document, and sample reports before reading individual benchmark modules. Those files show whether the project is reproducible and honest before judging the benchmark conclusions.

## Next Improvements

The next maturity step is optional `pyperf` support for selected benchmarks, longer scheduled benchmark runs, and historical result comparison. Regression thresholds should wait until enough stable historical data exists to avoid noisy gates.
