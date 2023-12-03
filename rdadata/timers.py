"""
TIMER DECORATORS
"""

import time
from functools import wraps
from typing import Any, Callable


def time_function(func) -> Callable[..., Any]:
    """A decorator to report execution run time for freestanding functions"""

    @wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        tic: float = time.perf_counter()

        result: Any = func(*args, **kwargs)

        toc: float = time.perf_counter()
        print(f"{func.__name__} = {toc - tic: 0.1f} seconds")

        return result

    return wrapper


class Timer:
    """A decorator to report execution run time for methods w/in classes"""

    def __init__(self) -> None:
        pass

    @staticmethod
    def time_method(func) -> Callable[..., Any]:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            start_counter: float = time.process_time()  # perf_counter?

            result: Any = func(*args, **kwargs)

            end_counter: float = time.process_time()  # perf_counter?
            counter_time: float = end_counter - start_counter
            print(func.__name__, "=", "{:.10f}".format(counter_time), "seconds")

            return result

        return wrapper


### END ###
