"""
github3.repos.comment
=====================

This module contains the RepoComment class

"""
from github3.decorators import requires_auth
from github3.models import BaseComment
from github3.users import User


class RepoComment(BaseComment):
    """The :class:`RepoComment <RepoComment>` object. This stores the
    information about a comment on a file in a repository.
    """
    def __init__(self, comment, session=None):
        super(RepoComment, self).__init__(comment, session)
        #: Commit id on which the comment was made.
        self.commit_id = comment.get('commit_id')
        #: URL of the comment on GitHub.
        self.html_url = comment.get('html_url')
        #: The line number where the comment is located.
        self.line = comment.get('line')
        #: The path to the file where the comment was made.
        self.path = comment.get('path')
        #: The position in the diff where the comment was made.
        self.position = comment.get('position')
        #: datetime object representing when the comment was updated.
        self.updated_at = comment.get('updated_at')
        if self.updated_at:
            self.updated_at = self._strptime(self.updated_at)
        #: Login of the user who left the comment.
        self.user = None
        if comment.get('user'):
            self.user = User(comment.get('user'), self)

    def __repr__(self):
        return '<Repository Comment [{0}/{1}]>'.format(
            self.commit_id[:7], self.user.login or ''
        )

    def _update_(self, comment):
        super(RepoComment, self)._update_(comment)
        self.__init__(comment, self._session)

    @requires_auth
    def update(self, body, sha, line, path, position):
        """Update this comment.

        :param str body: (required)
        :param str sha: (required), sha id of the commit to comment on
        :param int line: (required), line number to comment on
        :param str path: (required), relative path of the file you're
            commenting on
        :param int position: (required), line index in the diff to comment on
        :returns: bool
        """
        json = None
        if body and sha and path and line > 0 and position > 0:
            data = {'body': body, 'commit_id': sha, 'line': line,
                    'path': path, 'position': position}
            json = self._json(self._post(self._api, data=data), 200)

        if json:
            self._update_(json)
            return True
        return False
