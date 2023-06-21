"""This module contains all the classes relating to GitHub Actions secrets."""
import typing

from .. import models


class PublicKey(models.GitHubCore):

    """Object representing a Public Key for GitHub Actions secrets.

    See https://docs.github.com/en/rest/actions/secrets for more details.

    .. attribute:: key_id

        The ID of the public key

    .. attribute:: key

        The actual public key as a string
    """

    def _update_attributes(self, publickey):
        self.key_id = publickey["key_id"]
        self.key = publickey["key"]

    def _repr(self):
        return f"<PublicKey [{self.key_id}]>"

    def __str__(self):
        return self.key


class _Secret(models.GitHubCore):

    """Base class for all secrets for GitHub Actions.

    See https://docs.github.com/en/rest/actions/secrets for more details.
    GitHub never reveals the secret value through its API, it is only accessible
    from within actions. Therefore, this object represents the secret's metadata
    but not its actual value.
    """

    class_name = "_Secret"

    def _repr(self):
        return f"<{self.class_name} [{self.name}]>"

    def __str__(self):
        return self.name

    def _update_attributes(self, secret):
        self.name = secret["name"]
        self.created_at = self._strptime(secret["created_at"])
        self.updated_at = self._strptime(secret["updated_at"])


class RepositorySecret(_Secret):
    """An object representing a repository secret for GitHub Actions.

    See https://docs.github.com/en/rest/actions/secrets for more details.
    GitHub never reveals the secret value through its API, it is only accessible
    from within actions. Therefore, this object represents the secret's metadata
    but not its actual value.

    .. attribute:: name

        The name of the secret

    .. attribute:: created_at

        The timestamp of when the secret was created

    .. attribute:: updated_at

        The timestamp of when the secret was last updated
    """

    class_name = "RepositorySecret"


class SharedOrganizationSecret(_Secret):
    """An object representing an organization secret for GitHub Actions that is
    shared with the repository.

    See https://docs.github.com/en/rest/actions/secrets for more details.
    GitHub never reveals the secret value through its API, it is only accessible
    from within actions. Therefore, this object represents the secret's metadata
    but not its actual value.

    .. attribute:: name

        The name of the secret

    .. attribute:: created_at

        The timestamp of when the secret was created

    .. attribute:: updated_at

        The timestamp of when the secret was last updated
    """

    class_name = "SharedOrganizationSecret"


class OrganizationSecret(_Secret):
    """An object representing am organization secret for GitHub Actions.

    See https://docs.github.com/en/rest/actions/secrets for more details.
    GitHub never reveals the secret value through its API, it is only accessible
    from within actions. Therefore, this object represents the secret's metadata
    but not its actual value.

    .. attribute:: name

        The name of the secret

    .. attribute:: created_at

        The timestamp of when the secret was created

    .. attribute:: updated_at

        The timestamp of when the secret was last updated
    """

    class_name = "OrganizationSecret"

    def _update_attributes(self, secret):
        super()._update_attributes(secret)
        self.visibility = secret["visibility"]
        if self.visibility == "selected":
            self._selected_repos_url = secret["selected_repositories_url"]

    def selected_repositories(self, number=-1, etag=""):
        """Iterates over all repositories this secret is visible to.

        :param int number:
            (optional), number of repositories to return.
            Default: -1 returns all selected repositories.
        :param str etag:
            (optional), ETag from a previous request to the same endpoint
        :returns:
            Generator of selected repositories or None if the visibility of this
            secret is not set to 'selected'.
        :rtype:
            :class:`~github3.repos.ShortRepository`
        """
        from .. import repos

        if self.visibility != "selected":
            return None

        return self._iter(
            int(number),
            self._selected_repos_url,
            repos.ShortRepository,
            etag=etag,
            list_key="repositories",
        )

    def set_selected_repositories(self, repository_ids: typing.List[int]):
        """Sets the selected repositories this secret is visible to.

        :param list[int] repository_ids:
            A list of repository IDs which this secret should be visible to.
        :returns:
            A boolean indicating whether the update was successful.
        :rtype:
            bool
        """
        if self.visibility != "selected":
            raise ValueError(
                """cannot set a list of selected repositories when visibility
                is not 'selected'"""
            )

        data = {"selected_repository_ids": repository_ids}

        return self._boolean(
            self._put(self._selected_repos_url, json=data), 204, 404
        )

    def add_selected_repository(self, repository_id: int):
        """Adds a repository to the list of repositories this secret is
        visible to.

        :param int repository_id:
            The IDs of a repository this secret should be visible to.
        :raises:
            A ValueError if the visibility of this secret is not 'selected'.
        :returns:
            A boolean indicating if the repository was successfully added to
            the visible list.
        :rtype:
            bool
        """
        if self.visibility != "selected":
            raise ValueError(
                "cannot add a repository when visibility is not 'selected'"
            )

        url = "/".join([self._selected_repos_url, str(repository_id)])
        return self._boolean(self._put(url), 204, 409)

    def delete_selected_repository(self, repository_id: int):
        """Deletes a repository from the list of repositories this secret is
        visible to.

        :param int repository_id:
            The IDs of the repository this secret should no longer be
            visible to.
        :raises:
            A ValueError if the visibility of this secret is not 'selected'.
        :returns:
            A boolean indicating if the repository was successfully removed
            from the visible list.
        :rtype:
            bool
        """
        if self.visibility != "selected":
            raise ValueError(
                "cannot delete a repository when visibility is not 'selected'"
            )

        url = "/".join([self._selected_repos_url, str(repository_id)])
        return self._boolean(self._delete(url), 204, 409)
