# -*- coding: utf-8 -*-
"""
github3.api
===========

:copyright: (c) 2012-2014 by Ian Cordasco
:license: Modified BSD, see LICENSE for more details

"""

import warnings
from functools import wraps
from .github import GitHub, GitHubEnterprise

gh = GitHub()


def deprecated(func):
    """Decorator to mark a function as deprecated."""

    @wraps(func)
    def deprecation_wrapper(*args, **kwargs):
        warnings.warn(
            "The anonymous API function `github3.api.{0}` is deprecated. Use "
            "`GitHub.{0}` instead.".format(func.__name__),
            DeprecationWarning,
            stacklevel=2,
        )
        return func(*args, **kwargs)

    return deprecation_wrapper


@deprecated
def authorize(
    username,
    password,
    scopes,
    note="",
    note_url="",
    client_id="",
    client_secret="",
    two_factor_callback=None,
    github=None,
):
    """Obtain an authorization token for the GitHub API.

    .. deprecated:: 1.2.0

        Use :meth:`github3.github.GitHub.authorize` instead.

    :param str username: (required)
    :param str password: (required)
    :param list scopes: (required), areas you want this token to apply to,
        i.e., 'gist', 'user'
    :param str note: (optional), note about the authorization
    :param str note_url: (optional), url for the application
    :param str client_id: (optional), 20 character OAuth client key for which
        to create a token
    :param str client_secret: (optional), 40 character OAuth client secret for
        which to create the token
    :param func two_factor_callback: (optional), function to call when a
        Two-Factor Authentication code needs to be provided by the user.
    :param GitHub github: (optional), GitHub (or GitHubEnterprise) object for
        login.
    :returns: :class:`Authorization <Authorization>`

    """
    gh = github or GitHub()
    gh.login(two_factor_callback=two_factor_callback)
    return gh.authorize(
        username, password, scopes, note, note_url, client_id, client_secret
    )


def login(username=None, password=None, token=None, two_factor_callback=None):
    """Construct and return an authenticated GitHub session.

    .. note::

        To allow you to specify either a username and password combination or
        a token, none of the parameters are required. If you provide none of
        them, you will receive ``None``.

    :param str username: login name
    :param str password: password for the login
    :param str token: OAuth token
    :param func two_factor_callback: (optional), function you implement to
        provide the Two-factor Authentication code to GitHub when necessary
    :returns: :class:`GitHub <github3.github.GitHub>`

    """
    g = None

    if (username and password) or token:
        g = GitHub()
        g.login(username, password, token, two_factor_callback)

    return g


def enterprise_login(
    username=None,
    password=None,
    token=None,
    url=None,
    two_factor_callback=None,
):
    """Construct and return an authenticated GitHubEnterprise session.

    .. note::

        To allow you to specify either a username and password combination or
        a token, none of the parameters are required. If you provide none of
        them, you will receive ``None``.

    :param str username: login name
    :param str password: password for the login
    :param str token: OAuth token
    :param str url: URL of a GitHub Enterprise instance
    :param func two_factor_callback: (optional), function you implement to
        provide the Two-factor Authentication code to GitHub when necessary
    :returns: :class:`GitHubEnterprise <github3.github.GitHubEnterprise>`

    """
    if not url:
        raise ValueError(
            "GitHub Enterprise requires you provide the URL of"
            " the instance"
        )

    g = None

    if (username and password) or token:
        g = GitHubEnterprise(url)
        g.login(username, password, token, two_factor_callback)

    return g


@deprecated
def emojis():
    return gh.emojis()


emojis.__doc__ = gh.emojis.__doc__


@deprecated
def gist(id_num):
    """Retrieve the gist identified by ``id_num``.

    .. deprecated:: 1.2.0

        Use :meth:`github3.github.GitHub.gist` instead.

    :param int id_num: (required), unique id of the gist
    :returns: :class:`Gist <github3.gists.Gist>`

    """
    return gh.gist(id_num)


@deprecated
def gitignore_template(language):
    """Return the template for language.

    .. deprecated:: 1.2.0

        Use :meth:`github3.github.GitHub.gitignore_template` instead.

    :returns: str

    """
    return gh.gitignore_template(language)


@deprecated
def gitignore_templates():
    """Return the list of available templates.

    .. deprecated:: 1.2.0

        Use :meth:`github3.github.GitHub.gitignore_templates` instead.

    :returns: list of template names

    """
    return gh.gitignore_templates()


@deprecated
def all_repositories(number=-1, etag=None):
    """Iterate over every repository in the order they were created.

    .. deprecated:: 1.2.0

        Use :meth:`github3.github.GitHub.all_repositories` instead.

    :param int number: (optional), number of repositories to return.
        Default: -1, returns all of them
    :param str etag: (optional), ETag from a previous request to the same
        endpoint
    :returns: generator of :class:`Repository <github3.repos.Repository>`

    """
    return gh.all_repositories(number, etag)


@deprecated
def all_users(number=-1, etag=None):
    """Iterate over every user in the order they signed up for GitHub.

    .. deprecated:: 1.2.0

        Use :meth:`github3.github.GitHub.all_users` instead.

    :param int number: (optional), number of users to return. Default: -1,
        returns all of them
    :param str etag: (optional), ETag from a previous request to the same
        endpoint
    :returns: generator of :class:`User <github3.users.User>`

    """
    return gh.all_users(number, etag)


@deprecated
def all_events(number=-1, etag=None):
    """Iterate over public events.

    .. deprecated:: 1.2.0

        Use :meth:`github3.github.GitHub.all_events` instead.

    :param int number: (optional), number of events to return. Default: -1
        returns all available events
    :param str etag: (optional), ETag from a previous request to the same
        endpoint
    :returns: generator of :class:`Event <github3.events.Event>`

    """
    return gh.all_events(number, etag)


@deprecated
def followers_of(username, number=-1, etag=None):
    """List the followers of ``username``.

    .. deprecated:: 1.2.0

        Use :meth:`github3.github.GitHub.followers_of` instead.

    :param str username: (required), login of the person to list the followers
        of
    :param int number: (optional), number of followers to return, Default: -1,
        return all of them
    :param str etag: (optional), ETag from a previous request to the same
        endpoint
    :returns: generator of :class:`User <github3.users.User>`

    """
    return gh.followers_of(username, number, etag) if username else []


@deprecated
def followed_by(username, number=-1, etag=None):
    """List the people ``username`` follows.

    .. deprecated:: 1.2.0

        Use :meth:`github3.github.GitHub.followed_by` instead.

    :param str username: (required), login of the user
    :param int number: (optional), number of users being followed by username
        to return. Default: -1, return all of them
    :param str etag: (optional), ETag from a previous request to the same
        endpoint
    :returns: generator of :class:`User <github3.users.User>`

    """
    return gh.followed_by(username, number, etag) if username else []


@deprecated
def public_gists(number=-1, etag=None):
    """Iterate over all public gists.

    .. deprecated:: 1.2.0

        Use :meth:`github3.github.GitHub.public_gists` instead.

    .. versionadded:: 1.0

        This was split from ``github3.iter_gists`` before 1.0.

    :param int number: (optional), number of gists to return. Default: -1,
        return all of them
    :param str etag: (optional), ETag from a previous request to the same
        endpoint
    :returns: generator of :class:`Gist <github3.gists.Gist>`

    """
    return gh.public_gists(number, etag)


@deprecated
def gists_by(username, number=-1, etag=None):
    """Iterate over gists created by the provided username.

    .. deprecated:: 1.2.0

        Use :meth:`github3.github.GitHub.gists_by` instead.

    :param str username: (required), if provided, get the gists for this user
        instead of the authenticated user.
    :param int number: (optional), number of gists to return. Default: -1,
        return all of them
    :param str etag: (optional), ETag from a previous request to the same
        endpoint
    :returns: generator of :class:`Gist <github3.gists.Gist>`

    """
    if username:
        return gh.gists_by(username, number, etag)
    return iter([])


@deprecated
def issues_on(
    owner,
    repository,
    milestone=None,
    state=None,
    assignee=None,
    mentioned=None,
    labels=None,
    sort=None,
    direction=None,
    since=None,
    number=-1,
    etag=None,
):
    r"""Iterate over issues on owner/repository.

    .. deprecated:: 1.2.0

        Use :meth:`github3.github.GitHub.issues_on` instead.

    .. versionchanged:: 0.9.0

        - The ``state`` parameter now accepts 'all' in addition to 'open'
          and 'closed'.

    :param str owner: login of the owner of the repository
    :param str repository: name of the repository
    :param int milestone: None, '*', or ID of milestone
    :param str state: accepted values: ('all', 'open', 'closed')
        api-default: 'open'
    :param str assignee: '*' or login of the user
    :param str mentioned: login of the user
    :param str labels: comma-separated list of label names, e.g.,
        'bug,ui,@high'
    :param str sort: accepted values: ('created', 'updated', 'comments')
        api-default: created
    :param str direction: accepted values: ('asc', 'desc')
        api-default: desc
    :param since: (optional), Only issues after this date will
        be returned. This can be a `datetime` or an ISO8601 formatted
        date string, e.g., 2012-05-20T23:10:27Z
    :type since: datetime or string
    :param int number: (optional), number of issues to return.
        Default: -1 returns all issues
    :param str etag: (optional), ETag from a previous request to the same
        endpoint
    :returns: generator of :class:`ShortIssue <github3.issues.ShortIssue>`\ s

    """
    if owner and repository:
        return gh.issues_on(
            owner,
            repository,
            milestone,
            state,
            assignee,
            mentioned,
            labels,
            sort,
            direction,
            since,
            number,
            etag,
        )
    return iter([])


@deprecated
def organizations_with(username, number=-1, etag=None):
    """List the organizations with ``username`` as a member.

    .. deprecated:: 1.2.0

        Use :meth:`github3.github.GitHub.organizations_with` instead.

    :param str username: (required), login of the user
    :param int number: (optional), number of orgs to return. Default: -1,
        return all of the issues
    :param str etag: (optional), ETag from a previous request to the same
        endpoint
    :returns: generator of
        :class:`ShortOrganization <github3.orgs.ShortOrganization>`

    """
    return gh.organizations_with(username, number, etag)


@deprecated
def repositories_by(
    username, type=None, sort=None, direction=None, number=-1, etag=None
):
    """List public repositories for the specified ``username``.

    .. deprecated:: 1.2.0

        Use :meth:`github3.github.GitHub.organizations_with` instead.

    .. versionadded:: 0.6

    .. note:: This replaces github3.iter_repos

    :param str username: (required)
    :param str type: (optional), accepted values:
        ('all', 'owner', 'member')
        API default: 'all'
    :param str sort: (optional), accepted values:
        ('created', 'updated', 'pushed', 'full_name')
        API default: 'created'
    :param str direction: (optional), accepted values:
        ('asc', 'desc'), API default: 'asc' when using 'full_name',
        'desc' otherwise
    :param int number: (optional), number of repositories to return.
        Default: -1 returns all repositories
    :param str etag: (optional), ETag from a previous request to the same
        endpoint
    :returns: generator of :class:`Repository <github3.repos.Repository>`
        objects

    """
    if login:
        return gh.repositories_by(
            username, type, sort, direction, number, etag
        )
    return iter([])


@deprecated
def starred_by(username, number=-1, etag=None):
    """Iterate over repositories starred by ``username``.

    .. deprecated:: 1.2.0

        Use :meth:`github3.github.GitHub.starred_by` instead.

    :param str username: (optional), name of user whose stars you want to see
    :param int number: (optional), number of repositories to return.
        Default: -1 returns all repositories
    :param str etag: (optional), ETag from a previous request to the same
        endpoint
    :returns: generator of :class:`Repository <github3.repos.Repository>`

    """
    return gh.starred_by(username, number, etag)


@deprecated
def subscriptions_for(username, number=-1, etag=None):
    """Iterate over repositories subscribed to by ``username``.

    .. deprecated:: 1.2.0

        Use :meth:`github3.github.GitHub.subscriptions_for` instead.

    :param str username: name of user whose subscriptions you want to see
    :param int number: (optional), number of repositories to return.
        Default: -1 returns all repositories
    :param str etag: (optional), ETag from a previous request to the same
        endpoint
    :returns: generator of :class:`Repository <github3.repos.Repository>`

    """
    return gh.subscriptions_for(username, number, etag)


@deprecated
def create_gist(description, files):
    """Create an anonymous public gist.

    .. deprecated:: 1.2.0

        Use :meth:`github3.github.GitHub.create_gist` instead.

    :param str description: (required), short description of the gist
    :param dict files: (required), file names with associated
        dictionaries for content, e.g.
        {'spam.txt': {'content': 'File contents ...'}}
    :returns: :class:`Gist <github3.gists.Gist>`

    """
    return gh.create_gist(description, files)  # (No coverage)


@deprecated
def issue(owner, repository, number):
    """Anonymously gets issue :number on :owner/:repository.

    .. deprecated:: 1.2.0

        Use :meth:`github3.github.GitHub.issue` instead.

    :param str owner: (required), repository owner
    :param str repository: (required), repository name
    :param int number: (required), issue number
    :returns: :class:`Issue <github3.issues.Issue>`

    """
    return gh.issue(owner, repository, number)


@deprecated
def markdown(text, mode="", context="", raw=False):
    """Render an arbitrary markdown document.

    .. deprecated:: 1.2.0

        Use :meth:`github3.github.GitHub.markdown` instead.

    :param str text: (required), the text of the document to render
    :param str mode: (optional), 'markdown' or 'gfm'
    :param str context: (optional), only important when using mode 'gfm',
        this is the repository to use as the context for the rendering
    :param bool raw: (optional), renders a document like a README.md, no gfm,
        no context
    :returns: str -- HTML formatted text

    """
    return gh.markdown(text, mode, context, raw)


@deprecated
def octocat(say=None):
    """Return an easter egg from the API.

    .. deprecated:: 1.2.0

        Use :meth:`github3.github.GitHub.octocat` instead.

    :params str say: (optional), pass in what you'd like Octocat to say
    :returns: ascii art of Octocat

    """
    return gh.octocat(say)


@deprecated
def organization(name):
    return gh.organization(name)


organization.__doc__ = gh.organization.__doc__


@deprecated
def pull_request(owner, repository, number):
    """Anonymously retrieve pull request :number on :owner/:repository.

    .. deprecated:: 1.2.0

        Use :meth:`github3.github.GitHub.pull_request` instead.

    :param str owner: (required), repository owner
    :param str repository: (required), repository name
    :param int number: (required), pull request number
    :returns: :class:`PullRequest <github3.pulls.PullRequest>`

    """
    return gh.pull_request(owner, repository, number)


@deprecated
def rate_limit():
    return gh.rate_limit()


rate_limit.__doc__ = gh.rate_limit.__doc__


@deprecated
def repository(owner, repository):
    return gh.repository(owner, repository)


repository.__doc__ = gh.repository.__doc__


@deprecated
def search_code(
    query,
    sort=None,
    order=None,
    per_page=None,
    text_match=False,
    number=-1,
    etag=None,
):
    """Find code via the code search API.

    .. deprecated:: 1.2.0

        Use :meth:`github3.github.GitHub.search_code` instead.

    .. warning::

        You will only be able to make 5 calls with this or other search
        functions. To raise the rate-limit on this set of endpoints, create an
        authenticated :class:`GitHub <github3.github.GitHub>` Session with
        ``login``.

    The query can contain any combination of the following supported
    qualifiers:

    - ``in`` Qualifies which fields are searched. With this qualifier you
      can restrict the search to just the file contents, the file path, or
      both.
    - ``language`` Searches code based on the language it’s written in.
    - ``fork`` Specifies that code from forked repositories should be
      searched.  Repository forks will not be searchable unless the fork
      has more stars than the parent repository.
    - ``size`` Finds files that match a certain size (in bytes).
    - ``path`` Specifies the path that the resulting file must be at.
    - ``extension`` Matches files with a certain extension.
    - ``user`` or ``repo`` Limits searches to a specific user or
      repository.

    For more information about these qualifiers, see: http://git.io/-DvAuA

    :param str query: (required), a valid query as described above, e.g.,
        ``addClass in:file language:js repo:jquery/jquery``
    :param str sort: (optional), how the results should be sorted;
        option(s): ``indexed``; default: best match
    :param str order: (optional), the direction of the sorted results,
        options: ``asc``, ``desc``; default: ``desc``
    :param int per_page: (optional)
    :param bool text_match: (optional), if True, return matching search
        terms. See http://git.io/4ct1eQ for more information
    :param int number: (optional), number of repositories to return.
        Default: -1, returns all available repositories
    :param str etag: (optional), previous ETag header value
    :return: generator of :class:`CodeSearchResult
        <github3.search.CodeSearchResult>`
    """
    return gh.search_code(
        query, sort, order, per_page, text_match, number, etag
    )


@deprecated
def search_issues(
    query,
    sort=None,
    order=None,
    per_page=None,
    text_match=False,
    number=-1,
    etag=None,
):
    """Find issues by state and keyword

    .. deprecated:: 1.2.0

        Use :meth:`github3.github.GitHub.search_issues` instead.

    .. warning::

        You will only be able to make 5 calls with this or other search
        functions. To raise the rate-limit on this set of endpoints, create an
        authenticated :class:`GitHub <github3.github.GitHub>` Session with
        ``login``.

    The query can contain any combination of the following supported
    qualifers:

    - ``type`` With this qualifier you can restrict the search to issues or
      pull request only.
    - ``in`` Qualifies which fields are searched. With this qualifier you can
      restrict the search to just the title, body, comments, or any
      combination of these.
    - ``author`` Finds issues created by a certain user.
    - ``assignee`` Finds issues that are assigned to a certain user.
    - ``mentions`` Finds issues that mention a certain user.
    - ``commenter`` Finds issues that a certain user commented on.
    - ``involves`` Finds issues that were either created by a certain user,
      assigned to that user, mention that user, or were commented on by that
      user.
    - ``state`` Filter issues based on whether they’re open or closed.
    - ``labels`` Filters issues based on their labels.
    - ``language`` Searches for issues within repositories that match a
      certain language.
    - ``created`` or ``updated`` Filters issues based on times of creation, or
      when they were last updated.
    - ``comments`` Filters issues based on the quantity of comments.
    - ``user`` or ``repo`` Limits searches to a specific user or repository.

    For more information about these qualifiers, see: http://git.io/d1oELA

    :param str query: (required), a valid query as described above, e.g.,
        ``windows label:bug``
    :param str sort: (optional), how the results should be sorted;
        options: ``created``, ``comments``, ``updated``; default: best match
    :param str order: (optional), the direction of the sorted results,
        options: ``asc``, ``desc``; default: ``desc``
    :param int per_page: (optional)
    :param bool text_match: (optional), if True, return matching search
        terms. See http://git.io/QLQuSQ for more information
    :param int number: (optional), number of issues to return.
        Default: -1, returns all available issues
    :param str etag: (optional), previous ETag header value
    :return: generator of :class:`IssueSearchResult
        <github3.search.IssueSearchResult>`
    """
    return gh.search_issues(
        query, sort, order, per_page, text_match, number, etag
    )


@deprecated
def search_repositories(
    query,
    sort=None,
    order=None,
    per_page=None,
    text_match=False,
    number=-1,
    etag=None,
):
    """Find repositories via various criteria.

    .. deprecated:: 1.2.0

        Use :meth:`github3.github.GitHub.search_repositories` instead.

    .. warning::

        You will only be able to make 5 calls with this or other search
        functions. To raise the rate-limit on this set of endpoints, create an
        authenticated :class:`GitHub <github3.github.GitHub>` Session with
        ``login``.

    The query can contain any combination of the following supported
    qualifers:

    - ``in`` Qualifies which fields are searched. With this qualifier you
      can restrict the search to just the repository name, description,
      readme, or any combination of these.
    - ``size`` Finds repositories that match a certain size (in
      kilobytes).
    - ``forks`` Filters repositories based on the number of forks, and/or
      whether forked repositories should be included in the results at
      all.
    - ``created`` or ``pushed`` Filters repositories based on times of
      creation, or when they were last updated. Format: ``YYYY-MM-DD``.
      Examples: ``created:<2011``, ``pushed:<2013-02``,
      ``pushed:>=2013-03-06``
    - ``user`` or ``repo`` Limits searches to a specific user or
      repository.
    - ``language`` Searches repositories based on the language they're
      written in.
    - ``stars`` Searches repositories based on the number of stars.

    For more information about these qualifiers, see: http://git.io/4Z8AkA

    :param str query: (required), a valid query as described above, e.g.,
        ``tetris language:assembly``
    :param str sort: (optional), how the results should be sorted;
        options: ``stars``, ``forks``, ``updated``; default: best match
    :param str order: (optional), the direction of the sorted results,
        options: ``asc``, ``desc``; default: ``desc``
    :param int per_page: (optional)
    :param bool text_match: (optional), if True, return matching search
        terms. See http://git.io/4ct1eQ for more information
    :param int number: (optional), number of repositories to return.
        Default: -1, returns all available repositories
    :param str etag: (optional), previous ETag header value
    :return: generator of :class:`Repository <github3.repos.Repository>`
    """
    return gh.search_repositories(
        query, sort, order, per_page, text_match, number, etag
    )


@deprecated
def search_users(
    query,
    sort=None,
    order=None,
    per_page=None,
    text_match=False,
    number=-1,
    etag=None,
):
    """Find users via the Search API.

    .. deprecated:: 1.2.0

        Use :meth:`github3.github.GitHub.search_users` instead.

    .. warning::

        You will only be able to make 5 calls with this or other search
        functions. To raise the rate-limit on this set of endpoints, create an
        authenticated :class:`GitHub <github3.github.GitHub>` Session with
        ``login``.

    The query can contain any combination of the following supported
    qualifers:


    - ``type`` With this qualifier you can restrict the search to just
      personal accounts or just organization accounts.
    - ``in`` Qualifies which fields are searched. With this qualifier you
      can restrict the search to just the username, public email, full
      name, or any combination of these.
    - ``repos`` Filters users based on the number of repositories they
      have.
    - ``location`` Filter users by the location indicated in their
      profile.
    - ``language`` Search for users that have repositories that match a
      certain language.
    - ``created`` Filter users based on when they joined.
    - ``followers`` Filter users based on the number of followers they
      have.

    For more information about these qualifiers see: http://git.io/wjVYJw

    :param str query: (required), a valid query as described above, e.g.,
        ``tom repos:>42 followers:>1000``
    :param str sort: (optional), how the results should be sorted;
        options: ``followers``, ``repositories``, or ``joined``; default:
        best match
    :param str order: (optional), the direction of the sorted results,
        options: ``asc``, ``desc``; default: ``desc``
    :param int per_page: (optional)
    :param bool text_match: (optional), if True, return matching search
        terms. See http://git.io/_V1zRwa for more information
    :param int number: (optional), number of search results to return;
        Default: -1 returns all available
    :param str etag: (optional), ETag header value of the last request.
    :return: generator of :class:`UserSearchResult
        <github3.search.UserSearchResult>`
    """
    return gh.search_users(
        query, sort, order, per_page, text_match, number, etag
    )


@deprecated
def user(username):
    return gh.user(username)


user.__doc__ = gh.user.__doc__


@deprecated
def zen():
    """Return a quote from the Zen of GitHub. Yet another API Easter Egg.

    .. deprecated:: 1.2.0

        Use :meth:`github3.github.GitHub.zen` instead.

    :returns: str

    """
    return gh.zen()
