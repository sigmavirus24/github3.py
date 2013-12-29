# -*- coding: utf-8 -*-
from github3.models import GitHubCore
from github3.issues import Issue


class IssueSearchResult(GitHubCore):
    def __init__(self, data, session=None):
        result = data.copy()
        #: Score of the result
        self.score = result.pop('score')
        #: Text matches
        self.text_matches = result.pop('text_matches', [])
        #: Issue object
        self.issue = Issue(result, self)

    def __repr__(self):
        return '<IssueSearchResult [{0}]>'.format(self.repository)
