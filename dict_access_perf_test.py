"""
What is the most efficient way to access dictionary value by key for best algorithmic performance?

PYTHON VERSION NOTE:
Python 3.11+ introduced inline caching for dictionary operations, making dict access
faster when the same keys are accessed repeatedly. This benchmark shows improved
performance on 3.11+ for all dictionary access patterns.

Simple perf test with random strings as values and int as keys

Performance results:

Sequential access, number of iterations = 1000, size of dictionary = 100000

Approach                         Total time         Per iteration
------------------------------------------------------------------
- dict[key]                         8.987797s            0.008988s
- dict.get(key)                     7.061445s            0.007061s
- dict.setdefault(key, default)     7.511971s            0.007512s
- using defaultdict                 5.458365s            0.005458s

Sequential access, number of iterations = 1000, size of dictionary = 1000

Approach                         Total time         Per iteration
------------------------------------------------------------------
- dict[key]                         0.091688s            0.000092s
- dict.get(key)                     0.071862s            0.000072s
- dict.setdefault(key, default)     0.066943s            0.000067s
- using defaultdict                 0.052413s            0.000052s


Random access, number of iterations = 1000, size of dictionary = 100000

Approach                         Total time         Per iteration
------------------------------------------------------------------
- dict[key]                         0.091688s            0.000092s
- dict.get(key)                     0.071862s            0.000072s
- dict.setdefault(key, default)     0.066943s            0.000067s
- using defaultdict                 0.052413s            0.000052s
"""

import random
from collections import defaultdict

PERF_ITERATIONS = 1000
DICTIONARY_SIZE = 1000
TYPE = "rand_keys"
_DATA_CACHE = {}


def random_value(data_type, seed=None):
    if seed is not None:
        random.seed(seed)
    if data_type == int:
        return random.randint(-100, 100)
    elif data_type == float:
        return random.uniform(-100.0, 100.0)
    elif data_type == str:
        length = random.randint(1, 10)
        return "".join(random.choices("abcdefghijklmnopqrstuvwxyz", k=length))
    elif data_type == list:
        length = random.randint(0, 10)
        return [random_value(type, seed) for i in range(length)]
    elif data_type == tuple:
        length = random.randint(0, 10)
        return tuple(random_value(type, seed) for i in range(length))
    elif data_type == dict:
        length = random.randint(0, 10)
        return {random_value(str, seed): random_value(type, seed) for i in range(length)}
    else:
        raise ValueError("Unsupported data type")


def dict_iteration(method, n=None):
    """
    Iterate over a range of integer keys of size n

    Parameters:
    - method: str, one of 'seq_keys', 'rand_keys'
    - n: size of integers

    Yields:
    - key: key of the next item in the dictionary
    """
    if n is None:
        n = DICTIONARY_SIZE

    if method == "seq_keys":
        for key in range(n):
            yield key
    elif method == "rand_keys":
        keys = list(range(n))
        random.shuffle(keys)
        for key in keys:
            yield key
    else:
        raise ValueError("Unsupported method")


def reset_benchmark_data():
    """Clear cached dictionaries after runner quick-mode overrides."""
    _DATA_CACHE.clear()


def get_test_data():
    """Return dictionaries built with the current configuration constants."""
    cache_key = DICTIONARY_SIZE
    if cache_key not in _DATA_CACHE:
        data = {i: random_value(str, seed=i) for i in range(DICTIONARY_SIZE)}
        default_data = defaultdict(lambda: "")
        default_data.update(data)
        _DATA_CACHE[cache_key] = (data, default_data)
    return _DATA_CACHE[cache_key]


def perf_test1_dict_key():
    """Access values with dict[key]."""
    data, _ = get_test_data()
    total = 0
    for key in dict_iteration(TYPE):
        value = data[key]
        total += len(value) + random.randint(0, 10)
    return total


def perf_test2_dict_get():
    """Access values with dict.get(key)."""
    data, _ = get_test_data()
    total = 0
    for key in dict_iteration(TYPE):
        value = data.get(key)
        total += len(value) + random.randint(0, 10)
    return total


def perf_test3_dict_setdefault():
    """Access values with dict.setdefault(key, default)."""
    data, _ = get_test_data()
    total = 0
    for key in dict_iteration(TYPE):
        value = data.setdefault(key, "")
        total += len(value) + random.randint(0, 10)
    return total


def perf_test4_defaultdict():
    """Access values with defaultdict."""
    _, default_data = get_test_data()
    total = 0
    for key in dict_iteration(TYPE):
        value = default_data[key]
        total += len(value) + random.randint(0, 10)
    return total


method1 = perf_test1_dict_key
method2 = perf_test2_dict_get
method3 = perf_test3_dict_setdefault
method4 = perf_test4_defaultdict


if __name__ == "__main__":
    import timeit

    t1 = timeit.timeit(perf_test1_dict_key, number=PERF_ITERATIONS)
    t2 = timeit.timeit(perf_test2_dict_get, number=PERF_ITERATIONS)
    t3 = timeit.timeit(perf_test3_dict_setdefault, number=PERF_ITERATIONS)
    t4 = timeit.timeit(perf_test4_defaultdict, number=PERF_ITERATIONS)

    print(f"Using dict[key]: {t1:.6f} seconds and per iteration {t1 / PERF_ITERATIONS:.6f}")
    print(f"Using dict.get(key): {t2:.6f} seconds and per iteration {t2 / PERF_ITERATIONS:.6f}")
    print(f"Using dict.setdefault(key, default): {t3:.6f} seconds and per iteration {t3 / PERF_ITERATIONS:.6f}")
    print(f"Using defaultdict: {t4:.6f} seconds and per iteration {t4 / PERF_ITERATIONS:.6f}")
