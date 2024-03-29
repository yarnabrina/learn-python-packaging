"""Define function for basic binary operations."""

import collections.abc
import enum
import functools
import typing

import pydantic

from ..utils import CustomPydanticBaseModel, CustomStrEnum
from .basics import add_numbers, divide_numbers, multiply_numbers, subtract_numbers

BinaryArithmeticOperation: typing.TypeAlias = collections.abc.Callable[[float, float], float]


@enum.unique
class BinaryArithmeticOperator(CustomStrEnum):
    """Define supported arithmetic operators."""

    ADDITION = "+"
    SUBTRACTION = "-"
    MULTIPLICATION = "*"
    DIVISION = "/"


BINARY_ARITHMETIC_OPERATIONS: dict[BinaryArithmeticOperator, BinaryArithmeticOperation] = {
    BinaryArithmeticOperator.ADDITION: add_numbers,
    BinaryArithmeticOperator.SUBTRACTION: subtract_numbers,
    BinaryArithmeticOperator.MULTIPLICATION: multiply_numbers,
    BinaryArithmeticOperator.DIVISION: divide_numbers,
}


class BinaryArithmeticExpression(CustomPydanticBaseModel):
    """Define binary arithmetic expression.

    Attributes
    ----------
    left_operand : float
        first number of binary arithmetic expression
    binary_operator : BinaryArithmeticOperator
        arithmetic operator of binary arithmetic expression
    right_operand : float
        second number of binary arithmetic expression
    operation : BinaryArithmeticOperation
        function to perform arithmetic operation corresponding to `binary_operator`
    result : float
        result of binary arithmetic expression
    """

    left_operand: float = pydantic.Field(
        description="first number of binary arithmetic expression"
    )
    binary_operator: BinaryArithmeticOperator = pydantic.Field(
        description="arithmetic operator of binary arithmetic expression"
    )
    right_operand: float = pydantic.Field(
        description="second number of binary arithmetic expression"
    )

    @pydantic.model_validator(mode="after")
    def validate_zero_division(self: "BinaryArithmeticExpression") -> "BinaryArithmeticExpression":
        """Validate that division by zero is not attempted.

        Returns
        -------
        BinaryArithmeticExpression
            unchanged instance if validation passes

        Raises
        ------
        ValueError
            if division by zero is attempted
        """
        if self.binary_operator == BinaryArithmeticOperator.DIVISION and not self.right_operand:
            raise ValueError("Division by zero is attempted.")

        return self

    @pydantic.computed_field  # type: ignore[misc] # will allow serialisation
    @property  # will be computed every time it is called
    def operation(self: "BinaryArithmeticExpression") -> BinaryArithmeticOperation:
        """Store implementation of binary arithmetic operation.

        Returns
        -------
        BinaryArithmeticOperation
            implementation of binary arithmetic operation corresponding to `binary_operator`
        """
        return BINARY_ARITHMETIC_OPERATIONS[self.binary_operator]

    @pydantic.computed_field  # type: ignore[misc] # will allow serialisation
    @functools.cached_property  # will be computed just once unless deleted
    def result(self: "BinaryArithmeticExpression") -> float:
        """Store result of binary arithmetic expression.

        Returns
        -------
        float
            result of binary arithmetic expression
        """
        return self.operation(self.left_operand, self.right_operand)


@pydantic.validate_call(validate_return=True)
def calculate_results(
    first_input: float, operator: BinaryArithmeticOperator, second_input: float
) -> float:
    """Perform basic binary arithmetic expressions.

    Parameters
    ----------
    first_input : float
        left operand of binary arithmetic expression
    operator : BinaryArithmeticOperator
        kind of binary arithmetic expression
    second_input : float
        right operand of binary arithmetic expression

    Returns
    -------
    float
        result of binary arithmetic expression

    Examples
    --------
    .. code-block:: pycon

        >>> from package_name_to_import_with import calculate_results
        >>> calculate_results(1, "+", 2)
        3.0
        >>> calculate_results(1, "-", 2)
        -1.0
        >>> calculate_results(1, "*", 2)
        2.0
        >>> calculate_results(1, "/", 2)
        0.5
    """
    arithmetic_expression = BinaryArithmeticExpression(
        left_operand=first_input, binary_operator=operator, right_operand=second_input
    )

    return arithmetic_expression.result


__all__ = [
    "BINARY_ARITHMETIC_OPERATIONS",
    "BinaryArithmeticExpression",
    "BinaryArithmeticOperation",
    "BinaryArithmeticOperator",
    "calculate_results",
]
