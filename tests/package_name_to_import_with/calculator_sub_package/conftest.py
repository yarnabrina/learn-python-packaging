"""Define common inputs for unit tests."""

import pytest

from package_name_to_import_with.calculator_sub_package.wrapper_module import (
    BinaryArithmeticOperator,
)


@pytest.fixture(params=[4, -9, 1.02, -3.4], name="first_number")
def fixture_first_number(request: pytest.FixtureRequest) -> float:
    """Define first input for unit tests.

    Parameters
    ----------
    request : pytest.FixtureRequest
        request for fixture from test function

    Returns
    -------
    float
        value of first input
    """
    return request.param


@pytest.fixture(params=[5, 10, -5.6, 7.89], name="second_number")
def fixture_second_number(request: pytest.FixtureRequest) -> float:
    """Define second input for unit tests.

    Parameters
    ----------
    request : pytest.FixtureRequest
        request for fixture from test function

    Returns
    -------
    float
        value of second input
    """
    return request.param


@pytest.fixture(params=BinaryArithmeticOperator, name="operator")
def fixture_operator(request: pytest.FixtureRequest) -> BinaryArithmeticOperator:
    """Define operator for unit tests.

    Parameters
    ----------
    request : pytest.FixtureRequest
        request for fixture from test function

    Returns
    -------
    BinaryArithmeticOperator
        value of operator
    """
    return request.param


@pytest.fixture()
def expected_result(
    first_number: float, second_number: float, operator: BinaryArithmeticOperator
) -> float:
    """Define expected result for unit tests.

    Parameters
    ----------
    first_number : float
        value of first number
    second_number : float
        value of second number
    operator : BinaryArithmeticOperator
        type of arithmetic operation

    Returns
    -------
    float
        value of expected result

    Raises
    ------
    ValueError
        if ``operator`` not one of ``+``, ``-``, ``*``, ``/``
    """
    match operator:
        case BinaryArithmeticOperator.ADDITION:
            return first_number + second_number
        case BinaryArithmeticOperator.SUBTRACTION:
            return first_number - second_number
        case BinaryArithmeticOperator.MULTIPLICATION:
            return first_number * second_number
        case BinaryArithmeticOperator.DIVISION:
            return first_number / second_number
