from github3.models import GitHubCore
from uritemplate import URITemplate


class Release(GitHubCore):
    """The :class:`Branch <Branch>` object. It holds the information GitHub
    returns about a branch on a
    :class:`Repository <github3.repos.repo.Repository>`.
    """
    def __init__(self, release, session=None):
        super(Release, self).__init__(release, session)
        #: URL for uploaded assets
        self.assets_url = release.get('assets_url')
        #: Body of the release (the description)
        self.body = release.get('body')
        #: Date the release was created
        self.created_at = self._strptime(release.get('created_at'))
        #: Boolean whether value is True or False
        self.draft = release.get('draft')
        #: HTML URL of the release
        self.html_url = release.get('html_url')
        #: GitHub id
        self.id = release.get('id')
        #: Name given to the release
        self.name = release.get('name')
        #; Boolean whether release is a prelease
        self.prerelease = release.get('prerelease')
        #: Date the release was published
        self.published_at = release.get('published_at')
        #: Name of the tag
        self.tag_name = release.get('tag_name')
        #: "Commit" that this release targets
        self.target_commitish = release.get('target_commitish')
        #: URITemplate to upload an asset with
        upload_url = release.get('upload_url')
        self.upload_urlt = URITemplate(upload_url) if upload_url else None

    def __repr__(self):
        return '<Release [{0}]>'.format(self.name)
