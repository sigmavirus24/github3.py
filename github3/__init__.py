"""
github3
=======

:copyright: (c) 2012 by Sigmavirus24
:license: Modified BSD, see LICENSE for more details

"""

__title__ = 'github3'
__author__ = 'sigmavirus24'
__license__ = 'Modified BSD'
__copyright__ = 'Copyright 2012 Sigmavirus24'
__version__ = '0.1 pre-alpha'

from .api import login, gist, gists, create_gist
from .github import GitHub
