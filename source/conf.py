# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys
sys.path.append(os.path.abspath('../'))

# this is to tell reathedocs not to try to document numpy which is external.
#autodoc_mock_imports = ['numpy']

# -- Project information -----------------------------------------------------

project = 'DREAM user manual'
copyright = '2023, nick hall'
author = 'nick hall'

# The full version, including alpha/beta/rc tags
release = '1.0.0'

master_doc = 'index'

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
#extensions = [
#    'sphinx.ext.autodoc'
#]
extensions = [
    'myst_parser','sphinx.ext.autosectionlabel' ,'sphinx_rtd_theme'
]

source_suffix = {
    '.rst': 'restructuredtext',
    '.txt': 'markdown',
    '.md': 'markdown',
}

myst_enable_extensions = ["dollarmath", "amsmath"]
myst_heading_anchors = 3

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
#html_theme = 'classic'
html_theme = 'sphinx_rtd_theme'
html_logo = './img/cover.png'

html_theme_options = {
    'logo_only': False}


# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
#html_static_path = ['_static']

exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']


# -- Options for LaTeX output --------------------------------------------------

preamble = r'''\usepackage{fixltx2e} % LaTeX patches, \textsubscript
\usepackage{cmap} % fix search and cut-and-paste in Acrobat
%\usepackage[raccourcis]{fast-diagram}
\usepackage{titlesec}
\usepackage[a4paper,left=2cm,right=2cm,top=2cm,bottom=2cm]{geometry}
%%% Redifined titleformat
\setlength{\parindent}{0cm}
\setlength{\parskip}{1ex plus 0.5ex minus 0.2ex}
\newcommand{\hsp}{\hspace{20pt}}
\newcommand{\HRule}{\rule{\linewidth}{0.5mm}}
\titleformat{\chapter}[hang]{\Huge\bfseries\sffamily}{\thechapter\hsp}{0pt}{\Huge\bfseries\sffamily}
%%% Custom font
\usepackage{libertine}
%%% Set numeration
%\setcounter{secnumdepth}{3}
'''


latex_elements = {
    'figure_align':'H',
    'passoptionstopackages': r'\PassOptionsToPackage{table}{xcolor}',
    # Additional stuff for the LaTeX preamble.
    'preamble': preamble
}




# The name of an image file (relative to this directory) to place at the top of
# the title page.
latex_logo = './img/cover.png'






