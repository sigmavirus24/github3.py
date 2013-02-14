from collections import Iterator
from github3.models import GitHubCore, urlparse


class GitHubIterator(GitHubCore, Iterator):
    def __init__(self, count, url, cls, session, params=None, etag=None):
        GitHubCore.__init__(self, {}, session)
        self.count = count
        self.url = url
        self.cls = cls
        self.params = params
        self.etag = None
        self.headers = {}

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

    def next(self):
        return self.__next__()
