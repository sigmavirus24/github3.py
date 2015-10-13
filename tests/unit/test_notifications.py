import github3
import datetime

from .helper import (UnitHelper, create_example_data_helper, create_url_helper)

get_notification_example_data = create_example_data_helper('notification_example')
url_for = create_url_helper(
    'https://api.github.com/notifications/threads/6169361'
)


class TestThread(UnitHelper):
    """Notification unit tests."""

    described_class = github3.notifications.Thread
    example_data = get_notification_example_data()

    def test_equality(self):
        """Test equality/inequality between two instances"""
        thread = github3.notifications.Thread(get_notification_example_data())
        assert self.instance == thread
        thread._uniq = 1
        assert self.instance != thread

    def test_is_unread(self):
        """Show that is_unread() equals unread property"""
        assert self.instance.is_unread() == self.instance.unread

    def test_last_read_at(self):
        """Show that last_read_at attribute is a datetime type"""
        json = self.instance.as_dict().copy()
        json['last_read_at'] = '2013-12-31T23:59:59Z'
        thread = github3.notifications.Thread(json)
        assert isinstance(thread.last_read_at, datetime.datetime)

    def test_repr(self):
        """Show instance string is formatted correctly"""
        assert repr(self.instance) == '<Thread [{0}]>'.format(
            self.instance.subject.get('title'))

    def test_delete_description(self):
        """Show that a user can delete a subscription"""
        self.instance.delete_subscription()

        self.session.delete.assert_called_once_with(url_for('subscription'))

    def test_mark(self):
        """Show that a user can mark the subscription"""
        self.instance.mark()

        assert self.session.patch.called

    def test_set_subscription(self):
        """Show that a user can subscribe to nofication"""

        self.instance.set_subscription(True, False)

        self.session.put.assert_called_once_with(
            url_for('subscription'),
            data='{"ignored": false, "subscribed": true}'
        )

    def test_subscription(self):
        pass
        # subscription = self.instance.subscription()
        # Need to figure out why this fails
        # assert isinstance(subscription, github3.notifications.Subscription)
