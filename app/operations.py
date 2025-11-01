import math
from .exceptions import OperationError

class Operation:
    name = "base"
    def compute(self, a, b):
        raise NotImplementedError

class Add(Operation):
    name = "add"
    def compute(self, a, b): return a + b

class Subtract(Operation):
    name = "subtract"
    def compute(self, a, b): return a - b

class Multiply(Operation):
    name = "multiply"
    def compute(self, a, b): return a * b

class Divide(Operation):
    name = "divide"
    def compute(self, a, b):
        if b == 0: raise OperationError("Division by zero")
        return a / b

class Power(Operation):
    name = "power"
    def compute(self, a, b): return a ** b

class Root(Operation):
    name = "root"
    def compute(self, a, b):
        if b == 0: raise OperationError("Zero root undefined")
        # nth root => a ** (1/b)
        # handle negative base with odd b
        if a < 0 and int(b) % 2 == 0:
            raise OperationError("Even root of negative number")
        return math.copysign(abs(a) ** (1.0 / b), 1 if a >= 0 else -1)

class Modulus(Operation):
    name = "modulus"
    def compute(self, a, b):
        if b == 0: raise OperationError("Modulus by zero")
        return a % b

class IntDivide(Operation):
    name = "int_divide"
    def compute(self, a, b):
        if b == 0: raise OperationError("Division by zero")
        return int(a // b)

class Percent(Operation):
    name = "percent"
    def compute(self, a, b):
        if b == 0: raise OperationError("Percent with divisor zero")
        return (a / b) * 100.0

class AbsDiff(Operation):
    name = "abs_diff"
    def compute(self, a, b): return abs(a - b)

FACTORY = {
    cls.name: cls for cls in [
        Add, Subtract, Multiply, Divide,
        Power, Root, Modulus, IntDivide, Percent, AbsDiff
    ]
}

def create_operation(op_name: str) -> Operation:
    key = op_name.strip().lower()
    if key not in FACTORY:
        raise OperationError(f"Unknown operation: {op_name}")
    return FACTORY[key]()
