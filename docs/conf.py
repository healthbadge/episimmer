# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

import datetime
# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import os.path as osp
import sys

sys.path.insert(0, os.path.abspath('..'))
import episimmer

# Read version from file
version_file = os.path.join('..', 'episimmer', 'version.txt')

with open(version_file) as f:
    __version__ = f.read().strip()

# -- Project information -----------------------------------------------------

project = 'episimmer'
author = 'HealthBadge'
copyright = f'{datetime.datetime.now().year}, {author}'

version = __version__
release = __version__

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.autodoc', 'sphinx.ext.autosummary', 'sphinx.ext.intersphinx',
    'sphinx.ext.mathjax', 'sphinx.ext.napoleon', 'sphinx.ext.viewcode',
    'sphinx.ext.githubpages', 'sphinx.ext.coverage',
    'sphinx.ext.autosectionlabel', 'myst_parser'
]

# Examples
examples = {}
sub_examples_list = [
    s for s in os.listdir('../examples')
    if osp.isdir(osp.join('../examples', s))
]
for j in sorted(sub_examples_list):
    examples[j] = {}
    examples[j]['read_me_path'] = osp.join('../../examples', j, 'README.md')
    examples_list = [
        p for p in os.listdir(osp.join('../examples', j))
        if osp.isdir(osp.join('../examples', j, p))
        and osp.isfile(osp.join('../examples', j, p, 'config.txt'))
    ]
    for i, example in enumerate(sorted(examples_list)):
        example_path = osp.join('../examples', j, example)
        examples[j][example] = {}
        for k in sorted(os.listdir(example_path)):
            if osp.isfile(osp.join(example_path, k)):
                if k == 'README.md':
                    examples[j][example]['read_me_path'] = osp.join(
                        '../', example_path, k)
                else:
                    examples[j][example][k] = {}
                    examples[j][example][k]['name'] = k
                    line_count = sum(1 for _ in open(\
                                        osp.join(example_path, k)))
                    examples[j][example][k][
                        'line_count'] = line_count if line_count < 200 else 200
                    examples[j][example][k]['path'] = osp.join(
                        '../', example_path, k)

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'sphinx_rtd_theme'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']
add_module_names = False
autodoc_member_order = 'bysource'
autodoc_typehints = 'description'
# suppress_warnings = ['autosectionlabel.*']
# autosectionlabel_maxdepth = 1

rst_context = {'episimmer': episimmer, 'examples': examples}


def setup(app):

    def skip(app, what, name, obj, skip, options):
        members = [
            '__init__',
            '__repr__',
            '__weakref__',
            '__dict__',
            '__module__',
        ]
        return True if name in members else skip

    def rst_jinja_render(app, docname, source):
        src = source[0]
        rendered = app.builder.templates.render_string(src, rst_context)
        source[0] = rendered

    app.connect('autodoc-skip-member', skip)
    app.connect('source-read', rst_jinja_render)
