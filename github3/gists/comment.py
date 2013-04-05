from github3.models import BaseComment
from github3.users import User


class GistComment(BaseComment):
    """The :class:`GistComment <GistComment>` object. This represents a comment
    on a gist.

    See also: http://developer.github.com/v3/gists/comments/
    """
    def __init__(self, comment, session=None):
        super(GistComment, self).__init__(comment, session)

        #: :class:`User <github3.users.User>` who made the comment
        self.user = None
        if comment.get('user'):
            self.user = User(comment.get('user'), self)  # (No coverage)

    def __repr__(self):
        return '<Gist Comment [{0}]>'.format(self.user.login)
