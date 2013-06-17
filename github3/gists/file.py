from github3.models import GitHubObject


class GistFile(GitHubObject):
    """The :class:`GistFile <GistFile>` object. This is used to represent a
    file object returned by GitHub while interacting with gists.
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
