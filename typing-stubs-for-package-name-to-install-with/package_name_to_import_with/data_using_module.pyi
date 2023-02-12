import typing

class PackageMetadata(typing.TypedDict):
    Name: str
    Version: str

METADATA_CONTENTS: str
METADATA: PackageMetadata
