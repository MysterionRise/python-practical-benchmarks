# Contributing to Python Practical Benchmarks

Thank you for your interest in contributing to this project! This guide will help you create high-quality performance benchmarks that follow our established patterns.

## Table of Contents

- [Getting Started](#getting-started)
- [Benchmark Structure](#benchmark-structure)
- [Writing Benchmarks](#writing-benchmarks)
- [Testing Your Benchmark](#testing-your-benchmark)
- [Submitting Changes](#submitting-changes)
- [Code Quality](#code-quality)

## Getting Started

1. **Fork and Clone**
   ```bash
   git clone https://github.com/YOUR_USERNAME/python-practical-benchmarks.git
   cd python-practical-benchmarks
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   pip install pre-commit
   pre-commit install
   ```

3. **Choose a Benchmark Topic**
   - Focus on practical, real-world performance questions
   - Look for common patterns developers face
   - Avoid trivial or overly academic examples

## Benchmark Structure

All benchmarks follow a consistent pattern. Here's the template:

```python
"""
What is [the performance question]?

Performance test comparing [approaches]:

[CATEGORY NAME] ([iterations] iterations):
Approach                         Total time    Per iteration  Relative
-----------------------------------------------------------------------
Method 1                         0.234s             234ns        1.0x (baseline)
Method 2                         0.456s             456ns        1.9x slower
Method 3                         0.123s             123ns        2.0x faster ✓ best

KEY FINDINGS:
- Clear, actionable insight 1
- Clear, actionable insight 2
- Clear, actionable insight 3
- When to use what approach
"""
import timeit
# Other imports

# Configuration constants
ITERATIONS = 1000000
OTHER_PARAMS = 100


# ============================================================================
# SECTION 1: [Category Name]
# ============================================================================

def perf_test1_baseline():
    """Baseline approach"""
    total = 0
    for i in range(ITERATIONS):
        # Test implementation
        total += i
    return total


def perf_test2_alternative():
    """Alternative approach"""
    total = 0
    for i in range(ITERATIONS):
        # Alternative implementation
        total += i
    return total


# Add more test functions as needed


if __name__ == "__main__":
    print("=" * 80)
    print("[BENCHMARK NAME]")
    print("=" * 80)
    print()

    # Run benchmarks
    print("=" * 80)
    print(f"[CATEGORY] ({ITERATIONS:,} iterations)")
    print("=" * 80)

    t1 = timeit.timeit(stmt="perf_test1_baseline()", number=1, globals=globals())
    print(f"Baseline:                        {t1:.6f}s  ({t1*1e9/ITERATIONS:.0f}ns per iter)")

    t2 = timeit.timeit(stmt="perf_test2_alternative()", number=1, globals=globals())
    print(f"Alternative:                     {t2:.6f}s  ({t2*1e9/ITERATIONS:.0f}ns per iter) {t2/t1:.1f}x")

    # Decision guide
    print("\n" + "=" * 80)
    print("DECISION GUIDE")
    print("=" * 80)
    print("""
    WHEN TO USE [APPROACH 1]:
    ✓ Use case 1
    ✓ Use case 2
    ⚠ Warning about limitations

    WHEN TO USE [APPROACH 2]:
    ✓ Use case 1
    ⚠ Warning

    BEST PRACTICES:
    1. Actionable guideline 1
    2. Actionable guideline 2
    3. Actionable guideline 3

    ANTI-PATTERNS:
    ✗ What not to do
    ✗ Common mistake

    REAL-WORLD EXAMPLES:
    # Example 1
    code_example()

    # Example 2
    another_example()
    """)
```

## Writing Benchmarks

### 1. Module Docstring

Start with results upfront so users can quickly see if the benchmark is relevant:

```python
"""
What is the overhead of X vs Y?

Performance comparison shows:
- X is 3x faster for small datasets
- Y is 2x faster for large datasets
- Z has lowest memory usage

[Include actual benchmark results table]
"""
```

### 2. Configuration Constants

Use uppercase constants that can be overridden for quick testing:

```python
ITERATIONS = 1000000
DATASET_SIZE = 10000
OTHER_PARAM = 100
```

### 3. Test Functions

- Name functions `perf_test1_`, `perf_test2_`, etc.
- Use descriptive suffixes: `perf_test1_baseline`, `perf_test2_comprehension`
- Return a value to prevent optimizer from eliminating code
- Keep tests focused on one specific pattern

### 4. Measurements

Use `timeit.timeit()` for accurate timing:

```python
t1 = timeit.timeit(stmt="perf_test1_baseline()", number=1, globals=globals())
```

Format output consistently:

```python
print(f"Method name:                     {t1:.6f}s  ({t1*1e9/ITERATIONS:.0f}ns per iter) {t1/baseline:.1f}x")
```

### 5. Decision Guide

Always include a comprehensive decision guide:

- **WHEN TO USE**: Clear use cases for each approach
- **BEST PRACTICES**: Actionable guidelines (numbered list)
- **ANTI-PATTERNS**: Common mistakes to avoid
- **REAL-WORLD EXAMPLES**: Actual code snippets
- **PERFORMANCE HIERARCHY**: Ranked summary of approaches

### 6. Handle Optional Dependencies

For optional libraries, use graceful degradation:

```python
try:
    import optional_library
    HAS_OPTIONAL = True
except ImportError:
    HAS_OPTIONAL = False

# Later in the benchmark:
if HAS_OPTIONAL:
    # Run benchmark with optional library
else:
    print("  ⚠ optional_library not installed, skipping test")
```

### 7. Dataset Sizes

Test across multiple scales when relevant:

```python
SIZES = {
    "small": 100,
    "medium": 10_000,
    "large": 100_000,
}

for name, size in SIZES.items():
    print(f"\nTesting with {name} dataset ({size:,} items)")
    # Run benchmarks
```

### 8. Cleanup

Clean up any temporary resources:

```python
import tempfile
import os

# Create temp file
with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
    temp_path = f.name
    # Use file

# Clean up
try:
    os.unlink(temp_path)
except OSError:
    pass
```

## Testing Your Benchmark

### 1. Run Directly

```bash
python your_new_perf_test.py
```

Verify:
- All tests complete without errors
- Results make sense (no negative times, reasonable comparisons)
- Decision guide is comprehensive

### 2. Add to Test Runner

Edit `run_all_tests.py`:

1. Add to the appropriate category in `BENCHMARKS` dict:
```python
BENCHMARKS = {
    "basic": [
        # existing benchmarks
        "your_new_perf_test",
    ],
}
```

2. Add quick mode parameters to `QUICK_ITERATIONS`:
```python
QUICK_ITERATIONS = {
    "your_new_perf_test": {"PERF_ITERATIONS": 100, "DATASET_SIZE": 100},
}
```

### 3. Test with Quick Mode

```bash
python run_all_tests.py --category basic --quick
```

### 4. Run Linting

```bash
black --line-length 120 your_new_perf_test.py
isort --profile black --line-length 120 your_new_perf_test.py
flake8 your_new_perf_test.py --max-line-length=120 --ignore=W605,E203,W503,E501
```

Or use pre-commit:

```bash
pre-commit run --files your_new_perf_test.py
```

## Submitting Changes

### 1. Update README

Add your benchmark to the appropriate section in README.md:

```markdown
### 21. Your Benchmark Name

**File**: `your_new_perf_test.py`

**Question**: What is [the question]?

**Key Findings**:
- Finding 1
- Finding 2
- Finding 3

**Example**:
```python
# code example
```

**When to use**: Recommendation
```

### 2. Update Key Takeaways

Add 1-3 key takeaways to the appropriate section in README.md.

### 3. Commit Message Format

Use conventional commits:

```bash
git commit -m "feat: add [benchmark name] performance test

- Compare [approach 1] vs [approach 2]
- Test across [small/medium/large] datasets
- Add comprehensive decision guide
- Include real-world examples"
```

### 4. Create Pull Request

1. Push to your fork
2. Create PR with clear description:
   - What performance question does this answer?
   - What approaches are compared?
   - What are the key findings?
   - Include sample output

## Code Quality

### Style Guidelines

- **Line length**: 120 characters max
- **Formatting**: Use Black with `--line-length 120`
- **Imports**: Sort with isort, `--profile black`
- **Naming**:
  - Functions: `snake_case`
  - Constants: `UPPER_CASE`
  - Classes: `PascalCase`

### Documentation

- Module docstrings must include results upfront
- Function docstrings should be brief (1 line for most test functions)
- Decision guides should be comprehensive and actionable

### Performance

- Use `timeit.timeit()` for measurements
- Run enough iterations for stable results (typically 1M+ for fast operations)
- Report both absolute time and relative performance
- Test across multiple dataset sizes when relevant

### Testing

- All benchmarks must run successfully with `python run_all_tests.py --all --quick`
- Must support quick mode with reduced iterations
- Should handle missing optional dependencies gracefully

## Benchmark Categories

### Basic
- Fundamental operations (strings, lists, dicts, file I/O)
- Clear winners in most cases
- Essential knowledge for all Python developers

### Advanced
- Complex patterns (concurrency, regex, object creation)
- Trade-offs between approaches
- Important for intermediate developers

### Expert
- Python internals (attribute access, exceptions, imports)
- Subtle performance considerations
- Deep understanding required

## Questions?

- Open an issue for discussions about new benchmark ideas
- Check existing benchmarks for patterns and examples
- Focus on practical, real-world performance questions

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
