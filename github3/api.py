"""
github3.api
===========

:copyright: (c) 2012 by SigmaVirus24
:license: Modified BSD, see LICENSE for more details

"""

from .github import GitHub


def login(username, password, token=None):
    """Constructs and returns a GitHub session with the username and
    password, or token
    
    :param username: login name
    :type username: str
    :param password: password for the login
    :type password: str
    :param token: (optional), OAuth token
    :type token: str
    :returns: :class:`GitHub <github.GitHub>`
    """
    gh = GitHub()
    gh.login(username, password, token)
    return gh


def gist(id_num):
    """Get the gist identified by ``id_num``.

    :param id_num: (required), unique id of the gist
    :type id_num: int
    :returns: :class:`Gist <gist.Gist>`
    """
    gh = GitHub()
    return gh.gist(id_num)


def list_gists(username=None):
    """Get public gists or gists for the provided username.

    :param username: (optional), if provided, get the gists for this user
        instead of the authenticated user.
    :type username: str
    :returns: list of :class:`Gist <gist.Gist>`\ s
    """
    gh = GitHub()
    return gh.list_gists(username)


def create_gist(description, files):
    """Creates an anonymous public gist.

    :param description: (required), short description of the gist
    :type description: str
    :param files: (required), file names with associated
        dictionaries for content, e.g.
        {'spam.txt': {'content': 'File contents ...'}}
    :type files: dict
    :returns: :class:`Gist <gist.Gist>`
    """
    gh = GitHub()
    return gh.create_gist(description, files)

def issue(owner, repository, number):
    """Anonymously gets issue :number on :owner/:repository.

    :param owner: (required), repository owner
    :type owner: str
    :param repository: (required), repository name
    :type repository: str
    :param number: (required), issue number
    :type number: int
    :returns: :class:`Issue <issue.Issue>`
    """
    gh = GitHub()
    return gh.issue(owner, repository, number)

def list_events():
    """List all recent public events from GitHub.
    
    :returns: list of :class:`Event <event.Event>`\ s
    """
    gh = GitHub()
    return gh.list_events()
