import pytest

from adder.adder import add_all


@pytest.mark.parametrize(
    "a,b,sum",
    [(1, 2, 3), (-1, 1, 0)],
)
def test_add_two(a, b, sum):
    assert add_all(a, b) == sum


def test_invalid():
    with pytest.raises(ValueError):
        add_all("a", 2) == 3


def test_conversion():
    assert add_all("1", "2") == 3


def test_none():
    with pytest.raises(ValueError):
        add_all(None)
