"""Define unit tests for arithmetic operations."""
import pytest

from package_name_to_import_with import calculator_sub_package


def test_successful_additive_inverse(first_number: float) -> None:
    """Check additive inverse of a real number.

    Parameters
    ----------
    first_number : float
        value of input number
    """
    result = calculator_sub_package.get_negative(first_number)
    assert calculator_sub_package.add_numbers(result, first_number) == 0  # nosec B101


def test_successful_multiplicative_inverse(second_number: float) -> None:
    """Check multiplicative inverse of a real number.

    Parameters
    ----------
    second_number : float
        value of input number
    """
    result = calculator_sub_package.get_reciprocal(second_number)
    assert calculator_sub_package.multiply_numbers(second_number, result) == 1  # nosec B101


def test_multiplicative_inverse_failure() -> None:
    """Check failure because of zero-division."""
    with pytest.raises(ValueError, match="Multiplicative inverse is not defined for zero"):
        calculator_sub_package.get_reciprocal(0)
