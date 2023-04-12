"""Define unit tests for arithmetic operations."""
import math

import pytest

from package_name_to_import_with import calculator_sub_package


def test_successful_additive_inverse(first_number: float, expected_negative: float) -> None:
    """Check additive inverse of a real number.

    Parameters
    ----------
    first_number : float
        value of input number
    expected_negative : float
        value of expected negative
    """
    result = calculator_sub_package.get_negative(first_number)
    assert math.isclose(result, expected_negative)  # nosec B101


def test_successful_multiplicative_inverse(
    second_number: float, expected_reciprocal: float
) -> None:
    """Check multiplicative inverse of a real number.

    Parameters
    ----------
    second_number : float
        value of input number
    expected_reciprocal : float
        value of expected reciprocal
    """
    result = calculator_sub_package.get_reciprocal(second_number)
    assert math.isclose(result, expected_reciprocal)  # nosec B101


def test_multiplicative_inverse_failure() -> None:
    """Check failure because of zero-division."""
    with pytest.raises(ValueError, match="Multiplicative inverse is not defined for zero"):
        calculator_sub_package.get_reciprocal(0)
