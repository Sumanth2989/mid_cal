import pytest
from app.operations import create_operation
from app.exceptions import OperationError

@pytest.mark.parametrize("op,a,b,expected", [
    ("add", 2, 3, 5),
    ("subtract", 5, 2, 3),
    ("multiply", 3, 4, 12),
    ("divide", 10, 2, 5),
    ("power", 2, 3, 8),
    ("modulus", 7, 4, 3),
    ("int_divide", 7, 2, 3),
    ("percent", 50, 200, 25),
    ("abs_diff", 5, 9, 4),
])
def test_ops(op, a, b, expected):
    assert create_operation(op).compute(a,b) == expected

def test_divide_by_zero():
    with pytest.raises(OperationError):
        create_operation("divide").compute(1,0)

def test_int_divide_truncates():
    assert create_operation("int_divide").compute(7, 3) == 2

def test_percent_zero_divisor():
    with pytest.raises(OperationError):
        create_operation("percent").compute(50, 0)

def test_modulus_zero_divisor():
    with pytest.raises(OperationError):
        create_operation("modulus").compute(5, 0)

def test_divide_zero_divisor():
    with pytest.raises(OperationError):
        create_operation("divide").compute(1, 0)
