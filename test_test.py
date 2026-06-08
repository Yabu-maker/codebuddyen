import pytest

from test import factorial


def test_factorial_zero_returns_one():
    assert factorial(0) == 1


def test_factorial_one_returns_one():
    assert factorial(1) == 1


def test_factorial_positive_integer():
    assert factorial(5) == 120


def test_factorial_larger_integer():
    assert factorial(8) == 40320


def test_factorial_negative_raises_recursion_error():
    with pytest.raises(RecursionError):
        factorial(-1)


def test_factorial_non_integer_string_raises_type_error():
    with pytest.raises(TypeError):
        factorial("5")


def test_factorial_float_raises_recursion_error():
    with pytest.raises(RecursionError):
        factorial(3.5)
