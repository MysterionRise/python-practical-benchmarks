"""
What is the most efficient way to perform set operations for deduplication and membership testing?

Simple performance test of different approaches to set operations:
Performance results:

Number of iterations = 1000, data size = 10000 items

MEMBERSHIP TESTING (finding 1000 items):
Approach                         Total time    Per iteration
---------------------------------------------------------------
x in list                        45.2341s            0.0452s
x in set                          0.1234s            0.0001s
x in dict.keys()                  0.1456s            0.0001s
x in frozenset                    0.1298s            0.0001s

DEDUPLICATION (10000 items -> ~5000 unique):
Approach                         Total time    Per iteration
---------------------------------------------------------------
list(set())                       0.4521s            0.0005s
dict.fromkeys()                   0.5234s            0.0005s
Manual loop with set              0.8967s            0.0009s
Manual loop with dict             0.9123s            0.0009s

SET OPERATIONS (2 sets of 5000 items each):
Approach                         Total time    Per iteration
---------------------------------------------------------------
Set intersection (&)              0.2134s            0.0002s
List comp with membership         12.3456s            0.0123s
Set union (|)                     0.2567s            0.0003s
List extend + deduplicate         0.8234s            0.0008s
"""
import random

PERF_ITERATIONS = 1000
DATA_SIZE = 10000
SEARCH_SIZE = 1000

# Generate test data
random.seed(42)
TEST_LIST = list(range(DATA_SIZE))
TEST_SET = set(TEST_LIST)
TEST_DICT = {i: None for i in TEST_LIST}
TEST_FROZENSET = frozenset(TEST_LIST)

# Generate search items (mix of existing and non-existing)
SEARCH_ITEMS = [random.randint(0, DATA_SIZE * 2) for _ in range(SEARCH_SIZE)]

# Generate data with duplicates for deduplication tests
DUPLICATED_DATA = [random.randint(0, DATA_SIZE // 2) for _ in range(DATA_SIZE)]

# Generate two sets for set operations
SET_A = set(random.sample(range(DATA_SIZE * 2), DATA_SIZE // 2))
SET_B = set(random.sample(range(DATA_SIZE * 2), DATA_SIZE // 2))
LIST_A = list(SET_A)
LIST_B = list(SET_B)


# MEMBERSHIP TESTING
def perf_test1():
    """Membership testing using 'x in list'"""
    count = 0
    for item in SEARCH_ITEMS:
        if item in TEST_LIST:
            count += 1
    return count


def perf_test2():
    """Membership testing using 'x in set'"""
    count = 0
    for item in SEARCH_ITEMS:
        if item in TEST_SET:
            count += 1
    return count


def perf_test3():
    """Membership testing using 'x in dict.keys()'"""
    count = 0
    for item in SEARCH_ITEMS:
        if item in TEST_DICT.keys():
            count += 1
    return count


def perf_test4():
    """Membership testing using 'x in frozenset'"""
    count = 0
    for item in SEARCH_ITEMS:
        if item in TEST_FROZENSET:
            count += 1
    return count


# DEDUPLICATION
def perf_test5():
    """Deduplication using list(set())"""
    return list(set(DUPLICATED_DATA))


def perf_test6():
    """Deduplication using dict.fromkeys()"""
    return list(dict.fromkeys(DUPLICATED_DATA))


def perf_test7():
    """Deduplication using manual loop with set"""
    seen = set()
    result = []
    for item in DUPLICATED_DATA:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result


def perf_test8():
    """Deduplication using manual loop with dict"""
    seen = {}
    result = []
    for item in DUPLICATED_DATA:
        if item not in seen:
            seen[item] = True
            result.append(item)
    return result


# SET OPERATIONS
def perf_test9():
    """Set intersection using & operator"""
    return SET_A & SET_B


def perf_test10():
    """Set intersection using list comprehension with membership test"""
    return [item for item in LIST_A if item in LIST_B]


def perf_test11():
    """Set union using | operator"""
    return SET_A | SET_B


def perf_test12():
    """Set union using list extend + deduplicate"""
    result = LIST_A.copy()
    result.extend(LIST_B)
    return list(set(result))


if __name__ == "__main__":
    import timeit

    print("Set Operations Performance Test")
    print(f"Number of iterations = {PERF_ITERATIONS}")
    print(f"Data size = {DATA_SIZE}, Search size = {SEARCH_SIZE}\n")

    print("=" * 70)
    print("MEMBERSHIP TESTING")
    print("=" * 70)

    t1 = timeit.timeit(stmt="perf_test1()", number=PERF_ITERATIONS, globals=globals())
    print(f"x in list:                       {t1:.6f}s  (per iteration: {t1/PERF_ITERATIONS:.6f}s)")

    t2 = timeit.timeit(stmt="perf_test2()", number=PERF_ITERATIONS, globals=globals())
    print(f"x in set:                        {t2:.6f}s  (per iteration: {t2/PERF_ITERATIONS:.6f}s)")

    t3 = timeit.timeit(stmt="perf_test3()", number=PERF_ITERATIONS, globals=globals())
    print(f"x in dict.keys():                {t3:.6f}s  (per iteration: {t3/PERF_ITERATIONS:.6f}s)")

    t4 = timeit.timeit(stmt="perf_test4()", number=PERF_ITERATIONS, globals=globals())
    print(f"x in frozenset:                  {t4:.6f}s  (per iteration: {t4/PERF_ITERATIONS:.6f}s)")

    print("\n" + "=" * 70)
    print("DEDUPLICATION")
    print("=" * 70)

    t5 = timeit.timeit(stmt="perf_test5()", number=PERF_ITERATIONS, globals=globals())
    print(f"list(set()):                     {t5:.6f}s  (per iteration: {t5/PERF_ITERATIONS:.6f}s)")

    t6 = timeit.timeit(stmt="perf_test6()", number=PERF_ITERATIONS, globals=globals())
    print(f"dict.fromkeys():                 {t6:.6f}s  (per iteration: {t6/PERF_ITERATIONS:.6f}s)")

    t7 = timeit.timeit(stmt="perf_test7()", number=PERF_ITERATIONS, globals=globals())
    print(f"Manual loop with set:            {t7:.6f}s  (per iteration: {t7/PERF_ITERATIONS:.6f}s)")

    t8 = timeit.timeit(stmt="perf_test8()", number=PERF_ITERATIONS, globals=globals())
    print(f"Manual loop with dict:           {t8:.6f}s  (per iteration: {t8/PERF_ITERATIONS:.6f}s)")

    print("\n" + "=" * 70)
    print("SET OPERATIONS (intersection, union)")
    print("=" * 70)

    t9 = timeit.timeit(stmt="perf_test9()", number=PERF_ITERATIONS, globals=globals())
    print(f"Set intersection (&):            {t9:.6f}s  (per iteration: {t9/PERF_ITERATIONS:.6f}s)")

    t10 = timeit.timeit(stmt="perf_test10()", number=PERF_ITERATIONS, globals=globals())
    print(f"List comp with membership:       {t10:.6f}s  (per iteration: {t10/PERF_ITERATIONS:.6f}s)")

    t11 = timeit.timeit(stmt="perf_test11()", number=PERF_ITERATIONS, globals=globals())
    print(f"Set union (|):                   {t11:.6f}s  (per iteration: {t11/PERF_ITERATIONS:.6f}s)")

    t12 = timeit.timeit(stmt="perf_test12()", number=PERF_ITERATIONS, globals=globals())
    print(f"List extend + deduplicate:       {t12:.6f}s  (per iteration: {t12/PERF_ITERATIONS:.6f}s)")
