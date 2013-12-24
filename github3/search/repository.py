# -*- coding: utf-8 -*-
from github3.models import GitHubCore
from github3.repos import Repository


class RepositorySearchResult(GitHubCore):
    def __init__(self, data, session=None):
        result = data.copy()
        #: Score of the result
        self.score = result.pop('score')
        #: Text matches
        self.text_matches = result.pop('text_matches', [])
        #: Repository object
        self.repository = Repository(result, self)

    def __repr__(self):
        return '<RepositorySearchResult [{0}]>'.format(self.repository)
