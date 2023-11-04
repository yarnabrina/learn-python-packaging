import collections.abc
import enum
import re

import pydantic

from .calculator_sub_package import ArithmeticOperator

class Parentheses(str, enum.Enum):
    LEFT: str
    RIGHT: str

class TokenType(str, enum.Enum):
    POSITIVE_NUMBER: str
    NEGATIVE_NUMBER: str
    OPERATOR: str
    PARENTHESIS: str

OPERATION_PRECEDENCES: dict[ArithmeticOperator | Parentheses, int]

def clean_and_tokenise_expression(
    raw_expression: str,
) -> pydantic.InstanceOf[collections.abc.Iterator[re.Match[str]]]: ...
def parse_infix_expression(
    infix_expression_tokens: pydantic.InstanceOf[collections.abc.Iterator[re.Match[str]]],
) -> list[ArithmeticOperator | float]: ...
def evaluate_postfix_expression(postfix_expression: list[ArithmeticOperator | float]) -> float: ...
def solve_simplification(expression: str) -> float: ...
