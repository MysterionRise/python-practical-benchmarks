# Python Practical Benchmarks Report

> Machine-specific benchmark evidence. Use it to verify reproducibility, not as a universal ranking.

## Environment

| Field | Value |
| --- | --- |
| Timestamp UTC | 2026-07-07T10:27:58.900903+00:00 |
| Python | CPython 3.10.0 |
| Platform | macOS-15.7.4-arm64-arm-64bit |
| Machine | arm64 |
| CPU count | 10 |
| Git SHA | bfc4258 |
| Quick mode | True |
| Runs / warmups | 3 / 1 |

## Summary

| Metric | Count |
| --- | ---: |
| Benchmarks total | 22 |
| Benchmarks passed | 22 |
| Benchmarks failed | 0 |
| Benchmarks skipped | 0 |
| Cases total | 228 |
| Cases passed | 209 |
| Cases failed | 0 |
| Cases skipped | 19 |

## Benchmark Summary

| Benchmark | Category | Status | Cases passed | Cases skipped | Cases failed | Median range |
| --- | --- | --- | ---: | ---: | ---: | ---: |
| `iterate_2d_array_perf_test` | basic | passed | 5 | 0 | 0 | 781.5 us - 5.287 ms |
| `iterate_df_pandas_perf_test` | basic | passed | 7 | 0 | 0 | 583.0 ns - 665.460 ms |
| `dict_access_perf_test` | basic | passed | 4 | 0 | 0 | 61.5 us - 63.0 us |
| `string_concat_perf_test` | basic | passed | 7 | 0 | 0 | 8.2 us - 18.1 us |
| `list_operations_perf_test` | basic | passed | 7 | 0 | 0 | 2.8 us - 6.8 us |
| `file_io_perf_test` | basic | passed | 7 | 0 | 0 | 21.0 us - 28.8 us |
| `json_perf_test` | basic | passed | 3 | 4 | 0 | 11.8 us - 77.9 us |
| `set_operations_perf_test` | basic | passed | 12 | 0 | 0 | 37.3 us - 130.554 ms |
| `function_call_perf_test` | basic | passed | 9 | 0 | 0 | 8.0 us - 17.1 us |
| `data_structure_lookup_perf_test` | basic | passed | 6 | 0 | 0 | 3.7 us - 143.0 us |
| `concurrency_patterns_perf_test` | advanced | passed | 7 | 1 | 0 | 419.0 us - 15.080 ms |
| `regex_performance_perf_test` | advanced | passed | 13 | 0 | 0 | 235.7 us - 5.566 ms |
| `object_creation_patterns_perf_test` | advanced | passed | 12 | 4 | 0 | 203.8 us - 462.6 us |
| `deep_copy_strategies_perf_test` | advanced | passed | 19 | 0 | 0 | 1.8 us - 21.589 ms |
| `generator_vs_iterator_perf_test` | advanced | passed | 13 | 0 | 0 | 9.5 us - 1.288 ms |
| `attribute_access_perf_test` | expert | passed | 16 | 0 | 0 | 295.2 us - 2.056 ms |
| `exception_handling_perf_test` | expert | passed | 16 | 0 | 0 | 2.6 us - 123.5 us |
| `serialization_formats_perf_test` | expert | passed | 11 | 10 | 0 | 3.5 us - 1.207 ms |
| `context_manager_perf_test` | expert | passed | 13 | 0 | 0 | 2.5 us - 651.4 us |
| `import_strategies_perf_test` | expert | passed | 9 | 0 | 0 | 58.3 us - 12.897 ms |
| `free_threaded_perf_test` | expert | passed | 5 | 0 | 0 | 6.261 ms - 25.323 ms |
| `jit_numeric_perf_test` | expert | passed | 8 | 0 | 0 | 28.5 us - 4.344 ms |

## Explicit Skips

- `json_perf_test.perf_test3`: optional dependency not installed: ujson
- `json_perf_test.perf_test4`: optional dependency not installed: orjson
- `json_perf_test.perf_test6`: optional dependency not installed: ujson
- `json_perf_test.perf_test7`: optional dependency not installed: orjson
- `concurrency_patterns_perf_test.perf_test8_multiprocessing_cpu`: environment denied process creation: [Errno 1] Operation not permitted
- `object_creation_patterns_perf_test.perf_test6_create_attrs`: optional dependency not installed: attr
- `object_creation_patterns_perf_test.perf_test7_create_attrs_slotted`: optional dependency not installed: attr
- `object_creation_patterns_perf_test.perf_test14_access_attrs`: optional dependency not installed: attr
- `object_creation_patterns_perf_test.perf_test15_access_attrs_slotted`: optional dependency not installed: attr
- `serialization_formats_perf_test.perf_test5_orjson_serialize_small`: optional dependency not installed: orjson
- `serialization_formats_perf_test.perf_test6_orjson_deserialize_small`: optional dependency not installed: orjson
- `serialization_formats_perf_test.perf_test7_msgpack_serialize_small`: optional dependency not installed: msgpack
- `serialization_formats_perf_test.perf_test8_msgpack_deserialize_small`: optional dependency not installed: msgpack
- `serialization_formats_perf_test.perf_test13_orjson_serialize_nested`: optional dependency not installed: orjson
- `serialization_formats_perf_test.perf_test14_orjson_deserialize_nested`: optional dependency not installed: orjson
- `serialization_formats_perf_test.perf_test15_msgpack_serialize_nested`: optional dependency not installed: msgpack
- `serialization_formats_perf_test.perf_test16_msgpack_deserialize_nested`: optional dependency not installed: msgpack
- `serialization_formats_perf_test.perf_test18_orjson_serialize_numbers`: optional dependency not installed: orjson
- `serialization_formats_perf_test.perf_test19_msgpack_serialize_numbers`: optional dependency not installed: msgpack
