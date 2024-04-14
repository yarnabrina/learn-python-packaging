import functools
import typing

from ..utils import CustomPydanticBaseModel, CustomStrEnum

__all__ = [
    "BINARY_ARITHMETIC_OPERATIONS",
    "BinaryArithmeticExpression",
    "BinaryArithmeticOperation",
    "BinaryArithmeticOperator",
    "calculate_results",
]

BinaryArithmeticOperation: typing.TypeAlias

class BinaryArithmeticOperator(CustomStrEnum):
    ADDITION: str
    SUBTRACTION: str
    MULTIPLICATION: str
    DIVISION: str

BINARY_ARITHMETIC_OPERATIONS: dict[BinaryArithmeticOperator, BinaryArithmeticOperation]

class BinaryArithmeticExpression(CustomPydanticBaseModel):
    left_operand: float
    binary_operator: BinaryArithmeticOperator
    right_operand: float
    def validate_zero_division(self: BinaryArithmeticExpression) -> BinaryArithmeticExpression: ...
    @property
    def operation(self: BinaryArithmeticExpression) -> BinaryArithmeticOperation: ...
    @functools.cached_property
    def result(self: BinaryArithmeticExpression) -> float: ...

def calculate_results(
    first_input: float, operator: BinaryArithmeticOperator, second_input: float
) -> float: ...
