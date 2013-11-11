import github3

from .helper import IntegrationHelper


SSH_KEY = (
    # Generated for this alone then deleted
    'ssh-rsa '
    'AAAAB3NzaC1yc2EAAAADAQABAAABAQCl4l154T4deeLsMHge0TpwDVd5rlDYVyFFr3PP3ZfW+'
    'RZJAHs2QdwbpfoEWUaJmuYvepo/L8JrglKg1LGm99iR/qRg3Nbr8kVCNK+Tb5bUBO5JarnYIT'
    'hwzhRxamZeyZxbmpYFHW3WozPJDD+FU6qg6ZQf1coSqXcnA3U29FBB3CfHu89hkfVvKvMGJnZ'
    'lFHeAkTuDrirWgzFkm+CXT65W7UhJKZD2IBB+JmY0Wkxbv6ayePoydCKfP+pOZRxSTsAMHRSj'
    'RfERbT59VefKa2tAJd2wMJg04Wclgz/q1rx/T9hVCa1O5K8meJBLUDxP6sapMlMr4RYdi0DRr'
    'qncY0b1'
)


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

    def test_create_key(self):
        """Test the ability to create a key and delete it."""
        self.basic_login()
        cassette_name = self.cassette_name('create_delete_key')
        with self.recorder.use_cassette(cassette_name):
            k = self.gh.create_key('Key name', SSH_KEY)
            k.delete()

        assert isinstance(k, github3.users.Key)
        assert k.title == 'Key name'
        assert k.key == SSH_KEY

    def test_meta(self):
        """Test the ability to get the CIDR formatted addresses"""
        cassette_name = self.cassette_name('meta')
        with self.recorder.use_cassette(cassette_name):
            m = self.gh.meta()
            assert isinstance(m, dict)

    def test_octocat(self):
        """Test the ability to use the octocat endpoint"""
        cassette_name = self.cassette_name('octocat')
        say = 'github3.py is awesome'
        with self.recorder.use_cassette(cassette_name):
            o = self.gh.octocat()
            assert o is not None
            assert o is not ''
            o = self.gh.octocat(say)
            assert say in o.decode()

    def test_organization(self):
        """Test the ability to retrieve an Organization"""
        cassette_name = self.cassette_name('organization')
        with self.recorder.use_cassette(cassette_name):
            o = self.gh.organization('github3py')

        assert isinstance(o, github3.orgs.Organization)

    def test_pull_request(self):
        """Test the ability to retrieve a Pull Request"""
        cassette_name = self.cassette_name('pull_request')
        with self.recorder.use_cassette(cassette_name):
            p = self.gh.pull_request('sigmavirus24', 'github3.py', 119)

        assert isinstance(p, github3.pulls.PullRequest)

    def test_repository(self):
        """Test the ability to retrieve a Repository"""
        cassette_name = self.cassette_name('repository')
        with self.recorder.use_cassette(cassette_name):
            r = self.gh.repository('sigmavirus24', 'github3.py')

        assert isinstance(r, github3.repos.repo.Repository)

    def test_user(self):
        """Test the ability to retrieve a User"""
        cassette_name = self.cassette_name('user')
        with self.recorder.use_cassette(cassette_name):
            r = self.gh.user('sigmavirus24')

        assert isinstance(r, github3.users.User)
