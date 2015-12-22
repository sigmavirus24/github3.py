"""Unit tests for Repositories."""
import datetime
import pytest

from github3 import GitHubError
from github3.null import NullObject
from github3.repos.repo import Repository

from . import helper

url_for = helper.create_url_helper(
    'https://api.github.com/repos/octocat/Hello-World'
)

get_repo_example_data = helper.create_example_data_helper(
    'repos_repo_example'
)
repo_example_data = get_repo_example_data()


class TestRepository(helper.UnitHelper):

    """Unit test for regular Repository methods."""

    described_class = Repository
    example_data = repo_example_data

    def test_add_collaborator(self):
        """Verify the request to add a collaborator to a repository."""
        self.instance.add_collaborator('sigmavirus24')

        self.session.put.assert_called_once_with(
            url_for('collaborators/sigmavirus24')
        )

    def test_add_null_collaborator(self):
        """Verify no request is made when adding `None` as a collaborator."""
        self.instance.add_collaborator(None)
        self.instance.add_collaborator(NullObject())

        assert self.session.put.called is False

    def test_asset(self):
        """Test retrieving an asset uses the right headers.

        The Releases section of the API is still in Beta and uses custom
        headers
        """
        self.instance.asset(1)

        self.session.get.assert_called_once_with(
            url_for('releases/assets/1'),
            headers={'Accept': 'application/vnd.github.manifold-preview'}
        )

    def test_asset_requires_a_positive_id(self):
        """Test that a positive asset id is required."""
        self.instance.asset(0)

        assert self.session.get.called is False

    def test_create_fork(self):
        """Verify the request to fork a repository."""
        self.instance.create_fork()
        self.post_called_with(
            url_for('forks')
        )

    def test_create_fork_to_organization(self):
        """Verify the request to fork a repository to an organization."""
        self.instance.create_fork('mattchung')

        self.post_called_with(
            url_for('forks'),
            data={
                'organization': 'mattchung'
            }
        )

    def test_create_hook(self):
        """Verify the request to create a hook."""
        data = {
            'name': 'web',
            'config': {
                'url': 'http://example.com/webhook',
                'content_type': 'json'
            }
        }

        self.instance.create_hook(**data)
        self.post_called_with(
            url_for('hooks'),
            data={
                'name': 'web',
                'config': {
                    'url': 'http://example.com/webhook',
                    'content_type': 'json'
                },
                'events': ['push'],
                'active': True
            }
        )

    def test_create_hook_requires_valid_name(self):
        """Test that we check the validity of a hook."""
        self.instance.create_hook(name='', config='config')

        assert self.session.post.called is False

    def test_create_hook_requires_valid_config(self):
        """Test that we check the validity of a hook."""
        self.instance.create_hook(name='name', config={})

        assert self.session.post.called is False

    def test_create_hook_requires_valid_name_and_config(self):
        """Test that we check the validity of a hook."""
        self.instance.create_hook(name='name', config='')

        assert self.session.post.called is False

    def test_create_issue(self):
        """Verify the request to create an issue."""
        data = {
            'title': 'Unit Issue',
            'body': 'Fake body',
            'assignee': 'sigmavirus24',
            'milestone': 1,
            'labels': ['bug', 'enhancement']
        }
        self.instance.create_issue(**data)
        self.post_called_with(
            url_for('issues'),
            data=data
        )

    def test_create_issue_require_valid_issue(self):
        """Test that we check the validity of an issue."""
        self.instance.create_issue(title=None)

        assert self.session.post.called is False

    def test_create_key(self):
        """Verify the request to create a key."""
        data = {
            'title': 'octocat@octomac',
            'key': 'ssh-rsa AAA'
        }
        self.instance.create_key(**data)
        self.post_called_with(
            url_for('keys'),
            data=data
        )

    def test_create_key_requires_a_valid_title(self):
        """Test that we check the validity of a key."""
        self.instance.create_key(title=None, key='ssh-rsa ...')

        assert self.session.post.called is False

    def test_create_key_requires_a_valid_key(self):
        """Test that we check the validity of a key."""
        self.instance.create_key(title='foo', key='')

        assert self.session.post.called is False

    def test_create_key_requires_a_valid_title_and_key(self):
        """Test that we check the validity of a key."""
        self.instance.create_key(title='foo', key='')

        assert self.session.post.called is False

    def test_create_ref(self):
        """Verify the request to create a reference."""
        self.instance.create_ref('refs/heads/foo', 'my-fake-sha')

        self.post_called_with(
            url_for('git/refs'),
            data={
                'ref': 'refs/heads/foo',
                'sha': 'my-fake-sha',
            },
        )

    def test_create_ref_requires_a_reference_with_two_slashes(self):
        """Test that we check the validity of a reference."""
        self.instance.create_ref('refs/heads', 'my-fake-sha')

        assert self.session.post.called is False

    def test_create_ref_requires_a_reference_start_with_refs(self):
        """Test that we check the validity of a reference."""
        self.instance.create_ref('my-silly-ref/foo/bar', 'my-fake-sha')

        assert self.session.post.called is False

    def test_create_ref_requires_a_non_None_sha(self):
        """Test that we don't send an empty SHA."""
        self.instance.create_ref('refs/heads/valid', None)

        assert self.session.post.called is False

    def test_create_ref_requires_a_truthy_sha(self):
        """Test that we don't send an empty SHA."""
        self.instance.create_ref('refs/heads/valid', '')

        assert self.session.post.called is False

    def test_create_tag_that_is_not_lightweight(self):
        """Verify we can create an annotated tag."""
        self.instance.create_tag(
            tag='tag-name',
            message='message',
            sha='my-sha',
            obj_type='commit',
            tagger={'name': 'Ian Cordasco',
                    'email': 'example@example.com',
                    'date': '2015-11-01T12:16:00Z'},
        )

        self.post_called_with(
            url_for('git/tags'),
            data={
                'tag': 'tag-name',
                'message': 'message',
                'object': 'my-sha',
                'type': 'commit',
                'tagger': {
                    'name': 'Ian Cordasco',
                    'email': 'example@example.com',
                    'date': '2015-11-01T12:16:00Z',
                },
            },
        )

    def test_create_tree(self):
        """Verify the request to create a tree."""
        self.instance.create_tree([{'foo': 'bar'}])

        self.post_called_with(
            url_for('git/trees'),
            data={
                'tree': [{'foo': 'bar'}]
            }
        )

    def test_create_tree_with_base_tree(self):
        """Verify the request to create a tree with a base tree."""
        self.instance.create_tree([{'foo': 'bar'}], base_tree='sha')

        self.post_called_with(
            url_for('git/trees'),
            data={
                'tree': [{'foo': 'bar'}],
                'base_tree': 'sha'
            }
        )

    def test_create_tree_rejects_invalid_trees(self):
        """Verify no request is made if tree is not a list or is None."""
        self.instance.create_tree({'foo': 'bar'})
        self.instance.create_tree(None)

        assert self.session.post.called is False

    def test_directory_contents(self):
        """Verify the request made to retrieve a directory's contents."""
        self.instance.directory_contents('path/to/directory')

        self.session.get.assert_called_once_with(
            url_for('contents/path/to/directory'),
            params={'ref': None}
        )

    def test_directory_contents_with_ref(self):
        """Verify the request made to retrieve a directory's contents."""
        self.instance.directory_contents('path/to/directory', ref='some-sha')

        self.session.get.assert_called_once_with(
            url_for('contents/path/to/directory'),
            params={'ref': 'some-sha'}
        )

    def test_deployment(self):
        """Verify the request made to retrieve a deployment."""
        self.instance.deployment(10)

        self.session.get.assert_called_once_with(url_for('deployments/10'))

    def test_deployment_requires_positive_int(self):
        """Verify that a positive deployment id is required."""
        self.instance.deployment(-10)

        assert self.session.get.called is False

    def test_file_contents(self):
        """Verify the request made to retrieve a dictionary's contents."""
        self.instance.file_contents('path/to/file.txt', ref='some-sha')

        self.session.get.assert_called_once_with(
            url_for('contents/path/to/file.txt'),
            params={'ref': 'some-sha'}
        )

    def test_key(self):
        """Test the ability to fetch a deploy key."""
        self.instance.key(10)

        self.session.get.assert_called_once_with(url_for('keys/10'))

    def test_key_requires_positive_id(self):
        """Test that a positive key id is required."""
        self.instance.key(-10)

        assert self.session.get.called is False

    def test_latest_pages_build(self):
        """Test retrieving the most recent pages build."""
        self.instance.latest_pages_build()

        self.session.get.assert_called_once_with(
            url_for('pages/builds/latest')
        )

    def test_milestone(self):
        """Test retrieving a specific milestone."""
        self.instance.milestone(20)

        self.session.get.assert_called_once_with(url_for('milestones/20'))

    def test_milestone_requires_positive_id(self):
        """Test that a positive milestone id is required."""
        self.instance.milestone(-1)

        assert self.session.get.called is False

    def test_pages(self):
        """Test retrieving information about a repository's page."""
        self.instance.pages()

        self.session.get.assert_called_once_with(url_for('pages'))

    def test_release_latest(self):
        """Test the request for retrieving the latest release"""
        self.instance.release_latest()

        self.session.get.assert_called_once_with(
            url_for('releases/latest')
        )

    def test_release_from_tag(self):
        """Test the request for retrieving release by tag name"""
        self.instance.release_from_tag('v1.0.0')

        self.session.get.assert_called_once_with(
            url_for('releases/tags/v1.0.0')
        )


class TestRepositoryIterator(helper.UnitIteratorHelper):

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
            headers={'Accept': 'application/vnd.github.loki-preview+json'}
        )

    def test_branches_protected(self):
        """Test ability to iterate over protected branches in a Repository."""
        i = self.instance.branches(protected=True)
        self.get_next(i)

        self.session.get.assert_called_once_with(
            url_for('branches'),
            params={'per_page': 100, 'protected': '1'},
            headers={'Accept': 'application/vnd.github.loki-preview+json'}
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
            headers={}
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

    def test_keys(self):
        """Test the ability to iterate over a repository's keys."""
        i = self.instance.keys()
        self.get_next(i)

        self.session.get.assert_called_once_with(
            url_for('keys'),
            params={'per_page': 100},
            headers={}
        )

    def test_labels(self):
        """Test the ability to iterate over a repository's labels."""
        i = self.instance.labels()
        self.get_next(i)

        self.session.get.assert_called_once_with(
            url_for('labels'),
            params={'per_page': 100},
            headers={}
        )

    def test_languages(self):
        """Test the ability to iterate over the languages used in a repo."""
        i = self.instance.languages()
        self.get_next(i)

        self.session.get.assert_called_once_with(
            url_for('languages'),
            params={'per_page': 100},
            headers={}
        )

    def test_milestones(self):
        """Test the ability to iterate over the milestones in a repo."""
        i = self.instance.milestones()
        self.get_next(i)

        self.session.get.assert_called_once_with(
            url_for('milestones'),
            params={'per_page': 100},
            headers={}
        )

    def test_network_events(self):
        """Test the ability to iterate over the network events for a repo."""
        i = self.instance.network_events()
        self.get_next(i)

        self.session.get.assert_called_once_with(
            url_for('events').replace('repos', 'networks'),
            params={'per_page': 100},
            headers={}
        )

    def test_notifications(self):
        """Test the ability to iterate over the notifications for a repo."""
        i = self.instance.notifications()
        self.get_next(i)

        self.session.get.assert_called_once_with(
            url_for('notifications'),
            params={'per_page': 100, 'participating': 'false', 'all': 'false'},
            headers={}
        )

    def test_pages_builds(self):
        """Test the request for the GitHub Pages builds for a repo."""
        i = self.instance.pages_builds()
        self.get_next(i)

        self.session.get.assert_called_once_with(
            url_for('pages/builds'),
            params={'per_page': 100},
            headers={}
        )

    def test_pull_requests(self):
        """Test the request for the retrieving pull requests."""
        i = self.instance.pull_requests()
        self.get_next(i)

        self.session.get.assert_called_once_with(
            url_for('pulls'),
            params={'per_page': 100, 'sort': 'created', 'direction': 'desc'},
            headers={}
        )

    def test_pull_requests_ignore_invalid_state(self):
        """Test the method ignores invalid pull request states."""
        i = self.instance.pull_requests(state='invalid')
        self.get_next(i)

        self.session.get.assert_called_once_with(
            url_for('pulls'),
            params={'per_page': 100, 'sort': 'created', 'direction': 'desc'},
            headers={}
        )

    def test_refs(self):
        """Test the request for retrieving references."""
        i = self.instance.refs()
        self.get_next(i)

        self.session.get.assert_called_once_with(
            url_for('git/refs'),
            params={'per_page': 100},
            headers={}
        )

    def test_refs_with_a_subspace(self):
        """Test the request for retrieivng refs in a subspace."""
        i = self.instance.refs('a-subspace')
        self.get_next(i)

        self.session.get.assert_called_once_with(
            url_for('git/refs/a-subspace'),
            params={'per_page': 100},
            headers={}
        )

    def test_releases(self):
        """Test the request for retrieving releases from a repository."""
        i = self.instance.releases()
        self.get_next(i)

        self.session.get.assert_called_once_with(
            url_for('releases'),
            params={'per_page': 100},
            headers={'Accept': 'application/vnd.github.manifold-preview'}
        )

    def test_stargazers(self):
        """Test the request for retrieving stargazers of a repository."""
        i = self.instance.stargazers()
        self.get_next(i)

        self.session.get.assert_called_once_with(
            url_for('stargazers'),
            params={'per_page': 100},
            headers={}
        )

    def test_statuses(self):
        """Test the request for retrieiving statuses of a commit."""
        i = self.instance.statuses('fake-sha')
        self.get_next(i)

        self.session.get.assert_called_once_with(
            url_for('statuses/fake-sha'),
            params={'per_page': 100},
            headers={}
        )

    def test_statuses_requires_a_sha(self):
        """Test the request is made only if given a SHA."""
        i = self.instance.statuses('')
        self.get_next(i)

        assert self.session.get.called is False

    def test_subscribers(self):
        """Test the request for retrieving subscribers to a repository."""
        i = self.instance.subscribers()
        self.get_next(i)

        self.session.get.assert_called_once_with(
            url_for('subscribers'),
            params={'per_page': 100},
            headers={}
        )

    def test_tags(self):
        """Test the request for retrieving tags in a repository."""
        i = self.instance.tags()
        self.get_next(i)

        self.session.get.assert_called_once_with(
            url_for('tags'),
            params={'per_page': 100},
            headers={}
        )

    def test_teams(self):
        """Test the request for retrieving teams on a repository."""
        i = self.instance.teams()
        self.get_next(i)

        self.session.get.assert_called_once_with(
            url_for('teams'),
            params={'per_page': 100},
            headers={}
        )


class TestRepositoryRequiresAuth(helper.UnitRequiresAuthenticationHelper):

    """Unit test for regular Repository methods."""

    described_class = Repository
    example_data = repo_example_data

    def test_add_collaborator(self):
        """Verify that adding a collaborator requires authentication."""
        with pytest.raises(GitHubError):
            self.instance.add_collaborator('foo')

    def test_create_ref(self):
        """Verify that creating a tag requires authentication."""
        with pytest.raises(GitHubError):
            self.instance.create_ref('some ref', 'some sha')

    def test_create_fork(self):
        """Verify that creating a fork requires authentication."""
        with pytest.raises(GitHubError):
            self.instance.create_fork()

    def test_create_hook(self):
        """Verify that creating a hook requires authentication."""
        with pytest.raises(GitHubError):
            self.instance.create_hook('foo', 'config')

    def test_create_issue(self):
        """Verify that creating an issue requires authentication."""
        with pytest.raises(GitHubError):
            self.instance.create_issue('some title', 'some body', 'foo')

    def test_create_key(self):
        """Verify that deploying a key requires authentication."""
        with pytest.raises(GitHubError):
            self.instance.create_key('key name', 'ssh-rsa ...')

    def test_hooks(self):
        """Show that a user must be authenticated to list hooks."""
        with pytest.raises(GitHubError):
            self.instance.hooks()

    def test_key(self):
        """Show that a user must be authenticated to fetch a key."""
        with pytest.raises(GitHubError):
            self.instance.key(10)

    def test_keys(self):
        """Show that a user must be authenticated to list keys."""
        with pytest.raises(GitHubError):
            self.instance.keys()

    def test_notifications(self):
        """Show that a user must be authenticated to list notifications."""
        with pytest.raises(GitHubError):
            self.instance.notifications()

    def test_pages_builds(self):
        """Show that a user must be authenticated to list their builds."""
        with pytest.raises(GitHubError):
            self.instance.pages_builds()

    def test_teams(self):
        """Show that a user must be authenticated to list teams on a repo."""
        with pytest.raises(GitHubError):
            self.instance.teams()
