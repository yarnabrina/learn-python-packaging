"""Define unit tests for version."""

import module_that_can_be_imported_directly
import package_name_to_import_with


def test_package_version() -> None:
    """Check version of package and exposed module."""
    package_version = package_name_to_import_with.__version__
    module_version = module_that_can_be_imported_directly.VERSION

    assert package_version == module_version  # nosec B101
