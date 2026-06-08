"""
ClickHouse 查询结果缓存器（10行核心逻辑）
"""

import time
from typing import Any, Optional
from threading import RLock


class QueryCache:
    """线程安全的内存缓存，TTL 过期机制"""

    def __init__(self, ttl: int = 300):
        self._store: dict[str, tuple[Any, float]] = {}
        self._ttl = ttl
        self._lock = RLock()

    def get(self, key: str) -> Optional[Any]:
        with self._lock:
            if key not in self._store:
                return None
            value, ts = self._store[key]
            if time.time() - ts > self._ttl:
                del self._store[key]
                return None
            return value

    def set(self, key: str, value: Any) -> None:
        with self._lock:
            self._store[key] = (value, time.time())

    def clear(self) -> int:
        with self._lock:
            count = len(self._store)
            self._store.clear()
            return count


cache = QueryCache(ttl=300)
