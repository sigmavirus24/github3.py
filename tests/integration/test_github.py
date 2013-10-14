import github3

from .helper import IntegrationHelper


class TestGitHub(IntegrationHelper):
    described_class = 'GitHub'

    def test_create_gist(self):
        self.token_login()
        with self.recorder.use_cassette(self.cassette_name('create_gist')):
            g = self.gh.create_gist(
                'Gist Title', {'filename.py': {'content': '#content'}}
            )

        assert isinstance(g, github3.gists.Gist)
        assert g.files == 1
        assert g.is_public() is True
