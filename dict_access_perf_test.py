"""
What is the most efficient way to access dictionary value by key for best algorithmic performance?

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
import timeit
from collections import defaultdict

PERF_ITERATIONS = 1000
DICTIONARY_SIZE = 1000
TYPE = "rand_keys"


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


def dict_iteration(method, n=DICTIONARY_SIZE):
    """
    Iterate over a range of integer keys of size n

    Parameters:
    - method: str, one of 'seq_keys', 'rand_keys'
    - n: size of integers

    Yields:
    - key: key of the next item in the dictionary
    """

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


# create a dictionary with random keys and values
d = {i: random_value(str, seed=i) for i in range(DICTIONARY_SIZE)}


# method 1: using dict[key]
def method1():
    llist = []
    for key in dict_iteration(TYPE):
        x = d[key]
        v = random.random() * x
        llist.append(v)


# method 2: using dict.get(key)
def method2():
    llist = []
    for key in dict_iteration(TYPE):
        x = d.get(key)
        v = random.random() * x
        llist.append(v)


# method 3: using dict.setdefault(key, default)
def method3():
    llist = []
    for key in dict_iteration(TYPE):
        x = d.setdefault(key, 0)
        v = random.random() * x
        llist.append(v)


# method 4: using defaultdict
dd = defaultdict(lambda: 0)
dd.update(d)


def method4():
    llist = []
    for key in dict_iteration(TYPE):
        x = dd[key]
        v = random.random() * x
        llist.append(v)


# measure the time taken by each method
t1 = timeit.timeit(method1, number=PERF_ITERATIONS)
t2 = timeit.timeit(method2, number=PERF_ITERATIONS)
t3 = timeit.timeit(method3, number=PERF_ITERATIONS)
t4 = timeit.timeit(method4, number=PERF_ITERATIONS)

# print the results
print(f"Using dict[key]: {t1:.6f} seconds and per iteration {t1 / PERF_ITERATIONS:.6f}")
print(f"Using dict.get(key): {t2:.6f} seconds and per iteration {t2 / PERF_ITERATIONS:.6f}")
print(f"Using dict.setdefault(key, default): {t3:.6f} seconds and per iteration {t3 / PERF_ITERATIONS:.6f}")
print(f"Using defaultdict: {t4:.6f} seconds and per iteration {t4 / PERF_ITERATIONS:.6f}")
