# Configuration file for the Sphinx documentation builder.
import os
import sys
from pathlib import Path

# --- Caminhos do projeto ---
THIS = Path(__file__).resolve()
DOCS_DIR = THIS.parent           # pasta do conf.py
ROOT = (DOCS_DIR / ".." / "..").resolve()  # ajuste se seu conf.py não estiver em docs/documentos
SRC = ROOT / "src"

# Garante que o Sphinx ache seus módulos em src/
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(SRC))

# --- Info do projeto ---
project = "Nome do projeto"
author = "Kaio Figueira"
copyright = "2025, Kaio Figueira"
release = "0.0.0.1"

# --- Extensões ---
extensions = [
    "myst_parser",
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.napoleon",
    "sphinx_autodoc_typehints",
    "sphinx.ext.doctest",
    "sphinx.ext.todo",
    "sphinx.ext.coverage",
    "sphinx.ext.mathjax",
    "sphinx.ext.ifconfig",
    "sphinx.ext.viewcode",
    "sphinx_copybutton",
]

# MyST (markdown)
source_suffix = {
    ".rst": "restructuredtext",
    ".md": "markdown",
}

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store", ".venv"]
language = "pt-BR"

# --- HTML ---
html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]

# --- Napoleon (Google-style) ---
napoleon_google_docstring = True
napoleon_numpy_docstring = False
napoleon_include_init_with_doc = True
napoleon_use_param = True
napoleon_use_rtype = True
napoleon_use_ivar = True  # renderiza seção "Attributes" bonitinha

# --- Autodoc ---
autodoc_default_options = {
    "members": True,
    "undoc-members": True,
    "inherited-members": True,
    "show-inheritance": True,
    "member-order": "bysource",
}
autodoc_typehints = "description"      # tipos na descrição (mais limpo)
autodoc_class_signature = "mixed"      # mostra params do __init__ na classe
autosummary_generate = True            # gera sumários automáticos

# Opcional: se algo pesado quebra import em build, pode mockar:
# autodoc_mock_imports = ["pyspark", "pandas"]
