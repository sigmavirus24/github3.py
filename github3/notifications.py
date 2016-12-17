# -*- coding: utf-8 -*-
"""
github3.notifications
=====================

This module contains the classes relating to notifications.

See also: http://developer.github.com/v3/activity/notifications/
"""
from __future__ import unicode_literals

from json import dumps
from .models import GitHubCore


class Thread(GitHubCore):
    """The :class:`Thread <Thread>` object wraps notification threads. This
    contains information about the repository generating the notification, the
    subject, and the reason.

    Two thread instances can be checked like so::

        t1 == t2
        t1 != t2

    And is equivalent to::

        t1.id == t2.id
        t1.id != t2.id

    See also:
    http://developer.github.com/v3/activity/notifications/#view-a-single-thread
    """
    def _update_attributes(self, notif):
        self._api = self._get_attribute(notif, 'url')

        #: Comment responsible for the notification
        self.comment = self._get_attribute(notif, 'comment', {})

        #: Thread information
        self.thread = self._get_attribute(notif, 'thread', {})

        from .repos import Repository
        #: Repository the comment was made on
        self.repository = self._class_attribute(
            notif, 'repository', Repository, self
        )

        #: When the thread was last updated
        self.updated_at = self._strptime_attribute(notif, 'updated_at')

        #: Id of the thread
        self.id = self._get_attribute(notif, 'id')

        #: Dictionary of urls for the thread
        self.urls = self._get_attribute(notif, 'urls')

        #: datetime object representing the last time the user read the thread
        self.last_read_at = self._strptime_attribute(notif, 'last_read_at')

        #: The reason you're receiving the notification
        self.reason = self._get_attribute(notif, 'reason')

        #: Subject of the Notification, e.g., which issue/pull/diff is this in
        #: relation to. This is a dictionary
        self.subject = self._get_attribute(notif, 'subject')
        self.unread = self._get_attribute(notif, 'unread')

    def _repr(self):
        return '<Thread [{0}]>'.format(self.subject.get('title'))

    def delete_subscription(self):
        """Delete subscription for this thread.

        :returns: bool
        """
        url = self._build_url('subscription', base_url=self._api)
        return self._boolean(self._delete(url), 204, 404)

    def is_unread(self):
        """Tells you if the thread is unread or not."""
        return self.unread

    def mark(self):
        """Mark the thread as read.

        :returns: bool
        """
        return self._boolean(self._patch(self._api), 205, 404)

    def set_subscription(self, subscribed, ignored):
        """Set the user's subscription for this thread

        :param bool subscribed: (required), determines if notifications should
            be received from this thread.
        :param bool ignored: (required), determines if notifications should be
            ignored from this thread.
        :returns: :class:`Subscription <Subscription>`
        """
        url = self._build_url('subscription', base_url=self._api)
        sub = {'subscribed': subscribed, 'ignored': ignored}
        json = self._json(self._put(url, data=dumps(sub)), 200)
        return self._instance_or_null(Subscription, json)

    def subscription(self):
        """Checks the status of the user's subscription to this thread.

        :returns: :class:`Subscription <Subscription>`
        """
        url = self._build_url('subscription', base_url=self._api)
        json = self._json(self._get(url), 200)
        return self._instance_or_null(Subscription, json)


class Subscription(GitHubCore):

    """This object wraps thread and repository subscription information.

    See also:
    developer.github.com/v3/activity/notifications/#get-a-thread-subscription

    """

    def _update_attributes(self, sub):
        self._api = self._get_attribute(sub, 'url')

        #: reason user is subscribed to this thread/repository
        self.reason = self._get_attribute(sub, 'reason')

        #: datetime representation of when the subscription was created
        self.created_at = self._strptime_attribute(sub, 'created_at')

        #: API url of the thread if it exists
        self.thread_url = self._get_attribute(sub, 'thread_url')

        #: API url of the repository if it exists
        self.repository_url = self._get_attribute(sub, 'repository_url')

        self.ignored = self._get_attribute(sub, 'ignored', False)

        self.subscribed = self._get_attribute(sub, 'subscribed', False)

    def _repr(self):
        return '<Subscription [{0}]>'.format(self.subscribed)

    def delete(self):
        return self._boolean(self._delete(self._api), 204, 404)

    def is_ignored(self):
        return self.ignored

    def is_subscribed(self):
        return self.subscribed

    def set(self, subscribed, ignored):
        """Set the user's subscription for this subscription

        :param bool subscribed: (required), determines if notifications should
            be received from this thread.
        :param bool ignored: (required), determines if notifications should be
            ignored from this thread.
        """
        sub = {'subscribed': subscribed, 'ignored': ignored}
        json = self._json(self._put(self._api, data=dumps(sub)), 200)
        self._update_attributes(json)
