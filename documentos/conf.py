# Configuration file for the Sphinx documentation builder.
import os
import sys

# Adiciona o caminho da raiz do projeto (ajuste se necessário)
sys.path.insert(0, os.path.abspath('../../'))

# -- Informações do projeto --------------------------------------------------
project = 'Nome do projeto'
copyright = '2025, Kaio Figueira'
author = 'Kaio Figueira'
release = '0.0.0.1'

# -- Configuração geral ------------------------------------------------------
extensions = [
    "myst_parser",
    "sphinx.ext.autodoc",
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

source_suffix = {
    ".rst": "restructuredtext",
    ".md": "markdown"
}

templates_path = ['_templates']
exclude_patterns = [
    "_build",
    "Thumbs.db",
    ".DS_Store",
    ".venv",
]

language = 'pt-BR'

# -- Saída HTML --------------------------------------------------------------
html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
