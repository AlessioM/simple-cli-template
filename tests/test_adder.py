"""tests for the adder function"""

import pytest

from adder.adder import add_all


@pytest.mark.parametrize(
    "a,b,sum",
    [(1, 2, 3), (-1, 1, 0)],
)
def test_add_two(a, b, sum):
    """test that it calculates the total"""
    assert add_all(a, b) == sum


@pytest.mark.parametrize("val", ["a", None, "1.1"])
def test_invalid(val):
    """test that it only accept integer values"""
    with pytest.raises(ValueError):
        add_all(val)


def test_conversion():
    """test that it correctly converts strings to ints"""
    assert add_all("1", "2") == 3
