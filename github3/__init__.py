"""
github3
=======

:copyright: (c) 2012 by Ian Cordasco
:license: Modified BSD, see LICENSE for more details

"""

__title__ = 'github3'
__author__ = 'Ian Cordasco'
__license__ = 'Modified BSD'
__copyright__ = 'Copyright 2012 Ian Cordasco'
__version__ = '0.1a'

from .api import login, gist, gists, create_gist
from .github import GitHub
