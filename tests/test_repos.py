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
        self.request.return_value = generate_response('blob')
        sha = '3ceb856e2f14e9669fed6384e58c9a1590a2314f'
        self.args = ('get', self.api + 'git/blobs/' + sha)

        expect(self.repo.blob(sha)).isinstance(github3.git.Blob)
        self.mock_assertions()

    def test_branch(self):
        self.request.return_value = generate_response('branch')
        self.args = ('get', self.api + 'branches/master')

        expect(self.repo.branch('master')).isinstance(github3.repos.Branch)
        self.mock_assertions()

    def test_commit(self):
        self.request.return_value = generate_response('commit')
        sha = '76dcc6cb4b9860034be81b7e58adc286a115aa97'
        self.args = ('get', self.api + 'commits/' + sha)

        expect(self.repo.commit(sha)).isinstance(github3.repos.RepoCommit)
        self.mock_assertions()

    def test_commit_comment(self):
        self.request.return_value = generate_response('commit_comment')
        comment_id = 1380832
        self.args = ('get', self.api + 'comments/{0}'.format(comment_id))

        expect(self.repo.commit_comment(comment_id)
               ).isinstance(github3.repos.RepoComment)
        self.mock_assertions()

    def test_compare_commits(self):
        self.request.return_value = generate_response('comparison')
        base = 'a811e1a270f65eecb65755eca38d888cbefcb0a7'
        head = '76dcc6cb4b9860034be81b7e58adc286a115aa97'
        self.args = ('get', self.api + 'compare/{0}...{1}'.format(base, head))

        expect(self.repo.compare_commits(base, head)
               ).isinstance(github3.repos.Comparison)
        self.mock_assertions()

    def test_contents(self):
        self.request.return_value = generate_response('contents')
        filename = 'setup.py'
        self.args = ('get', self.api + 'contents/' + filename)

        expect(self.repo.contents(filename)).isinstance(github3.repos.Contents)
        self.mock_assertions()

    def test_create_blob(self):
        self.request.return_value = generate_response('blob', 201)
        content = 'VGVzdCBibG9i\n'
        encoding = 'base64'
        sha = '30f2c645388832f70d37ab2b47eb9ea527e5ae7c'
        self.args = ('post', self.api + 'git/blobs')
        self.conf = {'data': {'content': content, 'encoding': encoding}}

        with expect.githuberror():
            self.repo.create_blob(content, encoding)

        self.login()
        expect(self.repo.create_blob(None, None)) == ''
        expect(self.repo.create_blob(content, encoding)) == sha
        self.mock_assertions()
