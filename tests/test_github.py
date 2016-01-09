import github3

from tests.utils import BaseCase


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
