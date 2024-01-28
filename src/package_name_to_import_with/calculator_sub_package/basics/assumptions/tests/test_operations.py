"""Define unit tests for arithmetic operations."""

import math

from package_name_to_import_with.calculator_sub_package import add_numbers, multiply_numbers


def test_successful_addition(
    first_number: float, second_number: float, expected_sum: float
) -> None:
    """Check addition of two real numbers.

    Parameters
    ----------
    first_number : float
        value of first number
    second_number : float
        value of second number
    expected_sum : float
        value of expected sum
    """
    result = add_numbers(first_number, second_number)
    assert math.isclose(result, expected_sum)  # nosec B101


def test_successful_multiplication(
    first_number: float, second_number: float, expected_product: float
) -> None:
    """Check multiplication of two real numbers.

    Parameters
    ----------
    first_number : float
        value of first number
    second_number : float
        value of second number
    expected_product : float
        value of expected sum
    """
    result = multiply_numbers(first_number, second_number)
    assert math.isclose(result, expected_product)  # nosec B101
