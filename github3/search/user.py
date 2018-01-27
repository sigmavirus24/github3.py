# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from .. import users
from ..models import GitHubCore


class UserSearchResult(GitHubCore):
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

        #: User object matching the search
        self.user = users.ShortUser(result, self)

    def _repr(self):
        return '<UserSearchResult [{0}]>'.format(self.user)
