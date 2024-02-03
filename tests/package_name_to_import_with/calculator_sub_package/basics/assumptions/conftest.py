"""Define common inputs for unit tests."""

import pytest


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


@pytest.fixture()
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


@pytest.fixture()
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


@pytest.fixture()
def expected_negative(first_number: float) -> float:
    """Define expected negative for unit tests.

    Parameters
    ----------
    first_number : float
        value of input number

    Returns
    -------
    float
        value of expected negative
    """
    return (-1) * first_number


@pytest.fixture()
def expected_reciprocal(second_number: float) -> float:
    """Define expected reciprocal for unit tests.

    Parameters
    ----------
    second_number : float
        value of input number

    Returns
    -------
    float
        value of expected reciprocal
    """
    return 1 / second_number
