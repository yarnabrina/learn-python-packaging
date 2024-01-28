"""Define property based unit tests based on random data."""

import math
import sys

import hypothesis
import hypothesis.strategies

from package_name_to_import_with import solve_simplification
from package_name_to_import_with.calculator_sub_package import (
    BinaryArithmeticOperator,
    IdentityElements,
    add_numbers,
    calculate_results,
    divide_numbers,
    get_negative,
    get_reciprocal,
    multiply_numbers,
    subtract_numbers,
)


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


def generate_arithmetic_expression() -> hypothesis.strategies.SearchStrategy:
    """Generate an arbitrary arithmetic expression of positive finite real numbers.

    Returns
    -------
    hypothesis.strategies.SearchStrategy
        updated strategy
    """
    generate_non_negative_number_strategy = hypothesis.strategies.one_of(
        hypothesis.strategies.integers().map(str),
        hypothesis.strategies.floats(
            allow_nan=False, allow_infinity=False, allow_subnormal=False
        ).map(lambda element: format(element, "f")),
    )
    generate_conditional_space_strategy = hypothesis.strategies.booleans().map(
        lambda element: " " if element else ""
    )

    generate_binary_expression_strategy = hypothesis.strategies.tuples(
        generate_non_negative_number_strategy,
        generate_conditional_space_strategy,
        hypothesis.strategies.sampled_from(BinaryArithmeticOperator),
        generate_conditional_space_strategy,
        generate_non_negative_number_strategy,
    ).map("".join)

    generate_possibly_parenthesised_expression_strategy = hypothesis.strategies.tuples(
        hypothesis.strategies.booleans(), generate_binary_expression_strategy
    ).map(lambda elements: f"({elements[1]})" if elements[0] else elements[1])

    generate_generalised_expression_strategy = hypothesis.strategies.recursive(
        generate_possibly_parenthesised_expression_strategy,
        lambda children: hypothesis.strategies.tuples(
            children,
            generate_conditional_space_strategy,
            hypothesis.strategies.sampled_from(BinaryArithmeticOperator),
            generate_conditional_space_strategy,
            children,
        ).map("".join),
    )

    return generate_generalised_expression_strategy


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

    assert math.isclose(negative_definition, IdentityElements.ADDITIVE_IDENTITY)


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

    assert math.isclose(reciprocal_definition, IdentityElements.MULTIPLICATIVE_IDENTITY)


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
    operator=hypothesis.strategies.sampled_from(BinaryArithmeticOperator),
    second_number=generate_finite_numbers(),
)
def test_operation_hypothesis(
    first_number: float, operator: BinaryArithmeticOperator, second_number: float
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

    Raises
    ------
    ValueError
        if ``operator`` not one of ``+``, ``-``, ``*``, ``/``
    """
    hypothesis.assume(
        not (
            operator is BinaryArithmeticOperator.DIVISION
            and abs(second_number) <= sys.float_info.epsilon
        )
    )

    calculated_result = calculate_results(first_number, operator, second_number)

    match operator:
        case BinaryArithmeticOperator.ADDITION:
            expected_result = first_number + second_number
        case BinaryArithmeticOperator.SUBTRACTION:
            expected_result = first_number - second_number
        case BinaryArithmeticOperator.MULTIPLICATION:
            expected_result = first_number * second_number
        case BinaryArithmeticOperator.DIVISION:
            expected_result = first_number / second_number

    assert math.isclose(calculated_result, expected_result)


@hypothesis.given(expression=generate_arithmetic_expression())
def test_simplification_hypothesis(expression: str) -> None:
    """Check simplification of arithmetic expression.

    Parameters
    ----------
    expression : str
        arbitrary arithmetic expression
    """
    try:
        calculated_result = solve_simplification(expression)
    except ValueError as error:
        if str(error) != "Multiplicative inverse is not defined for additive identity":
            raise

        calculation_failed = True
    else:
        calculation_failed = False

    try:
        expected_result = eval(  # noqa: PGH001, S307  # pylint: disable=eval-used
            expression, {"__builtins__": {}}
        )
    except ZeroDivisionError:
        expectation_failed = True
    else:
        expectation_failed = False

    assert calculation_failed == expectation_failed

    if not calculation_failed and not expectation_failed:
        if math.isfinite(calculated_result):
            assert math.isfinite(expected_result)
            assert math.isclose(calculated_result, expected_result)
        else:
            assert math.isinf(calculated_result) is math.isinf(expected_result)
            assert math.isnan(calculated_result) is math.isnan(expected_result)
