import github3
from tests.utils import BaseCase

"""
http://github3py.readthedocs.org/en/0.7.0/github.html#github3.github.GitHub
says scopes are required to create an authorization.

http://developer.github.com/v3/oauth/#create-a-new-authorization (at time of
writing - 2013-09-06) disagrees
"""


class TestOptionalScope(BaseCase):
    def test_authorize_with_scope(self):
        """ Copypasted from TestGitHub """

        self.response('authorization', 201)
        scopes = ['scope1', 'scope2']

        self.g.authorize(None, None, scopes)
        self.not_called()

        a = self.g.authorize('user', 'password', scopes)
        assert isinstance(a, github3.auths.Authorization)
        assert self.request.called is True

        self.request.reset_mock()

        self.login()
        a = self.g.authorize(None, None, scopes=scopes)

    def test_authorize_without_scope(self):
        self.response('authorization', 201)

        self.g.authorize(None, None)
        self.not_called()

        a = self.g.authorize('user', 'password')
        assert isinstance(a, github3.auths.Authorization)
        assert self.request.called is True

        self.request.reset_mock()

        self.login()
        a = self.g.authorize(None, None)
