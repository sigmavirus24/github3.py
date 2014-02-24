# -*- coding: utf-8 -*-
from github3.models import GitHubCore
from github3.users import User


class Deployment(GitHubCore):
    CUSTOM_HEADERS = {
        'Accept': 'application/vnd.github.cannonball-preview+json'
        }

    def __init__(self, deployment, session=None):
        super(Deployment, self).__init__(deployment, session)
        self._api = deployment.get('url')

        #: GitHub's id of this deployment
        self.id = deployment.get('id')

        #: SHA of the branch on GitHub
        self.sha = deployment.get('sha')

        #: User object representing the creator of the deployment
        self.creator = deployment.get('creator')
        if self.creator:
            self.creator = User(self.creator, self)

        #: JSON string payload of the Deployment
        self.payload = deployment.get('payload')

        #: Date the Deployment was created
        self.created_at = deployment.get('created_at')
        if self.created_at:
            self.created_at = self._strptime(self.created_at)

        #: Date the Deployment was updated
        self.updated_at = deployment.get('updated_at')
        if self.updated_at:
            self.updated_at = self._strptime(self.updated_at)

        #: Description of the deployment
        self.description = deployment.get('description')

        #: URL to get the statuses of this deployment
        self.statuses_url = deployment.get('statuses_url')

    def __repr__(self):
        return '<Deployment [{0} @ {1}]>'.format(self.id, self.sha)

    def iter_statuses(self, number=-1, etag=None):
        """Iterate over the deployment statuses for this deployment.

        :param int number: (optional), the number of statuses to return.
            Default: -1, returns all statuses.
        :param str etag: (optional), the ETag header value from the last time
            you iterated over the statuses.
        :returns: generator of :class:`DeploymentStatus`\ es
        """
        i = self._iter(int(number), self.statuses_url, DeploymentStatus,
                       etag=etag)
        i.headers = Deployment.CUSTOM_HEADERS
        return i


class DeploymentStatus(GitHubCore):
    def __init__(self, status, session=None):
        pass
