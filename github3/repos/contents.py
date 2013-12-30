# -*- coding: utf-8 -*-
"""
github3.repos.contents
======================

This module contains the Contents object pertaining to READMEs and other files
that can be accessed via the GitHub API.

"""

from json import dumps
from base64 import b64decode, b64encode
from github3.git import Commit
from github3.models import GitHubCore
from github3.decorators import requires_auth


class Contents(GitHubCore):
    """The :class:`Contents <Contents>` object. It holds the information
    concerning any content in a repository requested via the API.

    Two content instances can be checked like so::

        c1 == c2
        c1 != c2

    And is equivalent to::

        c1.sha == c2.sha
        c1.sha != c2.sha

    See also: http://developer.github.com/v3/repos/contents/
    """
    def __init__(self, content, session=None):
        super(Contents, self).__init__(content, session)
        # links
        self._api = content.get('url')
        #: Dictionary of links
        self.links = content.get('_links')

        #: URL of the README on github.com
        self.html_url = content.get('html_url')

        #: URL for the git api pertaining to the README
        self.git_url = content.get('git_url')

        #: git:// URL of the content if it is a submodule
        self.submodule_git_url = content.get('submodule_git_url')

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
        self.decoded = ''
        if self.encoding == 'base64' and self.content:
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
        #: Type of content. ('file', 'symlink', 'submodule')
        self.type = content.get('type', '')
        #: Target will only be set of type is a symlink. This is what the link
        #: points to
        self.target = content.get('target', '')

        self._uniq = self.sha

    def __repr__(self):
        return '<Content [{0}]>'.format(self.path)

    def __eq__(self, other):
        return self.decoded == other

    def __ne__(self, other):
        return self.sha != other

    @requires_auth
    def delete(self, message, committer=None, author=None):
        """Delete this file.

        :param str message: (required), commit message to describe the removal
        :param dict committer: (optional), if no information is given the
            authenticated user's information will be used. You must specify
            both a name and email.
        :param dict author: (optional), if omitted this will be filled in with
            committer information. If passed, you must specify both a name and
            email.
        :returns: :class:`Commit <github3.git.Commit>`

        """
        json = None
        if message:
            data = {'message': message, 'sha': self.sha,
                    'committer': validate_commmitter(committer),
                    'author': validate_commmitter(author)}
            self._remove_none(data)
            json = self._json(self._delete(self._api, data=dumps(data)), 200)
            if 'commit' in json:
                json = Commit(json['commit'], self)
        return json

    @requires_auth
    def update(self, message, content, committer=None, author=None):
        """Update this file.

        :param str message: (required), commit message to describe the update
        :param str content: (required), content to update the file with
        :param dict committer: (optional), if no information is given the
            authenticated user's information will be used. You must specify
            both a name and email.
        :param dict author: (optional), if omitted this will be filled in with
            committer information. If passed, you must specify both a name and
            email.
        :returns: :class:`Commit <github3.git.Commit>`

        """
        if content and not isinstance(content, bytes):
            raise ValueError(  # (No coverage)
                'content must be a bytes object')  # (No coverage)

        json = None
        if message and content:
            content = b64encode(content).decode('utf-8')
            data = {'message': message, 'content': content, 'sha': self.sha,
                    'committer': validate_commmitter(committer),
                    'author': validate_commmitter(author)}
            self._remove_none(data)
            json = self._json(self._put(self._api, data=dumps(data)), 200)
            if 'content' in json and 'commit' in json:
                self.__init__(json['content'], self)
                json = Commit(json['commit'], self)
        return json


def validate_commmitter(d):
    if d and d.get('name') and d.get('email'):
        return d
    return None
