"""
What is the most efficient way to iterate over Pandas Dataframe?

Simple performance test of different approaches to work with Pandas Dataframe:
Performance results:

Number of iterations = 100, shape of dataframe  = (22544, 43)
2 columns interaction

Approach                         Total time    Per iteration
---------------------------------------------------------------
iterrows                         31.231000        0.31231
loc                              21.503000        0.21503
iloc                             14.528000        0.14528
itertuples                        4.045000        0.04045
list comprehension                0.236000        0.00236
pandas vectorisation             0.0000065        < 1e-7
numpy vectorisation              0.0000041        < 1e-7

2 col

31.79612575000101
21.784195291998913
14.85691958300049
4.17062041600002
0.24832708299982187
6.50000038149301e-06
4.042000000481494e-06

3 col

33.79612491700027
31.460863166999843
22.181582417000755
4.065327083000739
0.3585552079985064
4.249999619787559e-06
3.791999915847555e-06

4 col

35.80715099999907
42.19561391700154
29.120010167000146
4.144790874999671
0.46619262500098557
4.625000656233169e-06
3.99999953515362e-06

5 col

38.48405604199979
54.20556766700065
36.800116624999646
4.189976833000401
0.5641330420003214
4.624998837243766e-06
3.95800088881515e-06

6 col

41.418219708000834
63.516673832999004
43.06240587499997
4.292982209000911
0.6617459160006547
4.207999154459685e-06
4.0409995563095436e-06

7 col

42.687693292000404
72.66226558400012
49.7964803750001
4.387231624999913
0.7679926250002609
4.1669991333037615e-06
3.99999953515362e-06

new_shape = (45088, 43)

85.18077179200009
150.55690233399946
103.21720600000117
8.506990459000008
1.5353438330002973
4.0409995563095436e-06
4.124998667975888e-06

new_shape = (90176, 43)

174.06111883300036
294.61878745800095
200.05156754199925
17.02616954199948
3.0628705830004037
4.749999789055437e-06
5.208999937167391e-06

new_shape = (180352, 43)

341.17142633299954
609.5398932499993
401.8817630409976
34.17261445799886
6.207891915997607
4.249999619787559e-06
4.125002305954695e-06

new_shape = (360704, 43)

693.7480411670113
1194.9333910830028
800.0959380830027
69.81418574998679
12.582483334001154
4.665998858399689e-06
4.0829909266904e-06

"""

import pandas as pd

DATAFRAME = pd.read_csv("data/nslkdd_test.txt")
print(DATAFRAME.shape)

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
    return
    (
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
    return
    (
        DATAFRAME["dst_bytes"].to_numpy()
        + DATAFRAME["src_bytes"].to_numpy()
        + DATAFRAME["count"].to_numpy()
        + DATAFRAME["srv_count"].to_numpy()
        + DATAFRAME["dst_host_count"].to_numpy()
        + DATAFRAME["dst_host_srv_count"].to_numpy()
        + DATAFRAME["other"].to_numpy()
    ).to_list()


if __name__ == "__main__":
    import timeit

    print(timeit.timeit(stmt="perf_test()", number=PERF_ITERATIONS, globals=globals()))
    print(timeit.timeit(stmt="perf_test2()", number=PERF_ITERATIONS, globals=globals()))
    print(timeit.timeit(stmt="perf_test3()", number=PERF_ITERATIONS, globals=globals()))
    print(timeit.timeit(stmt="perf_test4()", number=PERF_ITERATIONS, globals=globals()))
    print(timeit.timeit(stmt="perf_test5()", number=PERF_ITERATIONS, globals=globals()))
    print(timeit.timeit(stmt="perf_test6()", number=PERF_ITERATIONS, globals=globals()))
    print(timeit.timeit(stmt="perf_test7()", number=PERF_ITERATIONS, globals=globals()))
