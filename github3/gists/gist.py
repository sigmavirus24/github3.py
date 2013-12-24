# -*- coding: utf-8 -*-
"""
github3.gists.gist
==================

This module contains the Gist class alone for simplicity.

"""
from json import dumps
from github3.models import GitHubCore
from github3.decorators import requires_auth
from github3.gists.comment import GistComment
from github3.gists.file import GistFile
from github3.gists.history import GistHistory
from github3.users import User


class Gist(GitHubCore):

    """This object holds all the information returned by Github about a gist.

    With it you can comment on or fork the gist (assuming you are
    authenticated), edit or delete the gist (assuming you own it).  You can
    also "star" or "unstar" the gist (again assuming you have authenticated).

    Two gist instances can be checked like so::

        g1 == g2
        g1 != g2

    And is equivalent to::

        g1.id == g2.id
        g1.id != g2.id

    See also: http://developer.github.com/v3/gists/

    """

    def __init__(self, data, session=None):
        super(Gist, self).__init__(data, session)
        #: Number of comments on this gist
        self.comments = data.get('comments', 0)

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

        owner = data.get('owner')
        #: :class:`User <github3.users.User>` object representing the owner of
        #  the gist.
        self.owner = User(owner, self) if owner else None

        self._files = [GistFile(data['files'][f]) for f in data['files']]
        #: Number of files in this gist.
        self.files = len(self._files)

        #: History of this gist, list of :class:`GistHistory <GistHistory>`
        self.history = [GistHistory(h, self) for h in data.get('history', [])]

        ## New urls

        #: Comments URL (not a template)
        self.comments_url = data.get('comments_url', '')

        #: Commits URL (not a template)
        self.commits_url = data.get('commits_url', '')

        #: Forks URL (not a template)
        self.forks_url = data.get('forks_url', '')

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
        :returns: :class:`GistComment <github3.gists.comment.GistComment>`

        """
        json = None
        if body:
            url = self._build_url('comments', base_url=self._api)
            json = self._json(self._post(url, data={'body': body}), 201)
        return GistComment(json, self) if json else None

    @requires_auth
    def delete(self):
        """Delete this gist.

        :returns: bool -- whether the deletion was successful

        """
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
        """Check to see if this gist is public or not.

        :returns: bool -- True if public, False if private

        """
        return self.public

    @requires_auth
    def is_starred(self):
        """Check to see if this gist is starred by the authenticated user.

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
        :returns: generator of
            :class:`GistComment <github3.gists.comment.GistComment>`

        """
        url = self._build_url('comments', base_url=self._api)
        return self._iter(int(number), url, GistComment, etag=etag)

    def iter_commits(self, number=-1):
        """Iter over the commits on this gist.

        These commits will be requested from the API and should be the same as
        what is in ``Gist.history``.

        .. versionadded:: 0.6

        :param int number: (optional), number of commits to iterate over.
            Default: -1 will iterate over all commits associated with this
            gist.
        :returns: generator of
            :class:`GistHistory <github3.gists.history.GistHistory>`

        """
        url = self._build_url('commits', base_url=self._api)
        return self._iter(int(number), url, GistHistory)

    def iter_files(self):
        """Iterator over the files stored in this gist.

        :returns: generator of :class`GistFile <github3.gists.file.GistFile>`

        """
        return iter(self._files)

    def iter_forks(self):
        """Iterator of forks of this gist.

        :returns: generator of :class:`Gist <Gist>`

        """
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
