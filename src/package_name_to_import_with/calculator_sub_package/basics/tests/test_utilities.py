"""Define unit tests for arithmetic operations."""

import math

from package_name_to_import_with.calculator_sub_package import divide_numbers, subtract_numbers


def test_successful_subtraction(
    first_number: float, second_number: float, expected_difference: float
) -> None:
    """Check subtraction of two real numbers.

    Parameters
    ----------
    first_number : float
        value of first number
    second_number : float
        value of second number
    expected_difference : float
        value of expected sum
    """
    result = subtract_numbers(first_number, second_number)
    assert math.isclose(result, expected_difference)  # nosec B101


def test_successful_division(
    first_number: float, second_number: float, expected_quotient: float
) -> None:
    """Check division of two real numbers.

    Parameters
    ----------
    first_number : float
        value of first number
    second_number : float
        value of second number
    expected_quotient : float
        value of expected sum
    """
    result = divide_numbers(first_number, second_number)
    assert math.isclose(result, expected_quotient)  # nosec B101
