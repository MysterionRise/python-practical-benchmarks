# Benchmark Methodology

This project measures practical Python implementation choices with a small, reproducible harness. The goal is not to publish universal performance rankings. The goal is to make performance claims inspectable on the machine, Python version, and dependency set where they are used.

## Measurement Model

`run_all_tests.py` discovers top-level `perf_test*` functions from the benchmark manifest and measures each case independently.

- Each measured case runs optional warmup executions before timing.
- Each measured case then runs repeated timed executions.
- The runner reports minimum, median, mean, standard deviation, run count, status, and a compact result preview.
- JSON output includes Python version, platform, CPU count, git SHA, timestamp, quick mode, runs, and warmups.

The default runner configuration is 1 warmup and 3 measured runs per case. Use `--runs` and `--warmups` when a review or CI job needs a different tradeoff.

## Quick Mode vs Full Mode

Quick mode applies manifest-defined overrides before benchmark cases execute. It is intended for CI, smoke testing, and portfolio review. It reduces dataset sizes, iteration counts, and sleep durations so the full suite can finish quickly.

Full mode keeps each benchmark module's default constants. It is more useful for local investigation, but it can take much longer and may amplify machine noise.

## Dependencies and Skips

Required dependencies are treated as benchmark failures when unavailable. Optional dependencies produce explicit skipped cases instead of silent passes. This keeps the result honest when fast JSON libraries, serialization libraries, or optional data-model libraries are not installed.

## Interpreting Results

Benchmark numbers vary by CPU, OS, Python version, dependency builds, background load, and thermal state. Compare results from the same machine and environment when possible. Treat small differences skeptically unless repeated runs show a stable pattern.

Microbenchmarks are useful for understanding tradeoffs, but they are not substitutes for profiling a production workload. Use these benchmarks to form hypotheses, then validate important decisions inside the real application path.

## Current Limits

The runner uses repeat-based `time.perf_counter()` measurement with warmups. It does not yet pin CPU affinity, isolate system load, use `pyperf`, or enforce cross-run regression thresholds. CI artifacts prove reproducibility and runner health; they are not performance SLAs.
