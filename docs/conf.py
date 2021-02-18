"""Sphinx configuration."""
import datetime

extensions = ["sphinx.ext.autodoc"]

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# The master toctree document.
master_doc = "index"

# General information about the project.
project = "github4.py"
author = "Thiago Carvalho D'Ávila"
copyright = f"{datetime.datetime.now().year}, {author}"

exclude_patterns = ["_build"]
html_theme = "sphinx_rtd_theme"

# Output file base name for HTML help builder.
htmlhelp_basename = "github4.pydoc"
