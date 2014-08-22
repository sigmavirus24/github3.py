import pytest

import github3

from .helper import (UnitHelper, UnitIteratorHelper, create_url_helper,)

url_for = create_url_helper(
    'https://api.github.com/users/octocat'
)

example_data = {
    "login": "octocat",
    "id": 1,
    "avatar_url": "https://github.com/images/error/octocat_happy.gif",
    "gravatar_id": "somehexcode",
    "url": "https://api.github.com/users/octocat",
    "html_url": "https://github.com/octocat",
    "followers_url": "https://api.github.com/users/octocat/followers",
    "following_url": ("https://api.github.com/users/octocat/following"
                      "{/other_user}"),
    "gists_url": "https://api.github.com/users/octocat/gists{/gist_id}",
    "starred_url": ("https://api.github.com/users/octocat/starred"
                    "{/owner}{/repo}"),
    "subscriptions_url": "https://api.github.com/users/octocat/subscriptions",
    "organizations_url": "https://api.github.com/users/octocat/orgs",
    "repos_url": "https://api.github.com/users/octocat/repos",
    "events_url": "https://api.github.com/users/octocat/events{/privacy}",
    "received_events_url": ("https://api.github.com/users/octocat/"
                            "received_events"),
    "type": "User",
    "site_admin": False,
    "name": "monalisa octocat",
    "company": "GitHub",
    "blog": "https://github.com/blog",
    "location": "San Francisco",
    "email": "octocat@github.com",
    "hireable": False,
    "bio": "There once was...",
    "public_repos": 2,
    "public_gists": 1,
    "followers": 20,
    "following": 0,
    "created_at": "2008-01-14T04:33:35Z",
    "updated_at": "2008-01-14T04:33:35Z"
}


class TestUserIterators(UnitIteratorHelper):

    """Test User methods that return iterators."""

    described_class = github3.users.User
    example_data = example_data.copy()

    def test_events(self):
        """Test the request to retrieve a user's events."""
        i = self.instance.events()
        self.get_next(i)

        self.session.get.assert_called_once_with(
            url_for('events'),
            params={'per_page': 100},
            headers={}
        )

    def test_followers(self):
        """Test the request to retrieve follwers."""
        f = self.instance.followers()
        self.get_next(f)

        self.session.get.assert_called_once_with(
            url_for('followers'),
            params={'per_page': 100},
            headers={}
        )

    def test_following(self):
        """Test the request to retrieve users a user is following."""
        i = self.instance.following()
        self.get_next(i)

        self.session.get.assert_called_once_with(
            url_for('following'),
            params={'per_page': 100},
            headers={}
        )

    def test_keys(self):
        """Test the request to retrieve a user's public keys."""
        i = self.instance.keys()
        self.get_next(i)

        self.session.get.assert_called_once_with(
            url_for('keys'),
            params={'per_page': 100},
            headers={}
        )

    def test_organization_events(self):
        """Test the request to retrieve a user's organization events."""
        i = self.instance.organization_events('org-name')
        self.get_next(i)

        self.session.get.assert_called_once_with(
            url_for('events/orgs/org-name'),
            params={'per_page': 100},
            headers={}
        )

    def test_organization_events_requires_an_org(self):
        """Test that organization_events will ignore empty org names."""
        i = self.instance.organization_events(None)

        with pytest.raises(StopIteration):
            next(i)

    def test_organizations(self):
        """Test the request to retrieve the orgs a user belongs to."""
        i = self.instance.organizations()
        self.get_next(i)

        self.session.get.assert_called_once_with(
            url_for('orgs'),
            params={'per_page': 100},
            headers={}
        )

    def test_received_events(self):
        """Test the request to retrieve the events a user receives."""
        i = self.instance.received_events()
        self.get_next(i)

        self.session.get.assert_called_once_with(
            url_for('received_events'),
            params={'per_page': 100},
            headers={}
        )

    def test_received_events_public_only(self):
        """Test the public request to retrieve the events a user received."""
        i = self.instance.received_events(True)
        self.get_next(i)

        self.session.get.assert_called_once_with(
            url_for('received_events/public'),
            params={'per_page': 100},
            headers={}
        )

    def test_starred_repositories(self):
        """Test the request to retrieve a user's starred repos."""
        i = self.instance.starred_repositories()
        self.get_next(i)

        self.session.get.assert_called_once_with(
            url_for('starred'),
            params={'per_page': 100},
            headers={}
        )

    def test_subscriptions(self):
        """Test the request to retrieve a user's subscriptions."""
        i = self.instance.subscriptions()
        self.get_next(i)

        self.session.get.assert_called_once_with(
            url_for('subscriptions'),
            params={'per_page': 100},
            headers={}
        )


class TestUsersRequiresAuth(UnitHelper):

    """Test that ensure certain methods on the User class requires auth."""

    described_class = github3.users.User
    example_data = example_data.copy()

    def after_setup(self):
        """Disable authentication on sessions."""
        self.session.has_auth.return_value = False

    def test_organization_events(self):
        """Test that #organization_events requires authentication."""
        with pytest.raises(github3.GitHubError):
            self.instance.organization_events('foo')
