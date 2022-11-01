"""
What is the most efficient way to iterate over Pandas Dataframe?

Simple performance test of different approaches to work with Pandas Dataframe:
Performance results:

Number of iterations = 100, shape of dataframe  = (22000, 43)

Approach                         Total time    Per iteration
---------------------------------------------------------------
iterrows                         31.231        0.31231
loc                              21.503        0.21503
iloc                             14.528        0.14528
itertuples                        4.045        0.04045
list comprehension                0.236        0.00236


"""
import pandas as pd

DATAFRAME = pd.read_csv("data/nslkdd_test.txt")

PERF_ITERATIONS = 100


def perf_test():
    """Iterate over dataframe with iterrows function"""
    total = []
    for _, row in DATAFRAME.iterrows():
        total.append(row["dst_bytes"] + row["src_bytes"])
    return total


def perf_test2():
    """Iterate over dataframe with loc function"""
    total = []
    for i in range(len(DATAFRAME)):
        total.append(DATAFRAME["dst_bytes"].loc[i] + DATAFRAME["src_bytes"].loc[i])
    return total


def perf_test3():
    """Iterate over dataframe with iloc function"""
    total = []
    for i in range(len(DATAFRAME)):
        total.append(DATAFRAME["dst_bytes"].iloc[i] + DATAFRAME["src_bytes"].iloc[i])
    return total


def perf_test4():
    """Iterate over dataframe with itertuples function"""
    total = []
    for row in DATAFRAME.itertuples():
        total.append(row.dst_bytes + row.src_bytes)
    return total


def perf_test5():
    """
    Iterate over dataframe with list comprehension

    WOULD ONLY PERFORM WELL IF LIMITED COLUMNS REQUIRED FOR EXTRACTION
    """
    return [
        dst + src for dst, src in zip(DATAFRAME["dst_bytes"], DATAFRAME["src_bytes"])
    ]


if __name__ == "__main__":
    import timeit

    print(timeit.timeit(stmt="perf_test()", number=PERF_ITERATIONS, globals=globals()))
    print(timeit.timeit(stmt="perf_test2()", number=PERF_ITERATIONS, globals=globals()))
    print(timeit.timeit(stmt="perf_test3()", number=PERF_ITERATIONS, globals=globals()))
    print(timeit.timeit(stmt="perf_test4()", number=PERF_ITERATIONS, globals=globals()))
    print(timeit.timeit(stmt="perf_test5()", number=PERF_ITERATIONS, globals=globals()))
