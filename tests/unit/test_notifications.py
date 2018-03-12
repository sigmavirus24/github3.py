"""Unit tests around the Thread class."""
import github3

from .helper import (UnitHelper, create_example_data_helper, create_url_helper)

get_example_data = create_example_data_helper('notification_example')
url_for = create_url_helper(
    'https://api.github.com/notifications/threads/1'
)


class TestThread(UnitHelper):
    """Notification unit tests."""

    described_class = github3.notifications.Thread
    example_data = get_example_data()

    def test_equality(self):
        """Test equality/inequality between two instances."""
        thread = github3.notifications.Thread(get_example_data(), self.session)
        assert self.instance == thread
        thread._uniq = 1
        assert self.instance != thread

    def test_repr(self):
        """Show instance string is formatted correctly."""
        assert repr(self.instance) == '<Thread [{0}]>'.format(
            self.instance.subject.get('title'))

    def test_delete_subscription(self):
        """Show that a user can delete a subscription."""
        self.instance.delete_subscription()

        self.session.delete.assert_called_once_with(url_for('subscription'))

    def test_mark(self):
        """Show that a user can mark the subscription."""
        self.instance.mark()

        self.session.patch.assert_called_once_with(url_for())

    def test_set_subscription(self):
        """Show that a user can subscribe to notification."""
        self.instance.set_subscription(True, False)

        self.put_called_with(
            url_for('subscription'),
            data={"ignored": False, "subscribed": True},
        )

    def test_subscription(self):
        """Show that a user can retrieve a subscription."""
        self.instance.subscription()

        self.session.get.assert_called_once_with(
            url_for('subscription'),
        )
