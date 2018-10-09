"""Unit tests for methods implemented on Branch."""
import github3
from . import helper

get_example_data = helper.create_example_data_helper('repos_branch_example')
url_for_commits = helper.create_url_helper(
    'https://api.github.com/repos/octocat/Hello-World/commits/master'
)
url_for_protection = helper.create_url_helper(
    'https://api.github.com/repos/octocat/Hello-World/'
    'branches/master/protection'
)


class TestBranch(helper.UnitHelper):
    """Branch unit tests."""

    described_class = github3.repos.branch.Branch
    example_data = get_example_data()

    def test_latest_sha(self):
        """Verify the request for retreiving the latest_sha."""
        headers = {
            'Accept': 'application/vnd.github.v3.sha',
            'If-None-Match': '"123"'
        }
        self.instance.latest_sha(differs_from='123')
        self.session.get.assert_called_once_with(
            url_for_commits(),
            headers=headers
        )

    def test_protect(self):
        """Verify the request to protect a branch."""
        headers = {
            'Accept': 'application/vnd.github.luke-cage-preview+json'
        }
        json = {
            'required_status_checks': {
                'contexts': [
                    'continuous-integration/travis-ci'
                ],
                'strict': True
            },
            'enforce_admins': True,
            'required_pull_request_reviews': {
                'dismissal_restrictions': {
                    'users': [
                        'octocat'
                    ],
                    'teams': [
                        'justice-league'
                    ]
                },
                'dismiss_stale_reviews': True,
                'require_code_owner_reviews': True,
                'required_approving_review_count': 2
            },
            'restrictions': {
                'users': [
                    'octocat'
                ],
                'teams': [
                    'justice-league'
                ]
            }
        }

        self.instance.protect(
            enforce_admins=True,
            required_status_checks={
                'contexts': [
                    'continuous-integration/travis-ci'
                ],
                'strict': True
            },
            required_pull_request_reviews={
                'dismissal_restrictions': {
                    'users': [
                        'octocat'
                    ],
                    'teams': [
                        'justice-league'
                    ]
                },
                'dismiss_stale_reviews': True,
                'require_code_owner_reviews': True,
                'required_approving_review_count': 2
            },
            restrictions={
                'users': [
                    'octocat'
                ],
                'teams': [
                    'justice-league'
                ]
            }
        )
        self.session.put.assert_called_once_with(
            url_for_protection(),
            headers=headers,
            json=json
        )

    def test_unprotect(self):
        """Verify the request to unprotect a branch."""
        headers = {
            'Accept': 'application/vnd.github.luke-cage-preview+json'
        }

        self.instance.unprotect()
        self.session.delete.assert_called_once_with(
            url_for_protection(),
            headers=headers
        )


class TestBranchRequiresAuth(helper.UnitRequiresAuthenticationHelper):

    """Unit tests for Branch methods that require authentication."""

    described_class = github3.repos.branch.Branch
    example_data = get_example_data()

    def test_protect(self):
        """Verify that protecting a branch requires authentication."""
        self.assert_requires_auth(self.instance.protect)

    def test_unprotect(self):
        """Verify that unprotecting a branch requires authentication."""
        self.assert_requires_auth(self.instance.unprotect)
