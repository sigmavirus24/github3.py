"""Unit tests for Repositories."""
import datetime
import mock
import pytest

from base64 import b64encode
from github3 import GitHubError
from github3.repos.comment import RepoComment
from github3.repos.commit import RepoCommit
from github3.repos.comparison import Comparison
from github3.repos.contents import Contents
from github3.repos.hook import Hook
from github3.repos.repo import Repository, ShortRepository
from github3.models import GitHubCore
from github3.projects import Project

from . import helper

comment_url_for = helper.create_url_helper(
    'https://api.github.com/repos/octocat/Hello-World/comments/1'
)
commit_url_for = helper.create_url_helper(
    ('https://api.github.com/repos/octocat/Hello-World/'
     'commits/6dcb09b5b57875f334f61aebed695e2e4193db5e')
)
compare_url_for = helper.create_url_helper(
    'https://api.github.com/repos/octocat/Hello-World/compare/master...topic'
)
contents_url_for = helper.create_url_helper(
    'https://api.github.com/repos/github3py/github3.py/contents/README.rst'
    '?ref=master'
)
hook_url_for = helper.create_url_helper(
    'https://api.github.com/repos/octocat/Hello-World/hooks/1'
)
url_for = helper.create_url_helper(
    'https://api.github.com/repos/octocat/Hello-World'
)
get_repo_example_data = helper.create_example_data_helper(
    'repo_example'
)
get_repo_2_12_example_data = helper.create_example_data_helper(
    'repo_2_12_example'
)
get_comment_example_data = helper.create_example_data_helper(
    'comment_example'
)
get_commit_example_data = helper.create_example_data_helper(
    'commit_example'
)
get_compare_example_data = helper.create_example_data_helper(
    'compare_example'
)
get_content_example_data = helper.create_example_data_helper(
    'content_example'
)
get_hook_example_data = helper.create_example_data_helper(
    'hook_example'
)
create_file_contents_example_data = helper.create_example_data_helper(
    'create_file_contents_example'
)
comment_example_data = get_comment_example_data()
commit_example_data = get_commit_example_data()
compare_example_data = get_compare_example_data()
content_example_data = get_content_example_data()
create_file_contents_example_data = create_file_contents_example_data()
hook_example_data = get_hook_example_data()
repo_example_data = get_repo_example_data()
repo_2_12_example_data = get_repo_2_12_example_data()


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

        assert self.session.put.called is False

    def test_asset(self):
        """Test retrieving an asset uses the right headers.

        The Releases section of the API is still in Beta and uses custom
        headers
        """
        self.instance.asset(1)

        self.session.get.assert_called_once_with(
            url_for('releases/assets/1')
        )

    def test_asset_requires_a_positive_id(self):
        """Test that a positive asset id is required."""
        self.instance.asset(0)

        assert self.session.get.called is False

    def test_create_file(self):
        """Verify the request for creating a file on a repository."""
        data = {
            'path': 'hello.txt',
            'message': 'my commit message',
            'content': b'bXkgbmV3IGZpbGUgY29udGVudHM=',
            'committer': {
                'name': 'Scott Chacon',
                'email': 'schacon@gmail.com'
            }
        }

        self.instance.create_file(**data)

        b64_encoded_content = b64encode(data['content']).decode('utf-8')
        data.update({
            'content': b64_encoded_content
        })
        del(data['path'])

        self.put_called_with(
            url_for('contents/hello.txt'),
            data=data
        )

    def test_create_file_required_content(self):
        """Verify the request for creating a file on a repository."""
        data = {
            'path': 'hello.txt',
            'message': 'my commit message',
            'content': 123,
            'committer': {
                'name': 'Scott Chacon',
                'email': 'schacon@gmail.com'
            }
        }

        with pytest.raises(ValueError):
            self.instance.create_file(**data)

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

    def test_create_issue_multiple_assignees(self):
        """Verify the request to create an issue with multiple assignees."""
        data = {
            'title': 'Unit Issue',
            'body': 'Fake body',
            'assignees': ['itsmemattchung', 'sigmavirus24'],
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
            'key': 'ssh-rsa AAA',
            'read_only': False
        }
        self.instance.create_key(**data)
        self.post_called_with(
            url_for('keys'),
            data=data
        )

    def test_create_key_readonly(self):
        """Verify the request to create a key with readonly true."""
        data = {
            'title': 'octocat@octomac',
            'key': 'ssh-rsa AAA',
            'read_only': True
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

    def test_create_label(self):
        """Verify the request for creating a label."""
        data = {
            'name': 'foo',
            'color': 'fafafa'
        }
        self.instance.create_label(**data)
        self.post_called_with(
            url_for('labels'),
            data=data,
            headers={'Accept': 'application/vnd.github.symmetra-preview+json'},
        )

    def test_create_label_required_name(self):
        """Verify the request for creating a label."""
        data = {
            'name': '',
            'color': 'fafafa'
        }
        self.instance.create_label(**data)
        assert self.session.post.called is False

    def test_create_label_required_color(self):
        """Verify the request for creating a label."""
        data = {
            'name': 'foo',
            'color': ''
        }
        self.instance.create_label(**data)
        assert self.session.post.called is False

    def test_create_label_required_name_and_color(self):
        """Verify the request for creating a label."""
        data = {
            'name': '',
            'color': ''
        }
        self.instance.create_label(**data)
        assert self.session.post.called is False

    def test_create_milestone(self):
        """Verify the request for creating a milestone."""
        data = {
            'title': 'foo'
        }
        self.instance.create_milestone(**data)
        self.post_called_with(
            url_for('milestones'),
            data=data
        )

    def test_create_milestone_accepted_state(self):
        """Verify the request for creating a milestone."""
        data = {
            'title': 'foo',
            'state': 'in_progress'
        }
        self.instance.create_milestone(**data)
        self.post_called_with(
            url_for('milestones'),
            data={
                'title': 'foo'
            }
        )

    def test_create_project(self):
        """Verify the request for creating a project."""
        data = {
            'name': 'test-project',
            'body': 'project body'
        }
        self.instance.create_project(**data)
        self.post_called_with(
            url_for('projects'),
            data=data,
            headers=Project.CUSTOM_HEADERS
        )

    def test_create_pull_private_required_data(self):
        """Verify the request for creating a pull request."""
        with helper.mock.patch.object(GitHubCore, '_remove_none') as rm_none:
            data = {}
            self.instance._create_pull(data)
            rm_none.assert_called_once_with({})
            assert self.session.post.called is False

    def test_create_pull_private(self):
        """Verify the request for creating a pull request."""
        data = {
            'title': 'foo',
            'base': 'master',
            'head': 'feature_branch'
        }
        self.instance._create_pull(data)
        self.post_called_with(
            url_for('pulls'),
            data=data
        )

    def test_create_pull(self):
        """Verify the request for creating a pull request."""
        data = {
            'title': 'foo',
            'base': 'master',
            'head': 'feature_branch',
            'body': 'body'
        }
        with helper.mock.patch.object(Repository, '_create_pull') as pull:
            self.instance.create_pull(**data)
            pull.assert_called_once_with(
                data
            )

    def test_create_pull_from_issue(self):
        """Verify the request for creating a pull request from an issue."""
        with helper.mock.patch.object(Repository, '_create_pull') as pull:
            data = {
                'issue': 1,
                'base': 'master',
                'head': 'feature_branch'
            }
            self.instance.create_pull_from_issue(
                **data
            )
            pull.assert_called_once_with(data)

    def test_create_pull_from_issue_required_issue_number(self):
        """Verify the request for creating a pull request from an issue."""
        with helper.mock.patch.object(Repository, '_create_pull') as pull:
            pull_request = self.instance.create_pull_from_issue(
                issue=-1,
                base='master',
                head='feature_branch'
            )
            assert pull.called is False
            assert pull_request is None

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

    def test_create_branch_ref(self):
        """Verify the request to create a branch."""
        self.instance.create_branch_ref('branch-name', 'my-fake-sha')

        self.post_called_with(
            url_for('git/refs'),
            data={
                'ref': 'refs/heads/branch-name',
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

    def test_create_status(self):
        """Verify the request for creating a status on a commit."""
        data = {
            'state': 'success',
            'target_url': 'foo',
            'description': 'bar',
            'context': 'default'
        }
        with helper.mock.patch.object(GitHubCore, '_remove_none') as rm_none:
            self.instance.create_status(sha='fake-sha', **data)
            rm_none.assert_called_once_with(data)
            self.post_called_with(
                url_for('statuses/fake-sha'),
                data=data
            )

    def test_create_status_required_sha(self):
        """Verify the request for creating a status on a commit."""
        self.instance.create_status(sha='', state='success')
        assert self.session.post.called is False

    def test_create_status_required_state(self):
        """Verify the request for creating a status on a commit."""
        self.instance.create_status(sha='fake-sha', state='')
        assert self.session.post.called is False

    def test_create_status_required_sha_and_state(self):
        """Verify the request for creating a status on a commit."""
        self.instance.create_status(sha='', state='')
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

    def test_delete(self):
        """Verify the request for deleting a repository."""
        self.instance.delete()

        assert self.session.delete.called is True

    def test_delete_key(self):
        """Verify the request for deleting a key on the repository."""
        self.instance.delete_key(1)

        self.session.delete.assert_called_once_with(
            url_for('keys/1')
        )

    def test_delete_key_required_id(self):
        """Verify the request for deleting a key on the repository."""
        assert self.instance.delete_key(-1) is False

        self.session.delete.called is False

    def test_delete_subscription(self):
        """Verify the request for deleting a subscription."""
        self.instance.delete_subscription()

        self.session.delete.assert_called_once_with(
            url_for('subscription')
        )

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

    def test_edit(self):
        """Verify the request for editing a repository."""
        data = {
            'name': 'hello-world',
            'description': 'repo description',
            'homepage': 'homepage_url',
            'private': True,
            'has_issues': True,
            'has_wiki': True,
            'has_downloads': True,
            'default_branch': 'develop',
            'allow_rebase_merge': True,
            'allow_squash_merge': True,
            'allow_merge_commit': False,
            'has_projects': False
        }

        with mock.patch.object(Repository, '_update_attributes') as up_attr:
            assert self.instance.edit(**data) is True
            assert up_attr.called is True
            self.patch_called_with(
                url_for(),
                data=data
            )

    def test_edit_required_name(self):
        """Verify the request for editing a repository."""
        assert self.instance.edit(None) is False
        assert self.session.patch.called is False

    def test_file_contents(self):
        """Verify the request made to retrieve a dictionary's contents."""
        self.instance.file_contents('path/to/file.txt', ref='some-sha')

        self.session.get.assert_called_once_with(
            url_for('contents/path/to/file.txt'),
            params={'ref': 'some-sha'}
        )

    def test_git_commit_required_sha(self):
        """Verify the request for retrieving a git commit from a repository."""
        self.instance.git_commit('')
        assert self.session.get.called is False

    def test_git_commit(self):
        """Verify the request for retrieving a git commit from a repository."""
        self.instance.git_commit('fake-sha')
        self.session.get.assert_called_once_with(
            url_for('git/commits/fake-sha')
        )

    def test_hook(self):
        """Verify the request for retrieving a hook on a repository."""
        self.instance.hook(1)
        self.session.get.assert_called_once_with(
            url_for('hooks/1')
        )

    def test_hook_required_hook(self):
        """Verify the request for retrieving a hook on a repository."""
        self.instance.hook(-1)
        assert self.session.get.called is False

    def test_is_assignee(self):
        """
        Verify the request for checking if a user can be assigned issues
        on a repository.
        """
        self.instance.is_assignee('octocat')
        self.session.get.assert_called_once_with(
            url_for('assignees/octocat')
        )

    def test_is_assignee_required_username(self):
        """
        Verify the request for checking if a user can be assigned issues
        on a repository.
        """
        assert self.instance.is_assignee('') is False
        assert self.session.get.called is False

    def test_import_issue(self):
        """Verify the request for importing an issue into a repository."""
        data = {
            'title': 'Foo',
            'body': 'Foobar body',
            'created_at': '2014-03-16T17:15:42Z',
            'assignee': 'octocat',
            'milestone': 1,
            'closed': True,
            'labels': ['easy', 'bug'],
            'comments': [{
                'created_at': '2014-03-18T17:15:42Z',
                'body': 'comment body'
            }]
        }
        issue = {
            'issue': {
                'title': 'Foo',
                'body': 'Foobar body',
                'created_at': '2014-03-16T17:15:42Z',
                'assignee': 'octocat',
                'milestone': 1,
                'closed': True,
                'labels': ['easy', 'bug'],
            },
            'comments': [{
                'created_at': '2014-03-18T17:15:42Z',
                'body': 'comment body'
            }]
        }
        with mock.patch.object(GitHubCore, '_remove_none') as rm_none:
            self.instance.import_issue(**data)
            rm_none.assert_any_call(issue['issue'])
            rm_none.assert_any_call(issue)

        self.post_called_with(
            url_for('import/issues'),
            data=issue,
            headers={
                'Accept': 'application/vnd.github.golden-comet-preview+json'
            }
        )

    def test_imported_issue(self):
        """Verify the request for retrieving an imported issue."""
        self.instance.imported_issue(1)
        self.session.get.assert_called_once_with(
            url_for('import/issues/1'),
            headers={
                'Accept': 'application/vnd.github.golden-comet-preview+json'
            }
        )

    def test_is_collaborator_required_username(self):
        """
        Verify the request for checking if a user is a collaborator on a
        repository.
        """
        assert self.instance.is_collaborator('') is False
        assert self.session.get.called is False

    def test_is_collaborator(self):
        """
        Verify the request for checking if a user is a collaborator on a
        repository.
        """
        self.instance.is_collaborator('octocat')
        self.session.get.assert_called_once_with(
            url_for('collaborators/octocat')
        )

    def test_issue(self):
        """Verify the request for retrieving an issue on a repository."""
        self.instance.issue(1)
        self.session.get.assert_called_once_with(
            url_for('issues/1')
        )

    def test_issue_required_number(self):
        """Verify the request for retrieving an issue on a repository."""
        self.instance.issue(-1)
        assert self.session.get.called is False

    def test_key(self):
        """Test the ability to fetch a deploy key."""
        self.instance.key(10)

        self.session.get.assert_called_once_with(url_for('keys/10'))

    def test_key_requires_positive_id(self):
        """Test that a positive key id is required."""
        self.instance.key(-10)

        assert self.session.get.called is False

    def test_label(self):
        """Verify the request for retrieving a label on a repository."""
        self.instance.label('bug')
        self.session.get.assert_called_once_with(
            url_for('labels/bug'),
            headers={'Accept': 'application/vnd.github.symmetra-preview+json'},
        )

    def test_label_required_name(self):
        """Verify the request for retrieving a label on a repository."""
        self.instance.label('')
        assert self.session.get.called is False

    def test_latest_pages_build(self):
        """Test retrieving the most recent pages build."""
        self.instance.latest_pages_build()

        self.session.get.assert_called_once_with(
            url_for('pages/builds/latest')
        )

    def test_latest_release(self):
        """Test the request for retrieving the latest release"""
        self.instance.latest_release()

        self.session.get.assert_called_once_with(
            url_for('releases/latest')
        )

    def test_milestone(self):
        """Test retrieving a specific milestone."""
        self.instance.milestone(20)

        self.session.get.assert_called_once_with(url_for('milestones/20'))

    def test_mark_notifications(self):
        """
        Verify the request for marking all notifications on a repository
        as read.
        """
        self.instance.mark_notifications('2012-10-09T23:39:01Z')
        self.put_called_with(
            url_for('notifications'),
            data={
                'read': True,
                'last_read_at': '2012-10-09T23:39:01Z'
            }
        )

    def test_mark_notifications_required_last_read(self):
        """
        Verify the request for marking all notifications on a repository
        as read.
        """

        self.instance.mark_notifications('')
        self.put_called_with(
            url_for('notifications'),
            data={
                'read': True
            }
        )

    def test_merge(self):
        """Verify the request for performing a merge on a repository."""
        self.instance.merge(base='develop',
                            head='feature',
                            message='merging now')

        self.post_called_with(
            url_for('merges'),
            data={
                'base': 'develop',
                'head': 'feature',
                'commit_message': 'merging now'
            }
        )

    def test_merge_no_message(self):
        """Verify the request for performing a merge on a repository."""
        data = {
            'base': 'develop',
            'head': 'feature'
        }

        self.instance.merge(**data)
        self.post_called_with(
            url_for('merges'),
            data=data
        )

    def test_milestone_requires_positive_id(self):
        """Test that a positive milestone id is required."""
        self.instance.milestone(-1)

        assert self.session.get.called is False

    def test_pages(self):
        """Test retrieving information about a repository's page."""
        self.instance.pages()

        self.session.get.assert_called_once_with(url_for('pages'))

    def test_parent(self):
        """Verify that parent of repository can be retrieved."""
        parent = self.instance.parent
        assert isinstance(parent, ShortRepository)

    def test_permission(self):
        """Verify permissions of a repository can be retrieved."""
        permissions = {
            'admin': False,
            'push': False,
            'pull': True
        }
        assert self.instance.permissions == permissions

    def test_project(self):
        """Show that a user can access a single repository project."""
        self.instance.project(400435)

        self.session.get.assert_called_once_with(
            'https://api.github.com/projects/400435',
            headers=Project.CUSTOM_HEADERS
        )

    def test_pull_request(self):
        """Verify the request for retrieving a pull request."""
        self.instance.pull_request(1)
        self.session.get.assert_called_once_with(
            url_for('pulls/1')
        )

    def test_pull_request_required_number(self):
        """Verify the request for retrieving a pull request."""
        self.instance.pull_request(-1)
        assert self.session.get.called is False

    def test_readme(self):
        """Verify the request for retrieving the README."""
        self.instance.readme()
        self.session.get.assert_called_once_with(
            url_for('readme')
        )

    def test_ref(self):
        """Verify the request for retrieving a reference."""
        self.instance.ref('heads/develop')
        self.session.get.assert_called_once_with(
            url_for('git/refs/heads/develop')
        )

    def test_ref_required_ref(self):
        """Verify the request for retrieving a reference."""
        self.instance.ref('')
        assert self.session.get.called is False

    def test_release_from_tag(self):
        """Test the request for retrieving release by tag name"""
        self.instance.release_from_tag('v1.0.0')

        self.session.get.assert_called_once_with(
            url_for('releases/tags/v1.0.0')
        )

    def test_remove_collaborator(self):
        """Verify the request for removing a collaborator."""
        self.instance.remove_collaborator('octocat')

        self.session.delete.assert_called_once_with(
            url_for('collaborators/octocat')
        )

    def test_remove_collaborator_required_username(self):
        """Verify the request for removing a collaborator."""
        assert self.instance.remove_collaborator('') is False

        assert self.session.delete.called is False

    def test_replace_topics(self):
        """Verify the request for replacing the topics."""
        self.instance.replace_topics(['flask', 'bpython', 'python'])

        self.session.put.assert_called_once_with(
            url_for('topics'),
            data='{"names": ["flask", "bpython", "python"]}',
            headers=self.instance.PREVIEW_HEADERS
        )

    def test_source(self):
        """Verify that the source of the repository can be retrieved."""
        source = self.instance.source

        assert isinstance(source, ShortRepository)

    def test_subscription(self):
        """Verify the request for retrieving the subscription on a repo."""
        self.instance.subscription()

        self.session.get.assert_called_once_with(
            url_for('subscription')
        )

    def test_tag(self):
        """Verify the request for retrieving an annotated tag."""
        self.instance.tag('fake-sha')

        self.session.get.assert_called_once_with(
            url_for('git/tags/fake-sha')
        )

    def test_tag_required_sha(self):
        """Verify the request for retrieving an annotated tag."""
        self.instance.tag('')

        assert self.session.get.called is False

    def test_topics(self):
        """Verify the request for retrieving the topics."""
        self.instance.topics()

        self.session.get.assert_called_once_with(
            url_for('topics'),
            headers=self.instance.PREVIEW_HEADERS
        )

    def test_tree(self):
        """Verify the request for retrieving a tree."""
        self.instance.tree('fake-sha')

        self.session.get.assert_called_once_with(
            url_for('git/trees/fake-sha'),
            params=None
        )

    def test_tree_required_sha(self):
        """Verify the request for retrieving a tree."""
        self.instance.tree('')

        assert self.session.get.called is False

    def test_tree_optional_recursive(self):
        """Verify the request for recursively retrieving a tree."""
        self.instance.tree('fake-sha', recursive=True)

        self.session.get.assert_called_once_with(
            url_for('git/trees/fake-sha'),
            params={'recursive': 1}
        )

    def test_str(self):
        """Verify instance string is formatted correctly."""
        owner = self.instance.owner
        repository = self.instance.name
        assert str(self.instance) == '{0}/{1}'.format(owner, repository)

    def test_weekly_commit_count(self):
        """Verify the request for retrieving total commit counts."""
        self.instance.weekly_commit_count()

        self.session.get.assert_called_once_with(
            url_for('stats/participation')
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
            params={'affiliation': 'all', 'per_page': 100},
            headers={}
        )

    def test_collaborators_valid_affiliation(self):
        """Test the iterating over repo collaborators with an affiliation."""
        i = self.instance.collaborators(affiliation='direct')
        self.get_next(i)

        self.session.get.assert_called_once_with(
            url_for('collaborators'),
            params={'affiliation': 'direct', 'per_page': 100},
            headers={}
        )

    def test_collaborators_invalid_affiliation(self):
        """Test invalid affiliation requests raise ValueError."""
        with pytest.raises(ValueError):
            self.instance.collaborators(affiliation='invalid')

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

    def test_commits_per_page(self):
        """Test the ability to specify page size for commits listing."""

        i = self.instance.commits(per_page=10)
        self.get_next(i)

        self.session.get.assert_called_once_with(
            url_for('commits'),
            params={'per_page': 10},
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

    def test_imported_issues(self):
        """Verify the request for retrieving imported issues."""
        i = self.instance.imported_issues(since='2015-03-15')
        self.get_next(i)

        self.session.get.assert_called_once_with(
            url_for('import/issues'),
            params={'per_page': 100, 'since': '2015-03-15'},
            headers={
                'Accept': 'application/vnd.github.golden-comet-preview+json'
            }
        )

    def test_invitations(self):
        """Verify the request for retrieving invitations."""
        i = self.instance.invitations()
        self.get_next(i)

        self.session.get.assert_called_once_with(
            url_for('invitations'),
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
            headers={},
        )

    def test_labels(self):
        """Test the ability to iterate over a repository's labels."""
        i = self.instance.labels()
        self.get_next(i)

        self.session.get.assert_called_once_with(
            url_for('labels'),
            params={'per_page': 100},
            headers={'Accept': 'application/vnd.github.symmetra-preview+json'},
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

    def test_projects(self):
        """Show that a user can access all repository projects."""
        i = self.instance.projects()
        self.get_next(i)

        self.session.get.assert_called_once_with(
            url_for('projects'),
            params={'per_page': 100},
            headers=Project.CUSTOM_HEADERS
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
            headers={}
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

    def test_create_file(self):
        """
        Verify that creating a file on a repository requires authentication.
        """
        self.assert_requires_auth(self.instance.create_file)

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

    def test_create_project(self):
        """Verify that creating a project requires authentication."""
        with pytest.raises(GitHubError):
            self.instance.create_project('name', 'body')

    def test_create_pull(self):
        """Verify that creating a pull request requires authentication."""
        with pytest.raises(GitHubError):
            self.instance.create_pull(title='foo', base='master')

    def test_create_pull_from_issue(self):
        """
        Verify that creating a pull request from issue requires authentication.
        """
        with pytest.raises(GitHubError):
            self.instance.create_pull_from_issue(
                issue=1,
                title='foo',
                base='master'
            )

    def test_create_status(self):
        """
        Show that a user must be authenticated to create a status object on a
        commit.
        """
        with pytest.raises(GitHubError):
            self.instance.create_status(
                sha='fake-sha'
            )

    def test_delete_key(self):
        """
        Show that a user must be authenticated to delete a key on a
        repository.
        """
        with pytest.raises(GitHubError):
            self.instance.delete_key(1)

    def test_delete_subscription(self):
        """Show that deleting a subscription requires authentication."""
        with pytest.raises(GitHubError):
            self.instance.delete_subscription()

    def test_edit(self):
        """Show that editing a repository requires authentication."""
        with pytest.raises(GitHubError):
            self.instance.edit(name='Hello')

    def test_invitations(self):
        """Show that iterating over the invitations requires authentication."""
        self.assert_requires_auth(self.instance.invitations)

    def test_is_collaborator(self):
        """
        Show that checking if a user is collaborator on a repository requires
        authentication.
        """
        with pytest.raises(GitHubError):
            self.instance.is_collaborator('octocat')

    def test_hook(self):
        """Show that a user must be authenticated to retrieve a hook."""
        with pytest.raises(GitHubError):
            self.instance.hook(1)

    def test_hooks(self):
        """Show that a user must be authenticated to list hooks."""
        with pytest.raises(GitHubError):
            self.instance.hooks()

    def test_import_issue(self):
        """Show that a user must be authenticated to import an issue."""
        with pytest.raises(GitHubError):
            self.instance.import_issue(title='foo',
                                       body='Foobar body',
                                       created_at='2014-03-16T17:15:42Z')

    def test_imported_issues(self):
        """
        Show that a user must be authenticated to retrieve imported issues.
        """
        self.assert_requires_auth(self.instance.imported_issues)

    def test_imported_issue(self):
        """
        Show that a user must be authenticated to retrieve an imported issue.
        """
        with pytest.raises(GitHubError):
            self.instance.import_issue(1)

    def test_key(self):
        """Show that a user must be authenticated to fetch a key."""
        with pytest.raises(GitHubError):
            self.instance.key(10)

    def test_keys(self):
        """Show that a user must be authenticated to list keys."""
        with pytest.raises(GitHubError):
            self.instance.keys()

    def test_mark_notifications(self):
        """
        Show that a user must be authenticated to mark notifications
        as read.
        """
        with pytest.raises(GitHubError):
            self.instance.mark_notifications('2012-10-09T23:39:01Z')

    def test_merge(self):
        """
        Show that a user must be authenticated to perform a merge on a
        repository.
        """
        with pytest.raises(GitHubError):
            self.instance.merge('master', 'octocat/feature')

    def test_notifications(self):
        """Show that a user must be authenticated to list notifications."""
        with pytest.raises(GitHubError):
            self.instance.notifications()

    def test_pages_builds(self):
        """Show that a user must be authenticated to list their builds."""
        with pytest.raises(GitHubError):
            self.instance.pages_builds()

    def test_remove_collaborator(self):
        """Show that a user must be authenticated to remove a collaborator."""
        self.assert_requires_auth(self.instance.remove_collaborator)

    def test_replace_topics(self):
        """Show that a user must be authenticated to replace the topics."""
        self.assert_requires_auth(self.instance.replace_topics)

    def test_subscription(self):
        """
        Show that a user must be authenticated to retrieve the
        subscription.
        """
        self.assert_requires_auth(self.instance.subscription)

    def test_teams(self):
        """Show that a user must be authenticated to list teams on a repo."""
        with pytest.raises(GitHubError):
            self.instance.teams()


class TestContents(helper.UnitHelper):
    "Unit tests for content methods."""

    described_class = Contents
    example_data = content_example_data

    def test_delete(self):
        """Verify the request for deleting content from a repository."""
        data = {
            'message': 'Deleting file from repository',
            'branch': 'featureA',
            'committer': {
                'name': 'Octocat',
                'email': 'octocat@github.com'
            },
            'author': {
                'name': 'Octocat',
                'email': 'octocat@github.com'
            }
        }
        self.instance.delete(**data)
        data.update({
            'sha': '3f4f0b9a43d13376679ee5710958ca88baa7c421'
        })
        self.delete_called_with(
            contents_url_for(),
            data=data
        )

    def test_git_url(self):
        """Veriy instance contains git url."""
        assert self.instance.links['git'] == self.instance.git_url

    def test_html_url(self):
        """Verify instance contains html url."""
        assert self.instance.links['html'] == self.instance.html_url

    def test_str(self):
        """Verify that instance string is formatted properly."""
        assert str(self.instance) == '<Contents [{0}]>'.format(
            self.instance.path
        )

    def test_update(self):
        """
        Verify the request for updating a file's contents on a repository.
        """
        data = {
            'message': 'Updating content files.',
            'content': b'Updated content here.'
        }

        self.instance.update(**data)
        data.update({
            'content': b64encode(data['content']).decode('utf-8'),
            'sha': self.instance.sha
        })

        self.put_called_with(
            contents_url_for(),
            data=data
        )

    def test_update_required_content(self):
        """
        Verify the request for updating a file's contents on a repository.
        """
        data = {
            'message': 'Updating content files.',
            'content': 1,
        }
        with pytest.raises(ValueError):
            self.instance.update(**data)


class TestContentsRequiresAuth(helper.UnitRequiresAuthenticationHelper):

    """Unit test for Content methods that require Auth."""

    described_class = Contents
    example_data = content_example_data

    def test_delete(self):
        """
        Show that deleting content from a repository requires authentication.
        """
        self.assert_requires_auth(self.instance.delete)

    def test_update(self):
        """
        Show that updating a file's content on a repository requires
        authentication.
        """
        self.assert_requires_auth(self.instance.update)


class TestHook(helper.UnitHelper):

    """Test methods on Hook class."""

    described_class = Hook
    example_data = hook_example_data

    def test_str(self):
        """Show that instance string is formatted correctly."""
        assert str(self.instance) == '<Hook [{0}]>'.format(self.instance.name)

    def test_delete(self):
        """Verify the request for editing a hook on a repository."""
        self.instance.delete()

        self.session.delete.assert_called_once_with(
            hook_url_for()
        )

    def test_edit(self):
        """Verify the request for editing a hook on a repository."""
        config = {
            'url': 'https://fake-url.com',
            'content_type': 'json'
        }

        self.instance.edit(config=config, events=['push'], add_events=['pull'],
                           rm_events=['release'])
        data = {
            'config': config,
            'events': ['push'],
            'add_events': ['pull'],
            'remove_events': ['release'],
            'active': True
        }
        self.patch_called_with(
            hook_url_for(),
            data=data
        )

    def test_edit_failed(self):
        """Verify the request for editing a hook on a repository."""

        assert self.instance.edit() is False

    def test_ping(self):
        """Verify the request for ping a hook on a repository."""
        self.instance.ping()

        self.post_called_with(
            hook_url_for('pings'),
        )

    def test_test(self):
        """Verify the request for testing a hook on a repository."""
        self.instance.test()

        self.post_called_with(
            hook_url_for('tests'),
        )


class TestHookRequiresAuth(helper.UnitRequiresAuthenticationHelper):

    """Test methods on Hook object that require authentication."""

    described_class = Hook
    example_data = hook_example_data

    def test_delete(self):
        """
        Show that a user must be authenticated to delete a hook on a
        repository.
        """
        self.assert_requires_auth(self.instance.delete)

    def test_edit(self):
        """
        Show that a user must be authenticated to edit a hook on a repository.
        """
        self.assert_requires_auth(self.instance.edit)

    def test_ping(self):
        """
        Show that a user must be authenticated to ping a hook on a repository.
        """
        self.assert_requires_auth(self.instance.ping)

    def test_test(self):
        """
        Show that a user must be authenticated to test a hook on a repository.
        """
        self.assert_requires_auth(self.instance.test)


class TestRepoComment(helper.UnitHelper):

    """Unit test for methods on RepoComment object."""

    example_data = comment_example_data
    described_class = RepoComment

    def test_delete(self):
        """Verify the request for deleting a comment on a repository."""
        self.instance.delete()

        self.session.delete.assert_called_once_with(
            comment_url_for()
        )

    def test_str(self):
        """Show that instance string is formatted correctly."""
        assert str(self.instance).startswith('<Repository Comment')

    def test_update(self):
        """Verify the request for updating a comment on a repository."""
        data = {
            'body': 'new body'
        }
        self.instance.update(body=data['body'])

        self.patch_called_with(
            comment_url_for(),
            json=data
        )


class TestRepoCommentRequiresAuth(helper.UnitRequiresAuthenticationHelper):

    """
    Unit test for methods that require authentication on RepoCommment
    object.
    """

    described_class = RepoComment
    example_data = comment_example_data

    def test_delete(self):
        """
        Show that a user must be authenticated to delete a comment on a
        repository.
        """
        self.assert_requires_auth(self.instance.delete)

    def test_update(self):
        """
        Show that a user must be authenticated to update a comment on a
        repository.
        """
        self.assert_requires_auth(self.instance.update)


class TestRepoCommit(helper.UnitHelper):

    """Unit tests for RepoCommit object."""

    described_class = RepoCommit
    example_data = commit_example_data

    def test_diff(self):
        """Verify the request for retrieving the diff for a commit."""
        self.instance.diff()

        self.session.get.assert_called_once_with(
            commit_url_for(),
            headers={'Accept': 'application/vnd.github.diff'}
        )

    def test_patch(self):
        """
        Verify the request for retrieving the patch formatted diff for a
        commit.
        """
        self.instance.patch()

        self.session.get.assert_called_once_with(
            commit_url_for(),
            headers={'Accept': 'application/vnd.github.patch'}
        )

    def test_str(self):
        """Show that instance string is formatted correctly."""
        assert str(self.instance).startswith('<Repository Commit')


class TestComparison(helper.UnitHelper):

    """Unit test for Comparison object."""
    described_class = Comparison
    example_data = compare_example_data

    def test_diff(self):
        """Verify the request for retrieving a diff for this comparison."""
        self.instance.diff()

        self.session.get.assert_called_once_with(
            compare_url_for(),
            headers={'Accept': 'application/vnd.github.diff'}
        )

    def test_patch(self):
        """Verify the request for retrieving a diff for this comparison."""
        self.instance.patch()

        self.session.get.assert_called_once_with(
            compare_url_for(),
            headers={'Accept': 'application/vnd.github.patch'}
        )

    def test_str(self):
        """Show that instance string is formatted correctly."""
        assert str(self.instance).startswith('<Comparison')


class TestRepositoryCompatibility_2_12(helper.UnitIteratorHelper):

    """Unit tests for Repository from Github Enterprise 2.12"""

    described_class = Repository
    example_data = repo_2_12_example_data

    def test_repository(self):
        """
        Test the ability to retrieve a Repository with older releases
        """
        assert isinstance(self.instance, Repository)
