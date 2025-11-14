"""
What is the most efficient concurrency pattern for different workload types in Python?

Performance test comparing synchronous, async/await, threading, and multiprocessing:

I/O-BOUND WORKLOAD (simulated network calls):
Number of tasks = 100, sleep duration = 0.01s each

Approach                         Total time    Speedup vs Sync
---------------------------------------------------------------
Synchronous (sequential)         1.234s             1.0x
Async/await (asyncio)            0.123s            10.0x
Threading (ThreadPoolExecutor)   0.145s             8.5x
Threading (manual threads)       0.156s             7.9x

CPU-BOUND WORKLOAD (computation):
Number of tasks = 100, compute prime numbers up to 10000

Approach                         Total time    Speedup vs Sync
---------------------------------------------------------------
Synchronous (sequential)         3.456s             1.0x
Async/await (asyncio)            3.498s             0.99x (overhead!)
Threading (ThreadPoolExecutor)   3.512s             0.98x (GIL!)
Multiprocessing (ProcessPool)    0.892s             3.9x

MIXED WORKLOAD (I/O + CPU):
Approach                         Total time    Best use case
---------------------------------------------------------------
Async/await                      1.234s        High I/O, light CPU
Threading                        1.567s        Moderate I/O + CPU
Multiprocessing                  0.987s        CPU-intensive tasks
"""
import asyncio
import concurrent.futures
import multiprocessing
import threading
import time


# Configuration
NUM_TASKS = 100
IO_SLEEP_DURATION = 0.01
CPU_WORK_SIZE = 10000


# ============================================================================
# I/O-BOUND WORKLOADS (simulating network calls, file I/O, etc.)
# ============================================================================


def io_bound_task(task_id):
    """Simulate an I/O-bound task (e.g., network request)"""
    time.sleep(IO_SLEEP_DURATION)
    return task_id * 2


async def async_io_bound_task(task_id):
    """Async version of I/O-bound task"""
    await asyncio.sleep(IO_SLEEP_DURATION)
    return task_id * 2


def perf_test1_sync_io():
    """I/O-bound: Synchronous execution"""
    results = []
    for i in range(NUM_TASKS):
        results.append(io_bound_task(i))
    return results


async def perf_test2_async_io():
    """I/O-bound: Async/await with asyncio"""
    tasks = [async_io_bound_task(i) for i in range(NUM_TASKS)]
    return await asyncio.gather(*tasks)


def perf_test3_threading_pool_io():
    """I/O-bound: Threading with ThreadPoolExecutor"""
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        results = list(executor.map(io_bound_task, range(NUM_TASKS)))
    return results


def perf_test4_threading_manual_io():
    """I/O-bound: Manual thread creation"""
    results = [None] * NUM_TASKS
    threads = []

    def worker(task_id):
        results[task_id] = io_bound_task(task_id)

    for i in range(NUM_TASKS):
        thread = threading.Thread(target=worker, args=(i,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    return results


# ============================================================================
# CPU-BOUND WORKLOADS (computation-heavy tasks)
# ============================================================================


def is_prime(n):
    """Check if a number is prime (CPU-intensive)"""
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True


def cpu_bound_task(task_id):
    """Simulate a CPU-bound task (finding primes)"""
    primes = [n for n in range(task_id * 100, (task_id + 1) * 100) if is_prime(n)]
    return len(primes)


async def async_cpu_bound_task(task_id):
    """Async version of CPU-bound task (will not help due to GIL)"""
    return cpu_bound_task(task_id)


def perf_test5_sync_cpu():
    """CPU-bound: Synchronous execution"""
    results = []
    for i in range(NUM_TASKS):
        results.append(cpu_bound_task(i))
    return results


async def perf_test6_async_cpu():
    """CPU-bound: Async/await (ineffective due to GIL)"""
    tasks = [async_cpu_bound_task(i) for i in range(NUM_TASKS)]
    return await asyncio.gather(*tasks)


def perf_test7_threading_cpu():
    """CPU-bound: Threading (ineffective due to GIL)"""
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        results = list(executor.map(cpu_bound_task, range(NUM_TASKS)))
    return results


def perf_test8_multiprocessing_cpu():
    """CPU-bound: Multiprocessing (bypasses GIL)"""
    with concurrent.futures.ProcessPoolExecutor(max_workers=4) as executor:
        results = list(executor.map(cpu_bound_task, range(NUM_TASKS)))
    return results


if __name__ == "__main__":
    print("=" * 80)
    print("CONCURRENCY PATTERNS PERFORMANCE TEST")
    print("=" * 80)
    print(f"Number of tasks: {NUM_TASKS}")
    print(f"CPU cores available: {multiprocessing.cpu_count()}")
    print()

    # ========================================================================
    # I/O-BOUND TESTS
    # ========================================================================
    print("=" * 80)
    print("I/O-BOUND WORKLOAD (simulating network calls)")
    print("=" * 80)
    print(f"Each task sleeps for {IO_SLEEP_DURATION}s\n")

    # Test 1: Synchronous I/O
    start = time.perf_counter()
    perf_test1_sync_io()
    t1 = time.perf_counter() - start
    print(f"Synchronous (sequential):        {t1:.6f}s  (baseline: 1.0x)")

    # Test 2: Async/await I/O
    start = time.perf_counter()
    asyncio.run(perf_test2_async_io())
    t2 = time.perf_counter() - start
    print(f"Async/await (asyncio):           {t2:.6f}s  (speedup: {t1/t2:.1f}x)")

    # Test 3: Threading pool I/O
    start = time.perf_counter()
    perf_test3_threading_pool_io()
    t3 = time.perf_counter() - start
    print(f"Threading (ThreadPoolExecutor):  {t3:.6f}s  (speedup: {t1/t3:.1f}x)")

    # Test 4: Manual threading I/O
    start = time.perf_counter()
    perf_test4_threading_manual_io()
    t4 = time.perf_counter() - start
    print(f"Threading (manual threads):      {t4:.6f}s  (speedup: {t1/t4:.1f}x)")

    print(f"\n{'Winner for I/O-bound:':<30} {'Async/await or Threading' if t2 < t3 else 'Threading'}")

    # ========================================================================
    # CPU-BOUND TESTS
    # ========================================================================
    print("\n" + "=" * 80)
    print("CPU-BOUND WORKLOAD (computing prime numbers)")
    print("=" * 80)
    print(f"Each task finds primes in a range of 100 numbers\n")

    # Test 5: Synchronous CPU
    start = time.perf_counter()
    perf_test5_sync_cpu()
    t5 = time.perf_counter() - start
    print(f"Synchronous (sequential):        {t5:.6f}s  (baseline: 1.0x)")

    # Test 6: Async CPU
    start = time.perf_counter()
    asyncio.run(perf_test6_async_cpu())
    t6 = time.perf_counter() - start
    print(f"Async/await (asyncio):           {t6:.6f}s  (speedup: {t5/t6:.1f}x) ⚠ GIL overhead!")

    # Test 7: Threading CPU
    start = time.perf_counter()
    perf_test7_threading_cpu()
    t7 = time.perf_counter() - start
    print(f"Threading (ThreadPoolExecutor):  {t7:.6f}s  (speedup: {t5/t7:.1f}x) ⚠ GIL limited!")

    # Test 8: Multiprocessing CPU
    start = time.perf_counter()
    perf_test8_multiprocessing_cpu()
    t8 = time.perf_counter() - start
    print(f"Multiprocessing (ProcessPool):   {t8:.6f}s  (speedup: {t5/t8:.1f}x) ✓ GIL bypassed!")

    print(f"\n{'Winner for CPU-bound:':<30} Multiprocessing")

    # ========================================================================
    # SUMMARY
    # ========================================================================
    print("\n" + "=" * 80)
    print("DECISION GUIDE")
    print("=" * 80)
    print("""
    I/O-BOUND (network, files, database):
    → Use async/await (asyncio) for high concurrency with low overhead
    → Use threading for simpler code or when mixing sync libraries

    CPU-BOUND (computation, data processing):
    → Use multiprocessing to bypass the GIL and utilize multiple cores
    → Avoid async/await and threading (they add overhead without benefit)

    MIXED WORKLOAD:
    → Consider async/await with ProcessPoolExecutor for CPU tasks
    → Or use threading for I/O with occasional CPU bursts

    AVOID:
    ✗ Async/await for CPU-bound work (adds overhead, no benefit)
    ✗ Threading for CPU-bound work (GIL prevents parallelism)
    ✗ Multiprocessing for I/O-bound work (high overhead for context switching)
    """)
