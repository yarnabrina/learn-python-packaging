import enum

from .calculator_sub_package import ArithmeticOperator


class Parentheses(str, enum.Enum):
    LEFT: str
    RIGHT: str


class TokenType(str, enum.Enum):
    NUMBER: str
    OPERATOR: str
    PARENTHESIS: str


OPERATION_PRECEDENCES: dict[ArithmeticOperator | Parentheses, int]

def parse_infix_expression(infix_expression: str) -> list[ArithmeticOperator | float]: ...
def evaluate_postfix_expression(postfix_expression: list[ArithmeticOperator | float]) -> float: ...
def solve_simplification(expression: str) -> float: ...
