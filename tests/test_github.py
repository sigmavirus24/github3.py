import github3
from mock import patch, Mock
from tests.utils import (BaseCase, load)


def merge(first, second=None, **kwargs):
    copy = first.copy()
    copy.update(second or {})
    copy.update(kwargs)
    return copy


class TestGitHub(BaseCase):
    def test_init(self):
        g = github3.GitHub('foo', 'bar')
        assert repr(g).endswith('[foo]>')

        g = github3.GitHub(token='foo')
        assert repr(g).endswith('{0:x}>'.format(id(g)))

    def test_context_manager(self):
        with github3.GitHub() as gh:
            gh.__exit__ = Mock()
            assert isinstance(gh, github3.GitHub)

        gh.__exit__.assert_called()

    def test_authorization(self):
        self.response('authorization')
        self.get('https://api.github.com/authorizations/10')
        self.assertRaises(github3.GitHubError, self.g.authorization, 10)
        assert self.request.called is False

        self.login()
        a = self.g.authorization(10)
        assert isinstance(a, github3.auths.Authorization)
        self.mock_assertions()

    def test_authorize(self):
        self.response('authorization', 201)
        scopes = ['scope1', 'scope2']

        self.g.authorize(None, None, scopes)
        self.not_called()

        a = self.g.authorize('user', 'password', scopes)
        assert isinstance(a, github3.auths.Authorization)
        assert self.request.called is True

        self.request.reset_mock()

        self.login()
        a = self.g.authorize(None, None, scopes=scopes)

    def test_check_authorization(self):
        self.response('', 200)
        self.get('https://api.github.com/applications/fake_id/tokens/'
                 'access_token')
        self.conf = {
            'params': {'client_id': None, 'client_secret': None},
            'auth': ('fake_id', 'fake_secret'),
        }

        assert self.g.check_authorization(None) is False
        self.not_called()

        self.g.set_client_id('fake_id', 'fake_secret')
        assert self.g.check_authorization('access_token')
        self.mock_assertions()

    def test_create_gist(self):
        self.response('gist', 201)

        g = self.g.create_gist('description', 'files')
        assert isinstance(g, github3.gists.Gist)
        assert self.request.called is True
        #with Betamax(self.session).use_cassette('GitHub_create_gist'):
        #    self.g.create_gist(
        #        'description of test_gist', {
        #            'filename': 'contents'
        #        })

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

        assert isinstance(i, github3.issues.Issue)
        assert self.request.called is True

    def test_create_key(self):
        self.response('key', 201)

        self.assertRaises(github3.GitHubError, self.g.create_key, None, None)
#            k = self.g.create_key(None, None)
#            assert k is None
        assert self.request.called is False

        self.login()
        k = self.g.create_key('Name', 'Key')

        assert isinstance(k, github3.users.Key)
        assert self.request.called is True

    def test_create_repo(self):
        self.response('repo', 201)
        self.login()
        r = self.g.create_repo('Repository')
        assert isinstance(r, github3.repos.Repository)
        assert self.request.called is True

    def test_delete_key(self):
        self.response(None, 204)

        self.login()
        with patch.object(github3.github.GitHub, 'key') as key:
            key.return_value = github3.users.Key(load('key'), self.g)
            assert self.g.delete_key(10) is True
            key.return_value = None
            assert self.g.delete_key(10) is False

        assert self.request.called is True

    def test_follow(self):
        self.response(None, 204)
        self.put('https://api.github.com/user/following/sigmavirus24')
        self.conf = {'data': None}

        self.assertRaises(github3.GitHubError, self.g.follow, 'sigmavirus24')

        self.login()
        assert self.g.follow(None) is False
        assert self.g.follow('sigmavirus24') is True
        self.mock_assertions()

    def test_gist(self):
        self.response('gist', 200)
        self.get('https://api.github.com/gists/10')

        assert isinstance(self.g.gist(10), github3.gists.Gist)
        self.mock_assertions()

    def test_gitignore_template(self):
        self.response('template')
        self.get('https://api.github.com/gitignore/templates/Python')

        template = self.g.gitignore_template('Python')

        assert template.startswith('*.py[cod]')
        self.mock_assertions()

    def test_gitignore_templates(self):
        self.response('templates')
        self.get('https://api.github.com/gitignore/templates')

        assert isinstance(self.g.gitignore_templates(), list)
        self.mock_assertions()

    def test_is_following(self):
        self.response(None, 204)
        self.get('https://api.github.com/user/following/login')

        self.assertRaises(github3.GitHubError, self.g.is_following, 'login')

        self.login()
        assert self.g.is_following(None) is False
        assert self.request.called is False

        assert self.g.is_following('login')
        self.mock_assertions()

    def test_is_starred(self):
        self.response(None, 204)
        self.get('https://api.github.com/user/starred/user/repo')

        self.assertRaises(github3.GitHubError, self.g.is_starred,
                          'user', 'repo')

        self.login()

        assert self.g.is_starred(None, None) is False
        assert self.request.called is False

        assert self.g.is_starred('user', 'repo') is True
        self.mock_assertions()

    def test_is_subscribed(self):
        self.response(None, 204)
        self.get('https://api.github.com/user/subscriptions/user/repo')

        self.assertRaises(github3.GitHubError, self.g.is_subscribed,
                          'user', 'repo')

        self.login()
        assert self.g.is_subscribed(None, None) is False
        assert self.request.called is False

        assert self.g.is_subscribed('user', 'repo')
        self.mock_assertions()

    def test_issue(self):
        self.response('issue', 200)
        self.get('https://api.github.com/repos/sigmavirus24/github3.py/'
                 'issues/1')

        assert self.g.issue(None, None, 0) is None
        with patch.object(github3.github.GitHub, 'repository') as repo:
            repo.return_value = github3.repos.Repository(load('repo'))
            i = self.g.issue('user', 'repo', 1)

        assert isinstance(i, github3.issues.Issue)
        self.mock_assertions()

    def test_key(self):
        self.response('key')
        self.get('https://api.github.com/user/keys/10')

        self.assertRaises(github3.GitHubError, self.g.key, 10)
        assert self.request.called is False

        self.login()
        assert self.g.key(-1) is None
        assert self.request.called is False

        assert isinstance(self.g.key(10), github3.users.Key)
        self.mock_assertions()

    def test_iter_all_repos(self):
        self.response('repo', _iter=True)
        self.get('https://api.github.com/repositories')
        self.conf.update(params={'per_page': 100})

        repo = next(self.g.iter_all_repos())
        assert isinstance(repo, github3.repos.Repository)
        self.mock_assertions()

        self.response('repo', _iter=True)
        self.get('https://api.github.com/repositories')
        self.conf.update(params={'since': 100000, 'per_page': 100})
        repo = next(self.g.iter_all_repos(since=100000))
        assert isinstance(repo, github3.repos.Repository)
        assert(repo.id > 100000)
        self.mock_assertions()

        repo = next(self.g.iter_all_repos(per_page=100))
        self.conf.update(params={'per_page': 100})
        assert isinstance(repo, github3.repos.Repository)
        self.mock_assertions()

    def test_iter_all_users(self):
        self.response('user', _iter=True)
        self.get('https://api.github.com/users')
        self.conf.update(params={'per_page': 100})

        repo = next(self.g.iter_all_users())
        assert isinstance(repo, github3.users.User)
        self.mock_assertions()

        repo = next(self.g.iter_all_users(per_page=100))
        self.conf.update(params={'per_page': 100})
        assert isinstance(repo, github3.users.User)
        self.mock_assertions()

    def test_iter_authorizations(self):
        self.response('authorization', _iter=True)
        self.get('https://api.github.com/authorizations')
        self.conf.update(params={'per_page': 100})

        self.assertRaises(github3.GitHubError, self.g.iter_authorizations)
        assert self.request.called is False

        self.login()
        auth = next(self.g.iter_authorizations())
        assert isinstance(auth, github3.auths.Authorization)
        self.mock_assertions()

    def test_iter_emails(self):
        self.response('emails', _iter=True)
        self.get('https://api.github.com/user/emails')
        self.conf.update(params={'per_page': 100})

        self.assertRaises(github3.GitHubError, self.g.iter_emails)
        assert self.request.called is False

        self.login()
        email = next(self.g.iter_emails())
        assert email['email'] == 'graffatcolmingov@gmail.com'
        self.mock_assertions()

    def test_iter_events(self):
        self.response('event', _iter=True)
        self.get('https://api.github.com/events')
        self.conf.update(params={'per_page': 100})

        event = next(self.g.iter_events())
        assert isinstance(event, github3.events.Event)
        self.mock_assertions()

    def test_iter_followers(self):
        self.response('user', _iter=True)
        self.get('https://api.github.com/users/sigmavirus24/followers')
        self.conf.update(params={'per_page': 100})

        self.assertRaises(github3.GitHubError, self.g.iter_followers)

        with patch.object(github3.github.GitHub, 'user') as ghuser:
            ghuser.return_value = github3.users.User(load('user'))
            u = next(self.g.iter_followers('sigmavirus24'))
            assert isinstance(u, github3.users.User)
            assert self.request.called is True
            self.mock_assertions()

            self.login()
            v = next(self.g.iter_followers())
            assert isinstance(v, github3.users.User)
            self.get('https://api.github.com/user/followers')
            assert self.request.called is True
            self.mock_assertions()

    def test_iter_following(self):
        self.response('user', _iter=True)
        self.get('https://api.github.com/users/sigmavirus24/following')
        self.conf.update(params={'per_page': 100})

        self.assertRaises(github3.GitHubError, self.g.iter_following)
        assert self.request.called is False

        with patch.object(github3.github.GitHub, 'user') as ghuser:
            ghuser.return_value = github3.users.User(load('user'))
            u = next(self.g.iter_following('sigmavirus24'))
            assert isinstance(u, github3.users.User)
            self.mock_assertions()

            self.login()
            v = next(self.g.iter_following())
            assert isinstance(v, github3.users.User)
            self.get('https://api.github.com/user/following')
            self.mock_assertions()

    def test_iter_gists(self):
        self.response('gist', _iter=True)
        self.get('https://api.github.com/users/sigmavirus24/gists')
        self.conf.update(params={'per_page': 100})

        g = next(self.g.iter_gists('sigmavirus24'))
        assert isinstance(g, github3.gists.Gist)
        self.mock_assertions()

        self.login()
        h = next(self.g.iter_gists())
        assert isinstance(h, github3.gists.Gist)
        self.get('https://api.github.com/gists')
        self.mock_assertions()

    def test_iter_notifications(self):
        self.response('notification', _iter=True)
        self.get('https://api.github.com/notifications')
        self.conf.update(params={'per_page': 100})

        self.assertRaises(github3.GitHubError, self.g.iter_notifications)

        self.not_called()
        self.login()
        thread = next(self.g.iter_notifications())
        assert isinstance(thread, github3.notifications.Thread)
        self.mock_assertions()

        self.conf.update(params={'all': True, 'per_page': 100})
        next(self.g.iter_notifications(True))
        self.mock_assertions()

        self.conf.update(params={'participating': True, 'per_page': 100})
        next(self.g.iter_notifications(participating=True))
        self.mock_assertions()

    def test_iter_org_issues(self):
        self.response('issue', _iter=True)
        self.get('https://api.github.com/orgs/github3py/issues')
        self.conf.update(params={'per_page': 100})

        self.assertRaises(github3.GitHubError, self.g.iter_org_issues,
                          'github3py')

        self.login()
        i = next(self.g.iter_org_issues('github3py'))
        assert isinstance(i, github3.issues.Issue)
        self.mock_assertions()

        params = {'filter': 'assigned', 'state': 'closed', 'labels': 'bug',
                  'sort': 'created', 'direction': 'asc',
                  'since': '2012-05-20T23:10:27Z'}
        request_params = merge(params, per_page=100)
        self.conf.update(params=request_params)
        j = next(self.g.iter_org_issues('github3py', **params))
        assert isinstance(j, github3.issues.Issue)
        self.mock_assertions()

    def test_iter_issues(self):
        self.response('issue', _iter=True)
        self.get('https://api.github.com/issues')
        self.conf.update(params={'per_page': 100})

        self.assertRaises(github3.GitHubError, self.g.iter_issues)

        self.login()
        assert isinstance(next(self.g.iter_issues()), github3.issues.Issue)
        self.mock_assertions()

        params = {'filter': 'assigned', 'state': 'closed', 'labels': 'bug',
                  'sort': 'created', 'direction': 'asc',
                  'since': '2012-05-20T23:10:27Z'}
        request_params = merge(params, per_page=100)
        self.conf.update(params=request_params)
        assert isinstance(next(self.g.iter_issues(**params)),
                          github3.issues.Issue)
        self.mock_assertions()

    def test_iter_user_issues(self):
        self.response('issue', _iter=True)
        self.get('https://api.github.com/user/issues')
        self.conf.update(params={'per_page': 100})

        self.assertRaises(github3.GitHubError, self.g.iter_user_issues)

        self.login()
        assert isinstance(next(self.g.iter_user_issues()),
                          github3.issues.Issue)
        self.mock_assertions()

        params = {'filter': 'assigned', 'state': 'closed', 'labels': 'bug',
                  'sort': 'created', 'direction': 'asc',
                  'since': '2012-05-20T23:10:27Z'}
        request_params = merge(params, per_page=100)
        self.conf.update(params=request_params)
        assert isinstance(next(self.g.iter_user_issues(**params)),
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

        assert isinstance(i, github3.issues.Issue)
        self.mock_assertions()

        with self.assertRaises(StopIteration):
            next(self.g.iter_repo_issues(None, None))

    def test_iter_keys(self):
        self.response('key', _iter=True)
        self.get('https://api.github.com/user/keys')
        self.conf.update(params={'per_page': 100})

        self.assertRaises(github3.GitHubError, self.g.iter_keys)

        self.login()
        assert isinstance(next(self.g.iter_keys()), github3.users.Key)
        self.mock_assertions()

    def test_iter_orgs(self):
        self.response('org', _iter=True)
        self.get('https://api.github.com/users/login/orgs')

        assert isinstance(next(self.g.iter_orgs('login')),
                          github3.orgs.Organization)
        self.mock_assertions()

        self.get('https://api.github.com/user/orgs')
        self.login()
        assert isinstance(next(self.g.iter_orgs()), github3.orgs.Organization)
        self.mock_assertions()

    def test_iter_repos(self):
        self.response('repo', _iter=True)
        self.get('https://api.github.com/user/repos')
        self.conf.update(params={'per_page': 100})

        self.assertRaises(github3.GitHubError, self.g.iter_repos)

        self.login()
        assert isinstance(next(self.g.iter_repos()), github3.repos.Repository)
        self.mock_assertions()

        assert isinstance(next(self.g.iter_repos('sigmavirus24')),
                          github3.repos.Repository)
        self.mock_assertions()

        self.conf.update(params={'type': 'all', 'direction': 'desc',
                                 'per_page': 100})

        next(self.g.iter_repos('all', direction='desc'))
        self.mock_assertions()

    def test_iter_user_repos(self):
        self.response('repo', _iter=True)
        self.get('https://api.github.com/users/sigmavirus24/repos')
        self.conf.update(params={'type': 'all', 'direction': 'desc',
                                 'per_page': 100})

        next(self.g.iter_user_repos('sigmavirus24', 'all', direction='desc'))
        self.mock_assertions()

        self.conf.update(params={'sort': 'created', 'per_page': 100})
        self.get('https://api.github.com/users/sigmavirus24/repos')

        assert isinstance(next(self.g.iter_user_repos('sigmavirus24',
                                                      sort="created")),
                          github3.repos.Repository)
        self.mock_assertions()

    def test_iter_repos_sort(self):
        self.response('repo', _iter=True)
        self.conf.update(params={'sort': 'created', 'per_page': 100})

        self.login()
        self.get('https://api.github.com/user/repos')
        assert isinstance(next(self.g.iter_repos(sort="created")),
                          github3.repos.Repository)
        self.mock_assertions()

    def test_iter_starred(self):
        self.response('repo', _iter=True)
        self.get('https://api.github.com/user/starred')
        self.conf.update(params={'per_page': 100})

        self.login()
        assert isinstance(next(self.g.iter_starred()),
                          github3.repos.Repository)
        self.mock_assertions()

        with patch.object(github3.github.GitHub, 'user') as user:
            user.return_value = github3.users.User(load('user'))
            self.get('https://api.github.com/users/sigmavirus24/starred')
            assert isinstance(next(self.g.iter_starred('sigmavirus24')),
                              github3.repos.Repository)
            self.mock_assertions()

    def test_iter_subscriptions(self):
        self.response('repo', _iter=True)
        self.get('https://api.github.com/user/subscriptions')
        self.conf.update(params={'per_page': 100})

        self.login()
        assert isinstance(next(self.g.iter_subscriptions()),
                          github3.repos.Repository)
        self.mock_assertions()

        with patch.object(github3.github.GitHub, 'user') as user:
            user.return_value = github3.users.User(load('user'))
            self.get('https://api.github.com/users/sigmavirus24/'
                     'subscriptions')
            assert isinstance(next(self.g.iter_subscriptions('sigmavirus24')),
                              github3.repos.Repository)
            self.mock_assertions()

    def test_login(self):
        self.g.login('user', 'password')
        assert self.g._session.auth == ('user', 'password')

        self.g.login(token='FakeOAuthToken')
        auth = self.g._session.headers.get('Authorization')
        assert auth == 'token FakeOAuthToken'

    # Unwritten test, not entirely sure how to mock this
    def test_markdown(self):
        self.response('archive')
        self.post('https://api.github.com/markdown')
        self.conf = dict(
            data={
                'text': 'Foo', 'mode': 'gfm', 'context': 'sigmavirus24/cfg'
            }
        )

        assert self.g.markdown(
            'Foo', 'gfm', 'sigmavirus24/cfg'
        ).startswith(b'archive_data')
        self.mock_assertions()

        self.post('https://api.github.com/markdown/raw')
        self.conf['data'] = 'Foo'
        self.g.markdown('Foo', raw=True)
        self.mock_assertions()

        assert self.g.markdown(None) == ''
        self.not_called()

    def test_meta(self):
        self.response('meta')
        self.get('https://api.github.com/meta')
        meta = self.g.meta()
        assert isinstance(meta, dict)
        self.mock_assertions()

    def test_octocat(self):
        self.response('archive')
        self.get('https://api.github.com/octocat')
        assert self.g.octocat().startswith(b'archive_data')
        self.mock_assertions()

    def test_organization(self):
        self.response('org')
        self.get('https://api.github.com/orgs/github3py')
        org = self.g.organization('github3py')
        assert isinstance(org, github3.orgs.Organization)
        self.mock_assertions()

    def test_pubsubhubbub(self):
        self.response('', 204)
        self.post('https://api.github.com/hub')
        body = [('hub.mode', 'subscribe'),
                ('hub.topic', 'https://github.com/foo/bar/events/push'),
                ('hub.callback', 'https://localhost/post')]
        self.conf = {}

        pubsubhubbub = self.g.pubsubhubbub

        self.assertRaises(github3.GitHubError, pubsubhubbub, '', '', '')

        self.login()
        assert pubsubhubbub('', '', '') is False
        self.not_called()

        assert pubsubhubbub('foo', 'https://example.com', 'foo') is False
        self.not_called()

        d = dict([(k[4:], v) for k, v in body])
        assert pubsubhubbub(**d) is True
        _, kwargs = self.request.call_args

        assert 'data' in kwargs
        assert body == kwargs['data']
        self.mock_assertions()

        d['secret'] = 'secret'
        body.append(('hub.secret', 'secret'))
        assert pubsubhubbub(**d)
        _, kwargs = self.request.call_args
        assert 'data' in kwargs
        assert body == kwargs['data']
        self.mock_assertions()

    def test_pull_request(self):
        self.response('pull')
        self.get('https://api.github.com/repos/sigmavirus24/'
                 'github3.py/pulls/18')
        pr = None

        with patch.object(github3.github.GitHub, 'repository') as repo:
            repo.return_value = github3.repos.Repository(load('repo'))
            pr = self.g.pull_request('sigmavirus24', 'github3.py', 18)

        assert isinstance(pr, github3.pulls.PullRequest)

        self.mock_assertions()

    def test_repository(self):
        self.response('repo')
        repo = self.g.repository(None, None)
        assert repo is None
        self.not_called()

        self.get('https://api.github.com/repos/sigmavirus24/github3.py')
        repo = self.g.repository('sigmavirus24', 'github3.py')
        assert isinstance(repo, github3.repos.Repository)
        self.mock_assertions()

    def test_set_client_id(self):
        auth = ('idXXXXXXXXXXXX', 'secretXXXXXXXXXXXXXXXX')
        self.g.set_client_id(*auth)
        assert self.g._session.params['client_id'] == auth[0]
        assert self.g._session.params['client_secret'] == auth[1]

    def test_set_user_agent(self):
        ua = 'Fake User Agents'
        self.g.set_user_agent(ua)
        assert self.g._session.headers['User-Agent'] == ua

        self.g.set_user_agent(None)
        assert self.g._session.headers['User-Agent'] == ua

    def test_star(self):
        self.response('', 204)
        self.put('https://api.github.com/user/starred/sigmavirus24/github3.py')
        self.conf = {'data': None}

        self.assertRaises(github3.GitHubError, self.g.star, 'foo', 'bar')

        self.login()
        assert self.g.star(None, None) is False
        assert self.g.star('sigmavirus24', 'github3.py')
        self.mock_assertions()

    def test_subscribe(self):
        self.response('', 204)
        self.put('https://api.github.com/user/subscriptions/'
                 'sigmavirus24/github3.py')
        self.conf = {'data': None}

        self.assertRaises(github3.GitHubError, self.g.subscribe, 'foo', 'bar')

        self.login()
        assert self.g.subscribe(None, None) is False
        assert self.g.subscribe('sigmavirus24', 'github3.py')
        self.mock_assertions()

    def test_unfollow(self):
        self.response('', 204)
        self.delete('https://api.github.com/user/following/'
                    'sigmavirus24')
        self.conf = {}

        self.assertRaises(github3.GitHubError, self.g.unfollow, 'foo')

        self.login()
        assert self.g.unfollow(None) is False
        assert self.g.unfollow('sigmavirus24')
        self.mock_assertions()

    def test_unstar(self):
        self.response('', 204)
        self.delete('https://api.github.com/user/starred/'
                    'sigmavirus24/github3.py')
        self.conf = {}

        self.assertRaises(github3.GitHubError, self.g.unstar, 'foo', 'bar')

        self.login()
        assert self.g.unstar(None, None) is False
        assert self.g.unstar('sigmavirus24', 'github3.py')
        self.mock_assertions()

    def test_unsubscribe(self):
        self.response('', 204)
        self.delete('https://api.github.com/user/subscriptions/'
                    'sigmavirus24/github3.py')
        self.conf = {}

        self.assertRaises(github3.GitHubError, self.g.unsubscribe,
                          'foo', 'bar')

        self.login()
        assert self.g.unsubscribe(None, None) is False
        assert self.g.unsubscribe('sigmavirus24', 'github3.py')
        self.mock_assertions()

    def test_update_user(self):
        self.login()
        args = ('Ian Cordasco', 'example@mail.com', 'www.blog.com', 'company',
                'loc', True, 'bio')

        with patch.object(github3.github.GitHub, 'user') as user:
            with patch.object(github3.users.User, 'update') as upd:
                user.return_value = github3.users.User(load('user'), self.g)
                upd.return_value = True
                assert self.g.update_user(*args)
                assert user.called
                assert upd.called
                upd.assert_called_with(*args)

    def test_user(self):
        self.response('user')
        self.get('https://api.github.com/users/sigmavirus24')

        assert isinstance(self.g.user('sigmavirus24'), github3.users.User)
        self.mock_assertions()

        self.get('https://api.github.com/user')
        self.login()
        assert isinstance(self.g.user(), github3.users.User)
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

    def test_zen(self):
        self.response('archive')
        self.get('https://api.github.com/zen')

        assert self.g.zen().startswith(b'archive_data')
        self.mock_assertions()


class TestGitHubEnterprise(BaseCase):
    def setUp(self):
        super(TestGitHubEnterprise, self).setUp()
        self.g = github3.GitHubEnterprise('https://github.example.com:8080/')

    def test_admin_stats(self):
        self.response('user')
        self.get('https://github.example.com:8080/api/v3/enterprise/stats/all')

        self.assertRaises(github3.GitHubError, self.g.admin_stats, None)

        self.not_called()
        self.login()
        assert isinstance(self.g.admin_stats('all'), dict)
        self.mock_assertions()

    def test_repr(self):
        assert repr(self.g).startswith('<GitHub Enterprise')

    def test_pubsubhubbub(self):
        self.response('', 204)
        self.post('https://github.example.com:8080/api/v3/hub')
        body = [('hub.mode', 'subscribe'),
                ('hub.topic',
                 'https://github.example.com:8080/foo/bar/events/push'),
                ('hub.callback', 'https://localhost/post')]
        self.conf = {}

        self.login()

        d = dict([(k[4:], v) for k, v in body])
        assert self.g.pubsubhubbub(**d)
        _, kwargs = self.request.call_args
        assert 'data' in kwargs
        assert body == kwargs['data']
        self.mock_assertions()

        d['secret'] = 'secret'
        body.append(('hub.secret', 'secret'))
        assert self.g.pubsubhubbub(**d)
        _, kwargs = self.request.call_args
        assert 'data' in kwargs
        assert body == kwargs['data']
        self.mock_assertions()


class TestGitHubStatus(BaseCase):
    def setUp(self):
        super(TestGitHubStatus, self).setUp()
        self.g = github3.GitHubStatus()
        self.api = 'https://status.github.com/'

    def test_repr(self):
        assert repr(self.g) == '<GitHub Status>'

    def test_api(self):
        self.response('user')
        self.get(self.api + 'api.json')
        assert isinstance(self.g.api(), dict)
        self.mock_assertions()

    def test_status(self):
        self.response('user')
        self.get(self.api + 'api/status.json')
        assert isinstance(self.g.status(), dict)
        self.mock_assertions()

    def test_last_message(self):
        self.response('user')
        self.get(self.api + 'api/last-message.json')
        assert isinstance(self.g.last_message(), dict)
        self.mock_assertions()

    def test_messages(self):
        self.response('user')
        self.get(self.api + 'api/messages.json')
        assert isinstance(self.g.messages(), dict)
        self.mock_assertions()
