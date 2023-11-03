"""Calculate arithmetic expressions from command line."""
import argparse
import enum
import sys
import typing

import pydantic

import package_name_to_import_with


@enum.unique
class CalculatorType(str, enum.Enum):
    """Define supported calculator types."""

    BINARY = "binary"
    GENERAL = "general"


class BinaryInputs(pydantic.BaseModel):
    """Define arguments for binary calculator."""

    calculator_type: typing.Literal[CalculatorType.BINARY]
    first_number: str
    operator: str
    second_number: str


class GeneralInputs(pydantic.BaseModel):
    """Define arguments of general calculator."""

    calculator_type: typing.Literal[CalculatorType.GENERAL]
    expression: str


class UserInputs(pydantic.BaseModel):
    """Define sub-commands and arguments of CLI calculator."""

    inputs: BinaryInputs | GeneralInputs = pydantic.Field(discriminator="calculator_type")


@pydantic.validate_call(validate_return=True)
def capture_user_inputs() -> UserInputs:
    """Capture user inputs for arithmetic expression.

    Returns
    -------
    UserInputs
        captured user inputs
    """
    parser = argparse.ArgumentParser(description="calculator for console", add_help=True)

    sub_parsers = parser.add_subparsers(
        dest="calculator_type", help="types of arithmetic expressions"
    )

    binary_parser = sub_parsers.add_parser(
        CalculatorType.BINARY.value, help="basic binary operations"
    )
    general_parser = sub_parsers.add_parser(
        CalculatorType.GENERAL.value, help="standard simplification problems"
    )

    binary_parser.add_argument("first_number", help="first number")
    binary_parser.add_argument("operator", help="arithmetic operator")
    binary_parser.add_argument("second_number", help="second number")

    general_parser.add_argument("expression", help="infix expression")

    parsed_arguments, _ = parser.parse_known_args()

    return UserInputs.model_validate({"inputs": vars(parsed_arguments)})


@pydantic.validate_call(validate_return=True)
def console_calculator() -> None:
    """Calculate arithmetic expressions."""
    user_inputs = capture_user_inputs()

    try:
        match user_inputs.inputs.calculator_type:
            case CalculatorType.BINARY:
                operation_result = package_name_to_import_with.calculate_results(
                    user_inputs.inputs.first_number,
                    user_inputs.inputs.operator,
                    user_inputs.inputs.second_number,
                )
            case CalculatorType.GENERAL:
                operation_result = package_name_to_import_with.solve_simplification(
                    user_inputs.inputs.expression
                )
            case _:
                operation_result = None
    except Exception as error:  # noqa: BLE001  # pylint: disable=broad-except
        sys.stderr.write(f"Error: {error}")
    else:
        sys.stdout.write(f"Result = {operation_result}")


if __name__ == "__main__":
    console_calculator()
