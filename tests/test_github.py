import github3
from json import load
from mock import patch
from tests.utils import (generate_response, expect, path, BaseCase)


class TestGitHub(BaseCase):
    # This is needed due to the structure of @patch_request
    __name__ = 'TestGitHub'

    def test_authorization(self):
        self.request.return_value = generate_response('authorization')
        args = ('get', 'https://api.github.com/authorizations/10')
        with expect.githuberror():
            self.g.authorization(10)

        self.login()
        a = self.g.authorization(10)
        expect(a).isinstance(github3.auths.Authorization)
        self.mock_assertions(*args, **self.conf)

    def test_authorize(self):
        self.request.return_value = generate_response('authorization', 201)
        scopes = ['scope1', 'scope2']

        self.g.authorize(None, None, scopes)
        assert self.request.called is False

        a = self.g.authorize('user', 'password', scopes)
        expect(a).isinstance(github3.auths.Authorization)
        assert self.request.called is True

    def test_create_gist(self):
        self.request.return_value = generate_response('gist', 201)

        g = self.g.create_gist('description', 'files')
        expect(g).isinstance(github3.gists.Gist)
        assert self.request.called is True

    def test_create_issue(self):
        self.request.return_value = generate_response('issue', 201)

        self.login()
        i = self.g.create_issue(None, None, None)
        assert i is None
        assert self.request.called is False

        i = self.g.create_issue('user', 'repo', '')
        assert i is None
        assert self.request.called is False

        with patch.object(github3.GitHub, 'repository') as repo:
            repo.return_value = github3.repos.Repository(load(path('repo')),
                    self.g)
            i = self.g.create_issue('user', 'repo', 'Title')

        expect(i).isinstance(github3.issues.Issue)
        assert self.request.called is True

    def test_create_key(self):
        self.request.return_value = generate_response('key', 201)

        k = self.g.create_key(None, None)
        assert k is None
        assert self.request.called is False

        self.login()
        k = self.g.create_key('Name', 'Key')
        expect(k).isinstance(github3.users.Key)
        assert self.request.called is True

    def test_create_repo(self):
        self.request.return_value = generate_response('repository', 201)
        self.login()
        r = self.g.create_repo('Repository')
        expect(r).isinstance(github3.repos.Repository)
        assert self.request.called is True

    def test_delete_key(self):
        self.request.return_value = generate_response(None, 204)
        args = ('delete', 'https://api.github.com/user/keys/10')

        self.login()
        with patch.object(github3.github.GitHub, 'key') as key:
            key.return_value = github3.users.Key(load(path('key')), self.g)
            assert self.g.delete_key(10) is True

        self.mock_assertions(*args, **self.conf)

    def test_follow(self):
        self.request.return_value = generate_response(None, 204)
        args = ('post', 'https://api.github.com/user/following/sigmavirus24')

        with expect.githuberror():
            self.g.follow('sigmavirus24')

        self.login()
        assert self.g.follow(None) is False
        assert self.g.follow('sigmavirus24') is True
        self.mock_assertions(*args, **self.conf)

    def test_gist(self):
        self.request.return_value = generate_response('gist', 200)
        args = ('get', 'https://api.github.com/gists/10')

        expect(self.g.gist(10)).isinstance(github3.gists.Gist)
        self.mock_assertions(*args, **self.conf)

    def test_is_starred(self):
        self.request.return_value = generate_response(None, 204)
        args = ('get', 'https://api.github.com/user/starred/user/repo')

        with expect.githuberror():
            self.g.is_starred('user', 'repo')

        self.login()
        expect(self.g.is_starred(None, None)).is_False()
        assert self.request.called is False

        expect(self.g.is_starred('user', 'repo')).is_True()
        self.mock_assertions(*args, **self.conf)

    def test_is_subscribed(self):
        self.request.return_value = generate_response(None, 204)
        args = ('get', 'https://api.github.com/user/subscriptions/user/repo')

        with expect.githuberror():
            self.g.is_subscribed('user', 'repo')

        self.login()
        expect(self.g.is_subscribed(None, None)).is_False()
        assert self.request.called is False

        expect(self.g.is_subscribed('user', 'repo')).is_True()
        self.mock_assertions(*args, **self.conf)

    def test_issue(self):
        self.request.return_value = generate_response('issue', 200)
        args = ('get', 'https://api.github.com/repos/user/repo/issues/1')

        assert self.g.issue(None, None) is None
        with patch.object(github3.github.GitHub, 'repository') as repo:
            repo.return_value = github3.repos.Repository(load(path('repo')))
            i = self.g.issue(1)

        expect(i).isinstance(github3.issues.Issue)
        self.mock_assertions(*args, **self.conf)

    def test_key(self):
        self.request.return_value = generate_response('key')
        args = ('get', 'https://api.github.com/user/keys/10')

        with expect.githuberror():
            self.g.key(10)
        assert self.request.called is False

        self.login()
        assert self.g.key(-1) is None
        assert self.request.called is False

        expect(self.g.key(10)).isinstance(github3.users.Key)
        self.mock_assertions(*args, **self.conf)

    def test_iter_authorizations(self):
        self.request.return_value = generate_response('authorization',
                _iter=True)
        args = ('get', 'https://api.github.com/user/authorizations')

        with expect.githuberror():
            self.g.iter_authorizations()
        assert self.request.called is False

        self.login()
        auth = next(self.g.iter_authorizations())
        expect(auth).isinstance(github3.auths.Authorization)
        self.mock_assertions(*args, **self.conf)

    def test_iter_emails(self):
        self.request.return_value = generate_response('emails')
        args = ('get', 'https://api.github.com/user/emails')

        with expect.githuberror():
            self.g.iter_emails()
        assert self.request.called is False

        self.login()
        email = next(self.g.iter_emails())
        expect(email) == 'user@example.com'
        self.mock_assertions(*args, **self.conf)

    def test_iter_events(self):
        self.request.return_value = generate_response('event', _iter=True)
        args = ('get', 'https://api.github.com/events')

        event = next(self.g.iter_events())
        expect(event).isinstance(github3.events.Event)
        self.mock_assertions(*args, **self.conf)

    def test_iter_followers(self):
        self.request.return_value = generate_response('user', _iter=True)
        args = ('get', 'https://api.github.com/users/sigmavirus24/followers')

        u = next(self.g.iter_followers('sigmavirus24'))
        expect(u).isinstance(github3.users.User)
        assert self.request.called is True
        self.mock_assertions(*args, **self.conf)

        with expect.githuberror():
            next(self.g.iter_followers())

        self.login()
        v = next(self.g.iter_followers())
        expect(v).isinstance(github3.users.User)
        args = (args[0], 'https://api.github.com/user/followers')
        assert self.request.called is True
        self.mock_assertions(*args, **self.conf)

    def test_iter_following(self):
        self.request.return_value = generate_response('user', _iter=True)
        args = ('get',
                'https://api.github.com/users/sigmavirus24/followering')

        with expect.githuberror():
            next(self.g.iter_following())
        assert self.request.called is False

        u = next(self.g.iter_following('sigmavirus24'))
        expect(u).isinstance(github3.users.User)
        self.mock_assertions(*args, **self.conf)

        self.login()
        v = next(self.g.iter_following())
        expect(v).isinstance(github3.users.User)
        args = (args[0], 'https://api.github.com/user/following')
        self.mock_assertions(*args, **self.conf)

    def test_iter_gists(self):
        self.request.return_value = generate_response('gist', _iter=True)
        args = ('get', 'https://api.github.com/users/sigmavirus24/gists')

        g = next(self.g.iter_gists('sigmavirus24'))
        expect(g).isinstance(github3.gists.Gist)
        self.mock_assertions(*args, **self.conf)

        self.login()
        h = next(self.g.iter_gists())
        expect(h).isinstance(github3.gists.Gist)
        self.mock_assertions(*args, **self.conf)
