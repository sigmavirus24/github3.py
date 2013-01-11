import github3
from mock import patch
from tests.utils import (expect, BaseCase, load)


class TestGitHub(BaseCase):
    def test_authorization(self):
        self.response('authorization')
        self.get('https://api.github.com/authorizations/10')
        with expect.githuberror():
            self.g.authorization(10)
        assert self.request.called is False

        self.login()
        a = self.g.authorization(10)
        expect(a).isinstance(github3.auths.Authorization)
        self.mock_assertions()

    def test_authorize(self):
        self.response('authorization', 201)
        scopes = ['scope1', 'scope2']

        self.g.authorize(None, None, scopes)
        assert self.request.called is False

        a = self.g.authorize('user', 'password', scopes)
        expect(a).isinstance(github3.auths.Authorization)
        assert self.request.called is True

    def test_create_gist(self):
        self.response('gist', 201)

        g = self.g.create_gist('description', 'files')
        expect(g).isinstance(github3.gists.Gist)
        assert self.request.called is True

    def test_create_issue(self):
        self.response('issue', 201)

        self.login()
        i = self.g.create_issue(None, None, None)
        assert i is None
        assert self.request.called is False

        i = self.g.create_issue('user', 'repo', '')
        assert i is None
        assert self.request.called is False

        with patch.object(github3.GitHub, 'repository') as repo:
            repo.return_value = github3.repos.Repository(
                load('repo'), self.g)
            i = self.g.create_issue('user', 'repo', 'Title')

        expect(i).isinstance(github3.issues.Issue)
        assert self.request.called is True

    def test_create_key(self):
        self.response('key', 201)

        with expect.githuberror():
            k = self.g.create_key(None, None)
            assert k is None
        assert self.request.called is False

        self.login()
        k = self.g.create_key('Name', 'Key')
        expect(k).isinstance(github3.users.Key)
        assert self.request.called is True

    def test_create_repo(self):
        self.response('repo', 201)
        self.login()
        r = self.g.create_repo('Repository')
        expect(r).isinstance(github3.repos.Repository)
        assert self.request.called is True

    def test_delete_key(self):
        self.response(None, 204)

        self.login()
        with patch.object(github3.github.GitHub, 'key') as key:
            key.return_value = github3.users.Key(load('key'), self.g)
            assert self.g.delete_key(10) is True

        assert self.request.called is True

    def test_follow(self):
        self.response(None, 204)
        self.put('https://api.github.com/user/following/sigmavirus24')
        self.conf = {'data': None}

        with expect.githuberror():
            self.g.follow('sigmavirus24')

        self.login()
        assert self.g.follow(None) is False
        assert self.g.follow('sigmavirus24') is True
        self.mock_assertions()

    def test_gist(self):
        self.response('gist', 200)
        self.get('https://api.github.com/gists/10')

        expect(self.g.gist(10)).isinstance(github3.gists.Gist)
        self.mock_assertions()

    def test_gitignore_template(self):
        self.response('template')
        self.get('https://api.github.com/gitignore/templates/Python')

        template = self.g.gitignore_template('Python')
        expect(template.startswith('*.py[cod]')).is_True()
        self.mock_assertions()

    def test_gitignore_templates(self):
        self.response('templates')
        self.get('https://api.github.com/gitignore/templates')

        expect(self.g.gitignore_templates()).isinstance(list)
        self.mock_assertions()

    def test_is_following(self):
        self.response(None, 204)
        self.get('https://api.github.com/user/following/login')

        with expect.githuberror():
            expect(self.g.is_following('login'))

        self.login()
        expect(self.g.is_following(None)).is_False()
        assert self.request.called is False

        expect(self.g.is_following('login')).is_True()
        self.mock_assertions()

    def test_is_starred(self):
        self.response(None, 204)
        self.get('https://api.github.com/user/starred/user/repo')

        with expect.githuberror():
            self.g.is_starred('user', 'repo')

        self.login()
        expect(self.g.is_starred(None, None)).is_False()
        assert self.request.called is False

        expect(self.g.is_starred('user', 'repo')).is_True()
        self.mock_assertions()

    def test_is_subscribed(self):
        self.response(None, 204)
        self.get('https://api.github.com/user/subscriptions/user/repo')

        with expect.githuberror():
            self.g.is_subscribed('user', 'repo')

        self.login()
        expect(self.g.is_subscribed(None, None)).is_False()
        assert self.request.called is False

        expect(self.g.is_subscribed('user', 'repo')).is_True()
        self.mock_assertions()

    def test_issue(self):
        self.response('issue', 200)
        self.get('https://api.github.com/repos/sigmavirus24/github3.py/'
                 'issues/1')

        assert self.g.issue(None, None, 0) is None
        with patch.object(github3.github.GitHub, 'repository') as repo:
            repo.return_value = github3.repos.Repository(load('repo'))
            i = self.g.issue('user', 'repo', 1)

        expect(i).isinstance(github3.issues.Issue)
        self.mock_assertions()

    def test_key(self):
        self.response('key')
        self.get('https://api.github.com/user/keys/10')

        with expect.githuberror():
            self.g.key(10)
        assert self.request.called is False

        self.login()
        assert self.g.key(-1) is None
        assert self.request.called is False

        expect(self.g.key(10)).isinstance(github3.users.Key)
        self.mock_assertions()

    def test_iter_all_repos(self):
        self.response('repo', _iter=True)
        self.get('https://api.github.com/repositories')
        self.conf.update(params=None)

        repo = next(self.g.iter_all_repos())
        expect(repo).isinstance(github3.repos.Repository)
        self.mock_assertions()

    def test_iter_all_users(self):
        self.response('user', _iter=True)
        self.get('https://api.github.com/users')
        self.conf.update(params=None)

        repo = next(self.g.iter_all_users())
        expect(repo).isinstance(github3.users.User)
        self.mock_assertions()

    def test_iter_authorizations(self):
        self.response('authorization', _iter=True)
        self.get('https://api.github.com/authorizations')
        self.conf.update(params=None)

        with expect.githuberror():
            self.g.iter_authorizations()
        assert self.request.called is False

        self.login()
        auth = next(self.g.iter_authorizations())
        expect(auth).isinstance(github3.auths.Authorization)
        self.mock_assertions()

    def test_iter_emails(self):
        self.response('emails', _iter=True)
        self.get('https://api.github.com/user/emails')
        self.conf.update(params=None)

        with expect.githuberror():
            self.g.iter_emails()
        assert self.request.called is False

        self.login()
        email = next(self.g.iter_emails())
        expect(email['email']) == 'graffatcolmingov@gmail.com'
        self.mock_assertions()

    def test_iter_events(self):
        self.response('event', _iter=True)
        self.get('https://api.github.com/events')
        self.conf.update(params=None)

        event = next(self.g.iter_events())
        expect(event).isinstance(github3.events.Event)
        self.mock_assertions()

    def test_iter_followers(self):
        self.response('user', _iter=True)
        self.get('https://api.github.com/users/sigmavirus24/followers')
        self.conf.update(params=None)

        with expect.githuberror():
            self.g.iter_followers()

        with patch.object(github3.github.GitHub, 'user') as ghuser:
            ghuser.return_value = github3.users.User(load('user'))
            u = next(self.g.iter_followers('sigmavirus24'))
            expect(u).isinstance(github3.users.User)
            assert self.request.called is True
            self.mock_assertions()

            self.login()
            v = next(self.g.iter_followers())
            expect(v).isinstance(github3.users.User)
            self.get('https://api.github.com/user/followers')
            assert self.request.called is True
            self.mock_assertions()

    def test_iter_following(self):
        self.response('user', _iter=True)
        self.get('https://api.github.com/users/sigmavirus24/following')
        self.conf.update(params=None)

        with expect.githuberror():
            next(self.g.iter_following())
        assert self.request.called is False

        with patch.object(github3.github.GitHub, 'user') as ghuser:
            ghuser.return_value = github3.users.User(load('user'))
            u = next(self.g.iter_following('sigmavirus24'))
            expect(u).isinstance(github3.users.User)
            self.mock_assertions()

            self.login()
            v = next(self.g.iter_following())
            expect(v).isinstance(github3.users.User)
            self.get('https://api.github.com/user/following')
            self.mock_assertions()

    def test_iter_gists(self):
        self.response('gist', _iter=True)
        self.get('https://api.github.com/users/sigmavirus24/gists')
        self.conf.update(params=None)

        g = next(self.g.iter_gists('sigmavirus24'))
        expect(g).isinstance(github3.gists.Gist)
        self.mock_assertions()

        self.login()
        h = next(self.g.iter_gists())
        expect(h).isinstance(github3.gists.Gist)
        self.get('https://api.github.com/gists')
        self.mock_assertions()

    def test_iter_org_issues(self):
        self.response('issue', _iter=True)
        self.get('https://api.github.com/orgs/github3py/issues')
        self.conf.update(params={})

        with expect.githuberror():
            self.g.iter_org_issues('github3py')

        self.login()
        i = next(self.g.iter_org_issues('github3py'))
        expect(i).isinstance(github3.issues.Issue)
        self.mock_assertions()

        params = {'filter': 'assigned', 'state': 'closed', 'labels': 'bug',
                  'sort': 'created', 'direction': 'asc',
                  'since': '2012-05-20T23:10:27Z'}
        self.conf.update(params=params)
        j = next(self.g.iter_org_issues('github3py', **params))
        expect(j).isinstance(github3.issues.Issue)
        self.mock_assertions()

    def test_iter_issues(self):
        self.response('issue', _iter=True)
        self.get('https://api.github.com/issues')
        self.conf.update(params={})

        with expect.githuberror():
            self.g.iter_issues()

        self.login()
        expect(next(self.g.iter_issues())).isinstance(github3.issues.Issue)
        self.mock_assertions()

        params = {'filter': 'assigned', 'state': 'closed', 'labels': 'bug',
                  'sort': 'created', 'direction': 'asc',
                  'since': '2012-05-20T23:10:27Z'}
        self.conf.update(params=params)
        expect(next(self.g.iter_issues(**params))).isinstance(
            github3.issues.Issue)
        self.mock_assertions()

    def test_iter_user_issues(self):
        self.response('issue', _iter=True)
        self.get('https://api.github.com/user/issues')
        self.conf.update(params={})

        with expect.githuberror():
            self.g.iter_user_issues()

        self.login()
        expect(next(self.g.iter_user_issues())).isinstance(
            github3.issues.Issue)
        self.mock_assertions()

        params = {'filter': 'assigned', 'state': 'closed', 'labels': 'bug',
                  'sort': 'created', 'direction': 'asc',
                  'since': '2012-05-20T23:10:27Z'}
        self.conf.update(params=params)
        expect(next(self.g.iter_user_issues(**params))).isinstance(
            github3.issues.Issue)
        self.mock_assertions()

    def test_iter_repo_issues(self):
        self.response('issue', _iter=True)
        self.get('https://api.github.com/repos/sigmavirus24/github3.py/'
                 'issues')

        with patch.object(github3.GitHub, 'repository') as repo:
            repo.return_value = github3.repos.Repository(load('repo'),
                                                         self.g)
            i = next(self.g.iter_repo_issues('sigmavirus24', 'github3.py'))

        expect(i).isinstance(github3.issues.Issue)
        self.mock_assertions()

    def test_iter_keys(self):
        self.response('key', _iter=True)
        self.get('https://api.github.com/user/keys')
        self.conf.update(params=None)

        with expect.githuberror():
            self.g.iter_keys()

        self.login()
        expect(next(self.g.iter_keys())).isinstance(github3.users.Key)
        self.mock_assertions()

    def test_iter_orgs(self):
        self.response('org', _iter=True)
        self.get('https://api.github.com/users/login/orgs')

        expect(next(self.g.iter_orgs('login'))).isinstance(
            github3.orgs.Organization)
        self.mock_assertions()

        self.get('https://api.github.com/user/orgs')
        self.login()
        expect(next(self.g.iter_orgs())).isinstance(github3.orgs.Organization)
        self.mock_assertions()

    def test_iter_repos(self):
        self.response('repo', _iter=True)
        self.get('https://api.github.com/user/repos')
        self.conf.update(params={})

        self.login()
        expect(next(self.g.iter_repos())).isinstance(github3.repos.Repository)
        self.mock_assertions()

        self.get('https://api.github.com/users/sigmavirus24/repos')
        expect(next(self.g.iter_repos('sigmavirus24'))).isinstance(
            github3.repos.Repository)
        self.mock_assertions()

    def test_iter_repos_sort(self):
        self.response('repo', _iter=True)
        self.conf.update(params={"sort": "created"})

        self.login()
        self.get('https://api.github.com/user/repos')
        expect(next(self.g.iter_repos(sort="created"))
               ).isinstance(github3.repos.Repository)
        self.mock_assertions()

        self.get('https://api.github.com/users/sigmavirus24/repos')
        expect(next(self.g.iter_repos('sigmavirus24', sort="created"))
               ).isinstance(github3.repos.Repository)
        self.mock_assertions()

    def test_iter_starred(self):
        self.response('repo', _iter=True)
        self.get('https://api.github.com/user/starred')
        self.conf.update(params=None)

        self.login()
        expect(next(self.g.iter_starred())).isinstance(
            github3.repos.Repository)
        self.mock_assertions()

        with patch.object(github3.github.GitHub, 'user') as user:
            user.return_value = github3.users.User(load('user'))
            self.get('https://api.github.com/users/sigmavirus24/starred')
            expect(next(self.g.iter_starred('sigmavirus24'))).isinstance(
                github3.repos.Repository)
            self.mock_assertions()

    def test_iter_subscriptions(self):
        self.response('repo', _iter=True)
        self.get('https://api.github.com/user/subscriptions')
        self.conf.update(params=None)

        self.login()
        expect(next(self.g.iter_subscriptions())).isinstance(
            github3.repos.Repository)
        self.mock_assertions()

        with patch.object(github3.github.GitHub, 'user') as user:
            user.return_value = github3.users.User(load('user'))
            self.get('https://api.github.com/users/sigmavirus24/'
                     'subscriptions')
            expect(next(self.g.iter_subscriptions('sigmavirus24'))).isinstance(
                github3.repos.Repository)
            self.mock_assertions()

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
        self.response('pull')
        self.get('https://api.github.com/repos/sigmavirus24/'
                 'github3.py/pulls/18')
        pr = None

        with patch.object(github3.github.GitHub, 'repository') as repo:
            repo.return_value = github3.repos.Repository(load('repo'))
            pr = self.g.pull_request('sigmavirus24', 'github3.py', 18)

        expect(pr).isinstance(github3.pulls.PullRequest)

        self.mock_assertions()

    def test_organization(self):
        self.response('org')
        self.get('https://api.github.com/orgs/github3py')
        org = self.g.organization('github3py')
        expect(org).isinstance(github3.orgs.Organization)
        self.mock_assertions()

    def test_repository(self):
        self.response('repo')
        repo = self.g.repository(None, None)
        expect(repo).is_None()
        self.not_called()

        self.get('https://api.github.com/repos/sigmavirus24/github3.py')
        repo = self.g.repository('sigmavirus24', 'github3.py')
        expect(repo).isinstance(github3.repos.Repository)
        self.mock_assertions()

    def test_search_issues(self):
        self.response('legacy_issue')
        self.get('https://api.github.com/legacy/{0}/{1}/{2}/{3}/{4}/'
                 '{5}'.format('issues', 'search', 'sigmavirus24',
                              'github3.py', 'closed', 'requests'))
        self.conf.update({'params': {}})
        issues = self.g.search_issues('sigmavirus24', 'github3.py', 'closed',
                                      'requests')

        expect(issues[0]).isinstance(github3.legacy.LegacyIssue)
        self.mock_assertions()

        self.conf.update({'params': {'start_page': 2}})
        issues = self.g.search_issues('sigmavirus24', 'github3.py', 'closed',
                                      'requests', 2)
        self.mock_assertions()

    def test_search_repos(self):
        self.response('legacy_repo')
        self.get('https://api.github.com/{0}/{1}/{2}/{3}'.format(
                 'legacy', 'repos', 'search', 'github3.py'))
        self.conf.update(params={})
        repos = self.g.search_repos('github3.py')
        expect(repos[0]).isinstance(github3.legacy.LegacyRepo)
        self.mock_assertions()

        self.conf.update(params={'language': 'python'})
        repos = self.g.search_repos('github3.py', language='python')
        self.mock_assertions()

    def test_search_users(self):
        self.response('legacy_user')
        self.get('https://api.github.com/{0}/{1}/{2}/{3}'.format(
                 'legacy', 'user', 'search', 'sigmavirus24'))
        self.conf.update({'params': {}})
        users = self.g.search_users('sigmavirus24')
        expect(users[0]).isinstance(github3.legacy.LegacyUser)
        self.mock_assertions()

        self.conf.update({'params': {'start_page': 2}})
        self.g.search_users('sigmavirus24', 2)
        self.mock_assertions()

    def test_search_email(self):
        self.response('legacy_email')
        self.get('https://api.github.com/{0}/{1}/{2}/{3}'.format(
                 'legacy', 'user', 'email', 'graffatcolmingov@gmail.com'))
        user = self.g.search_email('graffatcolmingov@gmail.com')
        expect(user).isinstance(github3.legacy.LegacyUser)
        self.mock_assertions()

    def test_set_client_id(self):
        auth = ('idXXXXXXXXXXXX', 'secretXXXXXXXXXXXXXXXX')
        self.g.set_client_id(*auth)
        expect(self.g._session.params['client_id']) == auth[0]
        expect(self.g._session.params['client_secret']) == auth[1]

    def test_set_user_agent(self):
        ua = 'Fake User Agents'
        self.g.set_user_agent(ua)
        expect(self.g._session.headers['User-Agent']) == ua

    def test_star(self):
        self.response('', 204)
        self.put('https://api.github.com/user/starred/sigmavirus24/github3.py')
        self.conf = {'data': None}

        with expect.githuberror():
            self.g.star('foo', 'bar')

        self.login()
        expect(self.g.star(None, None)).is_False()
        expect(self.g.star('sigmavirus24', 'github3.py')).is_True()
        self.mock_assertions()

    def test_subscribe(self):
        self.response('', 204)
        self.put('https://api.github.com/user/subscriptions/'
                 'sigmavirus24/github3.py')
        self.conf = {'data': None}

        with expect.githuberror():
            self.g.subscribe('foo', 'bar')

        self.login()
        expect(self.g.subscribe(None, None)).is_False()
        expect(self.g.subscribe('sigmavirus24', 'github3.py')).is_True()
        self.mock_assertions()

    def test_unfollow(self):
        self.response('', 204)
        self.delete('https://api.github.com/user/following/'
                    'sigmavirus24')
        self.conf = {}

        with expect.githuberror():
            self.g.unfollow('foo')

        self.login()
        expect(self.g.unfollow(None)).is_False()
        expect(self.g.unfollow('sigmavirus24')).is_True()
        self.mock_assertions()

    def test_unstar(self):
        self.response('', 204)
        self.delete('https://api.github.com/user/starred/'
                    'sigmavirus24/github3.py')
        self.conf = {}

        with expect.githuberror():
            self.g.unstar('foo', 'bar')

        self.login()
        expect(self.g.unstar(None, None)).is_False()
        expect(self.g.unstar('sigmavirus24', 'github3.py')).is_True()
        self.mock_assertions()

    def test_unsubscribe(self):
        self.response('', 204)
        self.delete('https://api.github.com/user/subscriptions/'
                    'sigmavirus24/github3.py')
        self.conf = {}

        with expect.githuberror():
            self.g.unsubscribe('foo', 'bar')

        self.login()
        expect(self.g.unsubscribe(None, None)).is_False()
        expect(self.g.unsubscribe('sigmavirus24', 'github3.py')).is_True()
        self.mock_assertions()

    def test_update_user(self):
        self.login()
        args = ('Ian Cordasco', 'example@mail.com', 'www.blog.com', 'company',
                'loc', True, 'bio')

        with patch.object(github3.github.GitHub, 'user') as user:
            with patch.object(github3.users.User, 'update') as upd:
                user.return_value = github3.users.User(load('user'), self.g)
                upd.return_value = True
                expect(self.g.update_user(*args)).is_True()
                expect(user.called).is_True()
                expect(upd.called).is_True()
                upd.assert_called_with(*args)

    def test_user(self):
        self.response('user')
        self.get('https://api.github.com/users/sigmavirus24')

        expect(self.g.user('sigmavirus24')).isinstance(github3.users.User)
        self.mock_assertions()

        self.get('https://api.github.com/user')
        self.login()
        expect(self.g.user()).isinstance(github3.users.User)
        self.mock_assertions()

    def test_utf8_user(self):
        self.response('utf8_user')
        self.get('https://api.github.com/users/alejandrogomez')

        u = self.g.user('alejandrogomez')

        try:
            repr(u)
        except UnicodeEncodeError:
            self.fail('Regression caught. See PR #52. Names must be utf-8'
                      ' encoded')

    # no test_zen
