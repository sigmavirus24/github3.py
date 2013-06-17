from github3.models import GitHubCore
from github3.decorators import requires_auth
from collections import Callable


class Download(GitHubCore):
    """The :class:`Download <Download>` object. It represents how GitHub sends
    information about files uploaded to the downloads section of a repository.

    .. warning::

        On 2013-03-11, this API was suppoed to be deprecated by GitHub. This
        means that at any time, GitHub could deprecate this part of the API at
        any time without further notice. Until I find out it has been
        deprecated, this will remain part of the API, although it will be
        unsupported.
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
