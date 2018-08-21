# -*- coding: utf-8 -*-
"""Integration tests for methods implemented on GitHub."""
from datetime import datetime

import github3
import pytest
import uritemplate

from .helper import (GitHubEnterpriseHelper, IntegrationHelper,
                     GitHubStatusHelper)

GPG_KEY = (
    # Generated for this alone then deleted
    '-----BEGIN PGP PUBLIC KEY BLOCK-----\n'
    '\n'
    'mI0EW3Gx5AEEAKkl8uAp56B9WlVMRl3ibQN99x/7JAkCWHVU1NjfAa4/AOmhG2Bl\n'
    'FmSCfQ6CBVgOGpdaMtzyq0YxYgvhnhzwwaEZ6mrwz2in1Mo8iOVkXv2eK3ov24PU\n'
    'aLoYxiGMtNT8nKQjJLLWrEjrJOnNNGkSUHM8eAVlz3TonZALp0lOsIg/ABEBAAG0\n'
    'aUphY29wbyBOb3RhcnN0ZWZhbm8gKENyZWF0ZWQgZm9yIGEgdGVzdCBmb3IgZ2l0\n'
    'aHViMy5weSBhbmQgdGhlbiBkZWxldGVkLikgPGphY29wby5ub3RhcnN0ZWZhbm9A\n'
    'Z21haWwuY29tPojOBBMBCgA4FiEEux/Ns2l9RasyufUE8C5SQOx2rKgFAltxseQC\n'
    'GwMFCwkIBwIGFQoJCAsCBBYCAwECHgECF4AACgkQ8C5SQOx2rKhwEgQApsTrwmfh\n'
    'PgwzX4zPtVvwKq+MYU6idhS2hwouHYPzgsVNOt5P6vW2V9jF9NQrK1gVXMSn1S16\n'
    '6iE/X8R5rkRYbAXlvFnww4xaVCWSrXBhBGDbOCQ4fSuTNEWXREhwHAHnP4nDR+mh\n'
    'mba6f9pMZBZalz8/0jYf2Q2ds5PEhzCQk6K4jQRbcbHkAQQAt9A5ebOFcxFyfxmt\n'
    'OeEkmQArt31U1yATLQQto9AmpQnPk1OHjEsv+4MWaydTnuWKG1sxZb9BQRq8T8ho\n'
    'jFcYXg3CAdz2Pi6dA+I6dSKgknVY2qTFURSegFcKOiVJd48oEScMyjnRcn+gDM3Y\n'
    'S3shYhDt1ff6cStm344+HWFyBPcAEQEAAYi2BBgBCgAgFiEEux/Ns2l9RasyufUE\n'
    '8C5SQOx2rKgFAltxseQCGwwACgkQ8C5SQOx2rKhlfgP/dhFe09wMtVE6qXpQAXWU\n'
    'T34sJD7GTcyYCleGtAgbtFD+7j9rk7VTG4hGZlDvW6FMdEQBE18Hd+0UhO1TA0c1\n'
    'XTLKl8sNmIg+Ph3yiED8Nn+ByNk7KqX3SeCNvAFkTZI3yeTAynUmQin68ZqrwMjp\n'
    'IMGmjyjdODb4qOpFvBPAlM8=\n'
    '=2MWr\n'
    '-----END PGP PUBLIC KEY BLOCK-----'
)

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

    def test_activate_membership(self):
        """Validate the ability to activate membership."""
        self.basic_login()
        cassette_name = self.cassette_name('activate_membership')
        with self.recorder.use_cassette(cassette_name):
            membership = self.gh.activate_membership('sv24-archive')

        assert isinstance(membership, github3.orgs.Membership)

    def test_authenticated_app(self):
        """Validate an app can retrieve its own metadata."""
        cassette_name = self.cassette_name('authenticated_app')
        with self.recorder.use_cassette(cassette_name):
            self.app_bearer_login()
            app = self.gh.authenticated_app()

        assert isinstance(app, github3.apps.App)

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

    def test_add_email_addresses(self):
        """Add email addresses to the authorized user's account."""
        self.basic_login()
        cassette_name = self.cassette_name('add_email_addresses')
        with self.recorder.use_cassette(cassette_name):
            emails = self.gh.add_email_addresses(
                ['example1@example.com', 'example2@example.com']
            )

        for email in emails:
            assert isinstance(email, github3.users.Email)

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

    def test_create_gpg_key(self):
        """Test the ability of a GitHub instance to create a new GPG key."""
        self.token_login()
        cassette_name = self.cassette_name('create_gpg_key')
        with self.recorder.use_cassette(cassette_name):
            gpg_key = self.gh.create_gpg_key(GPG_KEY)
            assert isinstance(gpg_key, github3.users.GPGKey)
            assert gpg_key.delete() is True

    def test_create_issue(self):
        """Test the ability of a GitHub instance to create a new issue."""
        self.auto_login()
        cassette_name = self.cassette_name('create_issue')
        with self.recorder.use_cassette(cassette_name):
            i = self.gh.create_issue(
                'github3py', 'fork_this', 'Test issue creation',
                "Let's see how well this works with Betamax"
                )

        assert isinstance(i, github3.issues.ShortIssue)
        assert i.title == 'Test issue creation'
        assert i.body == "Let's see how well this works with Betamax"

    def test_create_issue_multiple_assignees(self):
        """
        Test the ability of a GitHub instance to create a new issue.
        with multipole assignees
        """
        self.auto_login()
        cassette_name = self.cassette_name('create_issue_assignees')
        with self.recorder.use_cassette(cassette_name):
            i = self.gh.create_issue(
                'github3py', 'fork_this', 'Test issue creation assignees',
                "Let's see how well this works with Betamax",
                assignees=['omgjlk', 'sigmavirus24']
                )

        assert isinstance(i, github3.issues.ShortIssue)
        assert i.title == 'Test issue creation assignees'
        assert i.body == "Let's see how well this works with Betamax"
        assert ['omgjlk', 'sigmavirus24'] == [a.login for a in i.assignees]

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
        assert str(r).endswith('/my-new-repo')

    def test_delete_email_addresses(self):
        """Delete email addresses from authenticated user's account."""
        self.basic_login()
        cassette_name = self.cassette_name('delete_email_addresses')
        with self.recorder.use_cassette(cassette_name):
            assert self.gh.delete_email_addresses(
                ['graffatcolmingov+example1@gmail.com',
                 'graffatcolmingov+example2@gmail.com']
            ) is True

    def test_emojis(self):
        """Test the ability to retrieve from /emojis."""
        cassette_name = self.cassette_name('emojis')
        with self.recorder.use_cassette(cassette_name):
            emojis = self.gh.emojis()

        assert isinstance(emojis, dict)
        # Asserts that it's a string and looks ilke the URLs we expect to see
        assert emojis['+1'].startswith('https://github')

    def test_emojis_etag(self):
        """Test the ability to retrieve from /emojis."""
        cassette_name = self.cassette_name('emojis')
        with self.recorder.use_cassette(cassette_name):
            emojis = self.gh.emojis()

        assert 'ETag' not in emojis
        assert 'Last-Modified' not in emojis

    def test_feeds(self):
        """Test the ability to retrieve a user's timelime URLs."""
        self.basic_login()
        cassette_name = self.cassette_name('feeds')
        with self.recorder.use_cassette(cassette_name):
            feeds = self.gh.feeds()

        _links = feeds.pop('_links')

        for urls in feeds.values():
            if not isinstance(urls, list):
                urls = [urls]
            for url in urls:
                assert isinstance(url, uritemplate.URITemplate)

        for links in _links.values():
            if not isinstance(links, list):
                links = [links]
            for link in links:
                href = link.get('href')
                assert (href is None or
                        isinstance(href, uritemplate.URITemplate))

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

    def test_gpg_key(self):
        """Test the ability to retrieve a user's GPG key."""
        self.token_login()
        cassette_name = self.cassette_name('gpg_key')
        with self.recorder.use_cassette(cassette_name):
            created_gpg_key = self.gh.create_gpg_key(GPG_KEY)
            assert isinstance(created_gpg_key, github3.users.GPGKey)
            retrieved_gpg_key = self.gh.gpg_key(created_gpg_key.id)
            assert isinstance(retrieved_gpg_key, github3.users.GPGKey)
            assert created_gpg_key == retrieved_gpg_key
            assert created_gpg_key.delete() is True

    def test_gpg_keys(self):
        """Test the ability to retrieve all user's GPG keys."""
        self.token_login()
        cassette_name = self.cassette_name('gpg_keys')
        with self.recorder.use_cassette(cassette_name):
            created_gpg_key = self.gh.create_gpg_key(GPG_KEY)
            assert isinstance(created_gpg_key, github3.users.GPGKey)
            retrieved_gpg_keys = list(self.gh.gpg_keys())
            assert len(retrieved_gpg_keys) > 0
            for retrieved_gpg_key in retrieved_gpg_keys:
                assert isinstance(retrieved_gpg_key, github3.users.GPGKey)
            assert created_gpg_key in retrieved_gpg_keys
            assert created_gpg_key.delete() is True

    def test_key(self):
        """Test the ability to retrieve a user's key."""
        self.token_login()
        cassette_name = self.cassette_name('key')
        with self.recorder.use_cassette(cassette_name):
            key = self.gh.key(14948033)
        assert isinstance(key, github3.users.Key)

    def test_license(self):
        """Test the ability to retrieve a single license."""
        cassette_name = self.cassette_name('license')
        with self.recorder.use_cassette(cassette_name):
            license = self.gh.license('mit')

        assert isinstance(license, github3.licenses.License)

    def test_licenses(self):
        """Test the ability to retrieve open source licenses."""
        cassette_name = self.cassette_name('licenses')
        with self.recorder.use_cassette(cassette_name):
            licenses = list(self.gh.licenses())
            assert len(licenses) > 0

            license = licenses[0]
            assert isinstance(license, github3.licenses.ShortLicense)

    def test_markdown(self):
        """Test the ability to render a markdown document."""
        cassette_name = self.cassette_name('markdown')
        with self.recorder.use_cassette(cassette_name):
            text = "github3.py **is** a python wrapper"
            mode = 'markdown'
            markdown = self.gh.markdown(text=text, mode=mode)
        html = '<p>github3.py <strong>is</strong> a python wrapper</p>\n'
        assert markdown == html

    def test_non_existent_gitignore_template(self):
        """Test the ability to retrieve a single gitignore template."""
        cassette_name = self.cassette_name('non_existent_gitignore_template')
        with self.recorder.use_cassette(cassette_name):
            with pytest.raises(github3.exceptions.NotFoundError):
                self.gh.gitignore_template('i_donut_exist')

    def test_gitignore_templates(self):
        """Test the ability to retrieve a list of gitignore templates."""
        cassette_name = self.cassette_name('gitignore_templates')
        with self.recorder.use_cassette(cassette_name):
            thelist = self.gh.gitignore_templates()

        assert thelist != []
        assert isinstance(thelist, list)

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
                assert isinstance(r, github3.orgs.ShortOrganization)

    def test_all_repositories(self):
        """Test the ability to iterate over all of the repositories."""
        cassette_name = self.cassette_name('iter_all_repos')
        with self.recorder.use_cassette(cassette_name):
            for r in self.gh.all_repositories(number=25):
                assert isinstance(r, github3.repos.ShortRepository)

    def test_all_users(self):
        """Test the ability to iterate over all of the users."""
        cassette_name = self.cassette_name('iter_all_users')
        with self.recorder.use_cassette(cassette_name):
            for u in self.gh.all_users(number=25):
                assert isinstance(u, github3.users.ShortUser)

    def test_all_events(self):
        """Test the ability to iterate over all public events."""
        cassette_name = self.cassette_name('all_events')
        with self.recorder.use_cassette(cassette_name):
            for e in self.gh.all_events(number=25):
                assert isinstance(e, github3.events.Event)

    def test_followers_of(self):
        """Test the ability to iterate over a user's followers."""
        cassette_name = self.cassette_name('followers_of')
        with self.recorder.use_cassette(cassette_name):
            for u in self.gh.followers_of('sigmavirus24', number=25):
                assert isinstance(u, github3.users.ShortUser)

    def test_followers(self):
        """
        Test the ability to iterate over an authenticated user's followers.

        Show the difference between GitHub#followers_of and GitHub#followers.
        """
        self.basic_login()
        cassette_name = self.cassette_name('followers_auth')
        with self.recorder.use_cassette(cassette_name):
            for u in self.gh.followers():
                assert isinstance(u, github3.users.ShortUser)

    def test_user_teams(self):
        """Test the ability to iterate over a user's teams."""
        self.basic_login()
        cassette_name = self.cassette_name('iter_user_teams')
        with self.recorder.use_cassette(cassette_name):
            for t in self.gh.user_teams():
                assert isinstance(t, github3.orgs.ShortTeam)

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

    def test_project(self):
        """Test the ability to retrieve a project by its id."""
        self.token_login()
        cassette_name = self.cassette_name('project')
        with self.recorder.use_cassette(cassette_name):
            r = self.gh.project(398318)

        assert isinstance(r, github3.projects.Project)

    def test_project_card(self):
        """Test the ability to retrieve a project card by its id."""
        self.token_login()
        cassette_name = self.cassette_name('project_card')
        with self.recorder.use_cassette(cassette_name):
            r = self.gh.project_card(2665856)

        assert isinstance(r, github3.projects.ProjectCard)

    def test_project_column(self):
        """Test the ability to retrieve a project column by its id."""
        self.token_login()
        cassette_name = self.cassette_name('project_column')
        with self.recorder.use_cassette(cassette_name):
            r = self.gh.project_column(957217)

        assert isinstance(r, github3.projects.ProjectColumn)

    def test_public_gists(self):
        """Test the ability to iterate over the public gists."""
        since = datetime(2018, 7, 13)
        cassette_name = self.cassette_name('public_gists')
        with self.recorder.use_cassette(cassette_name):
            for r in self.gh.public_gists(since=since, number=25):
                assert isinstance(r, github3.gists.ShortGist)
                assert r.updated_at.replace(tzinfo=None) >= since

    def test_pubsubhubbub(self):
        """Test the ability to create a pubsubhubbub hook."""
        self.token_login()
        cassette_name = self.cassette_name('pubsubhubbub')
        with self.recorder.use_cassette(cassette_name,
                                        **self.betamax_simple_body):
            topic = 'https://github.com/itsmemattchung/github3.py/events/push'
            status = self.gh.pubsubhubbub(
                mode='subscribe',
                topic=topic,
                callback='http://requestb.in/13w3nwt1'
            )
        assert status

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

    def test_repository_invitations(self):
        """Test the ability to retrieve the repository invitation."""
        self.token_login()
        cassette_name = self.cassette_name('repository_invitations')
        with self.recorder.use_cassette(cassette_name):
            invitations = list(self.gh.repository_invitations())

        assert len(invitations) > 0
        for invitation in invitations:
            assert isinstance(invitation, github3.repos.invitation.Invitation)

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
                assert isinstance(r, github3.repos.ShortRepository)

    def test_repositories_by(self):
        """Test the ability to retrieve a user's repositories."""
        cassette_name = self.cassette_name('repositories_by')
        with self.recorder.use_cassette(cassette_name):
            for r in self.gh.repositories_by('dstufft'):
                assert isinstance(r, github3.repos.ShortRepository)

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

    def test_search_commits(self):
        """Test the ability to search for commits."""
        cassette_name = self.cassette_name('search_commits')
        with self.recorder.use_cassette(cassette_name):
            result_iterator = self.gh.search_commits(
                'css repo:octocat/Spoon-Knife')
            commit_result = next(result_iterator)

        assert isinstance(commit_result, github3.search.CommitSearchResult)

    def test_search_commits_with_text_match(self):
        """Test the ability to search for commits  with text matches."""
        cassette_name = self.cassette_name('search_commits_with_text_match')
        with self.recorder.use_cassette(cassette_name):
            result_iterator = self.gh.search_commits(
                'css repo:octocat/Spoon-Knife', text_match=True)
            commit_result = next(result_iterator)

        assert isinstance(commit_result, github3.search.CommitSearchResult)
        assert len(commit_result.text_matches) > 0

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
            issues = self.gh.search_issues('github3 label:Bug')
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

    def test_star(self):
        """Test the ability to star a repository."""
        self.token_login()
        cassette_name = self.cassette_name('star')
        with self.recorder.use_cassette(cassette_name):
            starred = self.gh.star('sigmavirus24', 'github3.py')
        assert starred is True

    def test_update_me(self):
        """Test the ability to update the current authenticated User."""
        cassette_name = self.cassette_name('update_me')
        self.basic_login()
        with self.recorder.use_cassette(cassette_name):
            assert self.gh.update_me(name='Matt "RFC" Chung') is True
            assert self.gh.update_me(name='Matt Chung') is True

    def test_user(self):
        """Test the ability to retrieve a User."""
        cassette_name = self.cassette_name('user')
        with self.recorder.use_cassette(cassette_name):
            sigmavirus24 = self.gh.user('sigmavirus24')

        assert isinstance(sigmavirus24, github3.users.User)
        try:
            assert repr(sigmavirus24)
        except UnicodeEncodeError:
            self.fail('Regression caught. See PR #52. Names must be utf-8'
                      ' encoded')

    def test_unfollow(self):
        """Test the ability to unfollow a user."""
        self.token_login()
        cassette_name = self.cassette_name('unfollow')
        with self.recorder.use_cassette(cassette_name):
            unfollowed = self.gh.unfollow('sigmavirus24')

        assert unfollowed is True

    def test_unstar(self):
        """Test the ability to unstar a repository."""
        self.token_login()
        cassette_name = self.cassette_name('unstar')
        with self.recorder.use_cassette(cassette_name):
            unstarred = self.gh.unstar('sigmavirus24', 'github3.py')

        assert unstarred is True

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


class TestGitHubEnterprise(GitHubEnterpriseHelper):

    def test_admin_stats(self):
        cassette_name = self.cassette_name('admin_stats')
        self.token_login()
        with self.recorder.use_cassette(cassette_name):
            stats = self.gh.admin_stats('all')

        assert isinstance(stats, dict)


class TestGitHubStatus(GitHubStatusHelper):

    def setUp(self):
        super(TestGitHubStatus, self).setUp()

    def test_api(self):
        """Test the ability to check the status of /api."""
        cassette_name = self.cassette_name('api')
        with self.recorder.use_cassette(cassette_name):
            api = self.gh.api()

        assert isinstance(api, dict)

    def test_last_message(self):
        """Test the ability to check the status of /api/last-message."""
        cassette_name = self.cassette_name('last_message')
        with self.recorder.use_cassette(cassette_name):
            last_message = self.gh.last_message()

        assert isinstance(last_message, dict)

    def test_messages(self):
        """Test the ability to check the status of /api/messages."""
        cassette_name = self.cassette_name('messages')
        with self.recorder.use_cassette(cassette_name):
            messages = self.gh.messages()

        assert isinstance(messages, list)

    def test_status(self):
        """Test the ability to check the status of /api/status."""
        cassette_name = self.cassette_name('status')
        with self.recorder.use_cassette(cassette_name):
            status = self.gh.status()

        assert isinstance(status, dict)
