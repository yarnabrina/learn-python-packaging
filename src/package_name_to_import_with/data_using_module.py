"""Define package contents."""
import importlib.resources
import json

METADATA_CONTENTS = (
    importlib.resources.files("package_name_to_import_with").joinpath("metadata.json").read_text()
)
METADATA = json.loads(METADATA_CONTENTS)
