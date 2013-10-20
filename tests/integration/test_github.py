import github3

from .helper import IntegrationHelper


class TestGitHub(IntegrationHelper):
    def test_create_gist(self):
        """Test the ability of a GitHub instance to create a new gist"""
        self.token_login()
        cassette_name = self.cassette_name('create_gist')
        with self.recorder.use_cassette(cassette_name):
            g = self.gh.create_gist(
                'Gist Title', {'filename.py': {'content': '#content'}}
                )

        assert isinstance(g, github3.gists.Gist)
        assert g.files == 1
        assert g.is_public() is True

    def test_create_issue(self):
        """Test the ability of a GitHub instance to create a new issue"""
        self.token_login()
        cassette_name = self.cassette_name('create_issue')
        with self.recorder.use_cassette(cassette_name):
            i = self.gh.create_issue(
                'github3py', 'fork_this', 'Test issue creation',
                "Let's see how well this works with Betamax"
                )

        assert isinstance(i, github3.issues.Issue)
        assert i.title == 'Test issue creation'
        assert i.body == "Let's see how well this works with Betamax"
