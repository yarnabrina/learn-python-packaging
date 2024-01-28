import enum

import pydantic

__all__ = ["CustomPydanticBaseModel", "CustomStrEnum"]

class CustomStrEnum(str, enum.Enum): ...

class CustomPydanticBaseModel(pydantic.BaseModel):
    model_config: pydantic.ConfigDict
