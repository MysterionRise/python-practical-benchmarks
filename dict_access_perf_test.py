"""
What is the most efficient way to access dictionary value by key for best algorithmic performance?

PYTHON VERSION NOTE:
Python 3.11+ specializes subscript bytecode by container type (the specializing
adaptive interpreter, PEP 659), which makes dict[key] faster on 3.11+. It is not a
per-key cache. Only existing keys are looked up here, so the default-value paths of
.get(), .setdefault() and defaultdict are not exercised.

Simple perf test with random strings as values and int as keys

Performance results:

Random key order, size of dictionary = 1000, existing keys only, CPython 3.13.17 on Linux x86-64
(30 interleaved rounds with rotating case order, median per call)

Approach                              Per call
------------------------------------------------
- dict[key]                            57.0 us
- dict.get(key)                        59.4 us
- dict.setdefault(key, default)        62.3 us
- using defaultdict                    57.8 us

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


def access_order(method, n):
    """Return the key order to access: 'seq_keys' (0..n-1) or 'rand_keys' (seeded shuffle)."""
    keys = list(range(n))
    if method == "rand_keys":
        random.Random(0).shuffle(keys)
    elif method != "seq_keys":
        raise ValueError("Unsupported method")
    return keys


def reset_benchmark_data():
    """Clear cached dictionaries after runner quick-mode overrides."""
    _DATA_CACHE.clear()


def get_test_data():
    """Return (dict, defaultdict, key order) built once per configuration, outside the timed loops."""
    cache_key = (DICTIONARY_SIZE, TYPE)
    if cache_key not in _DATA_CACHE:
        data = {i: random_value(str, seed=i) for i in range(DICTIONARY_SIZE)}
        default_data = defaultdict(lambda: "")
        default_data.update(data)
        _DATA_CACHE[cache_key] = (data, default_data, access_order(TYPE, DICTIONARY_SIZE))
    return _DATA_CACHE[cache_key]


def perf_test1_dict_key():
    """Access values with dict[key]."""
    data, _, keys = get_test_data()
    total = 0
    for key in keys:
        value = data[key]
        total += len(value)
    return total


def perf_test2_dict_get():
    """Access values with dict.get(key)."""
    data, _, keys = get_test_data()
    total = 0
    for key in keys:
        value = data.get(key)
        total += len(value)
    return total


def perf_test3_dict_setdefault():
    """Access values with dict.setdefault(key, default)."""
    data, _, keys = get_test_data()
    total = 0
    for key in keys:
        value = data.setdefault(key, "")
        total += len(value)
    return total


def perf_test4_defaultdict():
    """Access values with defaultdict."""
    _, default_data, keys = get_test_data()
    total = 0
    for key in keys:
        value = default_data[key]
        total += len(value)
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
