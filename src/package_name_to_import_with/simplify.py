"""Evaluate simplification expressions."""
import enum
import re
import typing

import pydantic

from .calculator_sub_package import ArithmeticOperator, calculate_results


@enum.unique
class Parentheses(str, enum.Enum):
    """Define supported brackets."""

    LEFT = "("
    RIGHT = ")"


@enum.unique
class TokenType(str, enum.Enum):
    """Define supported token types."""

    NUMBER = "number"
    OPERATOR = "operator"
    PARENTHESIS = "parenthesis"


OPERATION_PRECEDENCES: dict[ArithmeticOperator | Parentheses, int] = {
    Parentheses.LEFT: 0,
    Parentheses.RIGHT: 0,
    ArithmeticOperator.ADDITION: 1,
    ArithmeticOperator.SUBTRACTION: 1,
    ArithmeticOperator.MULTIPLICATION: 2,
    ArithmeticOperator.DIVISION: 2,
}


@pydantic.validate_call(validate_return=True)
def parse_infix_expression(infix_expression: str) -> list[ArithmeticOperator | float]:
    """Convert standard arithmetic expression into reverse Polish notation.

    Parameters
    ----------
    infix_expression : str
        standard arithmetoc expression

    Returns
    -------
    list[ArithmeticOperator | float]
        postfix arithmetic expression

    Raises
    ------
    ValueError
        if brackets are not matching
    """
    number_pattern = r"\d+(?:\.\d+)?"
    operator_pattern = (
        "[" + "".join(rf"\{operator.value}" for operator in ArithmeticOperator) + "]"
    )
    parenthesis_pattern = (
        "[" + "".join(rf"\{parenthesis.value}" for parenthesis in Parentheses) + "]"
    )

    token_pattern = "|".join(
        (
            f"(?P<{TokenType.NUMBER}>{number_pattern})",
            f"(?P<{TokenType.OPERATOR}>{operator_pattern})",
            f"(?P<{TokenType.PARENTHESIS}>{parenthesis_pattern})",
        )
    )

    tokens = re.finditer(token_pattern, infix_expression)

    operator_stack: list[ArithmeticOperator | typing.Literal[Parentheses.LEFT]] = []
    output_queue: list[ArithmeticOperator | float] = []
    for token in tokens:
        token_type, token_value = next(
            (element_type, element_value)
            for element_type, element_value in token.groupdict().items()
            if element_value is not None
        )

        match token_type:
            case TokenType.NUMBER:
                valid_number = float(token_value)

                output_queue.append(valid_number)
            case TokenType.OPERATOR:
                valid_operator = ArithmeticOperator(token_value)

                while (
                    operator_stack
                    and (last_operator := operator_stack[-1]) != Parentheses.LEFT
                    and OPERATION_PRECEDENCES[last_operator]
                    >= OPERATION_PRECEDENCES[valid_operator]
                ):
                    _ = operator_stack.pop()
                    output_queue.append(last_operator)

                operator_stack.append(valid_operator)
            case TokenType.PARENTHESIS:
                valid_parenthesis = Parentheses(token_value)

                match valid_parenthesis:
                    case Parentheses.LEFT:
                        operator_stack.append(valid_parenthesis)
                    case Parentheses.RIGHT:
                        while (
                            operator_stack
                            and (last_operator := operator_stack[-1]) != Parentheses.LEFT
                        ):
                            if not operator_stack:
                                raise ValueError("Mismatched parentheses")

                            _ = operator_stack.pop()
                            output_queue.append(last_operator)

                        if (last_operator := operator_stack[-1]) != Parentheses.LEFT:
                            raise ValueError("Mismatched parentheses")

                        _ = operator_stack.pop()

    while operator_stack:
        if (last_operator := operator_stack[-1]) == Parentheses.LEFT:
            raise ValueError("Mismatched parentheses")

        _ = operator_stack.pop()
        output_queue.append(last_operator)

    return output_queue


@pydantic.validate_call(validate_return=True)
def evaluate_postfix_expression(postfix_expression: list[ArithmeticOperator | float]) -> float:
    """Evaluate postfix arithmetic expression in reverse Polish notation.

    Parameters
    ----------
    postfix_expression : list[ArithmeticOperator | float]
        elements of arithmetic expression in postfix format

    Returns
    -------
    float
        result of arithmetic expression
    """
    stack: list[float] = []
    for element in postfix_expression:
        if isinstance(element, float | int):
            stack.append(element)
        else:
            operator = ArithmeticOperator(element)

            second_input = stack.pop()
            first_input = stack.pop()

            result = calculate_results(first_input, operator, second_input)
            stack.append(result)

    return stack.pop()


@pydantic.validate_call(validate_return=True)
def solve_simplification(expression: str) -> float:
    """Evaluate arithmetic expression.

    Parameters
    ----------
    expression : str
        standard arithmetic expression

    Returns
    -------
    float
        result of arithmetic expression

    Examples
    --------
    .. code-block:: pycon

        >>> from package_name_to_import_with import solve_simplification
        >>> solve_simplification("0 + 1 - 2 * 3 / 4")
        -0.5
        >>> solve_simplification("5 * 6 / (7 + 8) - 9")
        -7.0
    """
    contents = parse_infix_expression(expression)
    solution = evaluate_postfix_expression(contents)

    return solution


__all__ = [
    "OPERATION_PRECEDENCES",
    "Parentheses",
    "evaluate_postfix_expression",
    "parse_infix_expression",
    "solve_simplification",
]
