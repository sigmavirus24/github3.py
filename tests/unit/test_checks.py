"""Unit tests around github3's Checks classes."""
from json import dumps

import pytest

import github3
from .helper import create_example_data_helper
from .helper import create_url_helper
from .helper import UnitAppInstallHelper
from .helper import UnitHelper
from .helper import UnitIteratorHelper
from .helper import UnitRequiresAuthenticationHelper
from github3.checks import CheckRun
from github3.checks import CheckSuite
from github3.exceptions import GitHubException

url_for = create_url_helper("https://api.github.com/repos/github/hello-world")

check_run_example_data = create_example_data_helper("check_run_example")
check_suite_example_data = create_example_data_helper("check_suite_example")


class TestCheckRun(UnitAppInstallHelper):
    described_class = CheckRun
    example_data = check_run_example_data()

    def test_update(self):
        """Show that a check run can be updated"""

        data = {"name": "newname"}
        self.instance.update(**data)

        self.session.patch.assert_called_once_with(
            url_for("check-runs/4"),
            dumps(data),
            headers=CheckRun.CUSTOM_HEADERS,
        )

    def test_check_run_types(self):
        """Check that we get the right types"""

        assert isinstance(self.instance.app, github3.checks.CheckApp)

        assert isinstance(
            self.instance.original_pull_requests[0],
            github3.checks.CheckPullRequest,
        )


class TestCheckRunRequiresAuth(UnitRequiresAuthenticationHelper):
    described_class = CheckRun
    example_data = check_run_example_data()

    def test_update_requires_auth(self):
        """Show updating a run requires auth"""
        with pytest.raises(GitHubException):
            self.instance.update(name="newname")


class TestCheckSuite(UnitHelper):
    described_class = CheckSuite
    example_data = check_suite_example_data()

    def test_rerequest(self):
        """Show that a check suite can be rerequested"""

        self.instance.rerequest()
        self.session.post.assert_called_once_with(
            url_for("check-suites/5/rerequest"),
            None,
            headers=CheckSuite.CUSTOM_HEADERS,
        )

    def test_check_suite_types(self):
        """Check that we get the right types"""

        assert isinstance(self.instance.app, github3.checks.CheckApp)

        assert isinstance(
            self.instance.repository, github3.repos.ShortRepository
        )


class TestCheckSuiteIterator(UnitIteratorHelper):
    described_class = CheckSuite
    example_data = check_suite_example_data()

    def test_check_runs(self):
        i = self.instance.check_runs()
        self.get_next(i)

        self.session.get.assert_called_once_with(
            url_for("check-suites/5/check-runs"),
            params={"per_page": 100},
            headers=CheckSuite.CUSTOM_HEADERS,
        )
