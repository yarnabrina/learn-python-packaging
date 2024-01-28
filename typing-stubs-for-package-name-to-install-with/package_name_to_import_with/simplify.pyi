import collections.abc
import re

import pydantic

from .calculator_sub_package import BinaryArithmeticOperator
from .utils import CustomStrEnum

__all__ = [
    "OPERATION_PRECEDENCES",
    "Parentheses",
    "clean_and_tokenise_expression",
    "convert_infix_expression",
    "evaluate_postfix_expression",
    "solve_simplification",
]

class Parentheses(CustomStrEnum):
    LEFT: str
    RIGHT: str

class TokenType(CustomStrEnum):
    POSITIVE_NUMBER: str
    NEGATIVE_NUMBER: str
    OPERATOR: str
    LEFT_PARENTHESIS: str
    RIGHT_PARENTHESIS: str

OPERATION_PRECEDENCES: dict[BinaryArithmeticOperator | Parentheses, int]

def clean_and_tokenise_expression(
    raw_expression: str,
) -> pydantic.InstanceOf[collections.abc.Iterator[re.Match[str]]]: ...
def convert_infix_expression(
    infix_expression_tokens: pydantic.InstanceOf[collections.abc.Iterator[re.Match[str]]],
) -> list[BinaryArithmeticOperator | float]: ...
def evaluate_postfix_expression(
    postfix_expression: list[BinaryArithmeticOperator | float],
) -> float: ...
def solve_simplification(expression: str) -> float: ...
