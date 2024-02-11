"""Define helper utilities."""

import enum

import pydantic


class CustomFloatEnum(float, enum.Enum):
    """Inherit `enum.Enum` and modify behaviour of ``__str__``."""

    def __str__(self: "CustomFloatEnum") -> str:
        """Create printable string representation using value instead of name.

        Returns
        -------
        str
            value of the enum member
        """
        return str(self.value)


class CustomStrEnum(str, enum.Enum):
    """Inherit `enum.Enum` and modify behaviour of ``__str__``."""

    def __str__(self: "CustomStrEnum") -> str:
        """Create printable string representation using value instead of name.

        Returns
        -------
        str
            value of the enum member
        """
        return str(self.value)


class CustomPydanticBaseModel(pydantic.BaseModel):
    """Inherit `pydantic.BaseModel` and change behaviour to handle undefined attributes."""

    model_config = pydantic.ConfigDict(extra="forbid")


__all__ = ["CustomFloatEnum", "CustomPydanticBaseModel", "CustomStrEnum"]
