import enum

import pydantic

__all__ = ["CustomFloatEnum", "CustomPydanticBaseModel", "CustomStrEnum"]

class CustomFloatEnum(float, enum.Enum): ...
class CustomStrEnum(str, enum.Enum): ...

class CustomPydanticBaseModel(pydantic.BaseModel):
    model_config: dict
