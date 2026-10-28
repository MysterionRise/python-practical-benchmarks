"""
What is the most efficient way to iterate over Pandas Dataframe?

Simple performance test of different approaches to work with Pandas Dataframe:
Performance results:

Shape of dataframe = (22544, 43), 7 columns summed per row, CPython 3.13.17 on Linux x86-64, pandas 3.1,
run_all_tests.py harness (median of 3 runs)

Approach                         Per iteration
-----------------------------------------------
iterrows                              0.651s
loc                                   2.508s
iloc                                  2.149s
itertuples                            0.115s
list comprehension                    0.0103s
pandas vectorisation                  0.00081s
numpy vectorisation                   0.00045s

"""

from pathlib import Path

import pandas as pd

DATAFRAME = pd.read_csv(Path(__file__).parent / "data" / "nslkdd_test.txt")

PERF_ITERATIONS = 100


def perf_test():
    """Iterate over dataframe with iterrows function"""
    total = []
    for _, row in DATAFRAME.iterrows():
        total.append(
            row["dst_bytes"]
            + row["src_bytes"]
            + row["count"]
            + row["srv_count"]
            + row["dst_host_count"]
            + row["dst_host_srv_count"]
            + row["other"]
        )
    return total


def perf_test2():
    """Iterate over dataframe with loc function"""
    total = []
    for i in range(len(DATAFRAME)):
        total.append(
            DATAFRAME["dst_bytes"].loc[i]
            + DATAFRAME["src_bytes"].loc[i]
            + DATAFRAME["count"].loc[i]
            + DATAFRAME["srv_count"].loc[i]
            + DATAFRAME["dst_host_count"].loc[i]
            + DATAFRAME["dst_host_srv_count"].loc[i]
            + DATAFRAME["other"].loc[i]
        )
    return total


def perf_test3():
    """Iterate over dataframe with iloc function"""
    total = []
    for i in range(len(DATAFRAME)):
        total.append(
            DATAFRAME["dst_bytes"].iloc[i]
            + DATAFRAME["src_bytes"].iloc[i]
            + DATAFRAME["count"].iloc[i]
            + DATAFRAME["srv_count"].iloc[i]
            + DATAFRAME["dst_host_count"].iloc[i]
            + DATAFRAME["dst_host_srv_count"].iloc[i]
            + DATAFRAME["other"].iloc[i]
        )
    return total


def perf_test4():
    """Iterate over dataframe with itertuples function"""
    total = []
    for row in DATAFRAME.itertuples():
        total.append(
            row.dst_bytes
            + row.src_bytes
            + row.count
            + row.srv_count
            + row.dst_host_count
            + row.dst_host_srv_count
            + row.other
        )
    return total


def perf_test5():
    """
    Iterate over dataframe with list comprehension

    WOULD ONLY PERFORM WELL IF LIMITED COLUMNS REQUIRED FOR EXTRACTION
    """
    return [
        dst + src + cnt + srv_cnt + dst_host_count + dst_host_srv_count + other
        for dst, src, cnt, srv_cnt, dst_host_count, dst_host_srv_count, other in zip(
            DATAFRAME["dst_bytes"],
            DATAFRAME["src_bytes"],
            DATAFRAME["count"],
            DATAFRAME["srv_count"],
            DATAFRAME["dst_host_count"],
            DATAFRAME["dst_host_srv_count"],
            DATAFRAME["other"],
        )
    ]


def perf_test6():
    """
    Pandas vectorisation
    """
    return (
        DATAFRAME["dst_bytes"]
        + DATAFRAME["src_bytes"]
        + DATAFRAME["count"]
        + DATAFRAME["srv_count"]
        + DATAFRAME["dst_host_count"]
        + DATAFRAME["dst_host_srv_count"]
        + DATAFRAME["other"]
    ).to_list()


def perf_test7():
    """
    Numpy vectorisation
    """
    return (
        DATAFRAME["dst_bytes"].to_numpy()
        + DATAFRAME["src_bytes"].to_numpy()
        + DATAFRAME["count"].to_numpy()
        + DATAFRAME["srv_count"].to_numpy()
        + DATAFRAME["dst_host_count"].to_numpy()
        + DATAFRAME["dst_host_srv_count"].to_numpy()
        + DATAFRAME["other"].to_numpy()
    ).tolist()


if __name__ == "__main__":
    import timeit

    print(timeit.timeit(stmt="perf_test()", number=PERF_ITERATIONS, globals=globals()))
    print(timeit.timeit(stmt="perf_test2()", number=PERF_ITERATIONS, globals=globals()))
    print(timeit.timeit(stmt="perf_test3()", number=PERF_ITERATIONS, globals=globals()))
    print(timeit.timeit(stmt="perf_test4()", number=PERF_ITERATIONS, globals=globals()))
    print(timeit.timeit(stmt="perf_test5()", number=PERF_ITERATIONS, globals=globals()))
    print(timeit.timeit(stmt="perf_test6()", number=PERF_ITERATIONS, globals=globals()))
    print(timeit.timeit(stmt="perf_test7()", number=PERF_ITERATIONS, globals=globals()))
