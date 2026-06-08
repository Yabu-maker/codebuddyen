#!/usr/bin/env python3
"""timer.py - 简易计时装饰器"""
import time, functools, logging

logger = logging.getLogger(__name__)

def timer(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        cost = time.perf_counter() - start
        logger.info(f"⏱ {func.__name__}: {cost:.4f}s")
        return result
    return wrapper
    

@timer
def slow_task():
    return sum(range(10**6))

if __name__ == "__main__": slow_task()
