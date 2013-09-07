from collections import Iterator
from github3.models import GitHubCore, urlparse


class GitHubIterator(GitHubCore, Iterator):
    """The :class:`GitHubIterator` class powers all of the iter_* methods."""
    def __init__(self, count, url, cls, session, params=None, etag=None):
        GitHubCore.__init__(self, {}, session)
        #: Original number of items requested
        self.original = count
        #: Number of items left in the iterator
        self.count = count
        #: URL the class used to make it's first GET
        self.url = url
        self._api = self.url
        #: Class being used to cast all items to
        self.cls = cls
        #: Parameters of the query string
        self.params = params
        self._remove_none(self.params)
        # We do not set this from the parameter sent. We want this to
        # represent the ETag header returned by GitHub no matter what. # If this is not None, then it won't be set from the response and
        # that's not what we want.
        #: The ETag Header value returned by GitHub
        self.etag = None
        #: Headers generated for the GET request
        self.headers = {}
        #: The last response seen
        self.last_response = None
        #: Last status code received
        self.last_status = 0

        if etag:
            self.headers = {'If-None-Match': etag}

    def __repr__(self):
        path = urlparse(self.url).path
        return '<GitHubIterator [{0}, {1}]>'.format(self.count, path)

    def __iter__(self):
        url, params, cls = self.url, self.params, self.cls
        headers = self.headers

        while (self.count == -1 or self.count > 0) and url:
            response = self._get(url, params=params, headers=headers)
            self.last_response = response
            self.last_status = response.status_code
            if params:
                params = None  # rel_next already has the params

            if not self.etag and response.headers.get('ETag'):
                self.etag = response.headers.get('ETag')

            json = self._json(response, 200)

            if json is None:
                break

            # languages returns a single dict. We want the items.
            if isinstance(json, dict):
                json = json.items()

            for i in json:
                yield cls(i, self) if issubclass(cls, GitHubCore) else cls(i)
                self.count -= 1 if self.count > 0 else 0
                if self.count == 0:
                    break

            rel_next = response.links.get('next', {})
            url = rel_next.get('url', '')

    def __next__(self):
        if not hasattr(self, '__i__'):
            self.__i__ = self.__iter__()
        return next(self.__i__)

    def refresh(self, conditional=False):
        self.count = self.original
        if conditional:
            self.headers['If-None-Match'] = self.etag
        self.__i__ = self.__iter__()
        return self

    def next(self):
        return self.__next__()
