"""Define common inputs for unit tests."""
import typing

import pytest


@pytest.fixture(params=[4, -9], name="first_number")
def fixture_first_number(request: pytest.FixtureRequest) -> float:
    """Define first input for unit tests.

    Returns
    -------
    float
        value of first input
    """
    return request.param


@pytest.fixture(params=[5, 10], name="second_number")
def fixture_second_number(request: pytest.FixtureRequest) -> float:
    """Define second input for unit tests.

    Returns
    -------
    float
        value of second input
    """
    return request.param


@pytest.fixture(params=["+", "-", "*", "/"], name="operator")
def fixture_operator(request: pytest.FixtureRequest) -> typing.Literal["+", "-", "*", "/"]:
    """Define operator for unit tests.

    Returns
    -------
    typing.Literal["+", "-", "*", "/"]
        value of operator
    """
    return request.param


@pytest.fixture
def expected_sum(first_number: float, second_number: float) -> float:
    """Define expected sum for unit tests.

    Parameters
    ----------
    first_number : float
        value of first number
    second_number : float
        value of second number

    Returns
    -------
    float
        value of expected sum
    """
    return first_number + second_number


@pytest.fixture
def expected_difference(first_number: float, second_number: float) -> float:
    """Define expected difference for unit tests.

    Parameters
    ----------
    first_number : float
        value of first number
    second_number : float
        value of second number

    Returns
    -------
    float
        value of expected difference
    """
    return first_number - second_number


@pytest.fixture
def expected_product(first_number: float, second_number: float) -> float:
    """Define expected product for unit tests.

    Parameters
    ----------
    first_number : float
        value of first number
    second_number : float
        value of second number

    Returns
    -------
    float
        value of expected product
    """
    return first_number * second_number


@pytest.fixture
def expected_quotient(first_number: float, second_number: float) -> float:
    """Define expected quotient for unit tests.

    Parameters
    ----------
    first_number : float
        value of first number
    second_number : float
        value of second number

    Returns
    -------
    float
        value of expected quotient
    """
    return first_number / second_number


@pytest.fixture
def expected_result(
    first_number: float,
    second_number: float,
    operator: typing.Literal["+", "-", "*", "/"],
) -> float:
    """Define expected result for unit tests.

    Parameters
    ----------
    first_number : float
        value of first number
    second_number : float
        value of second number
    operator : typing.Literal["+", "-", "*", "/"]
        type of arithmetic operation

    Returns
    -------
    float
        value of expected result

    Raises
    ------
    ValueError
        if ``operator`` not one of "+", "-", "*", "/"
    """
    if operator == "+":
        return first_number + second_number

    if operator == "-":
        return first_number - second_number

    if operator == "*":
        return first_number * second_number

    if operator == "/":
        return first_number / second_number

    raise ValueError("Unexpected value of operation")
