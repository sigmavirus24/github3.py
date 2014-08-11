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
__version__ = '0.9.1'
__version_info__ = tuple(int(i) for i in __version__.split('.'))

from github3.api import *
from github3.github import GitHub, GitHubEnterprise, GitHubStatus
from github3.models import GitHubError

# flake8: noqa
