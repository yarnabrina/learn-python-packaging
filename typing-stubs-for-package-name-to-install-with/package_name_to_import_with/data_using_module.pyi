import pydantic
from _typeshed import Incomplete

class PackageMetadata(pydantic.BaseModel):
    Name: str
    Version: str

METADATA_CONTENTS: str
METADATA: Incomplete
