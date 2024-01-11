"""
What is the most efficient way to iterate over 2d array and maintain index for best algorithmic performance?

Simple performance test of different approaches to work with 2d array:
Performance results:

Number of iterations = 100, size of 2d array = 10000

Approach                         Total time    Per iteration
---------------------------------------------------------------
- range() + indices              11.2518s            0.1125s
- iterate + .index()            216.3334s            2.1633s
- enumerate()                     8.3070s            0.0830s
- 1d array approach              16.5849s            0.1658s
- numpy ndarray (NON-STDLIB)     28.0520s            0.2805s

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


def perf_test2():
    """Accessing 2d array with iterating over and getting needed index using
    .index() function"""
    current_board = [[0 for _ in range(ARRAY_SIZE)] for _ in range(ARRAY_SIZE)]
    for row in current_board:
        for cell in row:
            current_board[current_board.index(row)][row.index(cell)] = current_board.index(row) * row.index(cell)
            if current_board[current_board.index(row)][row.index(cell)] > LIMIT:
                current_board[current_board.index(row)][row.index(cell)] = 0


def perf_test3():
    """Accessing 2d array with enumerate() function"""
    current_board = [[0 for _ in range(ARRAY_SIZE)] for _ in range(ARRAY_SIZE)]
    for idx, row in enumerate(current_board):
        for jdx, val in enumerate(row):
            current_board[idx][jdx] = idx * jdx
            if val > LIMIT:
                current_board[idx][jdx] = 0


def perf_test4():
    """Mimicking 2d array with by using 1d array"""
    current_board = [0 for _ in range(ARRAY_SIZE * ARRAY_SIZE)]
    for i in range(ARRAY_SIZE):
        for j in range(ARRAY_SIZE):
            current_board[i * ARRAY_SIZE + j] = i * j
            if current_board[i * ARRAY_SIZE + j] > LIMIT:
                current_board[i * ARRAY_SIZE + j] = 0


def perf_test5():
    """Accessing 2d array with numpy ndarray"""
    current_board = np.zeros((ARRAY_SIZE, ARRAY_SIZE))
    for idx, row in enumerate(current_board):
        for jdx, val in enumerate(row):
            current_board[idx][jdx] = idx * jdx
            if val > LIMIT:
                current_board[idx][jdx] = 0


if __name__ == "__main__":
    import timeit

    print(timeit.timeit(stmt="perf_test()", number=PERF_ITERATIONS, globals=globals()))
    print(timeit.timeit(stmt="perf_test2()", number=PERF_ITERATIONS, globals=globals()))
    print(timeit.timeit(stmt="perf_test3()", number=PERF_ITERATIONS, globals=globals()))
    print(timeit.timeit(stmt="perf_test4()", number=PERF_ITERATIONS, globals=globals()))
    print(timeit.timeit(stmt="perf_test5()", number=PERF_ITERATIONS, globals=globals()))
