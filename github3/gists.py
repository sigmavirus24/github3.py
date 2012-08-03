"""
gist.py
=======

Module which contains all the gist related material.

"""

from json import dumps
from .models import GitHubObject, GitHubCore, BaseComment
from .users import User


class GistFile(GitHubObject):
    """The :class:`GistFile <GistFile>` object. This is used to represent a
    file object returned by GitHub while interacting with gists.
    """

    def __init__(self, attributes):
        super(GistFile, self).__init__(attributes)

        self._raw = attributes.get('raw_url')
        self._name = attributes.get('filename')
        self._language = attributes.get('language')
        self._size = attributes.get('size')
        self._content = attributes.get('content')

    def __repr__(self):
        return '<Gist File [{0}]>'.format(self._name)

    @property
    def content(self):
        """The content of the file."""
        return self._content

    @property
    def name(self):
        """The name of the file."""
        return self._name

    @property
    def lang(self):
        """The language associated with the file."""
        return self._language

    @property
    def raw_url(self):
        """The raw URL for the file at GitHub."""
        return self._raw

    @property
    def size(self):
        """The size of the file."""
        return self._size


class GistComment(BaseComment):
    """The :class:`GistComment <GistComment>` object. This represents a comment
    on a gist.
    """

    def __init__(self, comment, session=None):
        super(GistComment, self).__init__(comment, session)

    def __repr__(self):
        return '<Gist Comment [{0}]>'.format(self._user.login)


class Gist(GitHubCore):
    """The :class:`Gist <Gist>` object. This object holds all the information
    returned by Github about a gist. With it you can comment on or fork the
    gist (assuming you are authenticated), edit or delete the gist (assuming
    you own it).  You can also "star" or "unstar" the gist (again assuming you
    have authenticated).
    """

    def __init__(self, data, session=None):
        super(Gist, self).__init__(data, session)
        self._update_(data)

    def __repr__(self):
        return '<Gist [{0}]>'.format(self._id)

    def _update_(self, data):
        self._json_data = data
        # The gist identifier
        self._id = data.get('id')
        self._desc = data.get('description', '')

        # e.g. https://api.github.com/gists/1
        self._api = data.get('url')
        #self._api = self._build_url('gists', str(self._id))
        # e.g. https://gist.github.com/1
        self._url = data.get('html_url')
        self._public = data.get('public')
        # a list of all the forks of that gist
        self._forks = data.get('forks', [])
        # e.g. git://gist.github.com/1.git
        self._pull = data.get('git_pull_url')
        # e.g. git@gist.github.com/1.git
        self._push = data.get('git_push_url')
        # date the gist was created
        self._created = self._strptime(data.get('created_at'))
        self._updated = self._strptime(data.get('updated_at'))
        if data.get('user'):
            self._user = User(data.get('user'), self._session)
        else:
            self._user = None

        # Create a list of files in the gist
        self._files = []
        for file in data['files']:
            self._files.append(GistFile(data['files'][file]))

    @GitHubCore.requires_auth
    def create_comment(self, body):
        """Create a comment on this gist.

        :param body: (required), body of the comment
        :type body: str
        :returns: :class:`GistComment <GistComment>`
        """
        url = self._build_url('comments', base_url=self._api)
        json = self._json(self._post(url, dumps({'body': body})), 201)
        return GistComment(json, self) if json else None

    @property
    def created_at(self):
        """datetime object representing when the gist was created."""
        return self._created

    @GitHubCore.requires_auth
    def delete(self):
        """Delete this gist.

        :returns: bool -- whether the deletion was successful"""
        return self._boolean(self._delete(self._api), 204, 404)

    @property
    def description(self):
        """Description of the gist"""
        return self._desc

    @GitHubCore.requires_auth
    def edit(self, description='', files={}):
        """Edit this gist.

        :param description: (optional), description of the gist
        :type description: str
        :param files: (optional), files that make up this gist; the key(s)
            should be the file name(s) and the values should be another
            (optional) dictionary with (optional) keys: 'content' and
            'filename' where the former is the content of the file and the
            latter is the new name of the file.
        :type files: dict
        :returns: bool -- whether the edit was successful
        """
        data = {}
        json = None
        if description:
            data['description'] = description
        if files:
            data['files'] = files
        if data:
            json = self._json(self._patch(self._api, dumps(data)), 200)
        if json:
            self._update_(json)
            return True
        return False

    @property
    def files(self):
        """Number of files in this gist."""
        return len(self._files)

    @GitHubCore.requires_auth
    def fork(self):
        """Fork this gist.

        :returns: :class:`Gist <Gist>` if successful, ``None`` otherwise
        """
        url = self._api + '/fork'
        json = self._json(self._post(url), 201)
        return Gist(json, self) if json else None

    @property
    def forks(self):
        """The number of forks of this gist."""
        return len(self._forks)

    @property
    def git_pull_url(self):
        """Git URL to pull this gist."""
        return self._pull

    @property
    def git_push_url(self):
        """Git URL to push to gist."""
        return self._push

    @property
    def html_url(self):
        """URL of this gist at Github."""
        return self._url

    @property
    def id(self):
        """Unique id for this gist."""
        return self._id

    def is_public(self):
        """Checks to see if this gist is public or not.

        :returns: bool -- True if public, False if private
        """
        return self._public

    def is_starred(self):
        """Checks to see if this gist is starred by the authenticated user.

        :returns: bool -- True if it is starred, False otherwise
        """
        url = self._build_url('star', base_url=self._api)
        return self._boolean(self._get(url), 204, 404)

    def list_comments(self):
        """List comments on this gist.

        :returns: list of :class:`GistComment <GistComment>`\ s
        """
        url = self._build_url('comments', base_url=self._api)
        json = self._json(self._get(url), 200)
        return [GistComment(c, self) for c in json]

    def list_files(self):
        """List of :class:`GistFile <GistFile>` objects representing the files
        stored in this gist."""
        return self._files

    def list_forks(self):
        """List of :class:`Gist <Gist>`\ s representing forks of this gist."""
        return self._forks

    def refresh(self):
        """Updates this gist by getting the information from the API again.

        :returns: bool -- whether the update was successful or not"""
        json = self._json(self._get(self._api), 200)
        if json:
            self._update_(json)
            return True
        return False

    @GitHubCore.requires_auth
    def star(self):
        """Star this gist.

        :returns: bool -- True if successful, False otherwise
        """
        url = self._build_url('star', base_url=self._api)
        return self._boolean(self._put(url), 204, 404)

    @GitHubCore.requires_auth
    def unstar(self):
        """Un-star this gist.

        :returns: bool -- True if successful, False otherwise
        """
        url = self._build_url('star', base_url=self._api)
        return self._boolean(self._delete(url), 204, 404)

    @property
    def updated_at(self):
        """datetime object representing the last time this gist was updated."""
        return self._updated

    @property
    def user(self):
        """:class:`User <github3.user.User>` object representing the owner of
        the gist."""
        return self._user
