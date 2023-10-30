import enum

class IdentityElements(float, enum.Enum):
    ADDITIVE_IDENTITY: int
    MULTIPLICATIVE_IDENTITY: int

class InverseElements(float, enum.Enum):
    ADDITIVE_INVERSE: int
    MULTIPLICATIVE_INVERSE: int

def get_negative(input_number: float) -> float: ...
def get_reciprocal(input_number: float) -> float: ...
