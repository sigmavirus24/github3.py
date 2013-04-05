"""
github3.repos.contents
======================

This module contains the Contents object pertaining to READMEs and other files
that can be accessed via the GitHub API.

"""

from base64 import b64decode
from github3.models import GitHubObject


class Contents(GitHubObject):
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

    def __eq__(self, other):
        return self.sha == other.sha

    def __ne__(self, other):
        return self.sha != other.sha

    @property
    def git_url(self):
        """API URL for this blob"""
        return self.links['git']

    @property
    def html_url(self):
        """URL pointing to the content on GitHub."""
        return self.links['html']
