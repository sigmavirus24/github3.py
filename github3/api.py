"""
github3.api
===========

:copyright: (c) 2012 by SigmaVirus24
:license: Modified BSD, see LICENSE for more details

"""

from .github import GitHub

gh = GitHub()


def authorize(login, password, scopes, note='', note_url=''):
    """See :func:`authorize <github3.github.GitHub.authorize>`"""
    return gh.authorize(login, password, scopes, note, note_url)


def login(username, password, token=None):
    """Constructs and returns a GitHub session with the username and
    password, or token

    :param username: login name
    :type username: str
    :param password: password for the login
    :type password: str
    :param token: (optional), OAuth token
    :type token: str
    :returns: :class:`GitHub <github3.github.GitHub>`
    """
    g = GitHub()
    g.login(username, password, token)
    return g


def gist(id_num):
    """Get the gist identified by ``id_num``.

    :param id_num: (required), unique id of the gist
    :type id_num: int
    :returns: :class:`Gist <github3.gist.Gist>`
    """
    return gh.gist(id_num)


def list_gists(username=None):
    """Get public gists or gists for the provided username.

    :param username: (optional), if provided, get the gists for this user
        instead of the authenticated user.
    :type username: str
    :returns: list of :class:`Gist <github3.gist.Gist>`\ s
    """
    return gh.list_gists(username)


def list_followers(username):
    """List the followers of ``username``.

    :param username: (required), login of the person to list the followers of
    :type username: str
    """
    return gh.list_followers(username) if username else []


def list_following(username):
    """List the people ``username`` follows.

    :param username: (required), login of the user
    :type username: str
    """
    return gh.list_following(username) if username else []


def list_issues(owner, repository, filter='', state='', labels='', sort='',
        direction='', since=''):
    """See :func:`github3.github.GitHub.list_issues`"""
    issues = []
    if owner and repository:
        issues = gh.list_issues(owner, repository, filter, state, labels,
                sort, direction, since)
    return issues


def list_orgs(username):
    """List the organizations associated with ``username``.

    :param username: (required), login of the user
    :type username: str
    """
    return gh.list_orgs(username) if username else []


def list_repos(login, type='', sort='', direction=''):
    """See :func:`github3.github.GitHub.list_repos`"""
    return gh.list_repos(login, type, sort, direction) if login else []


def create_gist(description, files):
    """Creates an anonymous public gist.

    :param description: (required), short description of the gist
    :type description: str
    :param files: (required), file names with associated
        dictionaries for content, e.g.
        {'spam.txt': {'content': 'File contents ...'}}
    :type files: dict
    :returns: :class:`Gist <github3.gist.Gist>`
    """
    return gh.create_gist(description, files)


def issue(owner, repository, number):
    """Anonymously gets issue :number on :owner/:repository.

    :param owner: (required), repository owner
    :type owner: str
    :param repository: (required), repository name
    :type repository: str
    :param number: (required), issue number
    :type number: int
    :returns: :class:`Issue <github3.issue.Issue>`
    """
    return gh.issue(owner, repository, number)


def list_events():
    """List all recent public events from GitHub.

    :returns: list of :class:`Event <github3.event.Event>`\ s
    """
    return gh.list_events()


def markdown(text, mode='', context='', raw=False):
    """Render an arbitrary markdown document.

    :param text: (required), the text of the document to render
    :type text: str
    :param mode: (optional), 'markdown' or 'gfm'
    :type mode: str
    :param context: (optional), only important when using mode 'gfm',
        this is the repository to use as the context for the rendering
    :type context: str
    :param raw: (optional), renders a document like a README.md, no gfm, no
        context
    :type raw: bool
    :returns: str -- HTML formatted text
    """
    return gh.markdown(text, mode, context, raw)


def organization(login):
    """See :func:`organization <github3.github.GitHub.organization>`."""
    return gh.organization(login)


def repository(owner, repository):
    """See :func:`repository <github3.github.GitHub.repository>`."""
    return gh.repository(owner, repository)


def search_issues(owner, repo, state, keyword):
    """Find issues by state and keyword.

    :param owner: (required)
    :type owner: str
    :param repo: (required)
    :type repo: str
    :param state: (required), accepted values: ('open', 'closed')
    :type state: str
    :param keyword: (required), what to search for
    :type keyword: str
    :returns: list of :class:`LegacyIssue <github3.legacy.LegacyIssue>`\ s
    """
    return gh.search_issues(owner, repo, state, keyword)


def search_repos(keyword, **params):
    """Search all repositories by keyword.

    :param keyword: (required)
    :type keyword: str
    :param params: (optional), filter by language and/or start_page
    :type params: dict
    :returns: list of :class:`LegacyRepo <github3.legacy.LegacyRepo>`\ s
    """
    return gh.search_repos(keyword, **params)


def search_users(keyword):
    """Search all users by keyword.

    :param keyword: (required)
    :type keyword: str
    :returns: list of :class:`LegacyUser <github3.legacy.LegacyUser>`\ s
    """
    return gh.search_users(keyword)


def search_email(email):
    """Search users by email.

    :param email: (required)
    :type keyword: str
    :returns: :class:`LegacyUser <github3.legacy.LegacyUser>`
    """
    return gh.search_email(email)


def user(login):
    """See :func:`user <github3.github.GitHub.user>`."""
    return gh.user(login)


def ratelimit_remaining():
    """Get the remaining number of requests allowed."""
    return gh.ratelimit_remaining
