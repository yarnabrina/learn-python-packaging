"""Define package contents."""
import importlib.resources
import json

import pydantic


class PackageMetadata(pydantic.BaseModel):
    """Define keys and types of corresponding values for package metadata.

    Attributes
    ----------
    Name : str
        name of the package
    Version : str
        version of the package
    Description : str
        description of the package
    Keywords : list[str]
        keywords associated with the package
    License : str
        license of the package
    Maintainers : list[str]
        maintainers of the package
    Authors : list[str]
        authors of the package
    Links : dict[str, pydantic.HttpUrl]
        links associated with the package
    """

    Name: str = pydantic.Field(description="name of the package")
    Version: str = pydantic.Field(description="version of the package")
    Description: str = pydantic.Field(description="description of the package")
    Keywords: list[str] = pydantic.Field(description="keywords associated with the package")
    License: str = pydantic.Field(description="license of the package")
    Maintainers: list[str] = pydantic.Field(description="maintainers of the package")
    Authors: list[str] = pydantic.Field(description="authors of the package")
    Links: dict[str, pydantic.HttpUrl] = pydantic.Field(
        description="links associated with the package"
    )


METADATA_CONTENTS: str = (
    importlib.resources.files("package_name_to_import_with").joinpath("metadata.json").read_text()
)
METADATA = PackageMetadata(**json.loads(METADATA_CONTENTS))
