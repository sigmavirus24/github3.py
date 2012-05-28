"""
github3.git
===========

This module contains all the classes relating to Git Data.

"""

from json import dumps

class Commit(object):
    def __init__(self, commit):
        super(Commit, self).__init__()
        self._sha = commit.get('sha')
        self._api_url = commit.get('url')
