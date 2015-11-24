# -*- coding: utf-8 -*-
"""
github3.gists.file
------------------

Module containing the logic for the GistFile object.
"""
from __future__ import unicode_literals

from ..models import GitHubCore


class GistFile(GitHubCore):

    """This represents the file object returned by interacting with gists.

    It stores the raw url of the file, the file name, language, size and
    content.

    """

    def _update_attributes(self, attributes):
        #: The raw URL for the file at GitHub.
        self.raw_url = attributes.get('raw_url')
        #: The name of the file.
        self.filename = attributes.get('filename')
        #: The name of the file.
        self.name = attributes.get('filename')
        #: The language associated with the file.
        self.language = attributes.get('language')
        #: The size of the file.
        self.size = attributes.get('size')
        #: The content of the file.
        self.content = self.get_content(attributes)

    def _repr(self):
        return '<Gist File [{0}]>'.format(self.name)

    def get_content(self, attributes):
        """Retrieve contents of file."""
        content = attributes.get('content')
        if not content:
            response = self._get(self.raw_url)
            if self._boolean(response, 200, 404):
                content = response.content
        return content
