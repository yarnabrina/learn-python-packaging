"""Define unit tests for console calculator."""
import re
import unittest.mock

import pytest

import module_that_can_be_invoked_from_cli


def test_sum(capsys: pytest.CaptureFixture) -> None:
    """Check addition of two numbers."""
    with unittest.mock.patch("sys.argv", ["prog", "4", "+", "5"]):
        module_that_can_be_invoked_from_cli.console_calculator()
        sum_result, _ = capsys.readouterr()

    assert re.match("Result = 9.0", sum_result)  # nosec B101


def test_difference(capsys: pytest.CaptureFixture) -> None:
    """Check subtraction of two numbers."""
    with unittest.mock.patch("sys.argv", ["prog", "8", "-", "7"]):
        module_that_can_be_invoked_from_cli.console_calculator()
        difference_result, _ = capsys.readouterr()

    assert re.match("Result = 1.0", difference_result)  # nosec B101


def test_product(capsys: pytest.CaptureFixture) -> None:
    """Check multiplication of two numbers."""
    with unittest.mock.patch("sys.argv", ["prog", "2", "*", "3"]):
        module_that_can_be_invoked_from_cli.console_calculator()
        product_result, _ = capsys.readouterr()

    assert re.match("Result = 6.0", product_result)  # nosec B101


def test_quotient(capsys: pytest.CaptureFixture) -> None:
    """Check division of two numbers."""
    with unittest.mock.patch("sys.argv", ["prog", "0", "/", "10"]):
        module_that_can_be_invoked_from_cli.console_calculator()
        quotient_result, _ = capsys.readouterr()

    assert re.match("Result = 0.0", quotient_result)  # nosec B101
