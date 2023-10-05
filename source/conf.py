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
html_logo = "/img/cover.png"


# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
#html_static_path = ['_static']

exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']


# -- Options for LaTeX output --------------------------------------------------
preamble = r'''\usepackage{fixltx2e} % LaTeX patches, \textsubscript
\usepackage{cmap} % fix search and cut-and-paste in Acrobat
\usepackage[raccourcis]{fast-diagram}
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
\setcounter{secnumdepth}{3}
'''
latex_elements = {
    # The paper size ('letterpaper' or 'a4paper').
    'papersize': 'a4paper',

    # The font size ('10pt', '11pt' or '12pt').
    'pointsize': '12pt',

    # Babel for french
    'babel': '\\usepackage[french]{babel}',

    # Additional stuff for the LaTeX preamble.
    'preamble': preamble,

    # No default title
    'maketitle': '',

    # No default toc
    'tableofcontents': '',
}

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title, author, documentclass [howto/manual]).
#latex_documents = [
#  ('rapport', 'Rapport.tex', 'Rapport de stage 2A',
#   'Julien Enselme', 'manual'),
#]

# The name of an image file (relative to this directory) to place at the top of
# the title page.
latex_logo = '/img/cover.png'

# For "manual" documents, if this is true, then toplevel headings are parts,
# not chapters.
#latex_use_parts = False

# If true, show page references after internal links.
#latex_show_pagerefs = False

# If true, show URL addresses after external links.
#latex_show_urls = False

# Documents to append as an appendix to all manuals.
latex_appendices = []

# Additionnal files
#latex_additional_files = ['title_page_images/ecm.png']

# If false, no module index is generated.
#latex_domain_indices = True


# -- Options for manual page output --------------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
#man_pages = [
#    ('rapport.rst', 'rapport', 'Rapport Documentation',
#     ['Julien Enselme'], 1)
#]

# If true, show URL addresses after external links.
#man_show_urls = False


# -- Options for Texinfo output ------------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
#texinfo_documents = [
#  ('rapport.rst', 'Rapport', 'Rapport Documentation',
#   'Julien Enselme', 'Rapport', 'One line description of project.',
#   'Miscellaneous'),
#]

# Documents to append as an appendix to all manuals.
#texinfo_appendices = []

# If false, no module index is generated.
#texinfo_domain_indices = True

# How to display URL addresses: 'footnote', 'no', or 'inline'.
#texinfo_show_urls = 'footnote'




