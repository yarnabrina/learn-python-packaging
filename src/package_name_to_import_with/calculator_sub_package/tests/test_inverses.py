"""Define unit tests for arithmetic operations."""
import pytest

from package_name_to_import_with import calculator_sub_package

ADDITIVE_INVERSE_ELEMENT = 0
MULTIPLICATIVE_INVERSE_ELEMENT = 1


def test_successful_additive_inverse(first_number: float) -> None:
    """Check additive inverse of a real number.

    Parameters
    ----------
    first_number : float
        value of input number
    """
    result = calculator_sub_package.get_negative(first_number)

    additive_inverse_check = calculator_sub_package.add_numbers(result, first_number)
    assert additive_inverse_check == ADDITIVE_INVERSE_ELEMENT  # nosec B101


def test_successful_multiplicative_inverse(second_number: float) -> None:
    """Check multiplicative inverse of a real number.

    Parameters
    ----------
    second_number : float
        value of input number
    """
    result = calculator_sub_package.get_reciprocal(second_number)

    multiplicative_inverse_check = calculator_sub_package.multiply_numbers(second_number, result)
    assert multiplicative_inverse_check == MULTIPLICATIVE_INVERSE_ELEMENT  # nosec B101


def test_multiplicative_inverse_failure() -> None:
    """Check failure because of zero-division."""
    with pytest.raises(ValueError, match="Multiplicative inverse is not defined for zero"):
        calculator_sub_package.get_reciprocal(0)
