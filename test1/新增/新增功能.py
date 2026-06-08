#!/usr/bin/env python3
"""新增功能.py - 新增功能模块"""

def add(a, b):
    """两数相加"""
    return a + b

def greet(name):
    """个性化问候"""
    return f"欢迎你, {name}! ✨"

def multiply(a, b):
    """两数相乘"""
    return a * b

def factorial(n):
    """计算阶乘"""
    if n <= 1: return 1
    result = 1
    for i in range(2, n + 1): result *= i
    return result

def is_prime(n):
    """判断质数"""
    if n < 2: return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0: return False
    return True

if __name__ == "__main__":
    print(greet("开发者"))
    print(f"1 + 2 = {add(1, 2)}")
    print(f"3 × 4 = {multiply(3, 4)}")
    print(f"5! = {factorial(5)}")
    print(f"7 是质数? {is_prime(7)}")
