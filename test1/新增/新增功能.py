#!/usr/bin/env python3
"""新增功能.py - 新增功能模块"""

def add(a, b):
    """两数相加"""
    return a + b

def greet(name, time_of_day="白天", is_formal=False):
    """个性化问候"""
    
    if is_formal:
        title = "尊敬的"
    else:
        title = "亲爱的"
        
    time_greetings = {
        "早上": "早安",
        "下午": "午安",
        "晚上": "晚安",
        "白天": "你好"
    }
    
    greeting = time_greetings.get(time_of_day, "你好")
    
    return f"{greeting}，{title}{name}！欢迎你！✨"

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
