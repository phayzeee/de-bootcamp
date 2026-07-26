import time
from functools import wraps


def timed(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()

        result = func(*args, **kwargs)

        end = time.perf_counter()

        elapsed = (end - start) * 1000

        print(f"{func.__name__} took {elapsed:.1f} ms")

        return result

    return wrapper


#Example

@timed
def fetch():
    """Fetch some data."""
    time.sleep(0.2)
    return "done"


print(fetch())
print(fetch.__name__)
print(fetch.__doc__)