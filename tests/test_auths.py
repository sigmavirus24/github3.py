import github3
from tests.utils import (BaseCase, load)


class TestAuthorization(BaseCase):
    def __init__(self, methodName='runTest'):
        super(TestAuthorization, self).__init__(methodName)
        self.auth = github3.auths.Authorization(load('authorization'))
        self.api = "https://api.github.com/authorizations/10"

    def setUp(self):
        super(TestAuthorization, self).setUp()
        self.auth = github3.auths.Authorization(self.auth.to_json(), self.g)

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

    def test_update(self):
        self.response('authorization', 200)
        self.post(self.api)
        data = {
            'scopes': ['user']
        }
        self.conf = {'data': data}

        self.assertRaises(github3.GitHubError, self.auth.update)

        def sub_test():
            assert self.auth.update(**data)
            self.mock_assertions()

        self.login()
        assert self.auth.update() is False
        self.not_called()

        sub_test()

        del(data['scopes'])
        data['add_scopes'] = ['repo']
        sub_test()

        del(data['add_scopes'])
        data['rm_scopes'] = ['user']
        self.conf['data'] = {'remove_scopes': ['user']}
        sub_test()
        self.conf['data'] = data

        del(data['rm_scopes'])
        data['note'] = 'GitHub API'
        data['note_url'] = 'http://example.com'
        sub_test()
