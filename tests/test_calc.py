from app.calc import add
import pytest


# learning how to test


@pytest.mark.parametrize("num1, num2, expected", [(3, 2, 5), (2, 2, 4), (10, 5, 15)])
def test_add(num1, num2, expected):
    assert add(num1, num2) == expected

# create a fixture


@pytest.fixture
def zero_def():
    return 0
