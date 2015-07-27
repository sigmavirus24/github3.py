# -*- coding: utf-8 -*-
"""Integration tests for methods implemented on GitHub."""
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

    """GitHub integration tests."""

    match_on = ['method', 'uri', 'gh3-headers']

    def test_authorize(self):
        """Test the ability to create an authorization."""
        from ..conftest import credentials
        username, password = credentials
        cassette_name = self.cassette_name('authorize')
        with self.recorder.use_cassette(cassette_name):
            auth = self.gh.authorize(username, password,
                                     note='Test authorization',
                                     note_url='http://example.com')

        assert isinstance(auth, github3.auths.Authorization)

    def test_create_gist(self):
        """Test the ability of a GitHub instance to create a new gist."""
        self.token_login()
        cassette_name = self.cassette_name('create_gist')
        with self.recorder.use_cassette(cassette_name):
            g = self.gh.create_gist(
                'Gist Title', {'filename.py': {'content': '#content'}}
                )

        assert isinstance(g, github3.gists.Gist)
        assert g.public is True

    def test_create_issue(self):
        """Test the ability of a GitHub instance to create a new issue."""
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

    def test_create_repository(self):
        """Show an authenticated user can create a repository."""
        self.basic_login()
        cassette_name = self.cassette_name('create_repository')
        with self.recorder.use_cassette(cassette_name):
            r = self.gh.create_repository('my-new-repo',
                                          description='Test repo creation')

        assert isinstance(r, github3.repos.Repository)
        assert str(r) == 'sigmavirus24/my-new-repo'

    def test_emojis(self):
        """Test the ability to retrieve from /emojis."""
        cassette_name = self.cassette_name('emojis')
        with self.recorder.use_cassette(cassette_name):
            emojis = self.gh.emojis()

        assert isinstance(emojis, dict)
        # Asserts that it's a string and looks ilke the URLs we expect to see
        assert emojis['+1'].startswith('https://github')

    def test_feeds(self):
        """Test the ability to retrieve a user's timelime URLs."""
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
        """Test the ability to retrieve a single gist."""
        cassette_name = self.cassette_name('gist')
        with self.recorder.use_cassette(cassette_name):
            g = self.gh.gist(7160899)

        assert isinstance(g, github3.gists.Gist)

    def test_gitignore_template(self):
        """Test the ability to retrieve a single gitignore template."""
        cassette_name = self.cassette_name('gitignore_template')
        with self.recorder.use_cassette(cassette_name):
            t = self.gh.gitignore_template('Python')

        assert t is not None
        assert t != ''

    def test_non_existent_gitignore_template(self):
        """Test the ability to retrieve a single gitignore template."""
        cassette_name = self.cassette_name('non_existent_gitignore_template')
        with self.recorder.use_cassette(cassette_name):
            t = self.gh.gitignore_template('i_donut_exist')

        assert t is not None
        assert t == ''

    def test_gitignore_templates(self):
        """Test the ability to retrieve a list of gitignore templates."""
        cassette_name = self.cassette_name('gitignore_templates')
        with self.recorder.use_cassette(cassette_name):
            l = self.gh.gitignore_templates()

        assert l != []
        assert isinstance(l, list)

    def test_is_following(self):
        """Test the ability to check if a user is being followed."""
        self.basic_login()
        cassette_name = self.cassette_name('is_following')
        with self.recorder.use_cassette(cassette_name):
            assert self.gh.is_following('lukasa') is True

    def test_is_starred(self):
        """Test the ability to check if a user starred a repository."""
        self.basic_login()
        cassette_name = self.cassette_name('is_starred')
        with self.recorder.use_cassette(cassette_name):
            assert self.gh.is_starred('lukasa', 'mkcert') is True

    def test_issue(self):
        """Test the ability to retrieve a single issue."""
        cassette_name = self.cassette_name('issue')
        with self.recorder.use_cassette(cassette_name):
            i = self.gh.issue('sigmavirus24', 'github3.py', 1)

        assert isinstance(i, github3.issues.Issue)

    def test_all_organizations(self):
        """Test the ability to iterate over all of the organizations."""
        cassette_name = self.cassette_name('all_organizations')
        with self.recorder.use_cassette(cassette_name):
            for r in self.gh.all_organizations(number=25):
                assert isinstance(r, github3.orgs.Organization)

    def test_all_repositories(self):
        """Test the ability to iterate over all of the repositories."""
        cassette_name = self.cassette_name('iter_all_repos')
        with self.recorder.use_cassette(cassette_name):
            for r in self.gh.all_repositories(number=25):
                assert isinstance(r, github3.repos.repo.Repository)

    def test_all_users(self):
        """Test the ability to iterate over all of the users."""
        cassette_name = self.cassette_name('iter_all_users')
        with self.recorder.use_cassette(cassette_name):
            for u in self.gh.all_users(number=25):
                assert isinstance(u, github3.users.User)

    def test_all_events(self):
        """Test the ability to iterate over all public events."""
        cassette_name = self.cassette_name('iter_events')
        with self.recorder.use_cassette(cassette_name):
            for e in self.gh.all_events(number=25):
                assert isinstance(e, github3.events.Event)

    def test_followers_of(self):
        """Test the ability to iterate over a user's followers."""
        cassette_name = self.cassette_name('followers_of')
        with self.recorder.use_cassette(cassette_name):
            for u in self.gh.followers_of('sigmavirus24', number=25):
                assert isinstance(u, github3.users.User)

    def test_followers(self):
        """
        Test the ability to iterate over an authenticated user's followers.

        Show the difference between GitHub#followers_of and GitHub#followers.
        """
        self.basic_login()
        cassette_name = self.cassette_name('followers_auth')
        with self.recorder.use_cassette(cassette_name):
            for u in self.gh.followers():
                assert isinstance(u, github3.users.User)

    def test_user_teams(self):
        """Test the ability to iterate over a user's teams."""
        self.basic_login()
        cassette_name = self.cassette_name('iter_user_teams')
        with self.recorder.use_cassette(cassette_name):
            for t in self.gh.user_teams():
                assert isinstance(t, github3.orgs.Team)

    def test_me(self):
        """Test the ability to retrieve the authenticated user's info."""
        self.basic_login()
        cassette_name = self.cassette_name('me')
        with self.recorder.use_cassette(cassette_name):
            me = self.gh.me()

        assert isinstance(me, github3.users.User)

    def test_meta(self):
        """Test the ability to get the CIDR formatted addresses."""
        cassette_name = self.cassette_name('meta')
        with self.recorder.use_cassette(cassette_name):
            m = self.gh.meta()
            assert isinstance(m, dict)

    def test_notifications(self):
        """Test the ability to retrieve unread notifications."""
        self.basic_login()
        cassette_name = self.cassette_name('unread_notifications')
        with self.recorder.use_cassette(cassette_name):
            for notification in self.gh.notifications():
                assert isinstance(notification, github3.notifications.Thread)
                assert notification.unread is True

    def test_notifications_all(self):
        """Test the ability to retrieve read notifications as well."""
        self.basic_login()
        cassette_name = self.cassette_name('all_notifications')
        with self.recorder.use_cassette(cassette_name):
            read_notifications = []
            unread_notifications = []
            for notification in self.gh.notifications(all=True):
                assert isinstance(notification, github3.notifications.Thread)
                if notification.unread:
                    unread_notifications.append(notification)
                else:
                    read_notifications.append(notification)

            assert len(read_notifications) > 0
            assert len(unread_notifications) > 0

    def test_octocat(self):
        """Test the ability to use the octocat endpoint."""
        cassette_name = self.cassette_name('octocat')
        say = 'github3.py is awesome'
        with self.recorder.use_cassette(cassette_name):
            o = self.gh.octocat()
            assert o is not None
            assert o is not ''
            o = self.gh.octocat(say)
            assert say in o

    def test_organization(self):
        """Test the ability to retrieve an Organization."""
        cassette_name = self.cassette_name('organization')
        with self.recorder.use_cassette(cassette_name):
            o = self.gh.organization('github3py')

        assert isinstance(o, github3.orgs.Organization)

    def test_pull_request(self):
        """Test the ability to retrieve a Pull Request."""
        cassette_name = self.cassette_name('pull_request')
        with self.recorder.use_cassette(cassette_name):
            p = self.gh.pull_request('sigmavirus24', 'github3.py', 119)

        assert isinstance(p, github3.pulls.PullRequest)

    def test_rate_limit(self):
        """Test the ability to retrieve rate information."""
        cassette_name = self.cassette_name('rate_limit')
        with self.recorder.use_cassette(cassette_name):
            r = self.gh.rate_limit()

        assert isinstance(r, dict)
        assert 'resources' in r

    def test_repository(self):
        """Test the ability to retrieve a Repository."""
        cassette_name = self.cassette_name('repository')
        with self.recorder.use_cassette(cassette_name):
            r = self.gh.repository('sigmavirus24', 'github3.py')

        assert isinstance(r, github3.repos.repo.Repository)

    def test_repository_with_id(self):
        """Test the ability to retrieve a repository by its id."""
        cassette_name = self.cassette_name('repository_with_id')
        with self.recorder.use_cassette(cassette_name):
            r = self.gh.repository_with_id(11439734)

        assert isinstance(r, github3.repos.repo.Repository)

    def test_repositories(self):
        """Test the ability to retrieve an authenticated user's repos."""
        cassette_name = self.cassette_name('repositories')
        self.basic_login()
        with self.recorder.use_cassette(cassette_name):
            for r in self.gh.repositories():
                assert isinstance(r, github3.repos.Repository)

    def test_repositories_by(self):
        """Test the ability to retrieve a user's repositories."""
        cassette_name = self.cassette_name('repositories_by')
        with self.recorder.use_cassette(cassette_name):
            for r in self.gh.repositories_by('dstufft'):
                assert isinstance(r, github3.repos.Repository)

    def test_search_code(self):
        """Test the ability to use the code search endpoint."""
        cassette_name = self.cassette_name('search_code')
        with self.recorder.use_cassette(cassette_name):
            result_iterator = self.gh.search_code(
                'HTTPAdapter in:file language:python'
                ' repo:kennethreitz/requests'
                )
            code_result = next(result_iterator)

        assert isinstance(code_result, github3.search.CodeSearchResult)

    def test_search_code_with_text_match(self):
        """Test the ability to use the code search endpoint."""
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
        """Test the ability to use the user search endpoint."""
        cassette_name = self.cassette_name('search_users')
        with self.recorder.use_cassette(cassette_name):
            users = self.gh.search_users('tom followers:>1000')
            assert isinstance(next(users),
                              github3.search.UserSearchResult)

        assert isinstance(users, github3.structs.SearchIterator)

    def test_search_users_with_text_match(self):
        """Test the ability to use the user search endpoint."""
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
        """Test the ability to use the issues search endpoint."""
        cassette_name = self.cassette_name('search_issues')
        with self.recorder.use_cassette(cassette_name):
            issues = self.gh.search_issues('github3 labels:bugs')
            assert isinstance(next(issues), github3.search.IssueSearchResult)

        assert isinstance(issues, github3.structs.SearchIterator)

    def test_search_repositories(self):
        """Test the ability to use the repository search endpoint."""
        cassette_name = self.cassette_name('search_repositories')
        with self.recorder.use_cassette(cassette_name):
            repos = self.gh.search_repositories('github3 language:python')
            assert isinstance(next(repos),
                              github3.search.RepositorySearchResult)

        assert isinstance(repos, github3.structs.SearchIterator)

    def test_search_repositories_with_text_match(self):
        """Test the ability to use the repository search endpoint."""
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

    def test_update_me(self):
        """Test the ability to update the current authenticated User."""
        cassette_name = self.cassette_name('update_me')
        self.basic_login()
        with self.recorder.use_cassette(cassette_name):
            assert self.gh.update_me(name='Ian "RFC" Cordasco') is True
            assert self.gh.update_me(name='Ian Cordasco') is True

    def test_user(self):
        """Test the ability to retrieve a User."""
        cassette_name = self.cassette_name('user')
        with self.recorder.use_cassette(cassette_name):
            sigmavirus24 = self.gh.user('sigmavirus24')

        assert isinstance(sigmavirus24, github3.users.User)

    def test_user_with_id(self):
        """Test the ability to retrieve a user by their id."""
        cassette_name = self.cassette_name('user_with_id')
        with self.recorder.use_cassette(cassette_name):
            sigmavirus24 = self.gh.user_with_id(240830)

        assert isinstance(sigmavirus24, github3.users.User)

    def test_zen(self):
        """Test the ability to retrieve tidbits of Zen."""
        cassette_name = self.cassette_name('zen')
        with self.recorder.use_cassette(cassette_name):
            z = self.gh.zen()

        assert z is not None
        assert z != ''
