# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

from uritemplate import URITemplate

from .. import utils
from .. import models
from .. import users
from ..decorators import requires_auth
from ..exceptions import error_for


class Release(models.GitHubCore):

    """The :class:`Release <Release>` object.

    It holds the information GitHub returns about a release from a
    :class:`Repository <github3.repos.repo.Repository>`.

    Please see GitHub's `Releases Documentation`_ for more information.

    .. _Releases Documentation:
        https://developer.github.com/v3/repos/releases/
    """

    def _update_attributes(self, release):
        self._api = self.url = release['url']

        #: List of :class:`Asset <Asset>` objects for this release
        self.original_assets = [
            Asset(i, self) for i in release['assets']
        ]

        #: Body of the release (the description)
        self.body = release['body']

        #: Date the release was created
        self.created_at = self._strptime_attribute(release, 'created_at')

        #: Boolean whether value is True or False
        self.draft = release['draft']

        #: GitHub id
        self.id = release['id']

        #: Name given to the release
        self.name = release['name']

        #: Boolean whether release is a prerelease
        self.prerelease = release['prerelease']

        #: Date the release was published
        self.published_at = self._strptime_attribute(release, 'published_at')

        #: Name of the tag
        self.tag_name = release['tag_name']

        #: "Commit" that this release targets
        self.target_commitish = release['target_commitish']

        #: URITemplate to upload an asset with
        self.upload_urlt = URITemplate(release['upload_url'])

        #: :class:`User <github3.users.ShortUser>` object representing the
        #:  creator of the release
        self.author = users.ShortUser(release['author'])

        #: URLs to various attributes
        for urltype in ['assets_url', 'html_url', 'tarball_url',
                        'zipball_url']:
            setattr(self, urltype, release[urltype])

    def _repr(self):
        return '<Release [{0}]>'.format(self.name)

    def archive(self, format, path=''):
        """Get the tarball or zipball archive for this release.

        :param str format: (required), accepted values: ('tarball',
            'zipball')
        :param path: (optional), path where the file should be saved
            to, default is the filename provided in the headers and will be
            written in the current directory.
            it can take a file-like object as well
        :type path: str, file
        :returns: bool -- True if successful, False otherwise

        """
        resp = None
        if format in ('tarball', 'zipball'):
            repo_url = self._api[:self._api.rfind('/releases')]
            url = self._build_url(format, self.tag_name, base_url=repo_url)
            resp = self._get(url, allow_redirects=True, stream=True)

        if resp and self._boolean(resp, 200, 404):
            utils.stream_response_to_file(resp, path)
            return True
        return False

    def asset(self, asset_id):
        """Retrieve the asset from this release with ``asset_id``.

        :param int asset_id: ID of the Asset to retrieve
        :returns: :class:`~github3.repos.release.Asset`
        """
        json = None
        if int(asset_id) > 0:
            i = self._api.rfind('/')
            url = self._build_url('assets', str(asset_id),
                                  base_url=self._api[:i])
            json = self._json(self._get(url), 200)
        return self._instance_or_null(Asset, json)

    def assets(self, number=-1, etag=None):
        """Iterate over the assets available for this release.

        :param int number: (optional), Number of assets to return
        :param str etag: (optional), last ETag header sent
        :returns: generator of :class:`Asset <Asset>` objects
        """
        url = self._build_url('assets', base_url=self._api)
        return self._iter(number, url, Asset, etag=etag)

    @requires_auth
    def delete(self):
        """Delete this release.

        Users with push access to the repository can delete a release.

        :returns: True if successful; False if not successful
        """
        url = self._api
        return self._boolean(
            self._delete(url),
            204,
            404
        )

    @requires_auth
    def edit(self, tag_name=None, target_commitish=None, name=None, body=None,
             draft=None, prerelease=None):
        """Edit this release.

        Users with push access to the repository can edit a release.

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

        r = self.session.patch(
            url, data=json.dumps(data))

        successful = self._boolean(r, 200, 404)
        if successful:
            # If the edit was successful, let's update the object.
            self._update_attributes(r.json())

        return successful

    @requires_auth
    def upload_asset(self, content_type, name, asset, label=None):
        """Upload an asset to this release.

        All parameters are required.

        :param str content_type: The content type of the asset. Wikipedia has
            a list of common media types
        :param str name: The name of the file
        :param asset: The file or bytes object to upload.
        :param label: (optional), An alternate short description of the asset.
        :returns: :class:`Asset <Asset>`
        """
        headers = {'Content-Type': content_type}
        params = {'name': name, 'label': label}
        self._remove_none(params)
        url = self.upload_urlt.expand(params)
        r = self._post(url, data=asset, json=False, headers=headers)
        if r.status_code in (201, 202):
            return Asset(r.json(), self)
        raise error_for(r)


class Asset(models.GitHubCore):

    def _update_attributes(self, asset):
        self._api = asset['url']

        #: Content-Type provided when the asset was created
        self.content_type = asset['content_type']

        #: Date the asset was created
        self.created_at = asset['created_at']

        #: Number of times the asset was downloaded
        self.download_count = asset['download_count']

        #: URL to download the asset.
        #: Request headers must include ``Accept: application/octet-stream``.
        self.download_url = self._api

        # User friendly download URL
        self.browser_download_url = asset['browser_download_url']

        #: GitHub id of the asset
        self.id = asset['id']

        #: Short description of the asset
        self.label = asset['label']

        #: Name of the asset
        self.name = asset['name']

        #: Size of the asset
        self.size = asset['size']

        #: State of the asset, e.g., "uploaded"
        self.state = asset['state']

        #: Date the asset was updated
        self.updated_at = self._strptime_attribute(asset, 'updated_at')

    def _repr(self):
        return '<Asset [{0}]>'.format(self.name)

    def download(self, path=''):
        """Download the data for this asset.

        :param path: (optional), path where the file should be saved
            to, default is the filename provided in the headers and will be
            written in the current directory.
            it can take a file-like object as well
        :type path: str, file
        :returns: name of the file, if successful otherwise ``None``
        :rtype: str
        """
        headers = {
            'Accept': 'application/octet-stream'
        }
        resp = self._get(self._api, allow_redirects=False, stream=True,
                         headers=headers)
        if resp.status_code == 302:
            # Amazon S3 will reject the redirected request unless we omit
            # certain request headers
            headers.update({
                'Content-Type': None,
            })

            with self.session.no_auth():
                resp = self._get(resp.headers['location'], stream=True,
                                 headers=headers)

        if self._boolean(resp, 200, 404):
            return utils.stream_response_to_file(resp, path)
        return None

    @requires_auth
    def delete(self):
        """Delete this asset if the user has push access.

        :returns: True if successful; False if not successful
        :rtype: boolean
        """
        url = self._api
        return self._boolean(
            self._delete(url), 204, 404
        )

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
            data=json.dumps(edit_data)
        )
        successful = self._boolean(r, 200, 404)
        if successful:
            self._update_attributes(r.json())

        return successful
