from .exceptions import ValidationError
from .calculator_config import cfg

from .exceptions import ValidationError
from . import calculator_config  # import the module, not the object

def as_number(x):
    try:
        v = float(x)
    except Exception as e:
        raise ValidationError(f"Not a number: {x}") from e
    max_allowed = calculator_config.cfg.MAX_INPUT_VALUE  # read fresh
    if abs(v) > max_allowed:
        raise ValidationError(f"Input {v} exceeds max allowed {max_allowed}")
    return v

def two_numbers(a, b):
    return as_number(a), as_number(b) 
