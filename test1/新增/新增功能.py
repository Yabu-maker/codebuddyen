#!/usr/bin/env python3
"""新增功能.py - 新增功能模块"""

def add(a, b):
    """两数相加"""
    return a + b

def greet(name):
    """个性化问候"""
    return f"欢迎你, {name}! ✨"

if __name__ == "__main__":
    print(greet("开发者"))
    print(f"1 + 2 = {add(1, 2)}")
