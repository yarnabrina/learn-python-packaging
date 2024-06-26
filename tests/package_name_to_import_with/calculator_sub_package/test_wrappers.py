"""Define unit tests for basic binary operations."""

import math
import typing

import pydantic
import pytest

from package_name_to_import_with.calculator_sub_package import (
    BinaryArithmeticOperator,
    calculate_results,
)


def test_successful_operation(
    first_number: float,
    operator: BinaryArithmeticOperator,
    second_number: float,
    expected_result: float,
) -> None:
    """Check operation of two real numbers.

    Parameters
    ----------
    first_number : float
        value of first number
    operator : BinaryArithmeticOperator
        type of arithmetic operation
    second_number : float
        value of second number
    expected_result : float
        value of expected sum
    """
    result = calculate_results(first_number, operator, second_number)
    assert math.isclose(result, expected_result)  # nosec B101


@pytest.mark.parametrize(
    ("first_input", "operator", "second_input"),
    [
        ("not_number", "+", 3),
        ("not_number", "-", 6),
        ("not_number", "*", 7),
        ("not_number", "/", 8),
        (3, "+", "not_number"),
        (6, "-", "not_number"),
        (7, "*", "not_number"),
        (8, "/", "not_number"),
        (0, "^", 0),
    ],
)
def test_operation_failure(
    first_input: typing.Any,  # noqa: ANN401
    operator: typing.Any,  # noqa: ANN401
    second_input: typing.Any,  # noqa: ANN401
) -> None:
    """Check failure during calculations.

    Parameters
    ----------
    first_input : typing.Any
        input for first number
    operator : typing.Any
        input for operator
    second_input : typing.Any
        input for second number
    """
    with pytest.raises(pydantic.ValidationError):
        calculate_results(first_input, operator, second_input)
