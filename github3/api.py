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


def login(username=None, password=None, token=None):
    """Constructs and returns a GitHub session with the username and
    password, or token

    :param str username: login name
    :param str password: password for the login
    :param str token: OAuth token
    :returns: :class:`GitHub <github3.github.GitHub>`
    """
    g = None
    if (username and password) or token:
        g = GitHub()
        g.login(username, password, token)
    return g


def gist(id_num):
    """Get the gist identified by ``id_num``.

    :param int id_num: (required), unique id of the gist
    :returns: :class:`Gist <github3.gists.Gist>`
    """
    return gh.gist(id_num)


def list_gists(username=None):
    """Get public gists or gists for the provided username.

    :param str username: (optional), if provided, get the gists for this user
        instead of the authenticated user.
    :returns: list of :class:`Gist <github3.gists.Gist>`\ s
    """
    return gh.list_gists(username)


def list_followers(username):
    """List the followers of ``username``.

    :param str username: (required), login of the person to list the followers
        of
    """
    return gh.list_followers(username) if username else []


def list_following(username):
    """List the people ``username`` follows.

    :param str username: (required), login of the user
    """
    return gh.list_following(username) if username else []


def list_repo_issues(owner, repository, filter='', state='', labels='',
        sort='', direction='', since=''):
    """See :func:`github3.github.GitHub.list_issues`"""
    issues = []
    if owner and repository:
        issues = gh.list_repo_issues(owner, repository, filter, state, labels,
                sort, direction, since)
    return issues


def list_orgs(username):
    """List the organizations associated with ``username``.

    :param str username: (required), login of the user
    """
    return gh.list_orgs(username) if username else []


def list_repos(login, type='', sort='', direction=''):
    """See :func:`github3.github.GitHub.list_repos`"""
    return gh.list_repos(login, type, sort, direction) if login else []


def create_gist(description, files):
    """Creates an anonymous public gist.

    :param str description: (required), short description of the gist
    :param dict files: (required), file names with associated
        dictionaries for content, e.g.
        {'spam.txt': {'content': 'File contents ...'}}
    :returns: :class:`Gist <github3.gists.Gist>`
    """
    return gh.create_gist(description, files)  # (No coverage)


def issue(owner, repository, number):
    """Anonymously gets issue :number on :owner/:repository.

    :param str owner: (required), repository owner
    :param str repository: (required), repository name
    :param int number: (required), issue number
    :returns: :class:`Issue <github3.issues.Issue>`
    """
    return gh.issue(owner, repository, number)


def list_events():
    """List all recent public events from GitHub.

    :returns: list of :class:`Event <github3.events.Event>`\ s
    """
    return gh.list_events()


def markdown(text, mode='', context='', raw=False):
    """Render an arbitrary markdown document.

    :param str text: (required), the text of the document to render
    :param str mode: (optional), 'markdown' or 'gfm'
    :param str context: (optional), only important when using mode 'gfm',
        this is the repository to use as the context for the rendering
    :param bool raw: (optional), renders a document like a README.md, no gfm,
        no context
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

    :param str owner: (required)
    :param str repo: (required)
    :param str state: (required), accepted values: ('open', 'closed')
    :param str keyword: (required), what to search for
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

    :param str keyword: (required)
    :returns: list of :class:`LegacyUser <github3.legacy.LegacyUser>`\ s
    """
    return gh.search_users(keyword)


def search_email(email):
    """Search users by email.

    :param str email: (required)
    :returns: :class:`LegacyUser <github3.legacy.LegacyUser>`
    """
    return gh.search_email(email)


def user(login):
    """See :func:`user <github3.github.GitHub.user>`."""
    return gh.user(login)


def ratelimit_remaining():
    """Get the remaining number of requests allowed."""
    return gh.ratelimit_remaining
