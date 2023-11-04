"""Evaluate simplification expressions."""
import collections.abc
import enum
import re
import string
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

    POSITIVE_NUMBER = "positive_number"
    NEGATIVE_NUMBER = "negative_number"
    OPERATOR = "operator"
    PARENTHESIS = "parenthesis"


SUPPORTED_CHARACTERS = set.union(
    set(string.digits + "."), set(ArithmeticOperator), set(Parentheses)
)
ACCEPTABLE_CHARACTERS = set(" ")

REGULAR_EXPRESSION_PATTERNS = {
    TokenType.POSITIVE_NUMBER: r"\d+(?:\.\d+)?",
    TokenType.NEGATIVE_NUMBER: rf"(?<![\d|{Parentheses.RIGHT.value}])-\d+(?:\.\d+)?",
    TokenType.OPERATOR: (
        "[" + "".join(rf"\{operator.value}" for operator in ArithmeticOperator) + "]"
    ),
    TokenType.PARENTHESIS: (
        "[" + "".join(rf"\{parenthesis.value}" for parenthesis in Parentheses) + "]"
    ),
}
SUPPORTED_TOKEN_PATTERN = "|".join(
    f"(?P<{token_type.value}>{token_pattern})"
    for token_type, token_pattern in REGULAR_EXPRESSION_PATTERNS.items()
)

OPERATION_PRECEDENCES: dict[ArithmeticOperator | Parentheses, int] = {
    Parentheses.LEFT: 0,
    Parentheses.RIGHT: 0,
    ArithmeticOperator.ADDITION: 1,
    ArithmeticOperator.SUBTRACTION: 1,
    ArithmeticOperator.MULTIPLICATION: 2,
    ArithmeticOperator.DIVISION: 2,
}


@pydantic.validate_call(validate_return=True)
def clean_and_tokenise_expression(
    raw_expression: str,
) -> pydantic.InstanceOf[collections.abc.Iterator[re.Match[str]]]:
    """Extract tokens from arithmetic expression after pre-processing.

    Parameters
    ----------
    raw_expression : str
        infix expression

    Returns
    -------
    collections.abc.Iterator[re.Match[str]]
        tokens in standard arithmetic expression

    Raises
    ------
    ValueError
        if unsupported characters are passed
    """
    clean_expression = raw_expression.translate(
        str.maketrans(dict.fromkeys(ACCEPTABLE_CHARACTERS, None))
    )

    if unsupported_characters := set(clean_expression).difference(SUPPORTED_CHARACTERS):
        raise ValueError(f"Unexpected characters: {unsupported_characters}")

    tokens = re.finditer(SUPPORTED_TOKEN_PATTERN, clean_expression)

    return tokens


@pydantic.validate_call(validate_return=True)
def convert_infix_expression(  # noqa: C901
    infix_expression_tokens: pydantic.InstanceOf[collections.abc.Iterator[re.Match[str]]],
) -> list[ArithmeticOperator | float]:
    """Convert standard arithmetic expression into reverse Polish notation.

    Parameters
    ----------
    infix_expression_tokens : collections.abc.Iterator[re.Match[str]]
        tokens in standard arithmetic expression

    Returns
    -------
    list[ArithmeticOperator | float]
        postfix arithmetic expression

    Raises
    ------
    ValueError
        if brackets are not matching
    """
    operator_stack: list[ArithmeticOperator | typing.Literal[Parentheses.LEFT]] = []
    output_queue: list[ArithmeticOperator | float] = []
    for token in infix_expression_tokens:
        try:
            token_type, token_value = next(
                (element_type, element_value)
                for element_type, element_value in token.groupdict().items()
                if element_value is not None
            )
        except StopIteration:
            continue

        match token_type:
            case TokenType.POSITIVE_NUMBER | TokenType.NEGATIVE_NUMBER:
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
    raw_infix_tokens = clean_and_tokenise_expression(expression)
    ordered_postfix_tokens = convert_infix_expression(raw_infix_tokens)
    expression_value = evaluate_postfix_expression(ordered_postfix_tokens)

    return expression_value


__all__ = [
    "OPERATION_PRECEDENCES",
    "Parentheses",
    "clean_and_tokenise_expression",
    "convert_infix_expression",
    "evaluate_postfix_expression",
    "solve_simplification",
]
