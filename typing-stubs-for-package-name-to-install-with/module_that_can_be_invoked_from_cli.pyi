import enum
import typing

import pydantic

from package_name_to_import_with import BinaryArithmeticOperator

class CalculatorType(str, enum.Enum):
    BINARY: str
    GENERAL: str

class BinaryInputs(pydantic.BaseModel):
    calculator_type: typing.Literal[CalculatorType.BINARY]
    first_number: float
    operator: BinaryArithmeticOperator
    second_number: float

class GeneralInputs(pydantic.BaseModel):
    calculator_type: typing.Literal[CalculatorType.GENERAL]
    expression: str

class UserInputs(pydantic.BaseModel):
    inputs: BinaryInputs | GeneralInputs

def capture_user_inputs() -> UserInputs: ...
def console_calculator() -> None: ...
