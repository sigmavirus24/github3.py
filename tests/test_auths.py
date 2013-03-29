import github3
from tests.utils import (expect, BaseCase, load)


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
        expect(self.auth) == a
        a.id = 1
        expect(self.auth) != a

    def test_repr(self):
        expect(repr(self.auth).startswith('<Authorization')).is_True()

    def test_delete(self):
        self.response('', 204)
        self.delete(self.api)

        with expect.githuberror():
            self.auth.delete()
        self.not_called()

        self.login()
        expect(self.auth.delete()).is_True()
        self.mock_assertions()

    def test_update(self):
        self.response('authorization', 200)
        self.post(self.api)
        data = {
            'scopes': ['user']
        }
        self.conf = {'data': data}

        with expect.githuberror():
            self.auth.update()

        def sub_test():
            expect(self.auth.update(**data)).is_True()
            self.mock_assertions()

        self.login()
        expect(self.auth.update()).is_False()
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
