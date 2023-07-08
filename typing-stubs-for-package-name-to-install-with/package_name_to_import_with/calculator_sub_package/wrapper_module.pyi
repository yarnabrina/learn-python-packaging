import enum
import pydantic
import typing
from .operations_module import add_numbers as add_numbers, multiply_numbers as multiply_numbers
from .utility_module import divide_numbers as divide_numbers, subtract_numbers as subtract_numbers

ArithmeticOperation: typing.TypeAlias

class ArithmeticOperator(enum.Enum):
    ADDITION: str
    SUBTRACTION: str
    MULTIPLICATION: str
    DIVISION: str

ARITHMETIC_OPERATIONS: dict[ArithmeticOperator, ArithmeticOperation]

class ArithmeticExpression(pydantic.BaseModel):
    first_number: float
    operator: ArithmeticOperator
    second_number: float
    @property
    def operation(self) -> ArithmeticOperation: ...
    @property
    def result(self) -> float: ...

def calculate_results(first_input: float, operator: ArithmeticOperator, second_input: float) -> float: ...
