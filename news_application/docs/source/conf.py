import os
import sys
import django

sys.path.insert(0, os.path.abspath('../..'))
os.environ['DJANGO_SETTINGS_MODULE'] = 'news_project.settings'
django.setup()

project = 'News Application'
copyright = '2025,Dione Learns' 
author = 'Dione Learns'
release = '1.0'

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
]

templates_path = ['_templates']
exclude_patterns = []

html_theme = 'alabaster'
html_static_path = ['_static']
