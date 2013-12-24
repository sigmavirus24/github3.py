# -*- coding: utf-8 -*-
from github3.models import GitHubCore
from github3.repos.commit import RepoCommit


class Branch(GitHubCore):
    """The :class:`Branch <Branch>` object. It holds the information GitHub
    returns about a branch on a
    :class:`Repository <github3.repos.repo.Repository>`.
    """
    def __init__(self, branch, session=None):
        super(Branch, self).__init__(branch, session)
        #: Name of the branch.
        self.name = branch.get('name')
        #: Returns the branch's :class:`RepoCommit <RepoCommit>` or
        #  ``None``.
        self.commit = branch.get('commit')
        if self.commit:
            self.commit = RepoCommit(self.commit, self._session)
        #: Returns '_links' attribute.
        self.links = branch.get('_links', {})

    def __repr__(self):
        return '<Repository Branch [{0}]>'.format(self.name)
