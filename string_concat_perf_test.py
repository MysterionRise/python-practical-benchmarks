"""
What is the most efficient way to concatenate strings in Python?

Simple performance test of different approaches to string concatenation:
Performance results:

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
"""

import io

PERF_ITERATIONS = 100
NUM_STRINGS = 10000


def perf_test1():
    """String concatenation using + operator in loop"""
    result = ""
    for i in range(NUM_STRINGS):
        result += f"Item {i}, "
    return result


def perf_test2():
    """String concatenation using str.join() with list"""
    items = []
    for i in range(NUM_STRINGS):
        items.append(f"Item {i}, ")
    return "".join(items)


def perf_test3():
    """String concatenation using f-strings in loop (inefficient pattern)"""
    result = ""
    for i in range(NUM_STRINGS):
        result = f"{result}Item {i}, "
    return result


def perf_test4():
    """String concatenation using str.format() in loop"""
    result = ""
    for i in range(NUM_STRINGS):
        result = "{}Item {}, ".format(result, i)
    return result


def perf_test5():
    """String concatenation using io.StringIO"""
    output = io.StringIO()
    for i in range(NUM_STRINGS):
        output.write(f"Item {i}, ")
    return output.getvalue()


def perf_test6():
    """String concatenation using list comprehension + join"""
    return "".join([f"Item {i}, " for i in range(NUM_STRINGS)])


def perf_test7():
    """String concatenation using ''.join(generator expression)"""
    return "".join(f"Item {i}, " for i in range(NUM_STRINGS))


if __name__ == "__main__":
    import timeit

    print("String Concatenation Performance Test")
    print(f"Number of iterations = {PERF_ITERATIONS}, number of strings = {NUM_STRINGS}\n")

    t1 = timeit.timeit(stmt="perf_test1()", number=PERF_ITERATIONS, globals=globals())
    print(f"+ operator in loop:              {t1:.6f}s  (per iteration: {t1/PERF_ITERATIONS:.6f}s)")

    t2 = timeit.timeit(stmt="perf_test2()", number=PERF_ITERATIONS, globals=globals())
    print(f"str.join() with list:            {t2:.6f}s  (per iteration: {t2/PERF_ITERATIONS:.6f}s)")

    t3 = timeit.timeit(stmt="perf_test3()", number=PERF_ITERATIONS, globals=globals())
    print(f"f-strings in loop:               {t3:.6f}s  (per iteration: {t3/PERF_ITERATIONS:.6f}s)")

    t4 = timeit.timeit(stmt="perf_test4()", number=PERF_ITERATIONS, globals=globals())
    print(f"str.format() in loop:            {t4:.6f}s  (per iteration: {t4/PERF_ITERATIONS:.6f}s)")

    t5 = timeit.timeit(stmt="perf_test5()", number=PERF_ITERATIONS, globals=globals())
    print(f"io.StringIO:                     {t5:.6f}s  (per iteration: {t5/PERF_ITERATIONS:.6f}s)")

    t6 = timeit.timeit(stmt="perf_test6()", number=PERF_ITERATIONS, globals=globals())
    print(f"List comprehension + join:       {t6:.6f}s  (per iteration: {t6/PERF_ITERATIONS:.6f}s)")

    t7 = timeit.timeit(stmt="perf_test7()", number=PERF_ITERATIONS, globals=globals())
    print(f"''.join(generator):              {t7:.6f}s  (per iteration: {t7/PERF_ITERATIONS:.6f}s)")
