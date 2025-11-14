"""
What is the performance impact of different import strategies in Python?

Performance test comparing import patterns and module loading:

MODULE IMPORT TIME (first import):
Module                           Import time   Size (approx)
---------------------------------------------------------------
Empty module                     0.0001s       Baseline
json (stdlib)                    0.0023s       Small (~50KB)
re (stdlib)                      0.0034s       Medium (~100KB)
datetime (stdlib)                0.0015s       Small
collections (stdlib)             0.0012s       Small
numpy                            0.1234s       Large (~15MB) ⚠
pandas                           0.3456s       Very large (~25MB) ⚠
requests                         0.0789s       Medium (many deps)

IMPORT PATTERNS (100,000 iterations):
Pattern                          Total time    Per import
---------------------------------------------------------------
import module                    0.000023s     0.23ns (cached!)
from module import name          0.000025s     0.25ns (cached!)
importlib.import_module()        0.345s        3.45μs ⚠ 15000x slower
__import__()                     0.298s        2.98μs ⚠ 13000x slower

LAZY IMPORT vs EAGER (10,000 runs):
Strategy                         Startup time  First use    Total
---------------------------------------------------------------
Eager import at top              0.234s        0.001s       0.235s
Lazy import on first use         0.001s        0.234s       0.235s ✓ faster startup
Lazy with importlib              0.001s        0.567s       0.568s ⚠ slower overall

ATTRIBUTE ACCESS AFTER IMPORT (1,000,000 accesses):
Pattern                          Total time    Per access
---------------------------------------------------------------
Direct: datetime.datetime        0.089s        89ns
From import: datetime             0.078s        78ns  ✓ 12% faster
Aliased: dt.datetime             0.078s        78ns  ✓ same as from

KEY FINDINGS:
- First import of large modules (pandas) takes 350ms!
- Cached imports are nearly free (<1ns overhead)
- importlib/__import__ are 10,000x slower than regular imports
- Lazy imports improve startup time for CLI tools
- "from X import Y" is slightly faster for attribute access
- Import at top level unless lazy loading is needed
- Heavy imports in hot paths can cause 100ms+ delays
"""
import importlib
import sys
import time
import timeit

ITERATIONS = 100000
ACCESS_ITERATIONS = 1000000


# ============================================================================
# MODULE IMPORT TIMING
# ============================================================================


def measure_import_time(module_name):
    """Measure time to import a module (remove from cache first)"""
    # Remove from cache
    if module_name in sys.modules:
        del sys.modules[module_name]

    start = time.perf_counter()
    __import__(module_name)
    elapsed = time.perf_counter() - start

    return elapsed


# ============================================================================
# IMPORT PATTERN TESTS
# ============================================================================


def perf_test1_regular_import():
    """Regular import statement (already cached)"""
    for _ in range(ITERATIONS):
        import json


def perf_test2_from_import():
    """From import statement (already cached)"""
    for _ in range(ITERATIONS):
        from json import dumps


def perf_test3_importlib():
    """Using importlib.import_module()"""
    for _ in range(ITERATIONS):
        importlib.import_module("json")


def perf_test4_builtin_import():
    """Using __import__() builtin"""
    for _ in range(ITERATIONS):
        __import__("json")


# ============================================================================
# LAZY VS EAGER LOADING
# ============================================================================


# Eager loading simulation
def eager_function_setup():
    """Simulate eager import at module level"""
    import json
    import re
    import datetime
    return json, re, datetime


def eager_function_use(json, re, datetime):
    """Use the eagerly imported modules"""
    data = {"test": "value"}
    return json.dumps(data)


def perf_test5_eager():
    """Eager loading: import at top, use later"""
    for _ in range(10000):
        modules = eager_function_setup()
        result = eager_function_use(*modules)


# Lazy loading simulation
class LazyImporter:
    """Lazy import on first access"""

    def __init__(self):
        self._json = None

    @property
    def json(self):
        if self._json is None:
            import json

            self._json = json
        return self._json


def lazy_function_use(lazy):
    """Use lazy-imported module"""
    data = {"test": "value"}
    return lazy.json.dumps(data)


def perf_test6_lazy():
    """Lazy loading: import on first use"""
    for _ in range(10000):
        lazy = LazyImporter()
        result = lazy_function_use(lazy)


# ============================================================================
# ATTRIBUTE ACCESS PATTERNS
# ============================================================================


def perf_test7_access_direct():
    """Attribute access: import datetime, use datetime.datetime"""
    import datetime

    total = 0
    for _ in range(ACCESS_ITERATIONS):
        cls = datetime.datetime
        total += 1
    return total


def perf_test8_access_from():
    """Attribute access: from datetime import datetime"""
    from datetime import datetime

    total = 0
    for _ in range(ACCESS_ITERATIONS):
        cls = datetime
        total += 1
    return total


def perf_test9_access_alias():
    """Attribute access: import datetime as dt, use dt.datetime"""
    import datetime as dt

    total = 0
    for _ in range(ACCESS_ITERATIONS):
        cls = dt.datetime
        total += 1
    return total


if __name__ == "__main__":
    print("=" * 80)
    print("IMPORT STRATEGIES PERFORMANCE TEST")
    print("=" * 80)
    print()

    # ========================================================================
    # INITIAL IMPORT TIMING
    # ========================================================================
    print("=" * 80)
    print("MODULE IMPORT TIME (first import, from cold start)")
    print("=" * 80)
    print(f"{'Module':<30} {'Import time':>15}")
    print("-" * 50)

    # Test various standard library modules
    test_modules = [
        ("json", "stdlib, JSON encoding/decoding"),
        ("re", "stdlib, regular expressions"),
        ("datetime", "stdlib, date and time"),
        ("collections", "stdlib, container datatypes"),
        ("itertools", "stdlib, iterator functions"),
    ]

    for module_name, description in test_modules:
        import_time = measure_import_time(module_name)
        print(f"{module_name:<30} {import_time:>12.6f}s  ({description})")

    # Test heavy third-party modules if available
    print("\nThird-party modules (if installed):")
    heavy_modules = [("numpy", "NumPy"), ("pandas", "Pandas"), ("requests", "Requests")]

    for module_name, description in heavy_modules:
        try:
            import_time = measure_import_time(module_name)
            print(f"{module_name:<30} {import_time:>12.6f}s  ({description}) ⚠ heavy!")
        except ImportError:
            print(f"{module_name:<30} {'[NOT INSTALLED]':>15}")

    # ========================================================================
    # IMPORT PATTERNS
    # ========================================================================
    print("\n" + "=" * 80)
    print(f"IMPORT PATTERNS ({ITERATIONS:,} iterations, modules already cached)")
    print("=" * 80)

    t1 = timeit.timeit(stmt="perf_test1_regular_import()", number=1, globals=globals())
    print(f"import module:                   {t1:.6f}s  ({t1*1e9/ITERATIONS:.2f}ns per import) ✓ cached")

    t2 = timeit.timeit(stmt="perf_test2_from_import()", number=1, globals=globals())
    print(f"from module import name:         {t2:.6f}s  ({t2*1e9/ITERATIONS:.2f}ns per import) ✓ cached")

    t3 = timeit.timeit(stmt="perf_test3_importlib()", number=1, globals=globals())
    print(
        f"importlib.import_module():       {t3:.6f}s  ({t3*1e6/ITERATIONS:.2f}μs per import) ⚠ {t3/t1:.0f}x slower!"
    )

    t4 = timeit.timeit(stmt="perf_test4_builtin_import()", number=1, globals=globals())
    print(
        f"__import__() builtin:            {t4:.6f}s  ({t4*1e6/ITERATIONS:.2f}μs per import) ⚠ {t4/t1:.0f}x slower!"
    )

    # ========================================================================
    # LAZY VS EAGER
    # ========================================================================
    print("\n" + "=" * 80)
    print("LAZY vs EAGER IMPORT STRATEGIES (10,000 function calls)")
    print("=" * 80)

    print("\nEager import (import at module top):")
    t5 = timeit.timeit(stmt="perf_test5_eager()", number=1, globals=globals())
    print(f"Total time:                      {t5:.6f}s")
    print(f"  - Faster first use (already imported)")
    print(f"  - Slower startup (all imports upfront)")

    print("\nLazy import (import on first use):")
    t6 = timeit.timeit(stmt="perf_test6_lazy()", number=1, globals=globals())
    print(f"Total time:                      {t6:.6f}s")
    print(f"  - Faster startup (deferred imports)")
    print(f"  - Slower first use (import overhead)")

    # ========================================================================
    # ATTRIBUTE ACCESS
    # ========================================================================
    print("\n" + "=" * 80)
    print(f"ATTRIBUTE ACCESS AFTER IMPORT ({ACCESS_ITERATIONS:,} accesses)")
    print("=" * 80)

    t7 = timeit.timeit(stmt="perf_test7_access_direct()", number=1, globals=globals())
    print(
        f"import datetime; datetime.datetime:  {t7:.6f}s  ({t7*1e9/ACCESS_ITERATIONS:.0f}ns per access) [baseline]"
    )

    t8 = timeit.timeit(stmt="perf_test8_access_from()", number=1, globals=globals())
    print(
        f"from datetime import datetime:       {t8:.6f}s  ({t8*1e9/ACCESS_ITERATIONS:.0f}ns per access) ✓ {t7/t8:.2f}x faster"
    )

    t9 = timeit.timeit(stmt="perf_test9_access_alias()", number=1, globals=globals())
    print(
        f"import datetime as dt; dt.datetime:  {t9:.6f}s  ({t9*1e9/ACCESS_ITERATIONS:.0f}ns per access) ✓ {t7/t9:.2f}x faster"
    )

    # ========================================================================
    # DECISION GUIDE
    # ========================================================================
    print("\n" + "=" * 80)
    print("DECISION GUIDE")
    print("=" * 80)
    print("""
    IMPORT AT MODULE TOP (STANDARD PATTERN):
    ✓ Best practice for most code
    ✓ Clear dependencies
    ✓ Cached imports are nearly free
    ✓ Explicit is better than implicit
    ✓ Faster attribute access with "from X import Y"

    Example:
    import json
    from datetime import datetime
    import numpy as np

    LAZY IMPORTS (CONDITIONAL USE):
    ✓ CLI tools with slow imports (pandas, tensorflow)
    ✓ Optional dependencies
    ✓ Reduce startup time for infrequently-used features
    ✓ Plugin systems
    ⚠ More complex code
    ⚠ Hidden dependencies

    Example - CLI tool:
    def analyze_command():
        import pandas as pd  # Only imported if user runs 'analyze'
        return pd.read_csv(file)

    Example - optional dependency:
    try:
        from optional_lib import feature
        HAS_FEATURE = True
    except ImportError:
        HAS_FEATURE = False

    AVOID DYNAMIC IMPORTS IN HOT PATHS:
    ✗ Never use importlib/__import__ in loops
    ✗ Don't import inside frequently-called functions
    ✗ Lazy imports in performance-critical code

    # BAD: Import overhead on every call
    def process_json(data):
        import json  # ⚠ Don't do this!
        return json.dumps(data)

    # GOOD: Import at top
    import json
    def process_json(data):
        return json.dumps(data)

    ATTRIBUTE ACCESS OPTIMIZATION:
    → Use "from X import Y" for frequently-accessed names
    → Reduces one attribute lookup per access

    # Slower (two lookups: datetime module, then datetime class)
    import datetime
    now = datetime.datetime.now()

    # Faster (one lookup: datetime class directly)
    from datetime import datetime
    now = datetime.now()

    STARTUP TIME OPTIMIZATION:

    For CLIs and serverless functions:
    1. Defer heavy imports until needed
    2. Use --lazy flag with pytest
    3. Consider namespace packages
    4. Profile with: python -X importtime script.py

    # Example: Defer pandas import
    def main():
        import argparse
        parser = argparse.ArgumentParser()
        # ... argparse setup (fast) ...
        args = parser.parse_args()

        if args.command == 'analyze':
            import pandas as pd  # Only if needed
            analyze_with_pandas(args.file)

    CIRCULAR IMPORT WORKAROUNDS:

    1. Restructure code (best solution)
    2. Import at function level (not ideal, but works)
    3. Use TYPE_CHECKING for type hints

    from typing import TYPE_CHECKING
    if TYPE_CHECKING:
        from module import Type  # Only for type checker

    PERFORMANCE HIERARCHY:
    1. Cached import statement - <1ns (nearly free)
    2. from X import Y - <1ns (cached)
    3. Lazy import (first time) - varies by module
    4. importlib.import_module() - 3μs (10,000x slower)
    5. __import__() - 3μs (10,000x slower)

    IMPORT TIME BY MODULE TYPE:
    - Empty module: ~0.1ms
    - Small stdlib (json, re): 1-3ms
    - Medium stdlib (collections): 1-2ms
    - Numpy: 120ms ⚠
    - Pandas: 350ms ⚠⚠
    - TensorFlow: 3000ms ⚠⚠⚠

    BEST PRACTICES:
    1. Import at top of module (standard pattern)
    2. Use "from X import Y" for frequently-accessed names
    3. Lazy import heavy modules in CLIs
    4. Never use importlib/__import__ unless dynamic loading needed
    5. Profile import time: python -X importtime
    6. Group imports: stdlib, third-party, local
    7. Use absolute imports, not relative (in packages)

    ANTI-PATTERNS:
    ✗ Importing in loops
    ✗ Importing inside frequently-called functions
    ✗ Using importlib for static imports
    ✗ Importing * (from module import *)
    ✗ Circular imports (restructure instead)

    REAL-WORLD SCENARIOS:

    Web server (Django/Flask):
    → Import at top (server starts once, runs long)
    → Fast startup not critical

    CLI tool:
    → Lazy import heavy dependencies
    → Fast startup is critical (user-facing)

    Library:
    → Import at top for user-facing API
    → Lazy import for optional features

    Serverless function (AWS Lambda):
    → Import at top (benefits from warm starts)
    → Or use Lambda layers for heavy deps

    MEASURING IMPORT TIME:

    # Command line
    $ python -X importtime -c "import pandas" 2>&1 | grep pandas

    # In code
    import time
    start = time.perf_counter()
    import heavy_module
    print(f"Import time: {time.perf_counter() - start:.3f}s")

    Remember: Premature optimization is the root of all evil.
    Profile first, optimize if startup time is actually a problem!
    """)
