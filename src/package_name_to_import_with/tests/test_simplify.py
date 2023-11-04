"""Define unit tests for simplification problems."""
import math

import pytest

from package_name_to_import_with import solve_simplification


@pytest.mark.parametrize(
    ("expression"),
    [
        "0 + 1",
        "2-3",
        "4.5*6.7 /8.9",
        "11+(12-13)*14/ -15",
        "(-16)* (17.18/(19.20+ 21.22-(23*24))) ",
        "  25.26--27.28  -29.30",
    ],
)
def test_simplification(expression: str) -> None:
    """Check successful evaluation of standard infix expressions.

    Parameters
    ----------
    expression : str
        standard arithmetic expression
    """
    calculated_result = solve_simplification(expression)
    expected_result = eval(  # noqa: PGH001, S307  # pylint: disable=eval-used
        expression, {"__builtins__": {}}
    )

    assert math.isclose(calculated_result, expected_result)


@pytest.mark.parametrize(
    ("expression", "error"),
    [
        ("one + one", "Unexpected characters"),
        ("2 minus 3", "Unexpected characters"),
        ("1+(2*3", "Mismatched left parentheses"),
        ("4 - 5 / 6)", "Mismatched right parentheses"),
    ],
)
def test_simplification_failure(expression: str, error: str) -> None:
    """Check evaluation failures of standard infix expressions.

    Parameters
    ----------
    expression : str
        standard arithmetic expression
    error : str
        expected failure message
    """
    with pytest.raises(ValueError, match=error):
        solve_simplification(expression)
