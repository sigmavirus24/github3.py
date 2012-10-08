from github3.models import GitHubCore
from github3.repos import Repository


class Notification(GitHubCore):
    def __init__(self, notif, session=None):
        super(Notification, self).__init__(notif, session)
        self._api = notif.get('urls', {}).get('self', '')
        #: Comment responsible for the notification
        self.comment = notif.get('comment', {})
        #: Thread information
        self.thread = notif.get('thread', {})
        #: Repository the comment was made on
        self.repository = Repository(notif.get('repository', {}), self)
        #: When the thread was last updated
        self.updated_at = self._strptime(notif.get('updated_at'))
        #: Id of the thread
        self.id = notif.get('id')
        #: Dictionary of urls for the thread
        self.urls = notif.get('urls')
        #: datetime object representing the last time the user read the thread
        self.last_read_at = notif.get('last_read_at')
        if self.last_read_at:
            self.last_read_at = self._strptime(self.last_read_at)
        #: The reason you're receiving the notification
        self.reason = notif.get('reason')
        self._unread = notif.get('unread')

    def is_unread(self):
        """Tells you if the thread is unread or not."""
        return self._unread

    def mark(self):
        """Mark the thread as read.

        :returns: bool
        """
        return self._boolean(self._post(self.urls.get('mark')), 205, 404)

    # I suspect these three methods will be PUTs but I am weary to guess too
    # soon.
    def mute(self):
        """Mute the thread.

        :returns: bool
        """
        raise NotImplementedError

    def unmute(self):
        """Unmute the thread.

        :returns: bool
        """
        raise NotImplementedError
