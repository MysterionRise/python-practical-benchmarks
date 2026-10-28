# python-practical-benchmarks

[![Benchmark Tests](https://github.com/MysterionRise/python-practical-benchmarks/actions/workflows/tests.yml/badge.svg?branch=main)](https://github.com/MysterionRise/python-practical-benchmarks/actions/workflows/tests.yml)
[![Linting](https://github.com/MysterionRise/python-practical-benchmarks/actions/workflows/lint.yml/badge.svg?branch=main)](https://github.com/MysterionRise/python-practical-benchmarks/actions/workflows/lint.yml)
[![Security Scanning](https://github.com/MysterionRise/python-practical-benchmarks/actions/workflows/security-scan.yml/badge.svg?branch=main)](https://github.com/MysterionRise/python-practical-benchmarks/actions/workflows/security-scan.yml)
[![codecov](https://codecov.io/gh/MysterionRise/python-practical-benchmarks/branch/main/graph/badge.svg)](https://codecov.io/gh/MysterionRise/python-practical-benchmarks)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Checked with mypy](https://img.shields.io/badge/mypy-checked-blue)](https://mypy-lang.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**22 empirical benchmarks** answering real Python performance questions. Each benchmark includes timing data, caveats, and a decision guide for production use.

## Why This Project?

Most Python performance debates lack empirical data. This repository provides **real measurements** across 22 production scenarios—from basic dict access to free-threaded Python 3.13—with actionable decision guides.

**What makes this different:**
- **Data-driven**: Every recommendation backed by reproducible benchmarks
- **Production-focused**: Real-world scenarios, not micro-optimizations
- **Quality practices**: Type-checked, linted, security-scanned, and CI-tested on Python 3.9-3.15 and free-threaded 3.14t

Run the benchmarks on YOUR system—results vary by CPU, OS, and Python version.

## Quick Start

```bash
# First-time reviewer setup
make setup

# Run all quality gates and the quick benchmark suite
make verify

# Run a single benchmark
.venv/bin/python dict_access_perf_test.py

# See all available benchmarks
.venv/bin/python run_all_tests.py --list

# Run all benchmarks (fast mode for CI/testing)
.venv/bin/python run_all_tests.py --all --quick

# Produce structured benchmark results
.venv/bin/python run_all_tests.py --all --quick --format json
.venv/bin/python run_all_tests.py --category basic --quick --format json --output reports/output/basic.json

# Produce local portfolio evidence
make bench-report

# Run by category
.venv/bin/python run_all_tests.py --category basic --quick
.venv/bin/python run_all_tests.py --category advanced --quick
.venv/bin/python run_all_tests.py --category expert --quick
```

If your shell's `python` command already resolves to Python 3.9+, the direct `python run_all_tests.py ...` commands remain supported.

## Portfolio Evidence

- [Benchmark methodology](docs/METHODOLOGY.md) explains warmups, repeated runs, quick mode, optional skips, and measurement limits.
- [Portfolio case study](docs/PORTFOLIO_CASE_STUDY.md) explains the architecture, tradeoffs, and reviewer-facing proof points.
- [Report generation](reports/README.md) explains how JSON and Markdown benchmark evidence is produced.
- [Sample quick report](reports/samples/quick-summary.md) provides machine-specific evidence generated from the structured runner.

## Performance Caveats

**Results vary based on:**
- CPU architecture and speed
- Operating system (Linux, macOS, Windows)
- Python implementation (CPython, PyPy)
- Python version (3.11+ has significant optimizations)
- System load and available memory

**Run benchmarks on YOUR system for accurate decisions.** The result tables in this README are illustrative examples, not measured output from the current code. For measured, machine-specific results see the [sample quick report](reports/samples/quick-summary.md) or generate your own with `make bench-report`.

## Table of Contents

### Basic Benchmarks
1. [2D Array Iteration](#1-2d-array-iteration)
2. [Pandas DataFrame Iteration](#2-pandas-dataframe-iteration)
3. [Dictionary Access](#3-dictionary-access)
4. [String Concatenation](#4-string-concatenation)
5. [List Operations](#5-list-operations)
6. [File I/O Operations](#6-file-io-operations)
7. [JSON Serialization/Deserialization](#7-json-serializationdeserialization)
8. [Set Operations](#8-set-operations)
9. [Function Call Overhead](#9-function-call-overhead)
10. [Data Structure Lookups](#10-data-structure-lookups)

### Advanced Benchmarks
11. [Concurrency Patterns](#11-concurrency-patterns-asyncawait-vs-threading-vs-multiprocessing)
12. [Regex Performance](#12-regex-performance-compilation-and-alternatives)
13. [Object Creation Patterns](#13-object-creation-patterns-dataclass-vs-namedtuple-vs-slots)
14. [Deep Copy Strategies](#14-deep-copy-strategies)
15. [Generator vs Iterator Patterns](#15-generator-vs-iterator-patterns)

### Expert-Level Benchmarks
16. [Attribute Access & Descriptors](#16-attribute-access--descriptors)
17. [Exception Handling (EAFP vs LBYL)](#17-exception-handling-eafp-vs-lbyl)
18. [Serialization Formats](#18-serialization-formats)
19. [Context Manager Overhead](#19-context-manager-overhead)
20. [Import Strategies](#20-import-strategies)
21. [Free-Threaded Python (3.13+)](#21-free-threaded-python-313)
22. [JIT Compiler Performance (3.13+)](#22-jit-compiler-performance-313)

---

## 1. 2D Array Iteration

**File:** `iterate_2d_array_perf_test.py`

What is the optimal way to iterate 2d arrays (lists) in Python?

**Use case:** Algorithmic and competitive programming (Codeforces, TopCoder, ACM ICPC, etc.)

```
Number of iterations = 100, size of 2d array = 1000 x 1000

Approach                         Total time    Per iteration
---------------------------------------------------------------
- range() + indices              11.2518s            0.1125s
- iterate + .index()            216.3334s            2.1633s
- enumerate()                     8.3070s            0.0830s
- 1d array approach              16.5849s            0.1658s
- numpy ndarray (NON-STDLIB)     28.0520s            0.2805s
```

**Winner:** `range()` with indices and `enumerate()` perform about the same when both do the same work per cell, so prefer `enumerate()` for readability. Never look up indices with `.index()`, which makes the loop quadratic. Element-by-element access to a NumPy array is slower than plain lists; vectorize NumPy code instead.

---

## 2. Pandas DataFrame Iteration

**File:** `iterate_df_pandas_perf_test.py`

What is the optimal way to iterate over dataframes in Pandas?

**Use case:** Data scientists and data analysts working with Pandas DataFrames

```
Number of iterations = 100, shape of dataframe  = (22544, 43)
7 columns summed per row

Approach                         Total time    Per iteration
---------------------------------------------------------------
iterrows                         31.231000        0.31231
loc                              21.503000        0.21503
iloc                             14.528000        0.14528
itertuples                        4.045000        0.04045
list comprehension                0.236000        0.00236
pandas vectorisation             0.0000065        < 1e-7
numpy vectorisation              0.0000041        < 1e-7
```

Graph of performance with X-axis representing number of affecting columns (from 2 to 7):

<img src="performance.png">

**Winner:** Vectorization (Pandas or NumPy) is orders of magnitude faster than row iteration, and plain NumPy arrays skip some pandas overhead. Use `.itertuples()` if row-wise iteration is absolutely necessary. Earlier versions of this benchmark returned from the two vectorisation cases before computing anything, so their old timings measured an empty function.

---

## 3. Dictionary Access

**File:** `dict_access_perf_test.py`

What is the most efficient way to access dictionary values by key?

**Use case:** High-performance data lookups, caching, algorithmic competitions

```
Sequential access, number of iterations = 1000, size of dictionary = 100000

Approach                         Total time         Per iteration
------------------------------------------------------------------
- dict[key]                         8.987797s            0.008988s
- dict.get(key)                     7.061445s            0.007061s
- dict.setdefault(key, default)     7.511971s            0.007512s
- using defaultdict                 5.458365s            0.005458s
```

**Winner:** For keys that exist, `dict[key]`, `dict.get()`, `dict.setdefault()` and `defaultdict` perform about the same, so choose by semantics: `d[key]` when the key must exist, `.get()` when it may be missing, and `defaultdict` when a missing key should be created. This benchmark only looks up existing keys.

---

## 4. String Concatenation

**File:** `string_concat_perf_test.py`

What is the most efficient way to concatenate strings in Python?

**Use case:** Logging, CSV generation, HTML/XML generation, API response building

```
Number of iterations = 100, number of strings to concatenate = 10000

Approach                         Total time    Per iteration
---------------------------------------------------------------
+ operator in loop               5.2341s            0.0523s
str.join() with list             0.3214s            0.0032s
f-strings in loop                6.1203s            0.0612s
str.format() in loop             7.8934s            0.0789s
io.StringIO                      0.4521s            0.0045s
List comprehension + join        0.2987s            0.0030s
''.join(generator)               0.3102s            0.0031s
```

**Winner:** List comprehension + `str.join()` or generator expression + `str.join()` - avoid using `+` operator in loops!

---

## 5. List Operations

**File:** `list_operations_perf_test.py`

What is the most efficient way to build and manipulate lists in Python?

**Use case:** Data transformation, filtering, ETL pipelines

```
Number of iterations = 100, number of items = 10000

Approach                         Total time    Per iteration
---------------------------------------------------------------
append() in loop                 0.1234s            0.0012s
extend() with multiple items     0.0987s            0.0010s
List comprehension               0.0756s            0.0008s
map() + list()                   0.0823s            0.0008s
+= operator                      0.1456s            0.0015s
Pre-allocated list + indices     0.0891s            0.0009s
chain.from_iterable() flatten   0.0734s            0.0007s
```

**Winner:** List comprehension (or a pre-sized list) for building lists. `itertools.chain.from_iterable()` is the fast way to flatten lists you already have, not a way to compute new values. Avoid `+=` with one-item lists in loops.

---

## 6. File I/O Operations

**File:** `file_io_perf_test.py`

What is the most efficient way to read files in Python?

**Use case:** Log processing, data ingestion, configuration files

```
Number of iterations = 100, file size = ~1MB (10000 lines)

Approach                         Total time    Per iteration
---------------------------------------------------------------
read() entire file               0.3421s            0.0034s
readline() in loop               0.5234s            0.0052s
readlines() all at once          0.3567s            0.0036s
iteration with 'with open'       0.4123s            0.0041s
pathlib.Path.read_text()         0.3398s            0.0034s
buffered reading (8KB)           0.4567s            0.0046s
buffered reading (64KB)          0.3876s            0.0039s
```

**Winner:** `pathlib.Path.read_text()` or `read()` for small to medium files. Use iteration for large files to manage memory.

---

## 7. JSON Serialization/Deserialization

**File:** `json_perf_test.py`

What is the most efficient way to serialize/deserialize JSON in Python?

**Use case:** REST APIs, configuration management, data storage

```
Number of iterations = 1000, data structure size = 1000 nested objects

SERIALIZATION:
Approach                         Total time    Per iteration
---------------------------------------------------------------
json.dumps()                     2.3421s            0.0023s
json.dumps(indent=2)             3.5678s            0.0036s
ujson.dumps()                    0.8234s            0.0008s
orjson.dumps()                   0.4567s            0.0005s

DESERIALIZATION:
Approach                         Total time    Per iteration
---------------------------------------------------------------
json.loads()                     1.8234s            0.0018s
ujson.loads()                    0.6543s            0.0007s
orjson.loads()                   0.5123s            0.0005s
```

**Winner:** `orjson` for high-performance needs, standard `json` library for most use cases.

---

## 8. Set Operations

**File:** `set_operations_perf_test.py`

What is the most efficient way to perform set operations for deduplication and membership testing?

**Use case:** Duplicate removal, filtering, membership checks, data validation

```
Number of iterations = 1000, data size = 10000 items

MEMBERSHIP TESTING:
Approach                         Total time    Per iteration
---------------------------------------------------------------
x in list                        45.2341s            0.0452s
x in set                          0.1234s            0.0001s
x in dict.keys()                  0.1456s            0.0001s
x in frozenset                    0.1298s            0.0001s

DEDUPLICATION:
Approach                         Total time    Per iteration
---------------------------------------------------------------
list(set())                       0.4521s            0.0005s
dict.fromkeys()                   0.5234s            0.0005s
Manual loop with set              0.8967s            0.0009s
Manual loop with dict             0.9123s            0.0009s
```

**Winner:** Use `set` for membership testing (400x faster than list!). Use `list(set())` for deduplication unless you need to preserve order (then use `dict.fromkeys()`).

---

## 9. Function Call Overhead

**File:** `function_call_perf_test.py`

What is the overhead of different function call patterns in Python?

**Use case:** Framework design, API optimization, hot path optimization

```
Number of iterations = 100000, number of calls per iteration = 1000

Approach                         Total time    Per iteration
---------------------------------------------------------------
Direct function call             0.3421s            0.0000034s
Lambda function                  0.4234s            0.0000042s
Instance method call             0.5678s            0.0000057s
Static method call               0.4123s            0.0000041s
Class method call                0.4567s            0.0000046s
Function with *args, **kwargs    0.8234s            0.0000082s
Decorator overhead               0.4891s            0.0000049s
@lru_cache (cached)              0.1234s            0.0000012s
@lru_cache (uncached)            0.5432s            0.0000054s
```

**Winner:** Direct function calls are fastest, and a lambda costs the same as an equivalent `def`. `@lru_cache` pays off only when the function costs more than hashing its arguments; for a trivial function a cache hit can be slower than just calling it. Avoid `*args, **kwargs` in hot paths.

---

## 10. Data Structure Lookups

**File:** `data_structure_lookup_perf_test.py`

What is the most efficient data structure for lookups in Python?

**Use case:** Cache implementation, lookup tables, indexing strategies

```
SMALL DATASET (100 items):
Approach                         Total time    Per iteration
---------------------------------------------------------------
List sequential search           0.8234s            0.0008s
List binary search (bisect)      0.1234s            0.0001s
Dict lookup                      0.0456s            0.0000s
Set membership                   0.0467s            0.0000s

LARGE DATASET (100,000 items):
Approach                         Total time    Per iteration
---------------------------------------------------------------
List sequential search           [SKIPPED - too slow]
List binary search (bisect)      0.1789s            0.0002s
Dict lookup                      0.0501s            0.0001s
Set membership                   0.0512s            0.0001s
```

**Winner:** `dict` or `set` for O(1) constant-time lookups. Use `bisect` for sorted data when you need ordering.

---

## 11. Concurrency Patterns (async/await vs Threading vs Multiprocessing)

**File:** `concurrency_patterns_perf_test.py`

What is the most efficient concurrency pattern for different workload types?

**Use case:** Web servers, data processing, I/O operations, CPU-intensive tasks

```
I/O-BOUND WORKLOAD (100 tasks, 0.01s sleep each):
Approach                         Total time    Speedup
---------------------------------------------------------------
Synchronous (sequential)         1.234s             1.0x
Async/await (asyncio)            0.123s            10.0x ✓
Threading (ThreadPoolExecutor)   0.145s             8.5x
Threading (manual threads)       0.156s             7.9x

CPU-BOUND WORKLOAD (100 tasks, prime calculations):
Approach                         Total time    Speedup
---------------------------------------------------------------
Synchronous (sequential)         3.456s             1.0x
Async/await (asyncio)            3.498s             0.99x ⚠ overhead!
Threading (ThreadPoolExecutor)   3.512s             0.98x ⚠ GIL!
Multiprocessing (ProcessPool)    0.892s             3.9x ✓
```

**Winner:** Use **async/await** or threads for I/O-bound work. On standard (GIL) builds, use **multiprocessing** for CPU-bound work, but process start-up dominates small jobs, and since Python 3.14 Linux defaults to the slower-starting `forkserver` start method. Threads do run CPU-bound Python in parallel on free-threaded builds ([section 21](#21-free-threaded-python-313)).

---

## 12. Regex Performance (Compilation and Alternatives)

**File:** `regex_performance_perf_test.py`

What is the most efficient way to use regular expressions?

**Use case:** Pattern matching, validation, text processing, parsing

```
SIMPLE PATTERN MATCHING (1000 iterations, 10000 strings):
Approach                         Total time    Per iteration
---------------------------------------------------------------
re.match() uncompiled            2.345s            0.0023s
re.match() pre-compiled          1.234s            0.0012s ✓ 2x faster
str.startswith()                 0.123s            0.0001s ✓ 19x faster!
str in string                    0.089s            0.0001s ✓ 26x faster!

EMAIL VALIDATION:
Approach                         Total time    Per iteration
---------------------------------------------------------------
Full RFC-compliant regex         5.678s            0.0057s
Simple practical regex           1.234s            0.0012s ✓ 5x faster
String methods validation        0.567s            0.0006s ✓ 10x faster
```

**Winner:** **Pre-compile** patterns used in hot loops: the `re` module caches compiled patterns, so `re.match()` does not recompile, but `re.compile()` skips the cache lookup. Use **string methods** for simple patterns. Keep regex patterns simple - avoid RFC-compliant email validation.

---

## 13. Object Creation Patterns (dataclass vs namedtuple vs __slots__)

**File:** `object_creation_patterns_perf_test.py`

What is the most efficient way to create data-holding objects?

**Use case:** Data models, DTOs, configuration objects, ORM models

```
OBJECT CREATION (1,000,000 instances):
Approach                         Total time    Memory
---------------------------------------------------------------
Regular class                    0.234s             100%
Regular class with __slots__     0.198s              45% ✓
namedtuple                       0.156s              42% ✓ fastest immutable
dataclass                        0.287s             100%
dataclass with __slots__         0.245s              45% ✓
dict                             0.189s             110% ⚠

ATTRIBUTE ACCESS (10,000,000 reads):
Approach                         Time          Per access
---------------------------------------------------------------
Regular class                    0.456s            45.6ns
Regular class with __slots__     0.398s            39.8ns ✓ 15% faster
namedtuple                       0.423s            42.3ns
dataclass with __slots__         0.401s            40.1ns ✓
```

**Winner:** Use **namedtuple** for immutable data (fastest + least memory). Use **dataclass with __slots__=True** for mutable data (Python 3.10+). **__slots__** mainly saves memory; since Python 3.11 attribute access is specialized for regular classes too, so the speed gain is small.

---

## 14. Deep Copy Strategies

**File:** `deep_copy_strategies_perf_test.py`

What is the most efficient way to copy data structures?

**Use case:** Defensive copying, cloning objects, avoiding mutations

```
SIMPLE LISTS (10000 iterations, 1000 items):
Approach                         Total time    Per iteration
---------------------------------------------------------------
list.copy()                      0.234s            0.000023s ✓
list[:]                          0.235s            0.000024s
copy.deepcopy()                  2.345s            0.000235s ⚠ 10x slower!

NESTED LISTS (1000 iterations, 100x100 nested):
Approach                         Total time    Per iteration
---------------------------------------------------------------
list.copy() - WRONG!             0.123s            0.000123s ⚠ shallow!
copy.deepcopy()                  1.234s            0.001234s ✓ correct
json.loads(json.dumps())         0.456s            0.000456s (JSON-safe data only)

CUSTOM OBJECTS:
Approach                         Total time    Per iteration
---------------------------------------------------------------
Manual copy constructor          0.123s            0.000012s ✓ fastest
copy.copy()                      0.234s            0.000023s
copy.deepcopy()                  0.567s            0.000057s
```

**Winner:** Use **shallow copy** when possible (list.copy(), dict.copy()). For nested JSON-safe data, a **JSON round-trip** can beat `deepcopy` on older Pythons, but the gap disappears in our 3.14 runs, and the round-trip turns tuples into lists and non-string keys into strings. Use **manual copy constructors** for custom objects.

---

## 15. Generator vs Iterator Patterns

**File:** `generator_vs_iterator_perf_test.py`

What is the most memory-efficient way to iterate?

**Use case:** Large datasets, data pipelines, streaming, memory-constrained environments

```
SIMPLE ITERATION (1,000,000 items):
Approach                         Time          Memory
---------------------------------------------------------------
List (materialize all)           0.234s        ~38 MB           100%
Generator expression             0.267s        ~0.1 MB          0.26% ✓
Generator function               0.271s        ~0.1 MB          0.26% ✓
range() builtin                  0.245s        ~0.1 MB          0.26% ✓ fastest

DATA TRANSFORMATION PIPELINE (100,000 items):
Approach                         Time          Memory
---------------------------------------------------------------
List + multiple passes           0.456s        ~24 MB
Generator pipeline               0.389s        ~0.1 MB ✓ 1.2x faster
filter/map/islice pipeline       0.367s        ~0.1 MB ✓ 1.2x faster
```

**Winner:** Use **generators** or itertools for large datasets: memory stays flat, and lazy pipelines stop as soon as they have enough results, while list pipelines build every stage first. Use **lists** when you need random access, multiple passes, or the data is small.

---

## 16. Attribute Access & Descriptors

**File:** `attribute_access_perf_test.py`

What is the overhead of different attribute access patterns?

**Use case:** ORMs (SQLAlchemy), validation frameworks (Pydantic), dynamic attributes

```
ATTRIBUTE READ (10,000,000 accesses):
Approach                         Total time    Per access    Overhead
---------------------------------------------------------------
Direct attribute (normal)        0.234s            23.4ns        1.0x
__slots__ attribute              0.198s            19.8ns        0.85x ✓ 15% faster
Property (simple)                0.456s            45.6ns        1.95x
Property (cached_property)       0.201s            20.1ns        0.86x ✓ after cache
__getattribute__ override        1.234s           123.4ns        5.27x ⚠ very slow!
__getattr__ fallback             0.987s            98.7ns        4.22x ⚠ slow!
Descriptor protocol              0.678s            67.8ns        2.90x

ATTRIBUTE WRITE (10,000,000 writes):
Approach                         Total time    Per write
---------------------------------------------------------------
Direct attribute (normal)        0.312s            31.2ns        1.0x
__slots__ attribute              0.267s            26.7ns        0.86x ✓ 14% faster
Property with setter             0.567s            56.7ns        1.82x
__setattr__ override             1.456s           145.6ns        4.67x ⚠ very slow!
Descriptor protocol              0.789s            78.9ns        2.53x
```

**Winner:** Use **__slots__** for high-volume objects to save memory; the access-speed gain is small on Python 3.11+. Use **@property** for computed/validated attributes (2x overhead). AVOID **__getattribute__** and **__setattr__** in hot paths (4-5x overhead!).

---

## 17. Exception Handling (EAFP vs LBYL)

**File:** `exception_handling_perf_test.py`

What is the performance impact of exception handling?

**Use case:** Input validation, error handling, control flow decisions

```
DICTIONARY KEY ACCESS (1,000,000 iterations, 90% success):
Approach                         Total time    Per iteration
---------------------------------------------------------------
LBYL: if key in dict             0.234s            0.234μs
EAFP: try/except (90% success)   1.456s            1.456μs ⚠ 6x slower!
EAFP: try/except (100% success)  0.267s            0.267μs ✓ best case
dict.get() with default          0.198s            0.198μs ✓ fastest

EXCEPTION RAISING COST (100,000 iterations):
Approach                         Total time    Per raise
---------------------------------------------------------------
No exception                     0.012s            0.12μs
Raise + catch Exception          2.345s           23.45μs ⚠ 195x slower!
Return error code                0.045s            0.45μs ✓ 4x slower
```

**Winner:** Use **EAFP (try/except)** when errors are rare: since Python 3.11 a `try` block that doesn't raise is nearly free. Use **LBYL** or `.get()` when failures are common, because raising and catching costs far more than a branch. The crossover depends on your failure rate, so measure it.

---

## 18. Serialization Formats

**File:** `serialization_formats_perf_test.py`

What is the most efficient serialization format?

**Use case:** APIs, caching, inter-process communication, data persistence

```
SMALL DICT (1000 iterations, ~1KB data):
Format          Serialize    Deserialize  Size
---------------------------------------------------------------
pickle          0.012s       0.015s       158 bytes
json            0.034s       0.023s       142 bytes
orjson          0.008s       0.009s       142 bytes ✓ 3x faster
msgpack         0.010s       0.012s       128 bytes ✓ smallest
marshal         0.008s       0.010s       145 bytes ✓ fastest

NUMERIC ARRAYS (10,000 integers):
Format          Serialize    Size
---------------------------------------------------------------
pickle          0.234s       89,123 bytes
orjson          0.123s       88,894 bytes
msgpack         0.178s       70,123 bytes
numpy raw bytes 0.045s       40,080 bytes (no dtype/shape header)
```

**Winner:** Use **orjson** for JSON (3-5x faster than stdlib). Use **msgpack** for compact binary (20% smaller). Raw **NumPy buffers** are fast and compact for fixed-width numbers but carry no dtype or shape; use `np.save`/`np.load` for a self-describing format. Use **pickle** only for Python-to-Python. NEVER use pickle with untrusted data!

---

## 19. Context Manager Overhead

**File:** `context_manager_perf_test.py`

What is the overhead of context managers?

**Use case:** Resource management, setup/teardown, temporary state

```
BASIC OPERATIONS (1,000,000 iterations):
Approach                         Total time    Overhead
---------------------------------------------------------------
No context manager               0.089s        1.0x (baseline)
Class-based __enter__/__exit__   0.234s        2.6x
@contextmanager decorator        0.345s        3.9x
Manual try/finally               0.134s        1.5x ✓ lowest

EXCEPTION HANDLING (100,000 iterations, 10% errors):
Approach                         Total time
---------------------------------------------------------------
Class-based (propagate)          2.345s
Class-based (suppress)           0.456s ✓ 5x faster
contextlib.suppress()            0.389s ✓ fastest
```

**Winner:** **Class-based context managers** are cheaper than `@contextmanager` generators. Use **manual try/finally** only in performance-critical inner loops. Always use context managers for resources - each `with` adds a small fixed cost that is negligible next to real resource work.

---

## 20. Import Strategies

**File:** `import_strategies_perf_test.py`

What is the performance impact of imports?

**Use case:** Startup time, CLI tools, serverless functions, module organization

```
MODULE IMPORT TIME (first import):
Module                           Import time
---------------------------------------------------------------
json (stdlib)                    0.0023s
re (stdlib)                      0.0034s
numpy                            0.1234s ⚠
pandas                           0.3456s ⚠⚠ very heavy!

IMPORT PATTERNS (100,000 iterations, cached, measured on CPython 3.13):
Pattern                          Total time
---------------------------------------------------------------
import module                    0.0065s ✓ cheap (sys.modules lookup)
from module import name          0.0255s ✓ cheap, plus name binding
importlib.import_module()        0.0381s ⚠ ~6x import statement: hoist out of hot loops

LAZY vs EAGER (illustrative; the benchmark measures per-call cost after the first import, not startup):
Strategy                         Startup    First use
---------------------------------------------------------------
Eager (import at top)            0.234s     0.001s (fast use)
Lazy (import on use)             0.001s     0.234s (fast startup) ✓ CLI tools
```

**Winner:** **Import at module top** (standard pattern) - re-importing a loaded module is a cheap `sys.modules` lookup. Use **lazy imports** only for CLI tools with heavy dependencies (pandas, tensorflow). **"from X import Y"** saves one attribute lookup per use, which matters only in very hot loops. Hoist `importlib.import_module()` out of hot loops.

---

## 21. Free-Threaded Python (3.13+)

**File:** `free_threaded_perf_test.py`

How much faster is free-threaded Python for parallel CPU-bound work?

**Use case:** CPU-bound parallel workloads, scientific computing, data processing

```
CPU-BOUND WORKLOAD (4 threads, counting primes):
Mode                             Time      Speedup
---------------------------------------------------------------
Single-threaded                  1.000s    1.0x (baseline)
Threading (GIL Python)           1.020s    0.98x ⚠ NO SPEEDUP!
Threading (Free-threaded)        0.260s    3.85x ✓

I/O-BOUND WORKLOAD (4 threads, 10ms sleep each):
Mode                             Time      Speedup
---------------------------------------------------------------
Single-threaded                  0.040s    1.0x
Threading (both modes)           0.010s    4.0x ✓
```

**Winner:** **Free-threaded Python**, officially supported since 3.14 ([PEP 779](https://peps.python.org/pep-0779/)), lets threads run CPU-bound Python code in parallel. The Python docs put its single-threaded slowdown at roughly 1-8% depending on platform, and it uses more memory. Standard (GIL) builds see no speedup from threading for CPU work; use **multiprocessing** there.

**Note:** Free-threaded Python requires Python 3.13+ built with `--disable-gil`. Check with `python -c "import sys; print(sys._is_gil_enabled())"`, which prints `False` when the GIL is disabled.

---

## 22. JIT Compiler Performance (3.13+)

**File:** `jit_numeric_perf_test.py`

How much does Python's experimental JIT compiler improve numeric workloads?

**Use case:** Numeric computing, tight loops, simulations, scientific code

```
NUMERIC WORKLOADS (Python 3.13+ with JIT):
Workload                    No JIT      With JIT    Improvement
---------------------------------------------------------------
Tight numeric loop          1.00s       0.80s       ~20%
Mandelbrot calculation      1.00s       0.75s       ~25%
Float arithmetic            1.00s       0.70s       ~30%
Integer arithmetic          1.00s       0.85s       ~15%
```

**Winner:** Python's **experimental JIT** ranges from about 10% slower to 20% faster on 3.14 according to its release notes, and averages roughly 7-12% faster on pyperformance in 3.15. Official 3.14 macOS and Windows binaries include it switched off, and free-threaded builds have no JIT. For serious numeric work, **NumPy** or **Numba** remain far faster.

**Note:** The JIT needs a CPython 3.13+ build configured with `--enable-experimental-jit`. Builds configured with `=yes-off`, common for 3.14 distributions, ship it disabled, so enable it with `PYTHON_JIT=1`. Builds configured with plain `=yes` enable it by default, and `PYTHON_JIT=0` turns it off. On 3.14+, check with `python -c "import sys; print(sys._jit.is_enabled())"`.

---

## Installation

```bash
# Clone the repository
git clone https://github.com/MysterionRise/python-practical-benchmarks.git
cd python-practical-benchmarks

# Install dependencies (includes dev tools)
pip install -r requirements.txt

# Or install as editable package with all dependencies
pip install -e ".[all]"

# Optional: Install only optional benchmark libraries
pip install -r requirements-optional.txt
```

## Running Benchmarks

Each benchmark can be run independently:

```bash
# Basic benchmarks
python iterate_2d_array_perf_test.py
python iterate_df_pandas_perf_test.py
python dict_access_perf_test.py
python string_concat_perf_test.py
python list_operations_perf_test.py
python file_io_perf_test.py
python json_perf_test.py
python set_operations_perf_test.py
python function_call_perf_test.py
python data_structure_lookup_perf_test.py

# Advanced benchmarks
python concurrency_patterns_perf_test.py
python regex_performance_perf_test.py
python object_creation_patterns_perf_test.py
python deep_copy_strategies_perf_test.py
python generator_vs_iterator_perf_test.py

# Expert-level benchmarks
python attribute_access_perf_test.py
python exception_handling_perf_test.py
python serialization_formats_perf_test.py
python context_manager_perf_test.py
python import_strategies_perf_test.py
python free_threaded_perf_test.py    # Requires Python 3.13+ free-threaded build
python jit_numeric_perf_test.py      # Benefits from Python 3.13+ with JIT
```

## Key Takeaways

### Basic Performance Principles
1. **Always use vectorization** with Pandas/NumPy when possible (orders of magnitude faster)
2. **Prefer `str.join()`** for building strings in loops - CPython's in-place `s += t` optimization is an implementation detail (PEP 8)
3. **Use `set` or `dict` for membership testing** - they're O(1) vs O(n) for lists (400x faster!)
4. **List comprehensions are faster** than manual loops for building lists
5. **`enumerate()` is the most readable way** to iterate with indices, and as fast as `range()` indexing
6. **`@lru_cache` helps when the function is expensive** - for trivial functions a cache hit can cost more than the call
7. **Prefer comprehensions** - pre-allocating `[0] * n` rarely helps in CPython because `append` is amortized O(1)

### Advanced Performance Patterns
8. **Use async/await or threads for I/O-bound work**, **multiprocessing for CPU-bound work on GIL builds** - process start-up dominates small jobs
9. **On standard (GIL) builds, async and threads don't parallelize pure-Python CPU work** - free-threaded builds ([section 21](#21-free-threaded-python-313)) and GIL-releasing C code (NumPy, hashlib, zlib) do
10. **`re.compile()` skips the pattern-cache lookup** - module-level `re.match()` doesn't recompile, so gains are modest outside tight loops
11. **Use string methods** instead of regex for simple patterns (10-30x faster)
12. **Use `__slots__` for classes with many instances** - mainly a memory win; 3.11+ specializes attribute access for regular classes too
13. **namedtuple is fastest for immutable data**, dataclass with slots for mutable
14. **Shallow copy when possible** - deepcopy walks the whole structure
15. **Use generators for large datasets** - memory stays flat and lazy pipelines can stop early
16. **A JSON round-trip can beat deepcopy for JSON-safe data on older Pythons** - but it turns tuples into lists and non-string keys into strings
17. **Manual copy constructors are fastest** for custom objects

### Expert-Level Insights
18. **Avoid `__getattribute__` and `__setattr__`** - they add 4-5x overhead to every attribute access
19. **Use `@cached_property`** for expensive computations - nearly zero overhead after first access
20. **Raising and catching is far costlier than a branch** - a non-raising `try` is nearly free on 3.11+, so don't use exceptions for routine hot-loop control flow
21. **EAFP wins when failures are rare, LBYL or `.get()` when they are common** - measure the crossover for your failure rate
22. **orjson is 3-5x faster than standard json** - use for performance-critical APIs
23. **msgpack is 20% smaller than JSON** - best for network protocols
24. **Raw NumPy buffers are fast and compact for fixed-width numbers** - but carry no dtype or shape; use `np.save` for a self-describing format
25. **Each `with` has a small fixed cost** - negligible next to real resource work, so always use context managers for resources
26. **Class-based context managers are cheaper** than `@contextmanager` generators
27. **Import heavy modules (pandas) takes 350ms** - use lazy imports for CLI tools
28. **Re-importing a loaded module is cheap but not free** (a `sys.modules` lookup, roughly 100 ns) - import at module top unless lazy loading is needed
29. **"from X import Y" saves one attribute lookup per use** - it only matters in very hot loops, and it binds at import time, so later patching of `X.Y` is not seen
30. **`importlib.import_module()` costs several times more than an `import` statement** - use it for dynamic module names and hoist it out of hot loops

## Contributing

Feel free to suggest additional benchmarks or improvements via issues or pull requests!

## License

MIT License - feel free to use these benchmarks in your projects.
