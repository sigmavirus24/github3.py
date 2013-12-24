# -*- coding: utf-8 -*-
import json

from github3.decorators import requires_auth
from github3.models import GitHubCore, GitHubError
from uritemplate import URITemplate


class Release(GitHubCore):

    """The :class:`Release <Release>` object.

    It holds the information GitHub returns about a release from a
    :class:`Repository <github3.repos.repo.Repository>`.

    """

    CUSTOM_HEADERS = {'Accept': 'application/vnd.github.manifold-preview'}

    def __init__(self, release, session=None):
        super(Release, self).__init__(release, session)
        self._api = release.get('url')
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
        upload_url = release.get('upload_url')
        #: URITemplate to upload an asset with
        self.upload_urlt = URITemplate(upload_url) if upload_url else None

    def __repr__(self):
        return '<Release [{0}]>'.format(self.name)

    @requires_auth
    def delete(self):
        """Users with push access to the repository can delete a release.

        :returns: True if successful; False if not successful
        """
        url = self._api
        return self._boolean(
            self._delete(url, headers=Release.CUSTOM_HEADERS),
            204,
            404
        )

    @requires_auth
    def edit(self, tag_name=None, target_commitish=None, name=None, body=None,
             draft=None, prerelease=None):
        """Users with push access to the repository can edit a release.

        If the edit is successful, this object will update itself.

        :param str tag_name: (optional), Name of the tag to use
        :param str target_commitish: (optional), The "commitish" value that
            determines where the Git tag is created from. Defaults to the
            repository's default branch.
        :param str name: (optional), Name of the release
        :param str body: (optional), Description of the release
        :param boolean draft: (optional), True => Release is a draft
        :param boolean prerelease: (optional), True => Release is a prerelease
        :returns: True if successful; False if not successful
        """
        url = self._api
        data = {
            'tag_name': tag_name,
            'target_commitish': target_commitish,
            'name': name,
            'body': body,
            'draft': draft,
            'prerelease': prerelease,
        }
        self._remove_none(data)

        r = self._session.patch(
            url, data=json.dumps(data), headers=Release.CUSTOM_HEADERS
        )

        successful = self._boolean(r, 200, 404)
        if successful:
            # If the edit was successful, let's update the object.
            self.__init__(r.json(), self)

        return successful

    def iter_assets(self, number=-1, etag=None):
        """Iterate over the assets available for this release.

        :param int number: (optional), Number of assets to return
        :param str etag: (optional), last ETag header sent
        :returns: generator of :class:`Asset <Asset>` objects
        """
        url = self._build_url('assets', base_url=self._api)
        return self._iter(number, url, Asset, etag=etag)

    @requires_auth
    def upload_asset(self, content_type, name, asset):
        """Upload an asset to this release.

        All parameters are required.

        :param str content_type: The content type of the asset. Wikipedia has
            a list of common media types
        :param str name: The name of the file
        :param asset: The file or bytes object to upload.
        :returns: :class:`Asset <Asset>`
        """
        headers = Release.CUSTOM_HEADERS.copy()
        headers.update({'Content-Type': content_type})
        url = self.upload_urlt.expand({'name': name})
        r = self._post(url, data=asset, json=False, headers=headers,
                       verify=False)
        if r.status_code in (201, 202):
            return Asset(r.json(), self)
        raise GitHubError(r)


class Asset(GitHubCore):
    def __init__(self, asset, session=None):
        super(Asset, self).__init__(asset, session)
        self._api = asset.get('url')
        #: Content-Type provided when the asset was created
        self.content_type = asset.get('content_type')
        #: Date the asset was created
        self.created_at = self._strptime(asset.get('created_at'))
        #: Number of times the asset was downloaded
        self.download_count = asset.get('download_count')
        #: GitHub id of the asset
        self.id = asset.get('id')
        #: Short description of the asset
        self.label = asset.get('label')
        #: Name of the asset
        self.name = asset.get('name')
        #: Size of the asset
        self.size = asset.get('size')
        #: State of the asset, e.g., "uploaded"
        self.state = asset.get('state')
        #: Date the asset was updated
        self.updated_at = self._strptime(asset.get('updated_at'))

    def edit(self, name, label=None):
        """Edit this asset.

        :param str name: (required), The file name of the asset
        :param str label: (optional), An alternate description of the asset
        :returns: boolean
        """
        if not name:
            return False
        edit_data = {'name': name, 'label': label}
        self._remove_none(edit_data)
        r = self._patch(
            self._api,
            data=edit_data,
            headers=Release.CUSTOM_HEADERS
        )
        successful = self._boolean(r, 200, 404)
        if successful:
            self.__init__(r.json(), self)

        return successful
