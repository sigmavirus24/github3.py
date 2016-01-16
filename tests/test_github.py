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
