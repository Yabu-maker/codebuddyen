"""简洁的10行代码 - 缓存装饰器"""

from functools import wraps
import time
import json
from pathlib import Path


def cache_result(ttl: int = 60):
    """带TTL的缓存装饰器"""
    cache = {}

    def decorator(func):
        @wraps(func)
        def wrapper(*args):
            key = f"{func.__name__}:{args}"
            if key in cache and time.time() - cache[key]["time"] < ttl:
                return cache[key]["value"]
            result = func(*args)
            cache[key] = {"value": result, "time": time.time()}
            return result

        return wrapper

    return decorator


@cache_result(ttl=30)
def fetch_data(source: str) -> dict:
    return {"source": source, "data": [1, 2, 3]}


if __name__ == "__main__":
    print(fetch_data("api_v1"))
