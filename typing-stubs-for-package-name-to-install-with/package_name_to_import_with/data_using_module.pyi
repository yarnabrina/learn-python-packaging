import pydantic

from .utils import CustomPydanticBaseModel

class PackageMetadata(CustomPydanticBaseModel):
    Name: str
    Version: str
    Description: str
    Keywords: list[str]
    License: str
    Maintainers: list[str]
    Authors: list[str]
    Links: dict[str, pydantic.HttpUrl]

METADATA_CONTENTS: str
METADATA: PackageMetadata
