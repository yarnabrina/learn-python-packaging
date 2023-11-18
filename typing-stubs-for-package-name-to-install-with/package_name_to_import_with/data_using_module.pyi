import pydantic

class PackageMetadata(pydantic.BaseModel):
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
