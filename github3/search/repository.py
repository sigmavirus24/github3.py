# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from ..models import GitHubCore
from ..repos import Repository


class RepositorySearchResult(GitHubCore):
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

        #: Repository object
        self.repository = Repository(result, self)

    def _repr(self):
        return '<RepositorySearchResult [{0}]>'.format(self.repository)
