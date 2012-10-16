import github3
from json import load
from mock import call, patch
from unittest import TestCase
from mock_tests.utils import generate_response, expect, patch_request, path


class TestGitHub(TestCase):
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

    @patch_request
    def test_create_issue(self, request):
        request.return_value = generate_response('issue', 201)

        i = self.g.create_issue(None, None, None)
        assert i is None
        assert request.called is False

        i = self.g.create_issue('user', 'repo', '')
        assert i is None
        assert request.called is False

        with patch.object(github3.GitHub, 'repository') as repo:
            repo.return_value = github3.repos.Repository(load(path('repo')))
            i = self.g.create_issue('user', 'repo', 'Title')

        expect(i).isinstance(github3.issues.Issue)
        assert request.called is True
