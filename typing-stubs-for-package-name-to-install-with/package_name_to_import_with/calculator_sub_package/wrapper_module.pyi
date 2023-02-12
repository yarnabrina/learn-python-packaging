import collections.abc
import enum
import typing

from .operations_module import add_numbers, multiply_numbers
from .utility_module import divide_numbers, subtract_numbers

class ArithmeticOperator(enum.Enum):
    ADDITION: str
    SUBTRACTION: str
    MULTIPLICATION: str
    DIVISION: str

class ArithmeticOperation:
    first_number: float
    operation: collections.abc.Callable[[float, float], float]
    second_number: float
    @property
    def result(self) -> float: ...
    def __init__(self, first_number, operation, second_number) -> None: ...

def validate_number_input(user_input: typing.Any) -> float: ...
def validate_operator_input(
    user_input: typing.Any,
) -> collections.abc.Callable[[float, float], float]: ...
def process_inputs(
    first_input: typing.Any, operator: typing.Any, second_input: typing.Any
) -> ArithmeticOperation: ...
def calculate_results(
    first_input: typing.Any, operator: typing.Literal["+", "-", "*", "/"], second_input: typing.Any
) -> float: ...
