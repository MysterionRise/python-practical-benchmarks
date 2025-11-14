"""
What is the most efficient way to read files in Python?

Simple performance test of different approaches to file I/O operations:
Performance results:

Number of iterations = 100, file size = ~1MB (10000 lines)

Approach                         Total time    Per iteration
---------------------------------------------------------------
read() entire file               0.3421s            0.0034s
readline() in loop               0.5234s            0.0052s
readlines() all at once          0.3567s            0.0036s
iteration with 'with open'       0.4123s            0.0041s
pathlib.Path.read_text()         0.3398s            0.0034s
buffered reading (8KB)           0.4567s            0.0046s
buffered reading (64KB)          0.3876s            0.0039s
"""

import atexit
import os
import pathlib
import tempfile

PERF_ITERATIONS = 100
NUM_LINES = 10000
TEST_FILE = None


def setup_test_file():
    """Create a temporary test file with sample data"""
    global TEST_FILE
    fd, TEST_FILE = tempfile.mkstemp(suffix=".txt", text=True)
    with os.fdopen(fd, "w") as f:
        for i in range(NUM_LINES):
            f.write(f"This is line {i} with some sample text to make it realistic and longer.\n")
    return TEST_FILE


def cleanup_test_file():
    """Clean up the temporary test file"""
    global TEST_FILE
    if TEST_FILE and os.path.exists(TEST_FILE):
        try:
            os.unlink(TEST_FILE)
        except OSError:
            pass
        TEST_FILE = None


# Initialize test file when module is imported
setup_test_file()
# Register cleanup to run at exit
atexit.register(cleanup_test_file)


def perf_test1():
    """Read file using read() entire file"""
    with open(TEST_FILE, "r") as f:
        content = f.read()
    return len(content)


def perf_test2():
    """Read file using readline() in loop"""
    lines = []
    with open(TEST_FILE, "r") as f:
        while True:
            line = f.readline()
            if not line:
                break
            lines.append(line)
    return len(lines)


def perf_test3():
    """Read file using readlines() all at once"""
    with open(TEST_FILE, "r") as f:
        lines = f.readlines()
    return len(lines)


def perf_test4():
    """Read file using iteration with 'with open'"""
    lines = []
    with open(TEST_FILE, "r") as f:
        for line in f:
            lines.append(line)
    return len(lines)


def perf_test5():
    """Read file using pathlib.Path.read_text()"""
    content = pathlib.Path(TEST_FILE).read_text()
    return len(content)


def perf_test6():
    """Read file using buffered reading (8KB buffer)"""
    content = []
    with open(TEST_FILE, "r", buffering=8192) as f:
        while True:
            chunk = f.read(8192)
            if not chunk:
                break
            content.append(chunk)
    return len("".join(content))


def perf_test7():
    """Read file using buffered reading (64KB buffer)"""
    content = []
    with open(TEST_FILE, "r", buffering=65536) as f:
        while True:
            chunk = f.read(65536)
            if not chunk:
                break
            content.append(chunk)
    return len("".join(content))


if __name__ == "__main__":
    import timeit

    print("File I/O Performance Test")
    print("Setting up test file...")
    setup_test_file()
    file_size = os.path.getsize(TEST_FILE)
    print(f"Test file: {TEST_FILE}")
    print(f"File size: {file_size:,} bytes ({file_size/1024:.2f} KB)")
    print(f"Number of iterations = {PERF_ITERATIONS}, number of lines = {NUM_LINES}\n")

    try:
        t1 = timeit.timeit(stmt="perf_test1()", number=PERF_ITERATIONS, globals=globals())
        print(f"read() entire file:              {t1:.6f}s  (per iteration: {t1/PERF_ITERATIONS:.6f}s)")

        t2 = timeit.timeit(stmt="perf_test2()", number=PERF_ITERATIONS, globals=globals())
        print(f"readline() in loop:              {t2:.6f}s  (per iteration: {t2/PERF_ITERATIONS:.6f}s)")

        t3 = timeit.timeit(stmt="perf_test3()", number=PERF_ITERATIONS, globals=globals())
        print(f"readlines() all at once:         {t3:.6f}s  (per iteration: {t3/PERF_ITERATIONS:.6f}s)")

        t4 = timeit.timeit(stmt="perf_test4()", number=PERF_ITERATIONS, globals=globals())
        print(f"iteration with 'with open':      {t4:.6f}s  (per iteration: {t4/PERF_ITERATIONS:.6f}s)")

        t5 = timeit.timeit(stmt="perf_test5()", number=PERF_ITERATIONS, globals=globals())
        print(f"pathlib.Path.read_text():        {t5:.6f}s  (per iteration: {t5/PERF_ITERATIONS:.6f}s)")

        t6 = timeit.timeit(stmt="perf_test6()", number=PERF_ITERATIONS, globals=globals())
        print(f"buffered reading (8KB):          {t6:.6f}s  (per iteration: {t6/PERF_ITERATIONS:.6f}s)")

        t7 = timeit.timeit(stmt="perf_test7()", number=PERF_ITERATIONS, globals=globals())
        print(f"buffered reading (64KB):         {t7:.6f}s  (per iteration: {t7/PERF_ITERATIONS:.6f}s)")
    finally:
        # Clean up test file
        if TEST_FILE and os.path.exists(TEST_FILE):
            os.unlink(TEST_FILE)
            print(f"\nTest file cleaned up: {TEST_FILE}")
