## Summary

<!-- Brief description of the changes -->

## Type of Change

<!-- Check all that apply -->

- [ ] Bug fix (non-breaking change fixing an issue)
- [ ] New benchmark
- [ ] Enhancement to existing benchmark
- [ ] Documentation update
- [ ] CI/CD or infrastructure change
- [ ] Dependency update

## Changes Made

<!-- Describe your changes in detail -->

-
-
-

## Checklist

### General

- [ ] I have read the [CONTRIBUTING.md](../CONTRIBUTING.md) guide
- [ ] My code follows the project's style guidelines (120 char line length, Black formatting)
- [ ] I have run `pre-commit run --all-files` and all checks pass
- [ ] I have added/updated tests if applicable

### For New Benchmarks

- [ ] Benchmark file follows naming convention: `*_perf_test.py`
- [ ] Module docstring includes results table upfront
- [ ] Test functions named `perf_test1_*`, `perf_test2_*`, etc.
- [ ] Functions return values to prevent optimizer elimination
- [ ] Configuration constants are UPPERCASE and overridable
- [ ] Comprehensive DECISION GUIDE section included
- [ ] Added to appropriate category in `run_all_tests.py` BENCHMARKS dict
- [ ] Added quick mode settings to `QUICK_ITERATIONS` dict
- [ ] Updated README.md with benchmark summary
- [ ] Updated Table of Contents in README.md

### For Documentation Changes

- [ ] Spelling and grammar checked
- [ ] Links tested and working
- [ ] Code examples are correct and tested

### For CI/CD Changes

- [ ] Tested locally where possible
- [ ] No security implications or they are documented
- [ ] No breaking changes to existing workflows

## Test Results

<!-- If applicable, paste test output -->

```
python run_all_tests.py --all --quick
```

## Related Issues

<!-- Link any related issues -->

Closes #

## Screenshots/Output

<!-- If applicable, add screenshots or benchmark output -->
