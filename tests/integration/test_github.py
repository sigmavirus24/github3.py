import github3
import uritemplate

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
    match_on = ['method', 'uri', 'gh3-headers']

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

    def test_emojis(self):
        """Test the ability to retrieve from /emojis"""
        cassette_name = self.cassette_name('emojis')
        with self.recorder.use_cassette(cassette_name):
            emojis = self.gh.emojis()

        assert isinstance(emojis, dict)
        # Asserts that it's a string and looks ilke the URLs we expect to see
        assert emojis['+1'].startswith('https://github')

    def test_feeds(self):
        """Test the ability to retrieve a user's timelime URLs"""
        self.basic_login()
        cassette_name = self.cassette_name('feeds')
        with self.recorder.use_cassette(cassette_name):
            feeds = self.gh.feeds()

        for v in feeds['_links'].values():
            assert isinstance(v['href'], uritemplate.URITemplate)

        # The processing on _links has been tested. Get rid of it.
        del feeds['_links']

        # Test the rest of the response
        for v in feeds.values():
            assert isinstance(v, uritemplate.URITemplate)

    def test_gist(self):
        """Test the ability to retrieve a single gist"""
        cassette_name = self.cassette_name('gist')
        with self.recorder.use_cassette(cassette_name):
            g = self.gh.gist(7160899)

        assert isinstance(g, github3.gists.Gist)

    def test_gitignore_template(self):
        """Test the ability to retrieve a single gitignore template"""
        cassette_name = self.cassette_name('gitignore_template')
        with self.recorder.use_cassette(cassette_name):
            t = self.gh.gitignore_template('Python')

        assert t is not None
        assert t != ''

    def test_non_existent_gitignore_template(self):
        """Test the ability to retrieve a single gitignore template"""
        cassette_name = self.cassette_name('non_existent_gitignore_template')
        with self.recorder.use_cassette(cassette_name):
            t = self.gh.gitignore_template('i_donut_exist')

        assert t is not None
        assert t == ''

    def test_gitignore_templates(self):
        """Test the ability to retrieve a list of gitignore templates"""
        cassette_name = self.cassette_name('gitignore_templates')
        with self.recorder.use_cassette(cassette_name):
            l = self.gh.gitignore_templates()

        assert l != []
        assert isinstance(l, list)

    def test_issue(self):
        """Test the ability to retrieve a single issue"""
        cassette_name = self.cassette_name('issue')
        with self.recorder.use_cassette(cassette_name):
            i = self.gh.issue('sigmavirus24', 'github3.py', 1)

        assert isinstance(i, github3.issues.Issue)

    def test_iter_all_repos(self):
        """Test the ability to iterate over all of the repositories"""
        cassette_name = self.cassette_name('iter_all_repos')
        with self.recorder.use_cassette(cassette_name):
            for r in self.gh.iter_all_repos(number=25):
                assert isinstance(r, github3.repos.repo.Repository)

    def test_iter_all_users(self):
        """Test the ability to iterate over all of the users"""
        cassette_name = self.cassette_name('iter_all_users')
        with self.recorder.use_cassette(cassette_name):
            for u in self.gh.iter_all_users(number=25):
                assert isinstance(u, github3.users.User)

    def test_iter_events(self):
        """Test the ability to iterate over all public events"""
        cassette_name = self.cassette_name('iter_events')
        with self.recorder.use_cassette(cassette_name):
            for e in self.gh.iter_events(number=25):
                assert isinstance(e, github3.events.Event)

    def test_iter_followers(self):
        """Test the ability to iterate over a user's followers"""
        cassette_name = self.cassette_name('iter_followers')
        with self.recorder.use_cassette(cassette_name):
            for u in self.gh.iter_followers('sigmavirus24', number=25):
                assert isinstance(u, github3.users.User)

    def test_iter_user_teams(self):
        """Test the ability to iterate over a user's teams"""
        self.basic_login()
        cassette_name = self.cassette_name('iter_user_teams')
        with self.recorder.use_cassette(cassette_name):
            for t in self.gh.iter_user_teams():
                assert isinstance(t, github3.orgs.Team)

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

    def test_rate_limit(self):
        cassette_name = self.cassette_name('rate_limit')
        with self.recorder.use_cassette(cassette_name):
            r = self.gh.rate_limit()

        assert isinstance(r, dict)
        assert 'resources' in r

    def test_repository(self):
        """Test the ability to retrieve a Repository"""
        cassette_name = self.cassette_name('repository')
        with self.recorder.use_cassette(cassette_name):
            r = self.gh.repository('sigmavirus24', 'github3.py')

        assert isinstance(r, github3.repos.repo.Repository)

    def test_search_code(self):
        """Test the ability to use the code search endpoint"""
        cassette_name = self.cassette_name('search_code')
        with self.recorder.use_cassette(cassette_name):
            result_iterator = self.gh.search_code(
                'HTTPAdapter in:file language:python'
                ' repo:kennethreitz/requests'
                )
            code_result = next(result_iterator)

        assert isinstance(code_result, github3.search.CodeSearchResult)

    def test_search_code_with_text_match(self):
        """Test the ability to use the code search endpoint"""
        cassette_name = self.cassette_name('search_code_with_text_match')
        with self.recorder.use_cassette(cassette_name,
                                        match_requests_on=self.match_on):
            result_iterator = self.gh.search_code(
                ('HTTPAdapter in:file language:python'
                 ' repo:kennethreitz/requests'),
                text_match=True
                )
            code_result = next(result_iterator)

        assert isinstance(code_result, github3.search.CodeSearchResult)
        assert len(code_result.text_matches) > 0

    def test_search_users(self):
        """Test the ability to use the user search endpoint"""
        cassette_name = self.cassette_name('search_users')
        with self.recorder.use_cassette(cassette_name):
            users = self.gh.search_users('tom followers:>1000')
            assert isinstance(next(users),
                              github3.search.UserSearchResult)

        assert isinstance(users, github3.structs.SearchIterator)

    def test_search_users_with_text_match(self):
        """Test the ability to use the user search endpoint"""
        cassette_name = self.cassette_name('search_users_with_text_match')
        with self.recorder.use_cassette(cassette_name,
                                        match_requests_on=self.match_on):
            users = self.gh.search_users('tom followers:>1000',
                                         text_match=True)
            user_result = next(users)
            assert isinstance(user_result,
                              github3.search.UserSearchResult)

        assert isinstance(users, github3.structs.SearchIterator)
        assert len(user_result.text_matches) > 0

    def test_search_issues(self):
        """Test the ability to use the issues search endpoint"""
        cassette_name = self.cassette_name('search_issues')
        with self.recorder.use_cassette(cassette_name):
            issues = self.gh.search_issues('github3 labels:bugs')
            assert isinstance(next(issues), github3.search.IssueSearchResult)

        assert isinstance(issues, github3.structs.SearchIterator)

    def test_search_repositories(self):
        """Test the ability to use the repository search endpoint"""
        cassette_name = self.cassette_name('search_repositories')
        with self.recorder.use_cassette(cassette_name):
            repos = self.gh.search_repositories('github3 language:python')
            assert isinstance(next(repos),
                              github3.search.RepositorySearchResult)

        assert isinstance(repos, github3.structs.SearchIterator)

    def test_search_repositories_with_text_match(self):
        """Test the ability to use the repository search endpoint"""
        self.token_login()
        cassette_name = self.cassette_name('search_repositories_text_match')
        with self.recorder.use_cassette(cassette_name,
                                        match_requests_on=self.match_on):
            repos = self.gh.search_repositories('github3 language:python',
                                                text_match=True)
            repo_result = next(repos)
            assert isinstance(repo_result,
                              github3.search.RepositorySearchResult)

        assert isinstance(repos, github3.structs.SearchIterator)
        assert len(repo_result.text_matches) > 0

    def test_user(self):
        """Test the ability to retrieve a User"""
        self.token_login()
        cassette_name = self.cassette_name('user')
        with self.recorder.use_cassette(cassette_name):
            s = self.gh.user('sigmavirus24')
            self.basic_login()
            u = self.gh.user()

        assert isinstance(s, github3.users.User)
        assert isinstance(u, github3.users.User)

    def test_zen(self):
        """Test the ability to retrieve tidbits of Zen"""
        cassette_name = self.cassette_name('zen')
        with self.recorder.use_cassette(cassette_name):
            z = self.gh.zen()

        assert z is not None
        assert z != ''
