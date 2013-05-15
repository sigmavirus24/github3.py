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

    def __repr__(self):
        return '<Content [{0}]>'.format(self.path)

    def __str__(self):
        return self.decoded

    def __eq__(self, other):
        return self.decoded == other

    def __ne__(self, other):
        return self.sha != other
