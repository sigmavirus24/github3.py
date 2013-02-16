"""
github3.gists
=============

Module which contains all the gist related material.

"""

from json import dumps
from github3.models import GitHubObject, GitHubCore, BaseComment
from github3.users import User
from github3.decorators import requires_auth


class Gist(GitHubCore):
    """The :class:`Gist <Gist>` object. This object holds all the information
    returned by Github about a gist. With it you can comment on or fork the
    gist (assuming you are authenticated), edit or delete the gist (assuming
    you own it).  You can also "star" or "unstar" the gist (again assuming you
    have authenticated).
    """

    def __init__(self, data, session=None):
        super(Gist, self).__init__(data, session)
        #: Unique id for this gist.
        self.id = '{0}'.format(data.get('id', ''))

        #: Description of the gist
        self.description = data.get('description', '')

        # e.g. https://api.github.com/gists/1
        self._api = data.get('url', '')

        #: URL of this gist at Github, e.g., https://gist.github.com/1
        self.html_url = data.get('html_url')
        #: Boolean describing if the gist is public or private
        self.public = data.get('public')

        self._forks = data.get('forks', [])
        #: The number of forks of this gist.
        self.forks = len(self._forks)

        #: Git URL to pull this gist, e.g., git://gist.github.com/1.git
        self.git_pull_url = data.get('git_pull_url', '')

        #: Git URL to push to gist, e.g., git@gist.github.com/1.git
        self.git_push_url = data.get('git_push_url', '')

        #: datetime object representing when the gist was created.
        self.created_at = self._strptime(data.get('created_at'))

        #: datetime object representing the last time this gist was updated.
        self.updated_at = self._strptime(data.get('updated_at'))

        #: :class:`User <github3.users.User>` object representing the owner of
        #  the gist.
        self.owner = data.get('owner')
        if data.get('owner'):
            self.owner = User(data.get('owner'), self._session)

        self._files = [GistFile(data['files'][f]) for f in data['files']]
        #: Number of files in this gist.
        self.files = len(self._files)

        #: History of this gist, list of :class:`GistHistory <GistHistory>`
        self.history = [GistHistory(h, self) for h in data.get('history', [])]

    def __str__(self):
        return self.id

    def __repr__(self):
        return '<Gist [{0}]>'.format(self.id)

    def _update_(self, data):
        self.__init__(data, self._session)

    @requires_auth
    def create_comment(self, body):
        """Create a comment on this gist.

        :param str body: (required), body of the comment
        :returns: :class:`GistComment <GistComment>`
        """
        json = None
        if body:
            url = self._build_url('comments', base_url=self._api)
            json = self._json(self._post(url, data={'body': body}), 201)
        return GistComment(json, self) if json else None

    @requires_auth
    def delete(self):
        """Delete this gist.

        :returns: bool -- whether the deletion was successful"""
        return self._boolean(self._delete(self._api), 204, 404)

    @requires_auth
    def edit(self, description='', files={}):
        """Edit this gist.

        :param str description: (optional), description of the gist
        :param dict files: (optional), files that make up this gist; the
            key(s) should be the file name(s) and the values should be another
            (optional) dictionary with (optional) keys: 'content' and
            'filename' where the former is the content of the file and the
            latter is the new name of the file.
        :returns: bool -- whether the edit was successful
        """
        data = {}
        json = None
        if description:
            data['description'] = description
        if files:
            data['files'] = files
        if data:
            json = self._json(self._patch(self._api, data=dumps(data)), 200)
        if json:
            self._update_(json)
            return True
        return False

    @requires_auth
    def fork(self):
        """Fork this gist.

        :returns: :class:`Gist <Gist>` if successful, ``None`` otherwise
        """
        url = self._build_url('forks', base_url=self._api)
        json = self._json(self._post(url), 201)
        return Gist(json, self) if json else None

    def is_public(self):
        """Checks to see if this gist is public or not.

        :returns: bool -- True if public, False if private
        """
        return self.public

    @requires_auth
    def is_starred(self):
        """Checks to see if this gist is starred by the authenticated user.

        :returns: bool -- True if it is starred, False otherwise
        """
        url = self._build_url('star', base_url=self._api)
        return self._boolean(self._get(url), 204, 404)

    def iter_comments(self, number=-1, etag=None):
        """List comments on this gist.

        :param int number: (optional), number of comments to iterate over.
            Default: -1 will iterate over all comments on the gist
        :param str etag: (optional), ETag from a previous request to the same
            endpoint
        :returns: generator of :class:`GistComment <GistComment>`\ s
        """
        url = self._build_url('comments', base_url=self._api)
        return self._iter(int(number), url, GistComment, etag=etag)

    def iter_files(self):
        """List of :class:`GistFile <GistFile>` objects representing the files
        stored in this gist."""
        return iter(self._files)

    def iter_forks(self):
        """List of :class:`Gist <Gist>`\ s representing forks of this gist."""
        return iter(self._forks)  # (No coverage)

    @requires_auth
    def star(self):
        """Star this gist.

        :returns: bool -- True if successful, False otherwise
        """
        url = self._build_url('star', base_url=self._api)
        return self._boolean(self._put(url), 204, 404)

    @requires_auth
    def unstar(self):
        """Un-star this gist.

        :returns: bool -- True if successful, False otherwise
        """
        url = self._build_url('star', base_url=self._api)
        return self._boolean(self._delete(url), 204, 404)


class GistComment(BaseComment):
    """The :class:`GistComment <GistComment>` object. This represents a comment
    on a gist.
    """
    def __init__(self, comment, session=None):
        super(GistComment, self).__init__(comment, session)

        #: :class:`User <github3.users.User>` who made the comment
        self.user = None
        if comment.get('user'):
            self.user = User(comment.get('user'), self)  # (No coverage)

    def __repr__(self):
        return '<Gist Comment [{0}]>'.format(self.user.login)


class GistFile(GitHubObject):
    """The :class:`GistFile <GistFile>` object. This is used to represent a
    file object returned by GitHub while interacting with gists.
    """
    def __init__(self, attributes):
        super(GistFile, self).__init__(attributes)

        #: The raw URL for the file at GitHub.
        self.raw_url = attributes.get('raw_url')
        #: The name of the file.
        self.filename = attributes.get('filename')
        #: The name of the file.
        self.name = attributes.get('filename')
        #: The language associated with the file.
        self.language = attributes.get('language')
        #: The size of the file.
        self.size = attributes.get('size')
        #: The content of the file.
        self.content = attributes.get('content')

    def __repr__(self):
        return '<Gist File [{0}]>'.format(self.name)


class GistHistory(GitHubCore):
    """The :class:`GistHistory <GistHistory>` object represents one version
    (or revision) of a gist."""
    def __init__(self, history, session=None):
        super(GistHistory, self).__init__(history, session)
        self._api = history.get('url', '')

        #: SHA of the commit associated with this version
        self.version = history.get('version', '')

        #: user who made these changes
        self.user = User(history.get('user') or {}, session)

        #: dict containing the change status; see also: deletions, additions,
        #: total
        self.change_status = history.get('change_status', {})

        #: number of additions made
        self.additions = self.change_status.get('additions', 0)

        #: number of deletions made
        self.deletions = self.change_status.get('deletions', 0)

        #: total number of changes made
        self.total = self.change_status.get('total', 0)

        #: datetime representation of when the commit was made
        self.committed_at = self._strptime(history.get('committed_at'))

    def __repr__(self):
        return '<Gist History [{0}]>'.format(self.version)

    def get_gist(self):
        """Retrieves the gist at this version.

        :returns: :class:`Gist <Gist>`
        """
        json = self._json(self._get(self._api), 200)
        return Gist(json, self)
