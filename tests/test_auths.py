import github3
from tests.utils import (BaseCase, load)


class TestAuthorization(BaseCase):
    def __init__(self, methodName='runTest'):
        super(TestAuthorization, self).__init__(methodName)
        self.auth = github3.auths.Authorization(load('authorization'))
        self.api = "https://api.github.com/authorizations/10"

    def setUp(self):
        super(TestAuthorization, self).setUp()
        self.auth = github3.auths.Authorization(self.auth.as_dict(), self.g)

    def test_equality(self):
        a = github3.auths.Authorization(load('authorization'))
        assert self.auth == a
        a._uniq = 1
        assert self.auth != a

    def test_repr(self):
        assert repr(self.auth).startswith('<Authorization')

    def test_delete(self):
        self.response('', 204)
        self.delete(self.api)

        self.assertRaises(github3.GitHubError, self.auth.delete)
        self.not_called()

        self.login()
        assert self.auth.delete()
        self.mock_assertions()
