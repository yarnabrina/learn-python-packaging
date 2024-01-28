import functools
import typing

import pydantic

from ..utils import CustomStrEnum

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

class BinaryArithmeticExpression(pydantic.BaseModel):
    left_operand: float
    binary_operator: BinaryArithmeticOperator
    right_operand: float
    @property
    def operation(self) -> BinaryArithmeticOperation: ...
    @functools.cached_property
    def result(self) -> float: ...

def calculate_results(
    first_input: float, operator: BinaryArithmeticOperator, second_input: float
) -> float: ...
