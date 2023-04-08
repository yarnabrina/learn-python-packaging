"""Define property based unit tests based on random data."""
import enum
import math
import sys
import typing

import hypothesis
import hypothesis.strategies

from package_name_to_import_with.calculator_sub_package import (
    add_numbers,
    calculate_results,
    divide_numbers,
    get_negative,
    get_reciprocal,
    multiply_numbers,
    subtract_numbers,
)
from package_name_to_import_with.calculator_sub_package.wrapper_module import ArithmeticOperator


@enum.unique
class InverseElements(enum.Enum):
    """Define supported inverse elements."""

    ADDITIVE_INVERSE = 0
    MULTIPLICATIVE_INVERSE = 1


def generate_finite_numbers() -> hypothesis.strategies.SearchStrategy:
    """Generate real numbers which are neither infinity nor NaN.

    Returns
    -------
    hypothesis.strategies.SearchStrategy
        updated strategy
    """
    generate_numbers_strategy = hypothesis.strategies.one_of(
        hypothesis.strategies.integers(),
        hypothesis.strategies.floats(allow_nan=False, allow_infinity=False, allow_subnormal=False),
        hypothesis.strategies.fractions(),
    )

    return generate_numbers_strategy


@hypothesis.given(first_number=generate_finite_numbers(), second_number=generate_finite_numbers())
def test_addition_hypothesis(first_number: float, second_number: float) -> None:
    """Check addition of two real numbers.

    Parameters
    ----------
    first_number : float
        value of first number
    second_number : float
        value of second number
    """
    calculated_sum = add_numbers(first_number, second_number)
    expected_sum = first_number + second_number

    assert math.isclose(calculated_sum, expected_sum)


@hypothesis.given(first_number=generate_finite_numbers(), second_number=generate_finite_numbers())
def test_multiplication_hypothesis(first_number: float, second_number: float) -> None:
    """Check multiplication of two real numbers.

    Parameters
    ----------
    first_number : float
        value of first number
    second_number : float
        value of second number
    """
    calculated_product = add_numbers(first_number, second_number)
    expected_product = first_number + second_number

    assert math.isclose(calculated_product, expected_product)


@hypothesis.given(first_number=generate_finite_numbers())
def test_additive_inverse_hypothesis(first_number: float) -> None:
    """Check additive inverse of a real number.

    Parameters
    ----------
    first_number : float
        value of first number
    """
    calculated_negative = get_negative(first_number)
    negative_definition = add_numbers(first_number, calculated_negative)

    assert math.isclose(negative_definition, InverseElements.ADDITIVE_INVERSE.value)


@hypothesis.given(second_number=generate_finite_numbers())
def test_multiplicative_inverse_hypothesis(second_number: float) -> None:
    """Check multiplicative inverse of a real number.

    Parameters
    ----------
    second_number : float
        value of first number
    """
    hypothesis.assume(abs(second_number) > sys.float_info.epsilon)

    calculated_reciprocal = get_reciprocal(second_number)
    reciprocal_definition = multiply_numbers(second_number, calculated_reciprocal)

    assert math.isclose(reciprocal_definition, InverseElements.MULTIPLICATIVE_INVERSE.value)


@hypothesis.given(first_number=generate_finite_numbers(), second_number=generate_finite_numbers())
def test_subtraction_hypothesis(first_number: float, second_number: float) -> None:
    """Check subtraction of two real numbers.

    Parameters
    ----------
    first_number : float
        value of first number
    second_number : float
        value of second number
    """
    calculated_difference = subtract_numbers(first_number, second_number)
    expected_difference = first_number - second_number

    assert math.isclose(calculated_difference, expected_difference)


@hypothesis.given(first_number=generate_finite_numbers(), second_number=generate_finite_numbers())
def test_division_hypothesis(first_number: float, second_number: float) -> None:
    """Check division of two real numbers.

    Parameters
    ----------
    first_number : float
        value of first number
    second_number : float
        value of second number
    """
    hypothesis.assume(abs(second_number) > sys.float_info.epsilon)

    calculated_quotient = divide_numbers(first_number, second_number)
    expected_quotient = first_number / second_number

    assert math.isclose(calculated_quotient, expected_quotient)


@hypothesis.given(
    first_number=generate_finite_numbers(),
    operator=hypothesis.strategies.sampled_from(ArithmeticOperator),
    second_number=generate_finite_numbers(),
)
def test_operation_hypothesis(
    first_number: float, operator: typing.Literal["+", "-", "*", "/"], second_number: float
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

    Raises
    ------
    ValueError
        if ``operator`` not one of ``+``, ``-``, ``*``, ``/``
    """
    hypothesis.assume(
        not (
            operator == ArithmeticOperator.DIVISION
            and abs(second_number) <= sys.float_info.epsilon
        )
    )

    calculated_result = calculate_results(first_number, operator, second_number)

    if ArithmeticOperator(operator) == ArithmeticOperator.ADDITION:
        expected_result = first_number + second_number
    elif ArithmeticOperator(operator) == ArithmeticOperator.SUBTRACTION:
        expected_result = first_number - second_number
    elif ArithmeticOperator(operator) == ArithmeticOperator.MULTIPLICATION:
        expected_result = first_number * second_number
    elif ArithmeticOperator(operator) == ArithmeticOperator.DIVISION:
        expected_result = first_number / second_number
    else:
        raise ValueError("Unexpected value of operation")

    assert math.isclose(calculated_result, expected_result)
