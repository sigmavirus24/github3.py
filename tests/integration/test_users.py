import github3

from .helper import IntegrationHelper


class TestUser(IntegrationHelper):
    def test_iter_orgs(self):
        cassette_name = self.cassette_name('iter_orgs')
        with self.recorder.use_cassette(cassette_name):
            u = self.gh.user('sigmavirus24')
            for o in u.iter_orgs(number=25):
                assert isinstance(o, github3.orgs.Organization)
