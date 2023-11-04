import enum
import typing

import pydantic

ArithmeticOperation: typing.TypeAlias

class ArithmeticOperator(str, enum.Enum):
    ADDITION: str
    SUBTRACTION: str
    MULTIPLICATION: str
    DIVISION: str

ARITHMETIC_OPERATIONS: dict[ArithmeticOperator, ArithmeticOperation]

class ArithmeticExpression(pydantic.BaseModel):
    first_number: float
    operator: ArithmeticOperator
    second_number: float
    @property
    def operation(self) -> ArithmeticOperation: ...
    @property
    def result(self) -> float: ...

def calculate_results(
    first_input: float, operator: ArithmeticOperator, second_input: float
) -> float: ...
