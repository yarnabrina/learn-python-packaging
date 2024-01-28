"""Define package contents."""

import importlib.resources
import json
import re

import pydantic

from .utils import CustomPydanticBaseModel


class PackageMetadata(CustomPydanticBaseModel):
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

    @pydantic.field_validator("Version")
    @classmethod
    def validate_version(cls: type["PackageMetadata"], version: str) -> str:
        """Validate if specified version adhere to semantic versioning.

        Parameters
        ----------
        version : str
            specified value for version

        Returns
        -------
        str
            unchanged ``version`` if validation passes

        Raises
        ------
        ValueError
            if ``version`` is not a valid semantic version

        Notes
        -----
        #. Only checks for MAJOR.MINOR.PATCH format.

        References
        ----------
        `Semantic Versioning 2.0.0 <https://semver.org/>`_.
        """
        del cls  # unused

        if re.match(r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)$", version) is None:
            raise ValueError(f"Invalid semantic version: {version}")

        return version


METADATA_CONTENTS: str = (
    importlib.resources.files("package_name_to_import_with").joinpath("metadata.json").read_text()
)
METADATA = PackageMetadata(**json.loads(METADATA_CONTENTS))
