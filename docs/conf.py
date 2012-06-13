import sys, os

sys.path.insert(0, os.path.abspath('..'))
import github3

extensions = ['sphinx.ext.autodoc']

source_suffix = '.rst'

master_doc = 'index'

project = u'github3.py'
copyright = u'2012 - Ian Cordasco'

version = github3.__version__
release = version

exclude_patterns = ['_build']

highlight_lang = 'python'

html_theme = 'default'

htmlhelp_basename = 'github3.pydoc'
