# python-practical-benchmarks
Comparing practical options for routine tasks in Python

1. What is the optimal way to iterate 2d arrays (lists) in Python?

Could be useful - for algorithmic and sport programming competitions like
(https://codeforces.com, https://topcoder.com, ACM ICPC and many more)

```
Number of iterations = 100, size of 2d array = 10000

Approach                         Total time    Per iteration
---------------------------------------------------------------
- range() + indices              11.2518s            0.1125s
- iterate + .index()            216.3334s            2.1633s
- enumerate()                     8.3070s            0.0830s
- 1d array approach              16.5849s            0.1658s
- numpy ndarray (NON-STDLIB)     28.0520s            0.2805s
```

2. What is the optimal way to iterate over dataframes in Pandas?

Could be useful - for data scientists and data analytics using Pandas

```
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
```

Graph of performance with X-axis representing number of affecting columns (from 2 to 7)
Some methods are constants, some - not

<img src="performance.png">
