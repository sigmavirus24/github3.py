import github3

from .helper import IntegrationHelper


class TestUser(IntegrationHelper):
    def test_organizations(self):
        cassette_name = self.cassette_name('organizations')
        with self.recorder.use_cassette(cassette_name):
            u = self.gh.user('sigmavirus24')
            for o in u.organizations(number=25):
                assert isinstance(o, github3.orgs.Organization)
