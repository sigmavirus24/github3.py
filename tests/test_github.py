import github3
from mock import patch
from tests.utils import (generate_response, expect, BaseCase, load)


class TestGitHub(BaseCase):
    # This is needed due to the structure of @patch_request
    __name__ = 'TestGitHub'

    def test_authorization(self):
        self.request.return_value = generate_response('authorization')
        args = ('get', 'https://api.github.com/authorizations/10')
        with expect.githuberror():
            self.g.authorization(10)
        assert self.request.called is False

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
            repo.return_value = github3.repos.Repository(load('repo'),
                    self.g)
            i = self.g.create_issue('user', 'repo', 'Title')

        expect(i).isinstance(github3.issues.Issue)
        assert self.request.called is True

    def test_create_key(self):
        self.request.return_value = generate_response('key', 201)

        with expect.githuberror():
            k = self.g.create_key(None, None)
            assert k is None
        assert self.request.called is False

        self.login()
        k = self.g.create_key('Name', 'Key')
        expect(k).isinstance(github3.users.Key)
        assert self.request.called is True

    def test_create_repo(self):
        self.request.return_value = generate_response('repo', 201)
        self.login()
        r = self.g.create_repo('Repository')
        expect(r).isinstance(github3.repos.Repository)
        assert self.request.called is True

    def test_delete_key(self):
        self.request.return_value = generate_response(None, 204)

        self.login()
        with patch.object(github3.github.GitHub, 'key') as key:
            key.return_value = github3.users.Key(load('key'), self.g)
            assert self.g.delete_key(10) is True

        assert self.request.called is True

    def test_follow(self):
        self.request.return_value = generate_response(None, 204)
        args = ('put', 'https://api.github.com/user/following/sigmavirus24')
        conf = dict(headers={'Content-Length': '0'}, data=None)

        with expect.githuberror():
            self.g.follow('sigmavirus24')

        self.login()
        assert self.g.follow(None) is False
        assert self.g.follow('sigmavirus24') is True
        self.mock_assertions(*args, **conf)

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
        args = ('get',
                'https://api.github.com/repos/sigmavirus24/github3.py/issues/1'
               )

        assert self.g.issue(None, None, 0) is None
        with patch.object(github3.github.GitHub, 'repository') as repo:
            repo.return_value = github3.repos.Repository(load('repo'))
            i = self.g.issue('user', 'repo', 1)

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
        args = ('get', 'https://api.github.com/authorizations')
        self.conf.update(params=None)

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
        self.conf.update(params=None)

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
        self.conf.update(params=None)

        event = next(self.g.iter_events())
        expect(event).isinstance(github3.events.Event)
        self.mock_assertions(*args, **self.conf)

    def test_iter_followers(self):
        self.request.return_value = generate_response('user', _iter=True)
        args = ('get', 'https://api.github.com/users/sigmavirus24/followers')
        self.conf.update(params=None)

        with expect.githuberror():
            self.g.iter_followers()

        with patch.object(github3.github.GitHub, 'user') as ghuser:
            ghuser.return_value = github3.users.User(load('user'))
            u = next(self.g.iter_followers('sigmavirus24'))
            expect(u).isinstance(github3.users.User)
            assert self.request.called is True
            self.mock_assertions(*args, **self.conf)

            self.login()
            v = next(self.g.iter_followers())
            expect(v).isinstance(github3.users.User)
            args = (args[0], 'https://api.github.com/user/followers')
            assert self.request.called is True
            self.mock_assertions(*args, **self.conf)

    def test_iter_following(self):
        self.request.return_value = generate_response('user', _iter=True)
        args = ('get', 'https://api.github.com/users/sigmavirus24/following')
        self.conf.update(params=None)

        with expect.githuberror():
            next(self.g.iter_following())
        assert self.request.called is False

        with patch.object(github3.github.GitHub, 'user') as ghuser:
            ghuser.return_value = github3.users.User(load('user'))
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
        self.conf.update(params=None)

        g = next(self.g.iter_gists('sigmavirus24'))
        expect(g).isinstance(github3.gists.Gist)
        self.mock_assertions(*args, **self.conf)

        self.login()
        h = next(self.g.iter_gists())
        expect(h).isinstance(github3.gists.Gist)
        self.mock_assertions(*args, **self.conf)

    def test_iter_org_issues(self):
        self.request.return_value = generate_response('issue', _iter=True)
        args = ('get', 'https://api.github.com/orgs/github3py/issues')
        self.conf.update(params={})

        with expect.githuberror():
            self.g.iter_org_issues('github3py')

        self.login()
        i = next(self.g.iter_org_issues('github3py'))
        expect(i).isinstance(github3.issues.Issue)
        self.mock_assertions(*args, **self.conf)

        params = {'filter': 'assigned', 'state': 'closed', 'labels': 'bug',
                'sort': 'created', 'direction': 'asc',
                'since': '2012-05-20T23:10:27Z'}
        self.conf.update(params=params)
        j = next(self.g.iter_org_issues('github3py', **params))
        expect(j).isinstance(github3.issues.Issue)
        self.mock_assertions(*args, **self.conf)

    def test_iter_issues(self):
        self.request.return_value = generate_response('issue', _iter=True)
        args = ('get', 'https://api.github.com/issues')
        self.conf.update(params={})

        with expect.githuberror():
            self.g.iter_issues()

        self.login()
        expect(next(self.g.iter_issues())).isinstance(github3.issues.Issue)
        self.mock_assertions(*args, **self.conf)

        params = {'filter': 'assigned', 'state': 'closed', 'labels': 'bug',
                'sort': 'created', 'direction': 'asc',
                'since': '2012-05-20T23:10:27Z'}
        self.conf.update(params=params)
        expect(next(self.g.iter_issues(**params))).isinstance(
                github3.issues.Issue)
        self.mock_assertions(*args, **self.conf)

    def test_iter_user_issues(self):
        self.request.return_value = generate_response('issue', _iter=True)
        args = ('get', 'https://api.github.com/user/issues')
        self.conf.update(params={})

        with expect.githuberror():
            self.g.iter_user_issues()

        self.login()
        expect(next(self.g.iter_user_issues())).isinstance(
                github3.issues.Issue)
        self.mock_assertions(*args, **self.conf)

        params = {'filter': 'assigned', 'state': 'closed', 'labels': 'bug',
                'sort': 'created', 'direction': 'asc',
                'since': '2012-05-20T23:10:27Z'}
        self.conf.update(params=params)
        expect(next(self.g.iter_user_issues(**params))).isinstance(
                github3.issues.Issue)
        self.mock_assertions(*args, **self.conf)

    def test_iter_keys(self):
        self.request.return_value = generate_response('key', _iter=True)
        args = ('get', 'https://api.github.com/user/keys')
        self.conf.update(params=None)

        with expect.githuberror():
            self.g.iter_keys()

        self.login()
        expect(next(self.g.iter_keys())).isinstance(github3.users.Key)
        self.mock_assertions(*args, **self.conf)

    def test_iter_repos(self):
        self.request.return_value = generate_response('repo', _iter=True)
        args = ('get', 'https://api.github.com/user/repos')
        self.conf.update(params={})

        self.login()
        expect(next(self.g.iter_repos())).isinstance(github3.repos.Repository)
        self.mock_assertions(*args, **self.conf)

        args = ('get', 'https://api.github.com/users/sigmavirus24/repos')
        expect(next(self.g.iter_repos('sigmavirus24'))).isinstance(
                github3.repos.Repository)
        self.mock_assertions(*args, **self.conf)

    def test_iter_starred(self):
        self.request.return_value = generate_response('repo', _iter=True)
        args = ('get', 'https://api.github.com/user/starred')
        self.conf.update(params=None)

        self.login()
        expect(next(self.g.iter_starred())).isinstance(
                github3.repos.Repository)
        self.mock_assertions(*args, **self.conf)

        with patch.object(github3.github.GitHub, 'user') as user:
            user.return_value = github3.users.User(load('user'))
            args = ('get',
                    'https://api.github.com/users/sigmavirus24/starred')
            expect(next(self.g.iter_starred('sigmavirus24'))).isinstance(
                    github3.repos.Repository)
            self.mock_assertions(*args, **self.conf)

    def test_iter_subscribed(self):
        self.request.return_value = generate_response('repo', _iter=True)
        args = ('get', 'https://api.github.com/user/subscriptions')
        self.conf.update(params=None)

        self.login()
        expect(next(self.g.iter_subscribed())).isinstance(
                github3.repos.Repository)
        self.mock_assertions(*args, **self.conf)

        with patch.object(github3.github.GitHub, 'user') as user:
            user.return_value = github3.users.User(load('user'))
            args = ('get',
                    'https://api.github.com/users/sigmavirus24/subscriptions')
            expect(next(self.g.iter_subscribed('sigmavirus24'))).isinstance(
                    github3.repos.Repository)
            self.mock_assertions(*args, **self.conf)

    def test_login(self):
        self.g.login('user', 'password')
        expect(self.g._session.auth) == ('user', 'password')

        self.g.login(token='FakeOAuthToken')
        auth = self.g._session.headers.get('Authorization')
        expect(auth) == 'token FakeOAuthToken'

    # Unwritten test, not entirely sure how to mock this
    def test_markdown(self):
        pass

    def test_pull_request(self):
        self.request.return_value = generate_response('pull')
        args = ('get',
                'https://api.github.com/repos/sigmavirus24/github3.py/pulls/18'
               )
        pr = None

        with patch.object(github3.github.GitHub, 'repository') as repo:
            repo.return_value = github3.repos.Repository(load('repo'))
            pr = self.g.pull_request('sigmavirus24', 'github3.py', 18)

        expect(pr).isinstance(github3.pulls.PullRequest)

        self.mock_assertions(*args, **self.conf)

    def test_organization(self):
        self.request.return_value = generate_response('org')
        args = ('get', 'https://api.github.com/orgs/github3py')
        org = self.g.organization('github3py')
        expect(org).isinstance(github3.orgs.Organization)
        self.mock_assertions(*args, **self.conf)

    def test_repository(self):
        self.request.return_value = generate_response('repo')
        repo = self.g.repository(None, None)
        expect(repo).is_None()
        expect(self.request.called).is_False()

        args = ('get', 'https://api.github.com/repos/sigmavirus24/github3.py')
        repo = self.g.repository('sigmavirus24', 'github3.py')
        expect(repo).isinstance(github3.repos.Repository)
        self.mock_assertions(*args, **self.conf)

    def test_search_issues(self):
        self.request.return_value = generate_response('legacy_issue')
        args = ('get',
                'https://api.github.com/legacy/{0}/{1}/{2}/{3}/{4}/{5}'.format(
                    'issues', 'search', 'sigmavirus24', 'github3.py',
                    'closed', 'requests'
                    ))
        issues = self.g.search_issues('sigmavirus24', 'github3.py', 'closed',
                'requests')

        expect(issues[0]).isinstance(github3.legacy.LegacyIssue)
        self.mock_assertions(*args, **self.conf)
