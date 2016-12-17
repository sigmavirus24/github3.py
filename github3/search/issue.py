# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from ..models import GitHubCore
from ..issues import Issue


class IssueSearchResult(GitHubCore):
    def _update_attributes(self, data):
        result = data.copy()

        #: Score of the result
        self.score = self._get_attribute(result, 'score')
        if 'score' in result:
            del result['score']

        #: Text matches
        self.text_matches = self._get_attribute(result, 'text_matches', [])
        if 'text_matches' in result:
            del result['text_matches']

        #: Issue object
        self.issue = Issue(result, self)

    def _repr(self):
        return '<IssueSearchResult [{0}]>'.format(self.issue)
