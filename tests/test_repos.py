import github3
from tests.utils import (generate_response, expect, BaseCase, load)


class TestRepository(BaseCase):
    def __init__(self, methodName='runTest'):
        super(TestRepository, self).__init__(methodName)
        self.repo = github3.repos.Repository(load('repo'))

    def setUp(self):
        super(TestRepository, self).setUp()
        self.repo = github3.repos.Repository(self.repo.to_json(), self.g)
        self.api = 'https://api.github.com/repos/sigmavirus24/github3.py/'

    def test_add_collaborator(self):
        self.request.return_value = generate_response('', 204)
        self.args = ('put', self.api + 'collaborators/sigmavirus24')
        self.conf = {'headers': {'Content-Length': '0'}, 'data': None}

        with expect.githuberror():
            self.repo.add_collaborator('foo')

        self.login()
        expect(self.repo.add_collaborator(None)).is_False()
        expect(self.repo.add_collaborator('sigmavirus24')).is_True()
        self.mock_assertions()

    def test_archive(self):
        pass

    def test_blob(self):
        self.request.return_value = generate_response('blob', 200)
        self.args = ('get',
                     self.api + ('git/blobs/'
                                 '3ceb856e2f14e9669fed6384e58c9a1590a2314f')
                     )

        expect(self.repo.blob('3ceb856e2f14e9669fed6384e58c9a1590a2314f')
               ).isinstance(github3.git.Blob)
        self.mock_assertions()

    def test_branch(self):
        self.request.return_value = generate_response('branch', 200)
        self.args = ('get', self.api + 'branches/master')

        expect(self.repo.branch('master')).isinstance(github3.repos.Branch)
        self.mock_assertions()
