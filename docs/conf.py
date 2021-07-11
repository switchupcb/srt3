import sys
import os

# srt.py is in the /srt directory
sys.path.insert(0, os.path.abspath("../"))

# Project Information
project = "srt3"
version = "1.0.0"
release = version
copyright = "SwitchUpCB"

# General Configuration
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.doctest",
    "sphinx.ext.intersphinx",
]

intersphinx_mapping = {"python": ("https://docs.python.org/3.8", None)}
autosummary_generate = True  # Turn on sphinx.ext.autosummary
html_show_sourcelink = False  # Remove 'Page source' (html)
add_module_names = False  # Remove namespaces.

# Exclusions
exclude_patterns = ["_build"]


def exclude_cli_methods(app, what, name, obj, skip, options):
    return "main" == name or "set_args" == name or name.startswith("_")


def setup(app):
    app.connect("autodoc-skip-member", exclude_cli_methods)


# Theme
html_theme = "sphinx_rtd_theme"
pygments_style = "sphinx"

# Options
root_doc = "index"
source_suffix = ".rst"
htmlhelp_basename = "srtdoc"
templates_path = ["_templates"]
html_static_path = ["_static"]
