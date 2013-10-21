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
        #import pytest; pytest.set_trace()
        cassette_name = self.cassette_name('create_delete_key')
        with self.recorder.use_cassette(cassette_name):
            k = self.gh.create_key('Key name', SSH_KEY)
            k.delete()

        assert isinstance(k, github3.users.Key)
        assert k.title == 'Key name'
        assert k.key == SSH_KEY
