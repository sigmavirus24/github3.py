import github3
from mock import patch, Mock
from tests.utils import (expect, BaseCase, load)

"""
http://github3py.readthedocs.org/en/0.7.0/github.html#github3.github.GitHub.authorize says scopes are required.

http://developer.github.com/v3/oauth/#create-a-new-authorization (at time of writing - 2013-09-06) disagrees
"""


class TestOptionalScope(BaseCase):
    def test_authorize_with_scope(self):
        """ Copypasted from TestGitHub """

        self.response('authorization', 201)
        scopes = ['scope1', 'scope2']

        self.g.authorize(None, None, scopes)
        self.not_called()

        a = self.g.authorize('user', 'password', scopes)
        expect(a).isinstance(github3.auths.Authorization)
        assert self.request.called is True

        self.request.reset_mock()

        self.login()
        a = self.g.authorize(None, None, scopes=scopes)

    def test_authorize_without_scope(self):
        self.response('authorization', 201)

        self.g.authorize(None, None)
        self.not_called()

        a = self.g.authorize('user', 'password')
        expect(a).isinstance(github3.auths.Authorization)
        assert self.request.called is True

        self.request.reset_mock()

        self.login()
        a = self.g.authorize(None, None)
