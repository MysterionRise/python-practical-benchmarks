"""
FREE-THREADED PYTHON PERFORMANCE TEST (Python 3.13+ with free-threading build)

Question: How much faster is free-threaded Python for parallel CPU-bound work?

WHAT IS FREE-THREADING?
Python 3.13 introduced an experimental free-threaded mode (PEP 703) that removes
the Global Interpreter Lock (GIL), allowing true parallel execution of Python
threads on multiple CPU cores. This is a game-changer for CPU-bound workloads.

REQUIREMENTS:
- Python 3.13+ compiled with --disable-gil (free-threaded build)
- Check with: python -c "import sys; print(hasattr(sys, '_is_gil_enabled'))"
- On free-threaded builds: sys._is_gil_enabled() returns False

EXPECTED RESULTS (free-threaded vs standard Python):
| Workload Type           | Threads | GIL Python | Free-threaded | Speedup |
|-------------------------|---------|------------|---------------|---------|
| CPU-bound (prime calc)  | 1       | 1.0s       | 1.0s          | 1.0x    |
| CPU-bound (prime calc)  | 4       | 1.0s       | 0.25s         | ~4x     |
| CPU-bound (prime calc)  | 8       | 1.0s       | 0.13s         | ~8x     |
| I/O-bound (sleep)       | 4       | 0.25s      | 0.25s         | ~1x     |

KEY FINDINGS:
- Free-threaded Python provides near-linear speedup for CPU-bound threaded work
- Standard Python (with GIL) sees NO speedup from threading for CPU work
- I/O-bound work benefits from threading in both modes (GIL released during I/O)
- Free-threaded builds have ~5-10% single-thread overhead (tradeoff)

WHEN TO USE FREE-THREADED PYTHON:
- CPU-bound workloads that can be parallelized
- Scientific computing, data processing, simulations
- When multiprocessing overhead is prohibitive
- When shared memory is beneficial

WHEN TO STICK WITH STANDARD PYTHON:
- Single-threaded applications
- I/O-bound workloads (asyncio works great with GIL)
- When using C extensions not yet updated for free-threading
- Production systems (free-threading is still experimental)
"""

import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor

# Configuration
NUM_WORKERS = 4
WORK_ITERATIONS = 100000
PRIME_LIMIT = 1000


def is_free_threaded():
    """Check if running on a free-threaded Python build."""
    if hasattr(sys, "_is_gil_enabled"):
        return not sys._is_gil_enabled()
    return False


def get_python_mode():
    """Return a string describing the Python threading mode."""
    if hasattr(sys, "_is_gil_enabled"):
        if sys._is_gil_enabled():
            return "GIL enabled (standard mode)"
        else:
            return "GIL disabled (free-threaded mode)"
    return "Pre-3.13 (GIL always enabled)"


def is_prime(n):
    """Check if n is prime - CPU-intensive operation."""
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    for i in range(3, int(n**0.5) + 1, 2):
        if n % i == 0:
            return False
    return True


def cpu_bound_work(start, count):
    """CPU-bound work: count primes in a range."""
    primes = 0
    for n in range(start, start + count):
        if is_prime(n):
            primes += 1
    return primes


def io_bound_work(duration):
    """I/O-bound work: simulate with sleep."""
    time.sleep(duration)
    return duration


# ============================================================================
# BENCHMARK FUNCTIONS
# ============================================================================


def perf_test1_single_thread_cpu():
    """Baseline: Single-threaded CPU-bound work."""
    total = 0
    for i in range(NUM_WORKERS):
        total += cpu_bound_work(i * WORK_ITERATIONS, WORK_ITERATIONS)
    return total


def perf_test2_multi_thread_cpu():
    """Multi-threaded CPU-bound work using ThreadPoolExecutor."""
    with ThreadPoolExecutor(max_workers=NUM_WORKERS) as executor:
        futures = [executor.submit(cpu_bound_work, i * WORK_ITERATIONS, WORK_ITERATIONS) for i in range(NUM_WORKERS)]
        total = sum(f.result() for f in futures)
    return total


def perf_test3_manual_threads_cpu():
    """Multi-threaded CPU-bound work using manual threading."""
    results = [0] * NUM_WORKERS
    threads = []

    def worker(idx, start, count):
        results[idx] = cpu_bound_work(start, count)

    for i in range(NUM_WORKERS):
        t = threading.Thread(target=worker, args=(i, i * WORK_ITERATIONS, WORK_ITERATIONS))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    return sum(results)


def perf_test4_single_thread_io():
    """Baseline: Single-threaded I/O-bound work."""
    total = 0.0
    for _ in range(NUM_WORKERS):
        total += io_bound_work(0.01)
    return total


def perf_test5_multi_thread_io():
    """Multi-threaded I/O-bound work (should be fast in both modes)."""
    with ThreadPoolExecutor(max_workers=NUM_WORKERS) as executor:
        futures = [executor.submit(io_bound_work, 0.01) for _ in range(NUM_WORKERS)]
        total = sum(f.result() for f in futures)
    return total


if __name__ == "__main__":
    print("=" * 80)
    print("FREE-THREADED PYTHON PERFORMANCE TEST")
    print("=" * 80)
    print(f"Python version: {sys.version}")
    print(f"Threading mode: {get_python_mode()}")
    print(f"Workers: {NUM_WORKERS}")
    print(f"Work per worker: {WORK_ITERATIONS:,} iterations")
    print("=" * 80)
    print()

    # ========================================================================
    # CPU-BOUND WORKLOAD
    # ========================================================================
    print("CPU-BOUND WORKLOAD (counting primes)")
    print("-" * 60)

    start = time.perf_counter()
    result1 = perf_test1_single_thread_cpu()
    t1 = time.perf_counter() - start
    print(f"Single-threaded:              {t1:.4f}s  (found {result1} primes) [baseline]")

    start = time.perf_counter()
    result2 = perf_test2_multi_thread_cpu()
    t2 = time.perf_counter() - start
    speedup2 = t1 / t2 if t2 > 0 else 0
    symbol2 = "!" if speedup2 > 1.5 else ("~" if speedup2 > 0.9 else "-")
    print(f"ThreadPoolExecutor ({NUM_WORKERS} workers): {t2:.4f}s  (found {result2} primes) {speedup2:.2f}x {symbol2}")

    start = time.perf_counter()
    result3 = perf_test3_manual_threads_cpu()
    t3 = time.perf_counter() - start
    speedup3 = t1 / t3 if t3 > 0 else 0
    symbol3 = "!" if speedup3 > 1.5 else ("~" if speedup3 > 0.9 else "-")
    print(f"Manual threads ({NUM_WORKERS} workers):     {t3:.4f}s  (found {result3} primes) {speedup3:.2f}x {symbol3}")

    # ========================================================================
    # I/O-BOUND WORKLOAD
    # ========================================================================
    print()
    print("I/O-BOUND WORKLOAD (simulated with sleep)")
    print("-" * 60)

    start = time.perf_counter()
    result4 = perf_test4_single_thread_io()
    t4 = time.perf_counter() - start
    print(f"Single-threaded:              {t4:.4f}s  [baseline]")

    start = time.perf_counter()
    result5 = perf_test5_multi_thread_io()
    t5 = time.perf_counter() - start
    speedup5 = t4 / t5 if t5 > 0 else 0
    print(f"ThreadPoolExecutor ({NUM_WORKERS} workers): {t5:.4f}s  {speedup5:.2f}x (I/O parallelizes in both modes)")

    # ========================================================================
    # INTERPRETATION
    # ========================================================================
    print()
    print("=" * 80)
    print("INTERPRETATION")
    print("=" * 80)

    if is_free_threaded():
        print("""
    You are running FREE-THREADED Python (no GIL)!

    EXPECTED BEHAVIOR:
    - CPU-bound threading should show near-linear speedup (~{0}x with {0} workers)
    - I/O-bound threading works as expected (same as standard Python)

    This is the future of Python for CPU-bound parallel workloads!
        """.format(NUM_WORKERS))
    else:
        print("""
    You are running STANDARD Python (with GIL).

    EXPECTED BEHAVIOR:
    - CPU-bound threading shows NO speedup (GIL serializes execution)
    - I/O-bound threading works well (GIL released during I/O)

    TO TEST FREE-THREADED MODE:
    1. Install Python 3.13+ with free-threading enabled
       - macOS: brew install python@3.13 --enable-shared (check for free-threaded builds)
       - Linux: Build from source with ./configure --disable-gil
       - Or use the python3.13t binary if available

    2. Run this benchmark again to see the difference!

    ALTERNATIVE FOR CPU-BOUND PARALLELISM:
    - Use multiprocessing instead of threading
    - Use ProcessPoolExecutor for parallel CPU work
    - Each process has its own GIL, enabling true parallelism
        """)

    print("=" * 80)
    print("DECISION GUIDE")
    print("=" * 80)
    print("""
    WHEN FREE-THREADED PYTHON IS AVAILABLE:

    Use threading for CPU-bound work when:
    - Tasks can be parallelized
    - Shared memory access is beneficial
    - Process spawn overhead is prohibitive

    Use free-threaded Python for:
    - Scientific computing
    - Data processing pipelines
    - Image/video processing
    - Machine learning inference
    - Simulations and modeling

    COMPATIBILITY NOTES:
    - Not all C extensions support free-threading yet
    - Check extension documentation for GIL-free compatibility
    - Some packages may need updates (numpy, pandas, etc.)
    - Use threading.Lock for thread-safe shared state (still needed!)

    CURRENT STATE (as of Python 3.14):
    - Free-threading is experimental but functional
    - Performance overhead: ~5-10% for single-threaded code
    - Parallel speedup: Near-linear for CPU-bound work
    - Adoption: Growing ecosystem support
    """)
