"""
github3.api
===========

:copyright: (c) 2012 by SigmaVirus24
:license: Modified BSD, see LICENSE for more details

"""

from .github import GitHub

gh = GitHub()


def authorize(login, password, scopes, note='', note_url='', client_id='',
              client_secret=''):
    """Obtain an authorization token from the GitHub API for the GitHub
    API.

    :param str login: (required)
    :param str password: (required)
    :param list scopes: (required), areas you want this token to apply to,
        i.e., 'gist', 'user'
    :param str note: (optional), note about the authorization
    :param str note_url: (optional), url for the application
    :param str client_id: (optional), 20 character OAuth client key for which
        to create a token
    :param str client_secret: (optional), 40 character OAuth client secret for
        which to create the token
    :returns: :class:`Authorization <Authorization>`
    """
    return gh.authorize(login, password, scopes, note, note_url, client_id,
                        client_secret)


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


def gitignore_template(language):
    """Returns the template for language.

    :returns: str
    """
    return gh.gitignore_template(language)


def gitignore_templates():
    """Returns the list of available templates.

    :returns: list of template names
    """
    return gh.gitignore_templates()


def iter_all_repos(number=-1):
    """Iterate over every repository in the order they were created.

    :param int number: (optional), number of repositories to return.
        Default: -1, returns all of them
    :returns: generator of :class:`Repository <github3.repos.Repository>`
    """
    return gh.iter_all_repos(number)


def iter_all_users(number=-1):
    """Iterate over every user in the order they signed up for GitHub.

    :param int number: (optional), number of users to return. Default: -1,
        returns all of them
    :returns: generator of :class:`User <github3.users.User>`
    """
    return gh.iter_all_users(number)


def iter_events(number=-1):
    """Iterate over public events.

    :param int number: (optional), number of events to return. Default: -1
        returns all available events
    :returns: generator of :class:`Event <github3.events.Event>`\ s
    """
    return gh.iter_events(number)


def iter_followers(username, number=-1):
    """List the followers of ``username``.

    :param str username: (required), login of the person to list the followers
        of
    :param int number: (optional), number of followers to return, Default: -1,
        return all of them
    :returns: generator of :class:`User <github3.users.User>`
    """
    return gh.iter_followers(username, number) if username else []


def iter_following(username, number=-1):
    """List the people ``username`` follows.

    :param str username: (required), login of the user
    :param int number: (optional), number of users being followed by username
        to return. Default: -1, return all of them
    :returns: generator of :class:`User <github3.users.User>`
    """
    return gh.iter_following(username, number) if username else []


def iter_gists(username=None, number=-1):
    """Get public gists or gists for the provided username.

    :param str username: (optional), if provided, get the gists for this user
        instead of the authenticated user.
    :param int number: (optional), number of gists to return. Default: -1,
        return all of them
    :returns: generator of :class:`Gist <github3.gists.Gist>`\ s
    """
    return gh.iter_gists(username, number)


def iter_repo_issues(owner, repository, filter='', state='', labels='',
                     sort='', direction='', since='', number=-1):
    """List issues on owner/repository. Only owner and repository are
    required.

    :param str owner: login of the owner of the repository
    :param str repository: name of the repository
    :param int milestone: None, '*', or ID of milestone
    :param str state: accepted values: ('open', 'closed')
        api-default: 'open'
    :param str assignee: '*' or login of the user
    :param str mentioned: login of the user
    :param str labels: comma-separated list of label names, e.g.,
        'bug,ui,@high'
    :param str sort: accepted values: ('created', 'updated', 'comments')
        api-default: created
    :param str direction: accepted values: ('asc', 'desc')
        api-default: desc
    :param str since: ISO 8601 formatted timestamp, e.g.,
        2012-05-20T23:10:27Z
    :param int number: (optional), number of issues to return.
        Default: -1 returns all issues
    :returns: generator of :class:`Issue <github3.issues.Issue>`\ s
    """
    if owner and repository:
        return gh.iter_repo_issues(owner, repository, filter, state, labels,
                                   sort, direction, since, number)
    return iter([])


def iter_orgs(username, number=-1):
    """List the organizations associated with ``username``.

    :param str username: (required), login of the user
    :param int number: (optional), number of orgs to return. Default: -1,
        return all of the issues
    """
    return gh.iter_orgs(username, number) if username else []


def iter_repos(login, type='', sort='', direction='', number=-1):
    """List public repositories for the specified ``login`` or all
    repositories for the authenticated user if ``login`` is not
    provided.

    :param str login: (required)
    :param str type: (optional), accepted values:
        ('all', 'owner', 'public', 'private', 'member')
        API default: 'all'
    :param str sort: (optional), accepted values:
        ('created', 'updated', 'pushed', 'full_name')
        API default: 'created'
    :param str direction: (optional), accepted values:
        ('asc', 'desc'), API default: 'asc' when using 'full_name',
        'desc' otherwise
    :param int number: (optional), number of repositories to return.
        Default: -1 returns all repositories
    :returns: generator of :class:`Repository <github3.repos.Repository>`
        objects
    """
    if login:
        return gh.iter_repos(login, type, sort, direction, number)
    return iter([])


def iter_starred(username, number=-1):
    """Iterate over repositories starred by ``username``.

    :param str username: (optional), name of user whose stars you want to see
    :param int number: (optional), number of repositories to return.
        Default: -1 returns all repositories
    :returns: generator of :class:`Repository <github3.repos.Repository>`
    """
    return gh.iter_starred(username, number)


def iter_subscriptions(username, number=-1):
    """Iterate over repositories subscribed to by ``username``.

    :param str username: (optional), name of user whose subscriptions you want
        to see
    :param int number: (optional), number of repositories to return.
        Default: -1 returns all repositories
    :returns: generator of :class:`Repository <github3.repos.Repository>`
    """
    return gh.iter_subscriptions(username, number)


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


def octocat():
    """Returns an easter egg from the API."""
    return gh.octocat()


def organization(login):
    """See :func:`organization <github3.github.GitHub.organization>`."""
    return gh.organization(login)


def pull_request(owner, repository, number):
    """Anonymously retrieve pull request :number on :owner/:repository

    :param str owner: (required), repository owner
    :param str repository: (required), repository name
    :param int number: (required), pull request number
    :returns: :class:`PullRequest <github3.pulls.PullRequest>`
    """
    return gh.pull_request(owner, repository, number)


def repository(owner, repository):
    """See :func:`repository <github3.github.GitHub.repository>`."""
    return gh.repository(owner, repository)


def search_issues(owner, repo, state, keyword):
    """Find issues by state and keyword.

    :param str owner: (required)
    :param str repo: (required)
    :param str state: (required), accepted values: ('open', 'closed')
    :param str keyword: (required), what to search for
    :param int start_page: (optional), page to get (results come 100/page)
    :returns: list of :class:`LegacyIssue <github3.legacy.LegacyIssue>`\ s
    """
    return gh.search_issues(owner, repo, state, keyword)


def search_repos(keyword, **params):
    """Search all repositories by keyword.

    :param str keyword: (required)
    :param str language: (optional), language to filter by
    :param int start_page: (optional), page to get (results come 100/page)
    :returns: list of :class:`LegacyRepo <github3.legacy.LegacyRepo>`\ s
    """
    return gh.search_repos(keyword, **params)


def search_users(keyword):
    """Search all users by keyword.

    :param str keyword: (required)
    :param int start_page: (optional), page to get (results come 100/page)
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
    return gh.ratelimit_remaining()


def zen():
    """Returns a quote from the Zen of GitHub. Yet another API Easter Egg"""
    return gh.zen()
