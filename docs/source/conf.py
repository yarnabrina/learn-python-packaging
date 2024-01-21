"""Configure Sphinx documentation."""
# pylint: disable=invalid-name
import sys

import package_name_to_import_with

sys.path.insert(0, "../src")

project = "package-name-to-install-with"
version = str(package_name_to_import_with.__version__)
project_copyright = "2022-2024, Anirban Ray, First Maintainer, Second Maintainer"
author = "Anirban Ray, First Author, Second Author"
release = f"v{version}"

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.coverage",
    "sphinx.ext.doctest",
    "sphinx.ext.intersphinx",
    "sphinx.ext.napoleon",
    "sphinx.ext.todo",
    "sphinx.ext.viewcode",
    "sphinx_copybutton",
]

smartquotes = False
today_fmt = "%Y-%m-%d"
highlight_language = "python3"
pygments_style = "friendly"
add_function_parentheses = False
add_module_names = False
trim_doctest_flags = True

html_theme = "furo"
html_theme_options = {
    "top_of_page_button": None,
    "announcement": "<strong>all</strong> page <em>banner</em>",
}
html_title = f"Title of {project}'s Documentation at Release {release}"

html_last_updated_fmt = "%B %d, %Y"
html_use_index = True
html_split_index = False
html_copy_source = False
html_show_sourcelink = False
html_show_sphinx = False
html_output_encoding = "utf-8"

autoclass_content = "class"
autodoc_inherit_docstrings = True
autodoc_member_order = "bysource"
autodoc_typehints = "description"
autodoc_typehints_description_target = "documented"
autodoc_typehints_format = "fully-qualified"

intersphinx_mapping = {"python": ("https://docs.python.org/3", None)}

napoleon_google_docstring = False
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = False
napoleon_use_param = True
napoleon_use_keyword = True
napoleon_use_rtype = True
napoleon_preprocess_types = True

todo_include_todos = True

viewcode_follow_imported_members = True
viewcode_line_numbers = True

copybutton_prompt_text = r">>> |\.\.\. |\$ "
copybutton_prompt_is_regexp = True
copybutton_line_continuation_character = "\\"
