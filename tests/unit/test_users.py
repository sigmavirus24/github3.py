import pytest

import github3

from . import helper

url_for = helper.create_url_helper(
    'https://api.github.com/users/octocat'
)
github_url_for = helper.create_url_helper(
    'https://api.github.com'
)

gpg_key_url_for = helper.create_url_helper(
    'https://api.github.com/user/gpg_keys'
)

key_url_for = helper.create_url_helper(
    'https://api.github.com/user/keys'
)

get_authenticated_user_example_data = helper.create_example_data_helper(
    'authenticated_user_example'
)
get_authenticated_user_2_12_example_data = helper.create_example_data_helper(
    'authenticated_user_2_12_example'
)
get_users_example_data = helper.create_example_data_helper('users_example')
get_user_gpg_key_example_data = helper.create_example_data_helper(
    'user_gpg_key_example'
)
get_user_key_example_data = helper.create_example_data_helper(
    'user_key_example'
)

example_data = get_users_example_data()
authenticated_user_2_12_example_data = (
    get_authenticated_user_2_12_example_data()
)


class TestUser(helper.UnitHelper):

    """Test methods on User class."""

    described_class = github3.users.User
    example_data = get_users_example_data()

    def test_equality(self):
        """Show that two instances are equal."""
        user = github3.users.User(get_users_example_data(), self.session)
        self.instance == user

        user._uniq += 1
        assert self.instance != user

    def test_str(self):
        """Show that instance string is formatted correctly."""
        assert str(self.instance) == 'octocat'
        assert repr(self.instance) == '<User [octocat:monalisa octocat]>'

    def test_is_assignee_on(self):
        """Verify the request for checking if user can be assignee."""
        self.instance.is_assignee_on('octocat', 'hello-world')
        self.session.get.assert_called_once_with(
            github_url_for('repos/octocat/hello-world/assignees/octocat')
        )

    def test_is_following(self):
        """Verify request for checking if a user is following a user."""
        self.instance.is_following('sigmavirus24')
        self.session.get.assert_called_once_with(
            url_for('/following/sigmavirus24')
        )


class TestUserGPGKeyRequiresAuth(helper.UnitRequiresAuthenticationHelper):

    """Unit tests that demonstrate which GPGKey methods require auth."""

    described_class = github3.users.GPGKey
    example_data = get_user_gpg_key_example_data()

    def test_delete(self):
        """Test that deleting a GPG key requires authentication."""
        self.assert_requires_auth(self.instance.delete)


class TestUserGPGKey(helper.UnitHelper):

    """Unit tests for the GPGKey object."""

    described_class = github3.users.GPGKey
    example_data = get_user_gpg_key_example_data()

    def test_delete(self):
        """Verify the request to delete a GPG key."""
        self.instance.delete()

        self.session.delete.assert_called_once_with(
            gpg_key_url_for('3')
        )


class TestUserKeyRequiresAuth(helper.UnitRequiresAuthenticationHelper):

    """Test that ensure certain methods on Key class requires auth."""

    described_class = github3.users.Key
    example_data = get_user_key_example_data()

    def test_update(self):
        """Test that updating a key requires authentication."""
        self.assert_requires_auth(self.instance.update, title='New Title',
                                  key='Fake key')

    def test_delete(self):
        """Test that deleting a key requires authentication."""
        self.assert_requires_auth(self.instance.delete)


class TestUserKey(helper.UnitHelper):

    """Test methods on Key class."""

    described_class = github3.users.Key
    example_data = get_user_key_example_data()

    def test_equality(self):
        """Show that two instances of Key are equal."""
        key = github3.users.Key(get_user_key_example_data(), self.session)
        assert self.instance == key

        key._uniq += "cruft"
        assert self.instance != key

    def test_repr(self):
        """Show instance string is formatted properly."""
        assert str(self.instance) == self.instance.key
        assert repr(self.instance).startswith('<User Key')

    def test_delete(self):
        """Test the request for deleting key."""
        self.instance.delete()
        assert self.session.delete.called is True

    def test_update(self):
        """Test the request for updating a key."""
        data = {
            'title': 'New Title',
            'key': 'Fake key'
        }
        self.instance.update(**data)
        self.patch_called_with(
            key_url_for('1'),
            data=data
        )


class TestUserIterators(helper.UnitIteratorHelper):

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

    def test_gpg_keys(self):
        """Test the request to retrieve a user's GPG keys."""
        i = self.instance.gpg_keys()
        self.get_next(i)

        self.session.get.assert_called_once_with(
            url_for('gpg_keys'),
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
            headers={
                'Accept': 'application/vnd.github.v3.star+json'
            }
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


class TestUsersRequiresAuth(helper.UnitRequiresAuthenticationHelper):

    """Test that ensure certain methods on the User class requires auth."""

    described_class = github3.users.User
    example_data = example_data.copy()

    def test_organization_events(self):
        """Test that #organization_events requires authentication."""
        with pytest.raises(github3.GitHubError):
            self.instance.organization_events('foo')


class TestPlan(helper.UnitHelper):

    """Test for methods on Plan class."""

    described_class = github3.users.Plan
    example_data = get_authenticated_user_example_data()['plan']

    def test_str(self):
        """Show that the instance string is formatted correctly."""
        assert str(self.instance) == self.instance.name
        assert repr(self.instance) == '<Plan [{0}]>'.format(self.instance.name)

    def test_is_free(self):
        """Show that user can check if the plan is free."""
        assert self.instance.is_free() is False


class TestAuthenticatedUserCompatibility_2_12(helper.UnitHelper):

    """Test methods on AuthenticatedUser from Github Enterprise 2.12."""

    described_class = github3.users.AuthenticatedUser
    example_data = authenticated_user_2_12_example_data

    def test_user(self):
        """Test the ability to retrieve an AuthenticatedUser"""
        assert str(self.instance) == 'octocat'
