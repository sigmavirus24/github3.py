import github3

from tests.utils import BaseCase


def merge(first, second=None, **kwargs):
    copy = first.copy()
    copy.update(second or {})
    copy.update(kwargs)
    return copy


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


class TestUnsecureGitHubEnterprise(BaseCase):
    def setUp(self):
        super(TestUnsecureGitHubEnterprise, self).setUp()
        self.g = github3.GitHubEnterprise('https://github.example.com:8080/',
                                          verify=False)

    def test_skip_ssl_validation(self):
        self.response('pull_enterprise')
        self.g.pull_request('sigmavirus24', 'github3.py', 19)

        assert False == self.g.session.verify
        assert self.request.called


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
