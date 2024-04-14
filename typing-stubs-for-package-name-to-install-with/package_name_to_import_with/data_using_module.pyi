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
    @classmethod
    def validate_version(cls: PackageMetadata, version: str) -> str: ...

METADATA_CONTENTS: str
METADATA: PackageMetadata
