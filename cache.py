#!/usr/bin/env python3
"""cache.py - LRU 缓存实现（30行）"""
from collections import OrderedDict
from functools import wraps

class LRUCache:
    def __init__(self, capacity: int = 128):
        self.capacity = capacity
        self.store = OrderedDict()

    def get(self, key):
        if key not in self.store: return None
        self.store.move_to_end(key)
        return self.store[key]

    def put(self, key, value):
        if key in self.store: self.store.move_to_end(key)
        self.store[key] = value
        if len(self.store) > self.capacity: self.store.popitem(last=False)

def cached(capacity=128):
    cache = LRUCache(capacity)
    def decorator(func):
        @wraps(func)
        def wrapper(*args):
            key = (func.__name__,) + args
            result = cache.get(key)
            if result is not None: return result
            result = func(*args)
            cache.put(key, result)
            return result
        wrapper.clear = lambda: cache.store.clear()
        return wrapper
    return decorator

@cached(capacity=64)
def fib(n):
    if n < 2: return n
    return fib(n - 1) + fib(n - 2)

if __name__ == "__main__":
    print(f"fib(35) = {fib(35)}")