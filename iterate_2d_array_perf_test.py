"""
What is the most efficient way to iterate over 2d array and maintain index for best algorithmic performance?

Simple performance test of different approaches to work with 2d array:
Performance results:

Size of 2d array = 1000 x 1000, CPython 3.13.17 on Linux x86-64, run_all_tests.py harness (median of 3 runs)

Approach                         Per iteration
-----------------------------------------------
- range() + indices                   0.094s
- iterate + .index()                  3.374s
- enumerate()                         0.101s
- 1d array approach                   0.149s
- numpy ndarray (NON-STDLIB)          0.530s

"""

import numpy as np

LIMIT = 500
ARRAY_SIZE = 1000
PERF_ITERATIONS = 100


def perf_test():
    """Accessing 2d array with range() functions"""
    current_board = [[0 for _ in range(ARRAY_SIZE)] for _ in range(ARRAY_SIZE)]
    length = len(current_board)
    for i in range(length):
        length2 = len(current_board[i])
        for j in range(length2):
            current_board[i][j] = i * j
            if current_board[i][j] > LIMIT:
                current_board[i][j] = 0
    return current_board


def perf_test2():
    """Accessing 2d array by iterating values and recovering indices with .index() (quadratic anti-pattern)

    Cells start with unique values so .index() finds the real position; with duplicate
    values it would silently return the first match instead.
    """
    current_board = [[i * ARRAY_SIZE + j for j in range(ARRAY_SIZE)] for i in range(ARRAY_SIZE)]
    for row in current_board:
        i = current_board.index(row)
        for cell in row:
            j = row.index(cell)
            current_board[i][j] = i * j
            if current_board[i][j] > LIMIT:
                current_board[i][j] = 0
    return current_board


def perf_test3():
    """Accessing 2d array with enumerate() function"""
    current_board = [[0 for _ in range(ARRAY_SIZE)] for _ in range(ARRAY_SIZE)]
    for idx, row in enumerate(current_board):
        for jdx, _val in enumerate(row):
            current_board[idx][jdx] = idx * jdx
            if current_board[idx][jdx] > LIMIT:
                current_board[idx][jdx] = 0
    return current_board


def perf_test4():
    """Mimicking 2d array with by using 1d array"""
    current_board = [0 for _ in range(ARRAY_SIZE * ARRAY_SIZE)]
    for i in range(ARRAY_SIZE):
        for j in range(ARRAY_SIZE):
            current_board[i * ARRAY_SIZE + j] = i * j
            if current_board[i * ARRAY_SIZE + j] > LIMIT:
                current_board[i * ARRAY_SIZE + j] = 0
    return current_board


def perf_test5():
    """Accessing 2d array with numpy ndarray"""
    current_board = np.zeros((ARRAY_SIZE, ARRAY_SIZE))
    for idx, row in enumerate(current_board):
        for jdx, _val in enumerate(row):
            current_board[idx][jdx] = idx * jdx
            if current_board[idx][jdx] > LIMIT:
                current_board[idx][jdx] = 0
    return current_board


if __name__ == "__main__":
    import timeit

    print(timeit.timeit(stmt="perf_test()", number=PERF_ITERATIONS, globals=globals()))
    print(timeit.timeit(stmt="perf_test2()", number=PERF_ITERATIONS, globals=globals()))
    print(timeit.timeit(stmt="perf_test3()", number=PERF_ITERATIONS, globals=globals()))
    print(timeit.timeit(stmt="perf_test4()", number=PERF_ITERATIONS, globals=globals()))
    print(timeit.timeit(stmt="perf_test5()", number=PERF_ITERATIONS, globals=globals()))
