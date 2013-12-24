# -*- coding: utf-8 -*-
"""
github3.gists.file
------------------

Module containing the logic for the GistFile object.
"""

from github3.models import GitHubObject


class GistFile(GitHubObject):

    """This represents the file object returned by interacting with gists.

    It stores the raw url of the file, the file name, language, size and
    content.

    """

    def __init__(self, attributes):
        super(GistFile, self).__init__(attributes)

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
        self.content = attributes.get('content')

    def __repr__(self):
        return '<Gist File [{0}]>'.format(self.name)
