"""Define unit tests for console calculator."""
import re
import typing
import unittest.mock

import module_that_can_be_invoked_from_cli

if typing.TYPE_CHECKING:
    import pytest


def test_sum(capsys: "pytest.CaptureFixture") -> None:
    """Check addition of two numbers."""
    with unittest.mock.patch("sys.argv", ["prog", "4", "+", "5"]):
        module_that_can_be_invoked_from_cli.console_calculator()
        sum_result, _ = capsys.readouterr()

    assert re.match("Result = 9.0", sum_result)  # nosec B101


def test_difference(capsys: "pytest.CaptureFixture") -> None:
    """Check subtraction of two numbers."""
    with unittest.mock.patch("sys.argv", ["prog", "8", "-", "7"]):
        module_that_can_be_invoked_from_cli.console_calculator()
        difference_result, _ = capsys.readouterr()

    assert re.match("Result = 1.0", difference_result)  # nosec B101


def test_product(capsys: "pytest.CaptureFixture") -> None:
    """Check multiplication of two numbers."""
    with unittest.mock.patch("sys.argv", ["prog", "2", "*", "3"]):
        module_that_can_be_invoked_from_cli.console_calculator()
        product_result, _ = capsys.readouterr()

    assert re.match("Result = 6.0", product_result)  # nosec B101


def test_quotient(capsys: "pytest.CaptureFixture") -> None:
    """Check division of two numbers."""
    with unittest.mock.patch("sys.argv", ["prog", "0", "/", "10"]):
        module_that_can_be_invoked_from_cli.console_calculator()
        quotient_result, _ = capsys.readouterr()

    assert re.match("Result = 0.0", quotient_result)  # nosec B101


def test_first_input_failure(capsys: "pytest.CaptureFixture") -> None:
    """Check failure in first user input."""
    with unittest.mock.patch("sys.argv", ["prog", "one", "+", "1"]):
        module_that_can_be_invoked_from_cli.console_calculator()
        _, result_error = capsys.readouterr()

    assert re.match("Error: Supports only real numbers", result_error)  # nosec B101


def test_second_input_failure(capsys: "pytest.CaptureFixture") -> None:
    """Check failure in second user input."""
    with unittest.mock.patch("sys.argv", ["prog", "2", "*", "two"]):
        module_that_can_be_invoked_from_cli.console_calculator()
        _, result_error = capsys.readouterr()

    assert re.match("Error: Supports only real numbers", result_error)  # nosec B101


def test_operator_input_failure(capsys: "pytest.CaptureFixture") -> None:
    """Check failure in operator input."""
    with unittest.mock.patch("sys.argv", ["prog", "0", "x", "0"]):
        module_that_can_be_invoked_from_cli.console_calculator()
        _, result_error = capsys.readouterr()

    assert re.match("Error: Supports only basic arithmetic", result_error)  # nosec B101
