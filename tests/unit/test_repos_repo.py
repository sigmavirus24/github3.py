"""Unit tests for Repositories."""
import datetime
import pytest

from github3 import GitHubError
from github3.repos.repo import Repository

from .helper import (UnitHelper, UnitIteratorHelper, create_url_helper)

url_for = create_url_helper(
    'https://api.github.com/repos/octocat/Hello-World'
)

repo_example_data = {
    "id": 1296269,
    "owner": {
        "login": "octocat",
        "id": 1,
        "avatar_url": "https://github.com/images/error/octocat_happy.gif",
        "gravatar_id": "somehexcode",
        "url": "https://api.github.com/users/octocat"
        },
    "name": "Hello-World",
    "full_name": "octocat/Hello-World",
    "description": "This your first repo!",
    "private": False,
    "fork": False,
    "url": "https://api.github.com/repos/octocat/Hello-World",
    "html_url": "https://github.com/octocat/Hello-World",
    "clone_url": "https://github.com/octocat/Hello-World.git",
    "git_url": "git://github.com/octocat/Hello-World.git",
    "ssh_url": "git@github.com:octocat/Hello-World.git",
    "svn_url": "https://svn.github.com/octocat/Hello-World",
    "mirror_url": "git://git.example.com/octocat/Hello-World",
    "homepage": "https://github.com",
    "language": None,
    "forks": 9,
    "forks_count": 9,
    "watchers": 80,
    "watchers_count": 80,
    "size": 108,
    "master_branch": "master",
    "open_issues": 0,
    "open_issues_count": 0,
    "pushed_at": "2011-01-26T19:06:43Z",
    "created_at": "2011-01-26T19:01:12Z",
    "updated_at": "2011-01-26T19:14:43Z",
    "organization": {
        "login": "octocat",
        "id": 1,
        "avatar_url": "https://github.com/images/error/octocat_happy.gif",
        "gravatar_id": "somehexcode",
        "url": "https://api.github.com/users/octocat",
        "type": "Organization"
        },
    "parent": {
        "id": 1296269,
        "owner": {
            "login": "octocat",
            "id": 1,
            "avatar_url": "https://github.com/images/error/octocat.gif",
            "gravatar_id": "somehexcode",
            "url": "https://api.github.com/users/octocat"
            },
        "name": "Hello-World",
        "full_name": "octocat/Hello-World",
        "description": "This your first repo!",
        "private": False,
        "fork": True,
        "url": "https://api.github.com/repos/octocat/Hello-World",
        "html_url": "https://github.com/octocat/Hello-World",
        "clone_url": "https://github.com/octocat/Hello-World.git",
        "git_url": "git://github.com/octocat/Hello-World.git",
        "ssh_url": "git@github.com:octocat/Hello-World.git",
        "svn_url": "https://svn.github.com/octocat/Hello-World",
        "mirror_url": "git://git.example.com/octocat/Hello-World",
        "homepage": "https://github.com",
        "language": None,
        "forks": 9,
        "forks_count": 9,
        "watchers": 80,
        "watchers_count": 80,
        "size": 108,
        "master_branch": "master",
        "open_issues": 0,
        "open_issues_count": 0,
        "pushed_at": "2011-01-26T19:06:43Z",
        "created_at": "2011-01-26T19:01:12Z",
        "updated_at": "2011-01-26T19:14:43Z"
        },
    "source": {
        "id": 1296269,
        "owner": {
            "login": "octocat",
            "id": 1,
            "avatar_url": "https://github.com/images/error/octocat.gif",
            "gravatar_id": "somehexcode",
            "url": "https://api.github.com/users/octocat"
            },
        "name": "Hello-World",
        "full_name": "octocat/Hello-World",
        "description": "This your first repo!",
        "private": False,
        "fork": True,
        "url": "https://api.github.com/repos/octocat/Hello-World",
        "html_url": "https://github.com/octocat/Hello-World",
        "clone_url": "https://github.com/octocat/Hello-World.git",
        "git_url": "git://github.com/octocat/Hello-World.git",
        "ssh_url": "git@github.com:octocat/Hello-World.git",
        "svn_url": "https://svn.github.com/octocat/Hello-World",
        "mirror_url": "git://git.example.com/octocat/Hello-World",
        "homepage": "https://github.com",
        "language": None,
        "forks": 9,
        "forks_count": 9,
        "watchers": 80,
        "watchers_count": 80,
        "size": 108,
        "master_branch": "master",
        "open_issues": 0,
        "open_issues_count": 0,
        "pushed_at": "2011-01-26T19:06:43Z",
        "created_at": "2011-01-26T19:01:12Z",
        "updated_at": "2011-01-26T19:14:43Z"
        },
    "has_issues": True,
    "has_wiki": True,
    "has_downloads": True
}


class TestRepository(UnitHelper):

    """Unit test for regular Repository methods."""

    described_class = Repository
    example_data = repo_example_data

    def test_asset(self):
        """Test retrieving an asset uses the right headers.

        The Releases section of the API is still in Beta and uses custom
        headers
        """
        assert self.instance.asset(0) is None
        assert self.session.get.call_count == 0

        self.instance.asset(1)
        url = self.example_data['url'] + '/releases/assets/1'
        self.session.get.assert_called_once_with(
            url, headers={'Accept': 'application/vnd.github.manifold-preview'}
        )

    def test_latest_pages_build(self):
        """Test retrieving the most recent pages build."""
        url = self.example_data['url'] + '/pages/builds/latest'
        self.instance.latest_pages_build()
        self.session.get.assert_called_once_with(url)

    def test_pages(self):
        """Test retrieving information about a repository's page."""
        url = self.example_data['url'] + '/pages'
        self.instance.pages()
        self.session.get.assert_called_once_with(url)


class TestRepositoryIterator(UnitIteratorHelper):

    """Unit tests for Repository methods that return iterators."""

    described_class = Repository
    example_data = repo_example_data

    def test_assignees(self):
        """Test the ability to iterate over the assignees in a Repository."""
        i = self.instance.assignees()
        self.get_next(i)

        self.session.get.assert_called_once_with(
            url_for('assignees'),
            params={'per_page': 100},
            headers={}
        )

    def test_branches(self):
        """Test the ability to iterate over the branches in a Repository."""
        i = self.instance.branches()
        self.get_next(i)

        self.session.get.assert_called_once_with(
            url_for('branches'),
            params={'per_page': 100},
            headers={}
        )

    def test_code_frequency(self):
        """Test the ability to iterate over the statistics in a Repository."""
        i = self.instance.code_frequency()
        self.get_next(i)

        self.session.get.assert_called_once_with(
            url_for('stats/code_frequency'),
            params={'per_page': 100},
            headers={}
        )

    def test_collaborators(self):
        """Test the ability to iterate over the collaborators on a repo."""
        i = self.instance.collaborators()
        self.get_next(i)

        self.session.get.assert_called_once_with(
            url_for('collaborators'),
            params={'per_page': 100},
            headers={}
        )

    def test_comments(self):
        """Test the ability to iterate over the comments on a repository."""
        i = self.instance.comments()
        self.get_next(i)

        self.session.get.assert_called_once_with(
            url_for('comments'),
            params={'per_page': 100},
            headers={}
        )

    def test_comments_on_commit(self):
        """Test the ability to iterate over comments on a specific commit."""
        i = self.instance.comments_on_commit('some-sha')
        self.get_next(i)

        self.session.get.assert_called_once_with(
            url_for('commits/some-sha/comments'),
            params={'per_page': 100},
            headers={}
        )

    def test_commit_activity(self):
        """Test the ability to iterate over commit activity on a repo."""
        i = self.instance.commit_activity()
        self.get_next(i)

        self.session.get.assert_called_once_with(
            url_for('stats/commit_activity'),
            params={'per_page': 100},
            headers={}
        )

    def test_commits(self):
        """Test the ability to iterate over commits in a repo."""
        i = self.instance.commits()
        self.get_next(i)

        self.session.get.assert_called_once_with(
            url_for('commits'),
            params={'per_page': 100},
            headers={}
        )

    def test_commits_since_until_datetime(self):
        """Test the ability to iterate over repo's commits in a date range."""
        i = self.instance.commits(since=datetime.datetime(2014, 8, 1),
                                  until='2014-09-01T00:00:00Z')
        self.get_next(i)

        self.session.get.assert_called_once_with(
            url_for('commits'),
            params={'per_page': 100, 'since': '2014-08-01T00:00:00Z',
                    'until': '2014-09-01T00:00:00Z'},
            headers={}
        )

    def test_commits_sha_path(self):
        """Test the ability to filter commits by branch and path."""
        i = self.instance.commits(sha='branch', path='tests/')
        self.get_next(i)

        self.session.get.assert_called_once_with(
            url_for('commits'),
            params={'per_page': 100, 'sha': 'branch', 'path': 'tests/'},
            headers={}
        )

    def test_contributor_statistics(self):
        """Test the ability to iterate over contributor statistics."""
        i = self.instance.contributor_statistics()
        self.get_next(i)

        self.session.get.assert_called_once_with(
            url_for('stats/contributors'),
            params={'per_page': 100},
            headers={}
        )

    def test_contributors(self):
        """Test the ability to iterate over contributors to a repository."""
        i = self.instance.contributors()
        self.get_next(i)

        self.session.get.assert_called_once_with(
            url_for('contributors'),
            params={'per_page': 100},
            headers={}
        )

    def test_contributors_with_anon(self):
        """Test the ability to iterate over anonymous contributors."""
        i = self.instance.contributors(anon=True)
        self.get_next(i)

        self.session.get.assert_called_once_with(
            url_for('contributors'),
            params={'per_page': 100, 'anon': 'true'},
            headers={}
        )

    def test_deployments(self):
        """Test the ability to iterate over deployments."""
        i = self.instance.deployments()
        self.get_next(i)

        self.session.get.assert_called_once_with(
            url_for('deployments'),
            params={'per_page': 100},
            headers={
                'Accept': 'application/vnd.github.cannonball-preview+json'
            }
        )

    def test_events(self):
        """Test the ability to iterate over events from a repository."""
        i = self.instance.events()
        self.get_next(i)

        self.session.get.assert_called_once_with(
            url_for('events'),
            params={'per_page': 100},
            headers={}
        )

    def test_forks(self):
        """Test the ability to iterate over forks of a repository."""
        i = self.instance.forks()
        self.get_next(i)

        self.session.get.assert_called_once_with(
            url_for('forks'),
            params={'per_page': 100},
            headers={}
        )

    def test_hooks(self):
        """Test the ability to iterate over hooks of a repository."""
        i = self.instance.hooks()
        self.get_next(i)

        self.session.get.assert_called_once_with(
            url_for('hooks'),
            params={'per_page': 100},
            headers={}
        )

    def test_issue_events(self):
        """Test the ability to iterate over a repository's issue events."""
        i = self.instance.issue_events()
        self.get_next(i)

        self.session.get.assert_called_once_with(
            url_for('issues/events'),
            params={'per_page': 100},
            headers={}
        )

    def test_issues(self):
        """Test the ability to iterate over a repository's issues."""
        i = self.instance.issues()
        self.get_next(i)

        self.session.get.assert_called_once_with(
            url_for('issues'),
            params={'per_page': 100},
            headers={}
        )


class TestRepositoryRequiresAuth(UnitHelper):

    """Unit test for regular Repository methods."""

    described_class = Repository
    example_data = repo_example_data

    def after_setup(self):
        """Set-up the session to not be authenticated."""
        self.session.has_auth.return_value = False

    def test_hooks(self):
        """Show that a user must be authenticated to list hooks."""
        with pytest.raises(GitHubError):
            self.instance.hooks()
