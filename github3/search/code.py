# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from ..models import GitHubCore
from ..repos import Repository


class CodeSearchResult(GitHubCore):

    def _update_attributes(self, data):
        self._api = self._get_attribute(data, 'url')

        #: Filename the match occurs in
        self.name = self._get_attribute(data, 'name')

        #: Path in the repository to the file
        self.path = self._get_attribute(data, 'path')

        #: SHA in which the code can be found
        self.sha = self._get_attribute(data, 'sha')

        #: URL to the Git blob endpoint
        self.git_url = self._get_attribute(data, 'git_url')

        #: URL to the HTML view of the blob
        self.html_url = self._get_attribute(data, 'html_url')

        #: Repository the code snippet belongs to
        self.repository = self._class_attribute(
            data, 'repository', Repository, self
        )

        #: Score of the result
        self.score = self._get_attribute(data, 'score')

        #: Text matches
        self.text_matches = self._get_attribute(data, 'text_matches', [])

    def _repr(self):
        return '<CodeSearchResult [{0}]>'.format(self.path)
