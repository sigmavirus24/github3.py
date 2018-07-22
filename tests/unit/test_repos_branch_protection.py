"""Unit tests for methods implemented on Branch Protection."""

import github3
from github3.repos.branch import BranchProtection

from . import helper

protection_example_data = helper.create_example_data_helper(
    'branch_protection_example'
)
protection_url_for = helper.create_url_helper(
    'https://api.github.com/repos/octocat/Hello-World/'
    'branches/master/protection'
)


enforce_admins_url_for = helper.create_url_helper(
    'https://api.github.com/repos/octocat/Hello-World/'
    'branches/master/protection/enforce_admins'
)
enforce_admins_example_data = helper.create_example_data_helper(
    'branch_protection_enforce_admins_example')


class TestProtectionEnforceAdmins(helper.UnitHelper):
    """Unit tests around the ProtectionRequiredPullRequestReviews class."""

    described_class = github3.repos.branch.ProtectionEnforceAdmins
    example_data = enforce_admins_example_data()

    def test_enable(self):
        """Verify the request to enable admin enforcement."""
        self.instance.enable()
        self.post_called_with(enforce_admins_url_for(),
                              headers=BranchProtection.PREVIEW_HEADERS_MAP)

    def test_disable(self):
        """Verify the request to disable admin enforcement."""
        self.instance.disable()
        self.delete_called_with(enforce_admins_url_for(),
                                headers=BranchProtection.PREVIEW_HEADERS_MAP)


protection_required_pull_request_reviews_url_for = helper.create_url_helper(
    'https://api.github.com/repos/octocat/Hello-World/'
    'branches/master/protection/required_pull_request_reviews'
)
protection_required_pull_request_reviews_data = \
    helper.create_example_data_helper(
        'branch_protection_required_pull_request_reviews_example'
    )


class TestProtectionRequiredPullRequestReviews(helper.UnitHelper):
    """Unit tests around the ProtectionRequiredPullRequestReviews class."""

    described_class = github3.repos.branch.ProtectionRequiredPullRequestReviews
    example_data = protection_required_pull_request_reviews_data()

    def test_update(self):
        """Verify the request to update required PR review protections."""
        teams = [
            team.slug
            for team in self.instance.dismissal_restrictions.original_teams
        ]
        users = [
            user.login
            for user in self.instance.dismissal_restrictions.original_users
        ]
        update_json = {
            'dismiss_stale_reviews': self.instance.dismiss_stale_reviews,
            'require_code_owner_reviews':
                self.instance.require_code_owner_reviews,
            'required_approving_review_count':
                self.instance.required_approving_review_count,
            'dismissal_restrictions': {
                'teams': teams,
                'users': users
            }
        }

        self.instance.update()
        self.patch_called_with(
            protection_required_pull_request_reviews_url_for(),
            json=update_json
        )

    def test_delete(self):
        self.instance.delete()
        self.delete_called_with(
            protection_required_pull_request_reviews_url_for()
        )


protection_restrictions_url_for = helper.create_url_helper(
    'https://api.github.com/repos/octocat/Hello-World/'
    'branches/master/protection/restrictions'
)
protection_restrictions_teams_url_for = helper.create_url_helper(
    'https://api.github.com/repos/octocat/Hello-World/'
    'branches/master/protection/restrictions/teams'
)
protection_restrictions_users_url_for = helper.create_url_helper(
    'https://api.github.com/repos/octocat/Hello-World/'
    'branches/master/protection/restrictions/users'
)
protection_restrictions_example_data = helper.create_example_data_helper(
    'branch_protection_restrictions_example'
)


class TestProtectionRestrictions(helper.UnitHelper):
    """Unit tests around the ProtectionRestrictions class."""

    described_class = github3.repos.branch.ProtectionRestrictions
    example_data = protection_restrictions_example_data()

    def test_add_teams(self):
        """Verify the request to add new teams."""
        self.instance.add_teams(['justice-league'])
        self.post_called_with(
            protection_restrictions_teams_url_for(),
            data=['justice-league'],
            headers=BranchProtection.PREVIEW_HEADERS_MAP['nested_teams'],
        )

    def test_remove_teams(self):
        """Verify the request to remove teams."""
        self.instance.remove_teams(['justice-league'])
        self.delete_called_with(
            protection_restrictions_teams_url_for(),
            json=['justice-league'],
            headers=BranchProtection.PREVIEW_HEADERS_MAP['nested_teams'],
        )

    def test_add_users(self):
        """Verify the request to add new users."""
        self.instance.add_users(['sigmavirus24'])
        self.post_called_with(
            protection_restrictions_users_url_for(),
            data=['sigmavirus24'],
        )

    def test_remove_users(self):
        """Verify the request to remove users."""
        self.instance.remove_users(['sigmavirus24'])
        self.delete_called_with(
            protection_restrictions_users_url_for(),
            json=['sigmavirus24'],
        )

    def test_delete(self):
        """Verify the request to delete all restrictions."""
        self.instance.delete()
        self.delete_called_with(
            protection_restrictions_url_for(),
        )

    def test_replace_teams(self):
        """Verify the request to replace teams."""
        self.instance.replace_teams(['justice-league'])
        self.put_called_with(
            protection_restrictions_teams_url_for(),
            json=['justice-league'],
            headers=BranchProtection.PREVIEW_HEADERS_MAP['nested_teams'],
        )

    def test_replace_users(self):
        """Verify the request to replace users."""
        self.instance.replace_users(['sigmavirus24'])
        self.put_called_with(
            protection_restrictions_users_url_for(),
            json=['sigmavirus24'],
        )


protection_required_status_checks_url_for = helper.create_url_helper(
    'https://api.github.com/repos/octocat/Hello-World/'
    'branches/master/protection/required_status_checks'
)

protection_required_status_checks_contexts_url_for = helper.create_url_helper(
    'https://api.github.com/repos/octocat/Hello-World/'
    'branches/master/protection/required_status_checks/contexts'
)

protection_required_status_checks_example_data = \
    helper.create_example_data_helper(
        'branch_protection_required_status_checks_example'
    )


class TestProtectionRequiredStatusChecks(helper.UnitHelper):
    """Unit tests around the ProtectionRequiredStatusChecks class."""

    described_class = github3.repos.branch.ProtectionRequiredStatusChecks
    example_data = protection_required_status_checks_example_data()

    def test_add_contexts(self):
        """Verify the request to add contexts to required status checks."""
        self.instance.add_contexts(['continuous-integration/jenkins'])
        self.post_called_with(
            protection_required_status_checks_contexts_url_for(),
            data=['continuous-integration/jenkins']
        )

    def test_contexts(self):
        """Verify the request to retrieve contexts."""
        self.instance.contexts()
        self.session.get.assert_called_once_with(
            protection_required_status_checks_contexts_url_for(),
        )

    def test_replace_contexts(self):
        """Verify the request ro replace required status check contexts."""
        self.instance.replace_contexts(['continuous-integration/jenkins'])
        self.put_called_with(
            protection_required_status_checks_contexts_url_for(),
            json=['continuous-integration/jenkins']
        )

    def test_delete_contexts(self):
        """Verify the request to remove contexts."""
        self.instance.delete_contexts(['continuous-integration/jenkins'])
        self.delete_called_with(
            protection_required_status_checks_contexts_url_for(),
            json=['continuous-integration/jenkins']
        )

    def test_update(self):
        """Verify the request to update the required status checks."""
        self.instance.update(True, ['continuous-integration/jenkins'])
        update_data = {
            'strict': True,
            'contexts': ['continuous-integration/jenkins']
        }
        self.patch_called_with(protection_required_status_checks_url_for(),
                               json=update_data)

    def test_update_not_strict(self):
        """Verify another variant of the update request."""
        self.instance.update(False, ['continuous-integration/jenkins'])
        update_data = {
            'strict': False,
            'contexts': ['continuous-integration/jenkins']
        }
        self.patch_called_with(protection_required_status_checks_url_for(),
                               json=update_data)

    def test_update_no_strict(self):
        """Verify updating contexts only sends contexts."""
        self.instance.update(contexts=['continuous-integration/jenkins'])
        update_data = {
            'contexts': ['continuous-integration/jenkins']
        }
        self.patch_called_with(protection_required_status_checks_url_for(),
                               json=update_data)

    def test_delete(self):
        """Verify the request to delete required status checks."""
        self.instance.delete()
        self.delete_called_with(protection_required_status_checks_url_for())
