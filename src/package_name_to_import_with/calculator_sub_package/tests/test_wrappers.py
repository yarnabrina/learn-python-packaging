"""Define unit tests for calculators."""
import typing

import pytest

import package_name_to_import_with


def test_successful_operation(
    first_number: float,
    operator: typing.Literal["+", "-", "*", "/"],
    second_number: float,
    expected_result: float,
) -> None:
    """Check operation of two real numbers.

    Parameters
    ----------
    first_number : float
        value of first number
    operator : typing.Literal[ "+", "-", "*", "/" ]
        type of arithmetic operation
    second_number : float
        value of second number
    expected_result : float
        value of expected sum
    """
    result = package_name_to_import_with.calculate_results(first_number, operator, second_number)
    assert result == pytest.approx(expected_result)  # nosec B101


@pytest.mark.parametrize(
    ("first_input", "operator", "second_input", "error"),
    [
        ("not_number", "+", 3, "Supports only real numbers"),
        ("not_number", "-", 6, "Supports only real numbers"),
        ("not_number", "*", 7, "Supports only real numbers"),
        ("not_number", "/", 8, "Supports only real numbers"),
        (3, "+", "not_number", "Supports only real numbers"),
        (6, "-", "not_number", "Supports only real numbers"),
        (7, "*", "not_number", "Supports only real numbers"),
        (8, "/", "not_number", "Supports only real numbers"),
        (0, "^", 0, "Supports only basic arithmetic"),
    ],
)
def test_operation_failure(
    first_input: typing.Any, operator: typing.Any, second_input: typing.Any, error: str
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
    error : str
        expected error message
    """
    with pytest.raises(ValueError, match=error):
        package_name_to_import_with.calculate_results(first_input, operator, second_input)
