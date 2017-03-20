import pytest

from github3 import GitHubError
from github3.orgs import Organization

from . import helper

url_for = helper.create_url_helper('https://api.github.com/orgs/github')

get_org_example_data = helper.create_example_data_helper(
    'org_example')


class TestInvites(helper.UnitIteratorHelper):
    described_class = Organization
    example_data = get_org_example_data()

    def test_get_invitations_iterator(self):
        """Show that one can iterate of all outstanding invitations."""
        i = self.instance.invitations()
        self.get_next(i)

        self.session.get.assert_called_once_with(
            url_for('invitations'),
            params={'per_page': 100},
            headers={'Accept': 'application/vnd.github.korra-preview'}
        )


class TestInvitesRequiresAuth(helper.UnitRequiresAuthenticationHelper):
    described_class = Organization
    example_data = get_org_example_data()

    def test_get_invitations_requires_auth(self):
        """
            Show that getting outstanding invitations requires authentication.
        """
        with pytest.raises(GitHubError):
            self.instance.invitations()
