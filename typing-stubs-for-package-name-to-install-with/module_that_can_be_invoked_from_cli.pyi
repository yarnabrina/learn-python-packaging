import typing

from package_name_to_import_with import (
    BinaryArithmeticOperator,
    CustomPydanticBaseModel,
    CustomStrEnum,
)

class CalculatorType(CustomStrEnum):
    BINARY: str
    GENERAL: str

class BinaryInputs(CustomPydanticBaseModel):
    calculator_type: typing.Literal[CalculatorType.BINARY]
    first_number: float
    operator: BinaryArithmeticOperator
    second_number: float

class GeneralInputs(CustomPydanticBaseModel):
    calculator_type: typing.Literal[CalculatorType.GENERAL]
    expression: str

class UserInputs(CustomPydanticBaseModel):
    inputs: BinaryInputs | GeneralInputs

def capture_user_inputs() -> UserInputs: ...
def console_calculator() -> None: ...
