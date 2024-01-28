"""Calculate arithmetic expressions from command line."""

import argparse
import enum
import sys
import typing

import pydantic

from package_name_to_import_with import (
    BinaryArithmeticOperator,
    CustomStrEnum,
    calculate_results,
    solve_simplification,
)


@enum.unique
class CalculatorType(CustomStrEnum):
    """Define supported calculator types."""

    BINARY = "binary"
    GENERAL = "general"


class BinaryInputs(pydantic.BaseModel):
    """Define arguments for binary calculator.

    Attributes
    ----------
    calculator_type : typing.Literal[CalculatorType.BINARY]
        kind of calculator
    first_number : float
        first number for the calculation
    operator : BinaryArithmeticOperator
        arithmetic operator to be used
    second_number : float
        second number for the calculation
    """

    calculator_type: typing.Literal[CalculatorType.BINARY] = pydantic.Field(
        description="kind of calculator"
    )
    first_number: float = pydantic.Field(description="first number for the calculation")
    operator: BinaryArithmeticOperator = pydantic.Field(
        description="arithmetic operator to be used"
    )
    second_number: float = pydantic.Field(description="second number for the calculation")


class GeneralInputs(pydantic.BaseModel):
    """Define arguments of general calculator.

    Attributes
    ----------
    calculator_type : typing.Literal[CalculatorType.GENERAL]
        kind of calculator
    expression : str
        mathematical expression to be evaluated
    """

    calculator_type: typing.Literal[CalculatorType.GENERAL] = pydantic.Field(
        description="kind of calculator"
    )
    expression: str = pydantic.Field(description="mathematical expression to be evaluated")


class UserInputs(pydantic.BaseModel):
    """Define sub-commands and arguments of CLI calculator.

    Attributes
    ----------
    inputs : BinaryInputs | GeneralInputs
        inputs for the calculator
    """

    inputs: BinaryInputs | GeneralInputs = pydantic.Field(
        description="inputs for the calculator", discriminator="calculator_type"
    )


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

    binary_parser = sub_parsers.add_parser(CalculatorType.BINARY, help="basic binary operations")
    general_parser = sub_parsers.add_parser(
        CalculatorType.GENERAL, help="standard simplification problems"
    )

    binary_parser.add_argument("first_number", type=float, help="first number")
    binary_parser.add_argument(
        "operator", type=BinaryArithmeticOperator, help="arithmetic operator"
    )
    binary_parser.add_argument("second_number", type=float, help="second number")

    general_parser.add_argument("expression", type=str, help="infix expression")

    parsed_arguments, _ = parser.parse_known_args()

    return UserInputs.model_validate({"inputs": vars(parsed_arguments)})


@pydantic.validate_call(validate_return=True)
def console_calculator() -> None:
    """Calculate arithmetic expressions."""
    user_inputs = capture_user_inputs()

    try:
        match user_inputs.inputs.calculator_type:
            case CalculatorType.BINARY:
                operation_result = calculate_results(
                    user_inputs.inputs.first_number,  # type: ignore[union-attr]
                    user_inputs.inputs.operator,  # type: ignore[union-attr]
                    user_inputs.inputs.second_number,  # type: ignore[union-attr]
                )
            case CalculatorType.GENERAL:
                operation_result = solve_simplification(
                    user_inputs.inputs.expression  # type: ignore[union-attr]
                )
            case _:  # pragma: no cover
                operation_result = None
    except Exception as error:  # noqa: BLE001  # pylint: disable=broad-except
        sys.stderr.write(f"Error: {error}")
    else:
        sys.stdout.write(f"Result = {operation_result}")


if __name__ == "__main__":
    console_calculator()
