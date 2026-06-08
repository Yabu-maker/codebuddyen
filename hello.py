#!/usr/bin/env python3
"""hello.py - 极简问候程序"""
import sys

def greet(name="world"):
    return f"Hello, {name}! 🎉"

if __name__ == "__main__":
    arg = sys.argv[1] if len(sys.argv) > 1 else "world"
    print(greet(arg))
