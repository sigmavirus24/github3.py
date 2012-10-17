import github3
from json import load
from mock import call, patch
from unittest import TestCase
from tests.utils import generate_response, expect, patch_request, path


class TestGitHub(TestCase):
    # This is needed due to the structure of @patch_request
    __name__ = 'TestGitHub'

    def setUp(self):
        self.g = github3.GitHub()

    @patch_request
    def test_authorization(self, request):
        request.return_value = generate_response('authorization')
        url = 'https://api.github.com/authorizations/10'
        with expect.raises(github3.GitHubError):
            self.g.authorization(10)

        self.g.login('user', 'password')
        a = self.g.authorization(10)
        expect(a).isinstance(github3.auths.Authorization)
        assert request.called is True
        assert call('get', url, allow_redirects=True) in request.mock_calls

    @patch_request
    def test_authorize(self, request):
        request.return_value = generate_response('authorization', 201)
        scopes = ['scope1', 'scope2']

        self.g.authorize(None, None, scopes)
        assert request.called is False

        a = self.g.authorize('user', 'password', scopes)
        expect(a).isinstance(github3.auths.Authorization)
        assert request.called is True

    @patch_request
    def test_create_gist(self, request):
        request.return_value = generate_response('gist', 201)

        g = self.g.create_gist('description', 'files')
        expect(g).isinstance(github3.gists.Gist)
        assert request.called is True

    @patch_request('post')
    def test_create_issue(self, request):
        request.return_value = generate_response('issue', 201)

        self.g.login('user', 'password')
        i = self.g.create_issue(None, None, None)
        assert i is None
        assert request.called is False

        i = self.g.create_issue('user', 'repo', '')
        assert i is None
        assert request.called is False

        with patch.object(github3.GitHub, 'repository') as repo:
            repo.return_value = github3.repos.Repository(load(path('repo')),
                    self.g)
            i = self.g.create_issue('user', 'repo', 'Title')

        expect(i).isinstance(github3.issues.Issue)
        assert request.called is True

    @patch_request
    def test_create_key(self, request):
        request.return_value = generate_response('key', 201)

        k = self.g.create_key(None, None)
        assert k is None
        assert request.called is False

        self.g.login('user', 'password')
        k = self.g.create_key('Name', 'Key')
        expect(k).isinstance(github3.users.Key)
        assert request.called is True

    @patch_request
    def test_create_repo(self, request):
        request.return_value = generate_response('repository', 201)
        self.g.login('user', 'password')
        r = self.g.create_repo('Repository')
        expect(r).isinstance(github3.repos.Repository)
        assert request.called is True

    @patch_request
    def test_delete_key(self, request):
        request.return_value = generate_response(None, 204)

        self.g.login('user', 'password')
        with patch.object(github3.github.GitHub, 'key') as key:
            key.return_value = github3.users.Key(load(path('key')), self.g)
            assert self.g.delete_key(10) is True

        assert request.called is True

    @patch_request
    def test_follow(self, request):
        request.return_value = generate_response(None, 204)

        with expect.raises(github3.GitHubError):
            self.g.follow('sigmavirus24')

        self.g.login('user', 'password')
        assert self.g.follow(None) is False
        assert self.g.follow('sigmavirus24') is True
        assert request.called is True

    @patch_request
    def test_key(self, request):
        request.return_value = generate_response('key')

        with expect.raises(github3.GitHubError):
            self.g.key(10)

        self.g.login('user', 'password')
        assert self.g.key(-1) is None
        assert request.called is False

        expect(self.g.key(10)).isinstance(github3.users.Key)
        assert request.called is True
