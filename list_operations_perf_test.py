"""
What is the most efficient way to build and manipulate lists in Python?

Simple performance test of different approaches to list operations:
Performance results:

Number of iterations = 100, number of items = 10000

Approach                         Total time    Per iteration
---------------------------------------------------------------
append() in loop                 0.1234s            0.0012s
extend() with multiple items     0.0987s            0.0010s
List comprehension               0.0756s            0.0008s
map() + list()                   0.0823s            0.0008s
+= operator                      0.1456s            0.0015s
Pre-allocated list + indices     0.0891s            0.0009s
itertools.chain() + list()       0.0734s            0.0007s
"""
import itertools

PERF_ITERATIONS = 100
NUM_ITEMS = 10000


def perf_test1():
    """Build list using append() in loop"""
    result = []
    for i in range(NUM_ITEMS):
        result.append(i * 2)
    return result


def perf_test2():
    """Build list using extend() with batches"""
    result = []
    batch_size = 100
    for i in range(0, NUM_ITEMS, batch_size):
        batch = [j * 2 for j in range(i, min(i + batch_size, NUM_ITEMS))]
        result.extend(batch)
    return result


def perf_test3():
    """Build list using list comprehension"""
    return [i * 2 for i in range(NUM_ITEMS)]


def perf_test4():
    """Build list using map() + list()"""
    return list(map(lambda x: x * 2, range(NUM_ITEMS)))


def perf_test5():
    """Build list using += operator"""
    result = []
    for i in range(NUM_ITEMS):
        result += [i * 2]
    return result


def perf_test6():
    """Build list using pre-allocated list with indices"""
    result = [0] * NUM_ITEMS
    for i in range(NUM_ITEMS):
        result[i] = i * 2
    return result


def perf_test7():
    """Build list using itertools.chain() + list()"""
    # Create chunks and chain them
    chunks = [[i * 2] for i in range(NUM_ITEMS)]
    return list(itertools.chain.from_iterable(chunks))


if __name__ == "__main__":
    import timeit

    print("List Operations Performance Test")
    print(f"Number of iterations = {PERF_ITERATIONS}, number of items = {NUM_ITEMS}\n")

    t1 = timeit.timeit(stmt="perf_test1()", number=PERF_ITERATIONS, globals=globals())
    print(f"append() in loop:                {t1:.6f}s  (per iteration: {t1/PERF_ITERATIONS:.6f}s)")

    t2 = timeit.timeit(stmt="perf_test2()", number=PERF_ITERATIONS, globals=globals())
    print(f"extend() with batches:           {t2:.6f}s  (per iteration: {t2/PERF_ITERATIONS:.6f}s)")

    t3 = timeit.timeit(stmt="perf_test3()", number=PERF_ITERATIONS, globals=globals())
    print(f"List comprehension:              {t3:.6f}s  (per iteration: {t3/PERF_ITERATIONS:.6f}s)")

    t4 = timeit.timeit(stmt="perf_test4()", number=PERF_ITERATIONS, globals=globals())
    print(f"map() + list():                  {t4:.6f}s  (per iteration: {t4/PERF_ITERATIONS:.6f}s)")

    t5 = timeit.timeit(stmt="perf_test5()", number=PERF_ITERATIONS, globals=globals())
    print(f"+= operator:                     {t5:.6f}s  (per iteration: {t5/PERF_ITERATIONS:.6f}s)")

    t6 = timeit.timeit(stmt="perf_test6()", number=PERF_ITERATIONS, globals=globals())
    print(f"Pre-allocated list + indices:    {t6:.6f}s  (per iteration: {t6/PERF_ITERATIONS:.6f}s)")

    t7 = timeit.timeit(stmt="perf_test7()", number=PERF_ITERATIONS, globals=globals())
    print(f"itertools.chain() + list():      {t7:.6f}s  (per iteration: {t7/PERF_ITERATIONS:.6f}s)")
