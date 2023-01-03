"""Define unit tests for arithmetic operations."""
import pytest

from package_name_to_import_with import calculator_sub_package


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
    result = calculator_sub_package.add_numbers(first_number, second_number)
    assert result == pytest.approx(expected_sum)  # nosec B101


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
    result = calculator_sub_package.subtract_numbers(first_number, second_number)
    assert result == pytest.approx(expected_difference)  # nosec B101


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
    result = calculator_sub_package.multiply_numbers(first_number, second_number)
    assert result == pytest.approx(expected_product)  # nosec B101


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
    result = calculator_sub_package.divide_numbers(first_number, second_number)
    assert result == pytest.approx(expected_quotient)  # nosec B101
