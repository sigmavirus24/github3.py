# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from github3.models import GitHubCore
from github3.users import User


class UserSearchResult(GitHubCore):
    def __init__(self, data, session=None):
        super(UserSearchResult, self).__init__(data, session)
        result = data.copy()
        #: Score of this search result
        self.score = result.pop('score')
        #: Text matches
        self.text_matches = result.pop('text_matches', [])
        #: User object matching the search
        self.user = User(result, self)

    def _repr(self):
        return '<UserSearchResult [{0}]>'.format(self.user)
