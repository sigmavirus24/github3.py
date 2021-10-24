"""Integration tests for methods implemented on Check* classes."""
import datetime

import dateutil
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
                    assert not pref["setting"]
                    break
            else:
                pytest.fail(f"No setting in response for app: {app_id}")

            json = repo.auto_trigger_checks(app_id, enabled=True)
            for pref in json["preferences"]["auto_trigger_checks"]:
                if pref["app_id"] == app_id:
                    assert pref["setting"]
                    break
            else:
                pytest.fail(f"No setting in response for app: {app_id}")


class TestCheckApp(IntegrationHelper):
    @pytest.mark.skip
    def test_check_app_refresh(self):
        cassette_name = self.cassette_name("create_check_run")
        with self.recorder.use_cassette(cassette_name):
            self.app_installation_login()
            repo = self.gh.repository("westphahl", "github3.py")
            branch = repo.branch("checks-test")
            check_suite = next(branch.commit.check_suites())

            app = check_suite.app
            assert isinstance(app, github3.checks.CheckApp)
            app = app.refresh()
            assert isinstance(app, github3.apps.App)


class TestCheckRun(IntegrationHelper):
    def get_repo(self, repository="westphahl/github3.py"):
        owner, name = repository.split("/")
        return self.gh.repository(owner, name)

    def get_branch(self, repository=None, name="checks-test"):
        repo = repository or self.get_repo()
        return repo.branch(name)

    def test_create_check_run(self):
        cassette_name = self.cassette_name("create_check_run")
        with self.recorder.use_cassette(cassette_name):
            self.app_installation_login()
            repo = self.get_repo()
            branch = self.get_branch(repo)

            check_run = repo.create_check_run(
                name="test_create_check_run", head_sha=branch.commit.sha
            )
            assert isinstance(check_run, github3.checks.CheckRun)

    def test_check_runs_in_suite(self):
        cassette_name = self.cassette_name("check_runs_in_suite")
        with self.recorder.use_cassette(cassette_name):
            self.app_installation_login()
            branch = self.get_branch()
            check_suite = next(branch.commit.check_suites())

            check_runs = list(check_suite.check_runs())
            assert check_runs != []
            for run in check_runs:
                assert isinstance(run, github3.checks.CheckRun)

    def test_check_runs_for_ref(self):
        cassette_name = self.cassette_name("check_runs_for_ref")
        with self.recorder.use_cassette(cassette_name):
            self.app_installation_login()
            branch = self.get_branch()

            check_runs = list(branch.commit.check_runs())
            assert check_runs != []
            for run in check_runs:
                assert isinstance(run, github3.checks.CheckRun)

    def test_check_run_by_id(self):
        cassette_name = self.cassette_name("check_run_by_id")
        with self.recorder.use_cassette(cassette_name):
            self.app_installation_login()
            repo = self.get_repo()
            branch = self.get_branch(repo)

            check_run = next(branch.commit.check_runs())
            assert check_run == repo.check_run(check_run.id)

    def test_update_check_run(self):
        cassette_name = self.cassette_name("update_check_run")
        with self.recorder.use_cassette(cassette_name):
            self.app_installation_login()
            repo = self.get_repo()
            branch = self.get_branch(repo)

            check_run = repo.create_check_run(
                name="test_update_check_run", head_sha=branch.commit.sha
            )
            assert check_run.status == "queued"
            assert check_run.conclusion is None
            assert check_run.update(status="in_progress")
            check_run.refresh()
            assert check_run.status == "in_progress"
            completed_at = datetime.datetime(
                2019, 1, 1, 13, 37, tzinfo=dateutil.tz.UTC
            )
            assert check_run.update(
                status="completed",
                conclusion="success",
                completed_at=completed_at.isoformat(),
            )
            check_run.refresh()
            assert check_run.status == "completed"
            assert check_run.conclusion == "success"

    def test_check_run_annotations(self):
        cassette_name = self.cassette_name("check_run_annotations")
        with self.recorder.use_cassette(cassette_name):
            self.app_installation_login()
            repo = self.get_repo()
            branch = self.get_branch(repo)

            output = {
                "title": "Check run title",
                "summary": "Summary of this check run",
                "annotations": [
                    {
                        "path": "AUTHORS.rst",
                        "start_line": 179,
                        "end_line": 180,
                        "annotation_level": "failure",
                        "message": "Should be removed",
                    },
                    {
                        "path": "AUTHORS.rst",
                        "start_line": 180,
                        "end_line": 180,
                        "annotation_level": "warning",
                        "message": "Not sure if he is a contributor",
                    },
                    {
                        "path": "AUTHORS.rst",
                        "start_line": 180,
                        "end_line": 180,
                        "annotation_level": "notice",
                        "message": "lol",
                    },
                ],
            }

            check_run = repo.create_check_run(
                name="test_check_run_annotations",
                head_sha=branch.commit.sha,
                status="in_progress",
                output=output,
                actions=[
                    {
                        "label": "Abort",
                        "description": "Abort the check run",
                        "identifier": "abort_check_xyz",
                    }
                ],
            )
            assert check_run.status == "in_progress"
            assert len(list(check_run.output.annotations())) == 3

            completed_at = datetime.datetime(
                2019, 1, 1, 13, 37, tzinfo=dateutil.tz.UTC
            )
            assert check_run.update(
                status="completed",
                conclusion="failure",
                completed_at=completed_at.isoformat(),
                actions=[],
            )
            check_run.refresh()
            assert check_run.status == "completed"
            assert check_run.conclusion == "failure"
            assert len(list(check_run.output.annotations())) == 3
