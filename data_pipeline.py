#!/usr/bin/env python3
"""简洁的10行代码 - 数据处理管道"""

from typing import List

def process_data(items: List[int]) -> dict:
    """对数据进行统计处理"""
    return {
        "count": len(items),
        "sum": sum(items),
        "avg": sum(items) / len(items) if items else 0,
        "max": max(items) if items else None,
        "min": min(items) if items else None,
    }

if __name__ == "__main__":
    data = [3, 7, 2, 9, 4, 1, 8, 5, 6]
    print(process_data(data))
