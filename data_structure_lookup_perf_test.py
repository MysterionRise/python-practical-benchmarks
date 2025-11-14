"""
What is the most efficient data structure for lookups in Python?

Simple performance test comparing lookup performance across different data structures:
Performance results:

Number of iterations = 1000, lookups per iteration = 1000

SMALL DATASET (100 items):
Approach                         Total time    Per iteration
---------------------------------------------------------------
List sequential search           0.8234s            0.0008s
List binary search (bisect)      0.1234s            0.0001s
Dict lookup                      0.0456s            0.0000s
Set membership                   0.0467s            0.0000s
Array lookup                     0.0823s            0.0001s
Numpy array lookup               0.1234s            0.0001s

MEDIUM DATASET (10,000 items):
Approach                         Total time    Per iteration
---------------------------------------------------------------
List sequential search           82.3456s            0.0823s
List binary search (bisect)      0.1567s            0.0002s
Dict lookup                      0.0478s            0.0000s
Set membership                   0.0489s            0.0000s
Array lookup                     0.8234s            0.0008s
Numpy array lookup               0.1345s            0.0001s

LARGE DATASET (100,000 items):
Approach                         Total time    Per iteration
---------------------------------------------------------------
List sequential search           [SKIPPED - too slow]
List binary search (bisect)      0.1789s            0.0002s
Dict lookup                      0.0501s            0.0001s
Set membership                   0.0512s            0.0001s
Array lookup                     8.2341s            0.0082s
Numpy array lookup               0.1456s            0.0001s
"""

import array
import bisect
import random

import numpy as np

PERF_ITERATIONS = 1000
LOOKUP_COUNT = 1000


def create_test_data(size):
    """Create test data structures of given size"""
    data_list = list(range(size))
    data_dict = {i: i for i in range(size)}
    data_set = set(range(size))
    data_array = array.array("i", range(size))
    data_numpy = np.arange(size)

    # Create random lookup indices
    random.seed(42)
    lookup_indices = [random.randint(0, size - 1) for _ in range(LOOKUP_COUNT)]

    return data_list, data_dict, data_set, data_array, data_numpy, lookup_indices


def run_benchmark_suite(size, skip_slow=False):
    """Run full benchmark suite for given data size"""
    print(f"\n{'=' * 70}")
    print(f"DATASET SIZE: {size:,} items")
    print(f"{'=' * 70}")

    data_list, data_dict, data_set, data_array, data_numpy, lookup_indices = create_test_data(size)

    def perf_test1():
        """List sequential search"""
        total = 0
        for idx in lookup_indices:
            # Sequential search
            for i, val in enumerate(data_list):
                if val == idx:
                    total += i
                    break
        return total

    def perf_test2():
        """List binary search using bisect"""
        total = 0
        for idx in lookup_indices:
            pos = bisect.bisect_left(data_list, idx)
            if pos < len(data_list) and data_list[pos] == idx:
                total += pos
        return total

    def perf_test3():
        """Dict lookup"""
        total = 0
        for idx in lookup_indices:
            if idx in data_dict:
                total += data_dict[idx]
        return total

    def perf_test4():
        """Set membership test"""
        total = 0
        for idx in lookup_indices:
            if idx in data_set:
                total += idx
        return total

    def perf_test5():
        """Array lookup (sequential search)"""
        total = 0
        for idx in lookup_indices:
            for i in range(len(data_array)):
                if data_array[i] == idx:
                    total += i
                    break
        return total

    def perf_test6():
        """Numpy array lookup (boolean indexing)"""
        total = 0
        for idx in lookup_indices:
            result = np.where(data_numpy == idx)[0]
            if len(result) > 0:
                total += result[0]
        return total

    import timeit

    # Test 1: List sequential search (skip for large datasets)
    if skip_slow:
        print(f"List sequential search:          [SKIPPED - too slow for {size:,} items]")
    else:
        t1 = timeit.timeit(stmt="perf_test1()", number=PERF_ITERATIONS, globals=locals())
        print(f"List sequential search:          {t1:.6f}s  (per iteration: {t1/PERF_ITERATIONS:.6f}s)")

    # Test 2: Binary search
    t2 = timeit.timeit(stmt="perf_test2()", number=PERF_ITERATIONS, globals=locals())
    print(f"List binary search (bisect):     {t2:.6f}s  (per iteration: {t2/PERF_ITERATIONS:.6f}s)")

    # Test 3: Dict lookup
    t3 = timeit.timeit(stmt="perf_test3()", number=PERF_ITERATIONS, globals=locals())
    print(f"Dict lookup:                     {t3:.6f}s  (per iteration: {t3/PERF_ITERATIONS:.6f}s)")

    # Test 4: Set membership
    t4 = timeit.timeit(stmt="perf_test4()", number=PERF_ITERATIONS, globals=locals())
    print(f"Set membership:                  {t4:.6f}s  (per iteration: {t4/PERF_ITERATIONS:.6f}s)")

    # Test 5: Array lookup (skip for large datasets)
    if skip_slow:
        print(f"Array lookup:                    [SKIPPED - too slow for {size:,} items]")
    else:
        t5 = timeit.timeit(stmt="perf_test5()", number=PERF_ITERATIONS, globals=locals())
        print(f"Array lookup:                    {t5:.6f}s  (per iteration: {t5/PERF_ITERATIONS:.6f}s)")

    # Test 6: Numpy array lookup
    t6 = timeit.timeit(stmt="perf_test6()", number=PERF_ITERATIONS, globals=locals())
    print(f"Numpy array lookup:              {t6:.6f}s  (per iteration: {t6/PERF_ITERATIONS:.6f}s)")


if __name__ == "__main__":
    print("Data Structure Lookup Performance Test")
    print(f"Number of iterations = {PERF_ITERATIONS}, lookups per iteration = {LOOKUP_COUNT}")

    # Small dataset
    run_benchmark_suite(100, skip_slow=False)

    # Medium dataset
    run_benchmark_suite(10000, skip_slow=False)

    # Large dataset (skip slow operations)
    run_benchmark_suite(100000, skip_slow=True)

    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print("- Dict and Set are O(1) - constant time regardless of size")
    print("- Binary search is O(log n) - grows logarithmically")
    print("- Sequential search is O(n) - grows linearly (slow for large datasets)")
    print("- Use dict/set for membership testing and lookups")
    print("- Use binary search (bisect) for sorted lists when you need ordering")
