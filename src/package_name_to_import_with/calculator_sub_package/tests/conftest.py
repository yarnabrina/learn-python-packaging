"""Define common inputs for unit tests."""

import pytest

from package_name_to_import_with.calculator_sub_package.wrapper_module import ArithmeticOperator


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


@pytest.fixture(params=ArithmeticOperator, name="operator")
def fixture_operator(request: pytest.FixtureRequest) -> ArithmeticOperator:
    """Define operator for unit tests.

    Parameters
    ----------
    request : pytest.FixtureRequest
        request for fixture from test function

    Returns
    -------
    ArithmeticOperator
        value of operator
    """
    return request.param


@pytest.fixture()
def expected_result(
    first_number: float, second_number: float, operator: ArithmeticOperator
) -> float:
    """Define expected result for unit tests.

    Parameters
    ----------
    first_number : float
        value of first number
    second_number : float
        value of second number
    operator : ArithmeticOperator
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
    if ArithmeticOperator(operator) == ArithmeticOperator.ADDITION:
        return first_number + second_number

    if ArithmeticOperator(operator) == ArithmeticOperator.SUBTRACTION:
        return first_number - second_number

    if ArithmeticOperator(operator) == ArithmeticOperator.MULTIPLICATION:
        return first_number * second_number

    if ArithmeticOperator(operator) == ArithmeticOperator.DIVISION:
        return first_number / second_number

    raise ValueError("Unexpected value of operation")
