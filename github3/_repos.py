"""
github3.repos
=============

This module contains the classes relating to repositories.

"""

from json import dumps
from base64 import b64decode
from collections import Callable
from github3.issues import Issue, IssueEvent, Label, Milestone, issue_params
from github3.git import Blob, Commit, Reference, Tag, Tree
from github3.models import GitHubObject, GitHubCore, BaseComment, BaseCommit
from github3.pulls import PullRequest
from github3.users import User, Key
from github3.decorators import requires_auth


class Branch(GitHubCore):
    """The :class:`Branch <Branch>` object. It holds the information GitHub
    returns about a branch on a :class:`Repository <Repository>`.
    """
    def __init__(self, branch, session=None):
        super(Branch, self).__init__(branch, session)
        #: Name of the branch.
        self.name = branch.get('name')
        #: Returns the branch's :class:`RepoCommit <RepoCommit>` or
        #  ``None``.
        self.commit = branch.get('commit')
        if self.commit:
            self.commit = RepoCommit(self.commit, self._session)
        #: Returns '_links' attribute.
        self.links = branch.get('_links', {})

    def __repr__(self):
        return '<Repository Branch [{0}]>'.format(self.name)


class Contents(GitHubObject):
    """The :class:`Contents <Contents>` object. It holds the information
    concerning any content in a repository requested via the API.
    """

    def __init__(self, content):
        super(Contents, self).__init__(content)
        # links
        self._api = content['_links'].get('self', '')
        #: Dictionary of links
        self.links = content.get('_links')

        # should always be 'base64'
        #: Returns encoding used on the content.
        self.encoding = content.get('encoding', '')

        # content, base64 encoded and decoded
        #: Base64-encoded content of the file.
        self.content = content.get('content', '')

        #: Decoded content of the file as a bytes object. If we try to decode
        #: to character set for you, we might encounter an exception which
        #: will prevent the object from being created. On python2 this is the
        #: same as a string, but on python3 you should call the decode method
        #: with the character set you wish to use, e.g.,
        #: ``content.decoded.decode('utf-8')``.
        #: .. versionchanged:: 0.5.2
        self.decoded = self.content
        if self.encoding == 'base64':
            self.decoded = b64decode(self.content.encode())

        # file name, path, and size
        #: Name of the content.
        self.name = content.get('name', '')
        #: Path to the content.
        self.path = content.get('path', '')
        #: Size of the content
        self.size = content.get('size', 0)
        #: SHA string.
        self.sha = content.get('sha', '')

        # should always be 'file'
        #: Type of content.
        self.type = content.get('type', '')

    def __repr__(self):
        return '<Content [{0}]>'.format(self.path)

    def __str__(self):
        return self.decoded

    @property
    def git_url(self):
        """API URL for this blob"""
        return self.links['git']

    @property
    def html_url(self):
        """URL pointing to the content on GitHub."""
        return self.links['html']


class Download(GitHubCore):
    """The :class:`Download <Download>` object. It represents how GitHub sends
    information about files uploaded to the downloads section of a repository.

    .. warning::

        On 2013-03-11, this API will be deprecated by GitHub. There will also
        be a new version of github3.py to accompany this at that date.
    """

    def __init__(self, download, session=None):
        super(Download, self).__init__(download, session)
        self._api = download.get('url', '')
        #: URL of the download at GitHub.
        self.html_url = download.get('html_url', '')
        #: Unique id of the download on GitHub.
        self.id = download.get('id', 0)
        #: Name of the download.
        self.name = download.get('name', '')
        #: Description of the download.
        self.description = download.get('description', '')
        #: Size of the download.
        self.size = download.get('size', 0)
        #: How many times this particular file has been downloaded.
        self.download_count = download.get('download_count', 0)
        #: Content type of the download.
        self.content_type = download.get('content_type', '')

    def __repr__(self):
        return '<Download [{0}]>'.format(self.name)

    @requires_auth
    def delete(self):
        """Delete this download if authenticated"""
        return self._boolean(self._delete(self._api), 204, 404)

    def saveas(self, path=''):
        """Save this download to the path specified.

        :param str path: (optional), if no path is specified, it will be
            saved in the current directory with the name specified by GitHub.
            it can take a file-like object as well
        :returns: bool
        """
        if not path:
            path = self.name

        resp = self._get(self.html_url, allow_redirects=True, stream=True)
        if self._boolean(resp, 200, 404):
            if isinstance(getattr(path, 'write', None), Callable):
                file_like = True
                fd = path
            else:
                file_like = False
                fd = open(path, 'wb')
            for chunk in resp.iter_content(512):
                fd.write(chunk)
            if not file_like:
                fd.close()
            return True
        return False  # (No coverage)


class Hook(GitHubCore):
    """The :class:`Hook <Hook>` object. This handles the information returned
    by GitHub about hooks set on a repository."""

    def __init__(self, hook, session=None):
        super(Hook, self).__init__(hook, session)
        self._api = hook.get('url', '')
        #: datetime object representing when this hook was last updated.
        self.updated_at = None
        if hook.get('updated_at'):
            self.updated_at = self._strptime(hook.get('updated_at'))
        #: datetime object representing the date the hook was created.
        self.created_at = self._strptime(hook.get('created_at'))
        #: The name of the hook.
        self.name = hook.get('name')
        #: Events which trigger the hook.
        self.events = hook.get('events')
        #: Whether or not this Hook is marked as active on GitHub
        self.active = hook.get('active')
        #: Dictionary containing the configuration for the Hook.
        self.config = hook.get('config')
        #: Unique id of the hook.
        self.id = hook.get('id')

    def __repr__(self):
        return '<Hook [{0}]>'.format(self.name)

    def _update_(self, hook):
        self.__init__(hook, self._session)

    @requires_auth
    def delete(self):
        """Delete this hook.

        :returns: bool
        """
        return self._boolean(self._delete(self._api), 204, 404)

    @requires_auth
    def delete_subscription(self):
        """Delete the user's subscription to this repository.

        :returns: bool
        """
        url = self._build_url('subscription', base_url=self._api)
        return self._boolean(self._delete(url), 204, 404)

    @requires_auth
    def edit(self, name, config, events=[], add_events=[], rm_events=[],
             active=True):
        """Edit this hook.

        :param str name: (required), name of the service being called
        :param dict config: (required), key-value pairs of settings for this
            hook
        :param list events: (optional), which events should this be triggered
            for
        :param list add_events: (optional), events to be added to the list of
           events that this hook triggers for
        :param list rm_events: (optional), events to be remvoed from the list
            of events that this hook triggers for
        :param bool active: (optional), should this event be active
        :returns: bool
        """
        json = None
        if name and config and isinstance(config, dict):
            data = {'name': name, 'config': config, 'active': active}
            if events:
                data['events'] = events

            if add_events:
                data['add_events'] = add_events

            if rm_events:
                data['remove_events'] = rm_events

            json = self._json(self._patch(self._api, data=dumps(data)), 200)

        if json:
            self._update_(json)
            return True
        return False

    @requires_auth
    def test(self):
        """Test this hook

        :returns: bool
        """
        url = self._build_url('tests', base_url=self._api)
        return self._boolean(self._post(url), 204, 404)


class RepoTag(GitHubObject):
    """The :class:`RepoTag <RepoTag>` object. This stores the information
    representing a tag that was created on a repository.
    """

    def __init__(self, tag):
        super(RepoTag, self).__init__(tag)
        #: Name of the tag.
        self.name = tag.get('name')
        #: URL for the GitHub generated zipball associated with the tag.
        self.zipball_url = tag.get('zipball_url')
        #: URL for the GitHub generated tarball associated with the tag.
        self.tarball_url = tag.get('tarball_url')
        #: Dictionary containing the SHA and URL of the commit.
        self.commit = tag.get('commit', {})

    def __repr__(self):
        return '<Repository Tag [{0}]>'.format(self)

    def __str__(self):
        return self.name


class Comparison(GitHubCore):
    """The :class:`Comparison <Comparison>` object. This encapsulates the
    information returned by GitHub comparing two commit objects in a
    repository."""

    def __init__(self, compare):
        super(Comparison, self).__init__(compare)
        self._api = compare.get('url', '')
        #: URL to view the comparison at GitHub
        self.html_url = compare.get('html_url')
        #: Permanent link to this comparison.
        self.permalink_url = compare.get('permalink_url')
        #: URL to see the diff between the two commits.
        self.diff_url = compare.get('diff_url')
        #: Patch URL at GitHub for the comparison.
        self.patch_url = compare.get('patch_url')
        #: :class:`RepoCommit <RepoCommit>` object representing the base of
        #  comparison.
        self.base_commit = RepoCommit(compare.get('base_commit'), None)
        #: Behind or ahead.
        self.status = compare.get('status')
        #: Number of commits ahead by.
        self.ahead_by = compare.get('ahead_by')
        #: Number of commits behind by.
        self.behind_by = compare.get('behind_by')
        #: Number of commits difference in the comparison.
        self.total_commits = compare.get('total_commits')
        #: List of :class:`RepoCommit <RepoCommit>` objects.
        self.commits = [RepoCommit(com) for com in compare.get('commits')]
        #: List of dicts describing the files modified.
        self.files = compare.get('files', [])

    def __repr__(self):
        return '<Comparison of {0} commits>'.format(self.total_commits)

    def diff(self):
        """Return the diff"""
        resp = self._get(self._api,
                         headers={'Accept': 'application/vnd.github.diff'})
        return resp.content if self._boolean(resp, 200, 404) else None

    def patch(self):
        """Return the patch"""
        resp = self._get(self._api,
                         headers={'Accept': 'application/vnd.github.patch'})
        return resp.content if self._boolean(resp, 200, 404) else None


class Status(GitHubObject):
    """The :class:`Status <Status>` object. This represents information from
    the Repo Status API."""
    def __init__(self, status):
        super(Status, self).__init__(status)
        #: datetime object representing the creation of the status object
        self.created_at = self._strptime(status.get('created_at'))
        #: :class:`User <github3.users.User>` who created the object
        self.creator = User(status.get('creator'))
        #: Short description of the Status
        self.description = status.get('description')
        #: GitHub ID for the status object
        self.id = status.get('id')
        #: State of the status, e.g., 'success', 'pending', 'failed', 'error'
        self.state = status.get('state')
        #: URL to view more information about the status
        self.target_url = status.get('target_url')
        #: datetime object representing the last time the status was updated
        self.updated_at = None
        if status.get('updated_at'):
            self.updated_at = self._strptime(status.get('updated_at'))

    def __repr__(self):
        return '<Status [{s.id}:{s.state}]>'.format(s=self)
