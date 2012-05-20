"""
github3.api
===========

:copyright: (c) 2012 by SigmaVirus24
:license: Modified BSD, see LICENSE for more details

"""

from .github import GitHub


def login(username, password):
    """Constructs and returns a GitHub session with the username and
    password"""
    gh = GitHub()
    gh.login(username, password)
    return gh


def gist(id_num):
    gh = GitHub()
    return gh.gist(id_num)


def gists(username=None):
    gh = GitHub()
    return gh.gists(username)


def create_gist(description, files):
    """Creates an anonymous public gist.

    :param description: short description of the gist
    :param files: dictionary containing file names with associated
    dictionaries for content, e.g.
      {'spam.txt': {'content': 'File contents ...'}}
    """
    gh = GitHub()
    return gh.create_gist(description, files)
