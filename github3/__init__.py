# -*- coding: utf-8 -*-
"""
github3
=======

See http://github3py.rtfd.org/ for documentation.

:copyright: (c) 2012-2014 by Ian Cordasco
:license: Modified BSD, see LICENSE for more details

"""

__title__ = 'github3'
__author__ = 'Ian Cordasco'
__license__ = 'Modified BSD'
__copyright__ = 'Copyright 2012-2014 Ian Cordasco'
__version__ = '0.9.6'
__version_info__ = tuple(int(i) for i in __version__.split('.'))

from .api import *
from .github import GitHub, GitHubEnterprise, GitHubStatus
from .models import GitHubError

# flake8: noqa
