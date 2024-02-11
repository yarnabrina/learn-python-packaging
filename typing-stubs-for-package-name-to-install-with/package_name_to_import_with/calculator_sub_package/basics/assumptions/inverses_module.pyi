from ....utils import CustomFloatEnum

__all__ = ["IdentityElements", "InverseElements", "get_negative", "get_reciprocal"]

class IdentityElements(CustomFloatEnum):
    ADDITIVE_IDENTITY: int
    MULTIPLICATIVE_IDENTITY: int

class InverseElements(CustomFloatEnum):
    ADDITIVE_INVERSE: int
    MULTIPLICATIVE_INVERSE: int

def get_negative(input_number: float) -> float: ...
def get_reciprocal(input_number: float) -> float: ...
