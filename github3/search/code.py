# -*- coding: utf-8 -*-
from github3.models import GitHubCore
from github3.repos import Repository


class CodeSearchResult(GitHubCore):
    def __init__(self, data, session=None):
        super(CodeSearchResult, self).__init__(data, session)
        self._api = data.get('url')
        #: Filename the match occurs in
        self.name = data.get('name')
        #: Path in the repository to the file
        self.path = data.get('path')
        #: SHA in which the code can be found
        self.sha = data.get('sha')
        #: URL to the Git blob endpoint
        self.git_url = data.get('git_url')
        #: URL to the HTML view of the blob
        self.html_url = data.get('html_url')
        #: Repository the code snippet belongs to
        self.repository = Repository(data.get('repository', {}), self)
        #: Score of the result
        self.score = data.get('score')
        #: Text matches
        self.text_matches = data.get('text_matches', [])

    def __repr__(self):
        return '<CodeSearchResult [{0}]>'.format(self.path)
