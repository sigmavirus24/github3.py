import github3
try:
    from unittest.mock import patch
except ImportError:
    from mock import patch
from tests.utils import (BaseCase, load)
from datetime import datetime


class TestPlan(BaseCase):
    def __init__(self, methodName='runTest'):
        super(TestPlan, self).__init__(methodName)
        self.plan = github3.users.Plan({
            'name': 'free',
            'space': 400,
            'collaborators': 10,
            'private_repos': 20,
        })

    def test_str(self):
        assert str(self.plan) == self.plan.name
        assert repr(self.plan) == '<Plan [free]>'
        assert self.plan.is_free()


class TestUserEmail(BaseCase):
    def __init__(self, methodName='runTest'):
        super(TestUserEmail, self).__init__(methodName)
        self.useremail = github3.users.UserEmail({
            'email': 'test@email.com',
            'verified': True,
            'primary': True,
        })

    def test_str(self):
        assert str(self.useremail) == self.useremail.email
        assert repr(self.useremail) == '<UserEmail [test@email.com]>'


class TestUser(BaseCase):
    def __init__(self, methodName='runTest'):
        super(TestUser, self).__init__(methodName)
        self.user = github3.users.User(load('user'))
        self.api = "https://api.github.com/users/sigmavirus24"

    def setUp(self):
        super(TestUser, self).setUp()
        self.user = github3.users.User(self.user.as_dict(), self.g)
        if hasattr(self.user.name, 'decode'):
            self.user.name = self.user.name.decode('utf-8')

    def test_refresh(self):
        """This sort of tests all instances of refresh for good measure."""
        self.response('', 304)
        self.get(self.api)
        self.user.last_modified = last_modified = datetime.now().strftime(
            '%a, %d %b %Y %H:%M:%S GMT'
        )
        self.user.etag = etag = '644b5b0155e6404a9cc4bd9d8b1ae730'

        expected_headers = {
            'If-Modified-Since': last_modified,
        }

        self.user.refresh(True)
        self.request.assert_called_with('GET', self.api,
                                        headers=expected_headers,
                                        allow_redirects=True)

        self.user.last_modified = None
        expected_headers = {
            'If-None-Match': etag
        }

        self.user.refresh(True)
        self.request.assert_called_with('GET', self.api,
                                        headers=expected_headers,
                                        allow_redirects=True)

        self.response('user', 200)
        self.user.refresh()
        self.mock_assertions()

    def test_str(self):
        assert str(self.user) == 'sigmavirus24'
        assert repr(self.user) == '<User [sigmavirus24:Ian Cordasco]>'

    def test_add_email_address(self):
        self.assertRaises(github3.GitHubError, self.user.add_email_address,
                          'foo')

        self.not_called()
        self.login()
        with patch.object(github3.users.User, 'add_email_addresses') as p:
            self.user.add_email_address('foo')
            p.assert_called_once_with(['foo'])

    def test_add_email_addresses(self):
        self.response('emails', 201, _iter=True)
        self.post(self.github_url + 'user/emails')
        self.conf = {
            'data': '["foo@bar.com"]',
        }

        self.assertRaises(github3.GitHubError, self.user.add_email_addresses,
                          [])

        self.not_called()
        self.login()

        self.user.add_email_addresses(['foo@bar.com'])
        self.mock_assertions()

    def test_delete_email_address(self):
        self.assertRaises(github3.GitHubError, self.user.delete_email_address,
                          'foo')

        self.not_called()
        self.login()
        with patch.object(github3.users.User, 'delete_email_addresses') as p:
            self.user.delete_email_address('foo')
            p.assert_called_once_with(['foo'])

    def test_delete_email_addresses(self):
        self.response('', 204)
        self.delete(self.github_url + 'user/emails')
        self.conf = {
            'data': '["foo@bar.com"]'
        }

        self.assertRaises(github3.GitHubError,
                          self.user.delete_email_addresses,
                          [])

        self.not_called()
        self.login()
        assert self.user.delete_email_addresses(['foo@bar.com'])
        self.mock_assertions()

    def test_is_assignee_on(self):
        self.response('', 404)
        self.get(self.github_url + 'repos/abc/def/assignees/sigmavirus24')

        assert self.user.is_assignee_on('abc', 'def') is False
        self.mock_assertions()

    def test_is_following(self):
        self.response('', 204)
        self.get(self.api + '/following/kennethreitz')

        assert self.user.is_following('kennethreitz')
        self.mock_assertions()

    def test_equality(self):
        u = github3.users.User(load('user'))
        assert self.user == u
        u._uniq += 1
        assert self.user != u
