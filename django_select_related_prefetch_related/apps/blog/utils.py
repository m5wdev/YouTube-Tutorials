from django.db import connection, reset_queries

import time
import functools


def query_debugger(func):
    @functools.wraps(func)
    def inner_func(*args, **kwargs):
        reset_queries()
        start_queries = len(connection.queries)

        start = time.perf_counter()
        # res   = func(*args, **kwargs)
        func(*args, **kwargs)
        end   = time.perf_counter()

        end_queries = len(connection.queries)

        print(f"View (function name): {func.__name__}")
        print(f"Queries quantity: {end_queries - start_queries}")
        print(f"Execution time: {(end - start):.2f}s")
        # res
        # return res

    return inner_func
