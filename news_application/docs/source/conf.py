import os
import sys

sys.path.insert(0, os.path.abspath('../..'))

project = 'News Application'
copyright = '2025, Your Name' 
author = 'Your Name'
release = '1.0'

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
]

templates_path = ['_templates']
exclude_patterns = []

html_theme = 'alabaster'
html_static_path = ['_static']
