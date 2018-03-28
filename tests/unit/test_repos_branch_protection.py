"""Unit tests for methods implemented on Branch Protection."""
import github3
from github3.repos.branch import BranchProtection
from . import helper
from json import dumps

protection_example_data = helper.create_example_data_helper(
    'branch_protection_example'
)
protection_url_for = helper.create_url_helper(
    'https://api.github.com/repos/octocat/Hello-World/'
    'branches/master/protection'
)


# class TestBranchProtection(helper.UnitRequiresAuthenticationHelper):
#     """Branch protection unit test"""
#
#     described_class = github3.repos.branch.BranchProtection
#     example_data = protection_example_data()
#
#     def test_protect(self):
#         """Verify PUT method works"""
#         self.instance.enforce_admins = True
#         self.instance.restrictions = ['continuous-integration/travis-ci']
#         self.instance.update()
#         self.put_called_with(url_for())
#
#     def test_unprotect(self):
#         """Verify DELETE method works"""
#         self.instance.delete()
#         self.delete_called_with(url_for())


enforce_admins_url_for = helper.create_url_helper(
    'https://api.github.com/repos/octocat/Hello-World/'
    'branches/master/protection/enforce_admins'
)
enforce_admins_example_data = helper.create_example_data_helper(
    'branch_protection_enforce_admins_example')


class TestProtectionEnforceAdmins(helper.UnitHelper):
    described_class = github3.repos.branch.ProtectionEnforceAdmins
    example_data = enforce_admins_example_data()

    def test_enable(self):
        self.instance.enable()
        self.post_called_with(enforce_admins_url_for(),
                              headers=BranchProtection.PREVIEW_HEADERS_MAP)

    def test_disable(self):
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
    described_class = github3.repos.branch.ProtectionRequiredPullRequestReviews
    example_data = protection_required_pull_request_reviews_data()

    def test_set_required_code_owner_reviews(self):
        self.instance.set_required_code_owner_reviews(False)
        assert self.instance.require_code_owner_reviews is False

    def test_set_dismiss_stale_reviews(self):
        self.instance.set_dismiss_stale_reviews(False)
        assert self.instance.dismiss_stale_reviews is False

    def test_set_required_approving_review_count(self):
        self.instance.set_required_approving_review_count(10)
        assert self.instance.required_approving_review_count == 10

    def test_update(self):
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
    described_class = github3.repos.branch.ProtectionRestrictions
    example_data = protection_restrictions_example_data()

    def test_add_teams(self):
        self.instance.add_teams(['justice-league'])
        self.post_called_with(protection_restrictions_teams_url_for(),
                              data=['justice-league'],
                              headers=BranchProtection.PREVIEW_HEADERS_MAP)

    def test_remove_teams(self):
        self.instance.remove_teams(['justice-league'])
        self.delete_called_with(protection_restrictions_teams_url_for(),
                                json=dumps(['justice-league']),
                                headers=BranchProtection.PREVIEW_HEADERS_MAP)

    def test_add_users(self):
        self.instance.add_users(['sigmavirus24'])
        self.post_called_with(protection_restrictions_users_url_for(),
                              data=['sigmavirus24'],
                              headers=BranchProtection.PREVIEW_HEADERS_MAP)

    def test_remove_users(self):
        self.instance.remove_users(['sigmavirus24'])
        self.delete_called_with(protection_restrictions_users_url_for(),
                                json=dumps(['sigmavirus24']),
                                headers=BranchProtection.PREVIEW_HEADERS_MAP)

    def test_delete(self):
        self.instance.delete()
        self.delete_called_with(protection_restrictions_url_for(),
                                headers=BranchProtection.PREVIEW_HEADERS_MAP)

    def test_set_teams(self):
        self.instance.set_teams(['justice-league'])
        self.put_called_with(protection_restrictions_teams_url_for(),
                             json=dumps(['justice-league']),
                             headers=BranchProtection.PREVIEW_HEADERS_MAP)

    def test_set_users(self):
        self.instance.set_users(['sigmavirus24'])
        self.put_called_with(protection_restrictions_users_url_for(),
                             json=dumps(['sigmavirus24']),
                             headers=BranchProtection.PREVIEW_HEADERS_MAP)


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
    described_class = github3.repos.branch.ProtectionRequiredStatusChecks
    example_data = protection_required_status_checks_example_data()
    _json_data = dumps(['continuous-integration/jenkins'])

    def test_add_contexts(self):
        self.instance.add_contexts(['continuous-integration/jenkins'])
        self.post_called_with(
            protection_required_status_checks_contexts_url_for(),
            data=['continuous-integration/jenkins']
        )

    def test_contexts(self):
        self.instance.contexts()
        self.get_called_with(protection_required_status_checks_contexts_url_for())

    def test_replace_contexts(self):
        self.instance.replace_contexts(self._json_data)
        self.put_called_with(
            protection_required_status_checks_contexts_url_for(),
            json=self._json_data
        )

    def test_delete_contexts(self):
        self.instance.delete_contexts(self._json_data)
        self.delete_called_with(
            protection_required_status_checks_contexts_url_for(),
            json=self._json_data
        )

    def test_update(self):
        self.instance.update(True, ['continuous-integration/jenkins'])
        update_data = {
            'strict': True,
            'contexts': ['continuous-integration/jenkins']
        }
        self.patch_called_with(protection_required_status_checks_url_for(),
                               json=update_data)

    def test_update_not_strict(self):
        self.instance.update(False, ['continuous-integration/jenkins'])
        update_data = {
            'strict': False,
            'contexts': ['continuous-integration/jenkins']
        }
        self.patch_called_with(protection_required_status_checks_url_for(),
                               json=update_data)

    def test_update_no_strict(self):
        self.instance.update(None, ['continuous-integration/jenkins'])
        update_data = {
            'contexts': ['continuous-integration/jenkins']
        }
        self.patch_called_with(protection_required_status_checks_url_for(),
                               json=update_data)

    def test_delete(self):
        self.instance.delete()
        self.delete_called_with(protection_required_status_checks_url_for())
