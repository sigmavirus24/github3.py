"""Integration tests for methods implemented on Check* classes."""
import pytest

import github3

from .helper import IntegrationHelper


class TestCheckSuite(IntegrationHelper):
    def get_repo(self, repository="westphahl/github3.py"):
        owner, name = repository.split("/")
        return self.gh.repository(owner, name)

    def get_branch(self, repository=None, name="checks-test"):
        repo = repository or self.get_repo()
        return repo.branch(name)

    def test_create_check_suite(self):
        # auto trigger checks needs to be disabled
        # to be able to re-record this cassette
        cassette_name = self.cassette_name("create_check_suite")
        with self.recorder.use_cassette(cassette_name):
            self.app_installation_login()
            repo = self.get_repo()
            branch = self.get_branch(repo)

            suite = repo.create_check_suite(branch.commit.sha)
            assert isinstance(suite, github3.checks.CheckSuite)

    def test_check_suite_by_id(self):
        cassette_name = self.cassette_name("check_suite_by_id")
        with self.recorder.use_cassette(cassette_name):
            self.app_installation_login()
            repo = self.get_repo()
            branch = self.get_branch(repo)

            check_suite = next(branch.commit.check_suites())
            assert check_suite == repo.check_suite(check_suite.id)

    def test_check_suites_for_ref(self):
        cassette_name = self.cassette_name("list_check_suites")
        with self.recorder.use_cassette(cassette_name):
            self.app_installation_login()
            branch = self.get_branch()

            for suite in branch.commit.check_suites():
                assert isinstance(suite, github3.checks.CheckSuite)

    def test_rerequest_check_suite(self):
        cassette_name = self.cassette_name("rerequest_check_suite")
        with self.recorder.use_cassette(cassette_name):
            self.app_installation_login()
            branch = self.get_branch()

            check_suite = next(branch.commit.check_suites())
            assert check_suite.rerequest()

    def test_auto_trigger_checks_prefs(self):
        # App id needs to be fixed since we use a recorded session
        app_id = 22985
        cassette_name = self.cassette_name("auto_trigger_checks_prefs")
        with self.recorder.use_cassette(cassette_name):
            self.app_installation_login()
            repo = self.get_repo()

            json = repo.auto_trigger_checks(app_id, enabled=False)
            for pref in json["preferences"]["auto_trigger_checks"]:
                if pref["app_id"] == app_id:
                    assert pref["setting"] == False
                    break
            else:
                pytest.fail(
                    "No setting in response for app: {}".format(app_id)
                )

            json = repo.auto_trigger_checks(app_id, enabled=True)
            for pref in json["preferences"]["auto_trigger_checks"]:
                if pref["app_id"] == app_id:
                    assert pref["setting"] == True
                    break
            else:
                pytest.fail(
                    "No setting in response for app: {}".format(app_id)
                )
