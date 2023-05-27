"""Define unit tests for console calculator."""
import unittest.mock

import pytest

import module_that_can_be_invoked_from_cli


def test_sum(capsys: pytest.CaptureFixture) -> None:
    """Check addition of two numbers.

    Parameters
    ----------
    capsys : pytest.CaptureFixture
        fixture capturing ``sys.stdout`` and ``sys.stderr``
    """
    with unittest.mock.patch("sys.argv", ["prog", "4", "+", "5"]):
        module_that_can_be_invoked_from_cli.console_calculator()
        sum_result, _ = capsys.readouterr()

    assert sum_result == "Result = 9.0"  # nosec B101


def test_difference(capsys: pytest.CaptureFixture) -> None:
    """Check subtraction of two numbers.

    Parameters
    ----------
    capsys : pytest.CaptureFixture
        fixture capturing ``sys.stdout`` and ``sys.stderr``
    """
    with unittest.mock.patch("sys.argv", ["prog", "8", "-", "7"]):
        module_that_can_be_invoked_from_cli.console_calculator()
        difference_result, _ = capsys.readouterr()

    assert difference_result == "Result = 1.0"  # nosec B101


def test_product(capsys: pytest.CaptureFixture) -> None:
    """Check multiplication of two numbers.

    Parameters
    ----------
    capsys : pytest.CaptureFixture
        fixture capturing ``sys.stdout`` and ``sys.stderr``
    """
    with unittest.mock.patch("sys.argv", ["prog", "2", "*", "3"]):
        module_that_can_be_invoked_from_cli.console_calculator()
        product_result, _ = capsys.readouterr()

    assert product_result == "Result = 6.0"  # nosec B101


def test_quotient(capsys: pytest.CaptureFixture) -> None:
    """Check division of two numbers.

    Parameters
    ----------
    capsys : pytest.CaptureFixture
        fixture capturing ``sys.stdout`` and ``sys.stderr``
    """
    with unittest.mock.patch("sys.argv", ["prog", "0", "/", "10"]):
        module_that_can_be_invoked_from_cli.console_calculator()
        quotient_result, _ = capsys.readouterr()

    assert quotient_result == "Result = 0.0"  # nosec B101


def test_first_input_failure(capsys: pytest.CaptureFixture) -> None:
    """Check failure in first user input.

    Parameters
    ----------
    capsys : pytest.CaptureFixture
        fixture capturing ``sys.stdout`` and ``sys.stderr``
    """
    with unittest.mock.patch("sys.argv", ["prog", "one", "+", "1"]):
        module_that_can_be_invoked_from_cli.console_calculator()
        _, result_error = capsys.readouterr()

    assert "value is not a valid float" in result_error  # nosec B101


def test_second_input_failure(capsys: pytest.CaptureFixture) -> None:
    """Check failure in second user input.

    Parameters
    ----------
    capsys : pytest.CaptureFixture
        fixture capturing ``sys.stdout`` and ``sys.stderr``
    """
    with unittest.mock.patch("sys.argv", ["prog", "2", "*", "two"]):
        module_that_can_be_invoked_from_cli.console_calculator()
        _, result_error = capsys.readouterr()

    assert "value is not a valid float" in result_error  # nosec B101


def test_operator_input_failure(capsys: pytest.CaptureFixture) -> None:
    """Check failure in operator input.

    Parameters
    ----------
    capsys : pytest.CaptureFixture
        fixture capturing ``sys.stdout`` and ``sys.stderr``
    """
    with unittest.mock.patch("sys.argv", ["prog", "0", "x", "0"]):
        module_that_can_be_invoked_from_cli.console_calculator()
        _, result_error = capsys.readouterr()

    assert "value is not a valid enumeration member" in result_error  # nosec B101
