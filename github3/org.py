"""
github3.org
===========

This module contains all of the classes related to organizations.

"""

from .models import BaseAccount
from .user import User


class Organization(BaseAccount):
    def __init__(self, org, session):
        super(Organization, self).__init__(org, session)
        self._update_(org)
        if not self._type:
            self._type = 'Organization'

    @property
    def private_repos(self):
        return self._private_repos

    def edit(self,
        billing_email=None,
        company=None,
        email=None,
        location=None,
        name=None):
        """Edit this organization.

        :param billing_email: (optional) Billing email address (private)
        :param company: (optional)
        :param email: (optional) Public email address
        :param location: (optional)
        :param name: (optional)
        """
        resp = self._patch(self._api_url,
                dumps({'billing_email': billing_email,
                    'company': company, 'email': email,
                    'location': location,  'name': name}))
        if resp.status_code == 200:
            self._update_(resp.json)
            return True
        return False

    def list_members(self):
        """List members in this organization."""
        url = '/'.join([self._api_url, 'members'])
        users = []
        resp = self._get(url)
        if resp.status_code == 200:
            for user in resp.json:
                users.append(User(user, self._session))
        return users
