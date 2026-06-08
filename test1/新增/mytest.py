#!/usr/bin/env python3
"""mytest.py - 测试工具集"""

import unittest
from datetime import datetime
from typing import Any, Callable

def assert_type(value: Any, expected: type, label=""):
    """类型断言"""
    assert isinstance(value, expected), f"{label} 期望 {expected.__name__}, 实际 {type(value).__name__}"
    return True

def measure(func: Callable, *args, **kwargs) -> tuple:
    """执行函数并测量耗时，返回 (结果, 耗时秒数)"""
    start = datetime.now()
    result = func(*args, **kwargs)
    cost = (datetime.now() - start).total_seconds()
    return result, cost

class TestCase(unittest.TestCase):
    """基础测试用例"""

    def test_addition(self):
        self.assertEqual(1 + 2, 3)

    def test_string(self):
        s = "hello"
        assert_type(s, str)
        self.assertTrue(len(s) > 0)

    @staticmethod
    def run_all():
        suite = unittest.TestLoader().loadTestsFromTestCase(TestCase)
        runner = unittest.TextTestRunner(verbosity=2)
        runner.run(suite)

if __name__ == "__main__":
    TestCase.run_all()