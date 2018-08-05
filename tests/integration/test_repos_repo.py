"""Integration tests for Repositories."""
import github3
import github3.exceptions as exc

import pytest

from . import helper


class TestRepository(helper.IntegrationHelper):

    """Integration tests for the Repository object."""

    def test_add_collaborator(self):
        """Test the ability to add a collaborator to a repository."""
        self.basic_login()
        cassette_name = self.cassette_name('add_collaborator')
        with self.recorder.use_cassette(cassette_name):
            repository = self.gh.repository('gh3test', 'my-new-repo')
            assert repository
            assert repository.add_collaborator('sigmavirus24')
            repository.remove_collaborator('sigmavirus24')

    def test_assignees(self):
        """Test the ability to retrieve assignees of issues on a repo."""
        cassette_name = self.cassette_name('assignees')
        with self.recorder.use_cassette(cassette_name):
            repository = self.gh.repository('kennethreitz', 'requests')
            assert repository is not None
            for assignee in repository.assignees():
                assert isinstance(assignee, github3.users.ShortUser)

    def test_blob(self):
        """Test the ability to retrieve blob on a repository."""
        cassette_name = self.cassette_name('blob')
        with self.recorder.use_cassette(cassette_name):
            repository = self.gh.repository('sigmavirus24', 'github3.py')
            blob = repository.blob('e1bacfb242c7dee1d24aef52df23d7a3f7442ea3')
            assert isinstance(blob, github3.git.Blob)

    def test_branch(self):
        """Test the ability to retrieve a single branch in a repository."""
        cassette_name = self.cassette_name('branch')
        with self.recorder.use_cassette(cassette_name):
            repository = self.gh.repository('sigmavirus24', 'github3.py')
            assert repository is not None
            branch = repository.branch('develop')
            assert isinstance(branch, github3.repos.branch.Branch)
            assert 'enabled' in branch.original_protection

    def test_branches(self):
        """Test the ability to retrieve the branches in a repository."""
        cassette_name = self.cassette_name('branches')
        with self.recorder.use_cassette(cassette_name):
            repository = self.gh.repository('sigmavirus24', 'github3.py')
            assert repository is not None
            for branch in repository.branches():
                assert isinstance(branch, github3.repos.branch.ShortBranch)

    def test_project(self):
        """Test the ability to retrieve a single repository project."""
        self.token_login()
        cassette_name = self.cassette_name('project')
        with self.recorder.use_cassette(cassette_name):
            organization = self.gh.organization('testgh3py')
            repository = organization.create_repository('test_project')
            assert repository is not None
            created_project = repository.create_project('test-project',
                                                        body='test body')
            project = repository.project(created_project.id)
            assert isinstance(project, github3.projects.Project)
            repository.delete()

    def test_projects(self):
        """Test the ability to retrieve an repository's projects."""
        self.token_login()
        cassette_name = self.cassette_name('projects')
        with self.recorder.use_cassette(cassette_name):
            organization = self.gh.organization('testgh3py')
            repository = organization.create_repository('test_project')
            assert repository is not None
            repository.create_project('test-project-0', body='test body')
            repository.create_project('test-project-1', body='test body')
            for project in repository.projects():
                assert isinstance(project, github3.projects.Project)
            repository.delete()

    def test_protected_branches(self):
        """Test the ability to retrieve protected branches in a repository."""
        self.token_login()
        cassette_name = self.cassette_name('branches_protected')
        with self.recorder.use_cassette(cassette_name):
            repository = self.gh.repository('sigmavirus24', 'github3.py')
            assert repository is not None
            assert all(isinstance(b, github3.repos.branch.ShortBranch)
                       for b in repository.branches(protected=True))

    def test_code_frequency(self):
        """Test the ability to retrieve the code frequency in a repo."""
        cassette_name = self.cassette_name('code_frequency')
        with self.recorder.use_cassette(cassette_name):
            repository = self.gh.repository('sigmavirus24', 'github3.py')
            assert repository is not None
            for code_freq in repository.code_frequency():
                assert isinstance(code_freq, list)
                assert len(code_freq) > 0

    def test_collaborators(self):
        """Test the ability to retrieve the collaborators on a repository."""
        self.token_login()
        cassette_name = self.cassette_name('collaborators')
        with self.recorder.use_cassette(cassette_name):
            repository = self.gh.repository('sigmavirus24', 'github3.py')
            assert repository is not None
            for collaborator in repository.collaborators():
                assert isinstance(collaborator, github3.users.Collaborator)

    def test_comments(self):
        """Test the ability to retrieve comments on a repository."""
        cassette_name = self.cassette_name('comments')
        with self.recorder.use_cassette(cassette_name):
            repository = self.gh.repository('sigmavirus24', 'github3.py')
            assert repository is not None
            for comment in repository.comments():
                assert isinstance(comment, github3.repos.comment.RepoComment)

    def test_commit_activity(self):
        """Test the ability to retrieve commit activity on a repo."""
        cassette_name = self.cassette_name('commit_activity')
        with self.recorder.use_cassette(cassette_name):
            repository = self.gh.repository('sigmavirus24', 'github3.py')
            assert repository is not None
            for activity in repository.commit_activity():
                assert isinstance(activity, dict)

    def test_commit_comment(self):
        """Test the ability to retrieve single commit comment."""
        cassette_name = self.cassette_name('commit_comment')
        with self.recorder.use_cassette(cassette_name):
            repository = self.gh.repository('sigmavirus24', 'github3.py')
            comment = repository.commit_comment(1380832)
            assert isinstance(comment, github3.repos.comment.RepoComment)

    def test_commits(self):
        """Test the ability to retrieve commits on a repository."""
        cassette_name = self.cassette_name('commits')
        with self.recorder.use_cassette(cassette_name):
            repository = self.gh.repository('sigmavirus24', 'github3.py')
            assert repository is not None
            for commit in repository.commits(number=25):
                assert isinstance(commit, github3.repos.commit.ShortCommit)

    def test_compare_commits(self):
        """Test the ability to compare two commits."""
        cassette_name = self.cassette_name('compare_commits')
        with self.recorder.use_cassette(cassette_name):
            repository = self.gh.repository('sigmavirus24', 'github3.py')
            base = 'a811e1a270f65eecb65755eca38d888cbefcb0a7'
            head = '76dcc6cb4b9860034be81b7e58adc286a115aa97'
            comparison = repository.compare_commits(base, head)
            assert isinstance(comparison, github3.repos.comparison.Comparison)

    def test_contributor_statistics(self):
        """Test the ability to retrieve contributor statistics for a repo."""
        cassette_name = self.cassette_name('contributor_statistics')
        with self.recorder.use_cassette(cassette_name):
            repository = self.gh.repository('sigmavirus24', 'github3.py')
            assert repository is not None
            for stat in repository.contributor_statistics():
                assert isinstance(stat, github3.repos.stats.ContributorStats)

    def test_contributors(self):
        """Test the ability to retrieve the contributors to a repository."""
        cassette_name = self.cassette_name('contributors')
        with self.recorder.use_cassette(cassette_name):
            repository = self.gh.repository('sigmavirus24', 'github3.py')
            assert repository is not None
            for contributor in repository.contributors():
                assert isinstance(contributor, github3.users.Contributor)
                assert isinstance(contributor.contributions, int)

    def test_create_blob(self):
        """Test the ability to create a blob on a repository."""
        self.token_login()
        cassette_name = self.cassette_name('create_blob')
        with self.recorder.use_cassette(cassette_name):
            repository = self.gh.repository('github3py', 'github3.py')
            content = 'VGVzdCBibG9i\n'
            encoding = 'base64'
            sha = '30f2c645388832f70d37ab2b47eb9ea527e5ae7c'
            assert repository.create_blob(content, encoding) == sha

    def test_create_comment(self):
        """Test the ability to create a comment on a repository."""
        self.token_login()
        cassette_name = self.cassette_name('create_comment')
        with self.recorder.use_cassette(cassette_name):
            repository = self.gh.repository('github3py', 'github3.py')
            body = ('Early morning commits are a good idea. '
                    'It is just me. Me migrating unit/integration tests.')
            sha = '1ad1d8309317a4240d5f17b23a2e7dab25e4cb10'
            assert isinstance(repository.create_comment(body, sha),
                              github3.repos.comment.RepoComment)

    def test_create_commit(self):
        """Test the ability to create a commit."""
        self.token_login()
        cassette_name = self.cassette_name('create_commit')
        with self.recorder.use_cassette(cassette_name):
            repository = self.gh.repository('github3py', 'github3.py')
            data = {'message': 'My commit message',
                    'author': {
                        'name': 'Matt Chung',
                        'email': 'foo@example.com',
                        'date': '2015-12-03T16:13:30+12:00',
                    },
                    'parents': [
                        '679358c79005523246ec3f460410ceda6b94e006'
                    ],
                    'tree': '6857122c4eff3ea461516c066f6bb1eba206d694',
                    }
            commit = repository.create_commit(**data)
            assert isinstance(commit, github3.git.Commit)

    def test_create_commit_with_empty_committer(self):
        """Show that UnProcessableEntity is raised with empty comitter."""
        self.token_login()
        cassette_name = self.cassette_name(('create_commit_with_'
                                            'empty_committer'))
        with self.recorder.use_cassette(cassette_name):
            repository = self.gh.repository('github3py', 'github3.py')
            data = {'message': 'My commit message',
                    'author': {
                        'name': 'Matt Chung',
                        'email': 'foo@example.com',
                        'date': '2015-12-03T16:13:30+12:00',
                    },
                    'committer': {},
                    'parents': [
                        '679358c79005523246ec3f460410ceda6b94e006'
                    ],
                    'tree': '6857122c4eff3ea461516c066f6bb1eba206d694',
                    }
            with pytest.raises(exc.UnprocessableEntity):
                repository.create_commit(**data)

    def test_create_empty_blob(self):
        """Test the ability to create an empty blob on a repository."""
        self.basic_login()
        cassette_name = self.cassette_name('create_empty_blob')
        with self.recorder.use_cassette(cassette_name):
            repository = self.gh.repository('github3py', 'fork_this')
            assert repository is not None
            blob_sha = repository.create_blob('', 'utf-8')

        assert blob_sha is not None
        assert blob_sha != ''

    def test_create_deployment(self):
        """Test the ability to create a deployment for a repository."""
        self.basic_login()
        cassette_name = self.cassette_name('create_deployment')
        with self.recorder.use_cassette(cassette_name):
            repository = self.gh.repository('github3py', 'delete_contents')
            assert repository is not None
            deployment = repository.create_deployment('0.1.0')

        assert isinstance(deployment, github3.repos.deployment.Deployment)

    def test_create_file(self):
        """Test the ability to create a file on a repository."""
        self.token_login()
        cassette_name = self.cassette_name('create_file')
        with self.recorder.use_cassette(cassette_name):
            repository = self.gh.repository('github3py', 'delete_contents')
            data = {
                'path': 'hello.txt',
                'message': 'my commit message',
                'content': b'my new file contents',
                'branch': 'master',
                'committer': {
                    'name': 'Matt Chung',
                    'email': 'hello@itsmemattchung.com'
                }
            }

            created_file = repository.create_file(**data)
            created_file['content'].delete('Delete hello.txt')

        assert isinstance(
            created_file['content'],
            github3.repos.contents.Contents
        )
        assert isinstance(
            created_file['commit'],
            github3.git.Commit
        )

    def test_create_fork(self):
        """Test the ability to fork a repository."""
        self.token_login()
        betamax_kwargs = {'match_requests_on': ['method', 'uri', 'json-body']}
        cassette_name = self.cassette_name('create_fork')
        with self.recorder.use_cassette(cassette_name, **betamax_kwargs):
            repository = self.gh.repository('kennethreitz', 'requests')
            forked_repo = repository.create_fork()
            assert isinstance(forked_repo, github3.repos.Repository)

            org_forked_repo = repository.create_fork('github3py')
            assert isinstance(org_forked_repo, github3.repos.Repository)

    def test_create_hook(self):
        """Test the ability to create a hook for a repository."""
        self.token_login()
        cassette_name = self.cassette_name('create_hook')
        with self.recorder.use_cassette(cassette_name):
            repository = self.gh.repository('github3py', 'github3.py')
            data = {
                'name': 'web',
                'config': {
                    'url': 'http://example.com/webhook',
                    'content_type': 'json'
                }
            }
            hook = repository.create_hook(**data)
            assert isinstance(hook, github3.repos.hook.Hook)

    def test_create_issue(self):
        """Test the ability to create an issue for a repository."""
        self.auto_login()
        cassette_name = self.cassette_name('create_issue')
        with self.recorder.use_cassette(cassette_name):
            repository = self.gh.repository('sigmavirus24', 'github3.py')
            data = {
                'title': 'Create Issue Integration Test',
                'body': 'Delete me after',
                'assignee': 'itsmemattchung'
            }
            issue = repository.create_issue(**data)
            assert isinstance(issue, github3.issues.issue.ShortIssue)

    def test_create_issue_multiple_assignees(self):
        """
        Test the ability to create an issue with multiple assignees
        for a repository.
        """
        self.token_login()
        cassette_name = self.cassette_name('create_issue_multiple_assignees')
        with self.recorder.use_cassette(cassette_name):
            repository = self.gh.repository('sigmavirus24', 'github3.py')
            data = {
                'title': 'Create Issue Integration Test',
                'body': 'Delete me after',
                'assignees': ['itsmemattchung', 'sigmavirus24']
            }
            issue = repository.create_issue(**data)
            assert isinstance(issue, github3.issues.issue.ShortIssue)

    def test_create_issue_both_assignee_and_assignees(self):
        """
        Test the ability to create an issue with both assignee
        and assignees.
        """
        self.token_login()
        cassette_name = self.cassette_name(
            'create_issue_both_assignee_and_assignees'
        )
        with self.recorder.use_cassette(cassette_name):
            repository = self.gh.repository('sigmavirus24', 'github3.py')
            data = {
                'title': 'Create Issue Integration Test',
                'body': 'Delete me after',
                'assignee': 'itsmemattchung',
                'assignees': ['itsmemattchung', 'sigmavirus24']
            }
            with pytest.raises(exc.UnprocessableEntity):
                repository.create_issue(**data)

    def test_create_key(self):
        """Test the ability to deploy a key."""
        self.token_login()
        cassette_name = self.cassette_name('create_key')
        with self.recorder.use_cassette(cassette_name):
            repository = self.gh.repository('github3py', 'github3.py')
            key = ('ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDZn4/RGE9YQrfjq7wSr'
                   'YkdtKH3r1rEIkx/4Nv1AG/PqE4AWKSVzKkqhurnqKtctVCLtU9pNFIjl/'
                   'XvNluTW3zrfqKjgaDdiBtWwecWzSbQqugfzmwFqCE4smJkP8e7+e9Fd1k'
                   'GOGyqVJLBLfIUdEbHN3Ws40Z9OXgrJ/tiNdg1HHgAOjpknCMrQI8NDP9o'
                   '9CLuE/AfNVzRNOzpf/rrdZ4YW4kcDhbcQ8X7DGCnbvY9wUp3lDmSvVy6z'
                   'olYwLziYqsGjw0kLHvIzHdbGCjp+50iZSBrm29AlWa9eRsGskiUTIk6SA'
                   'Q8Fm5qKNkCtPYQ6YmjRiKyDtsMoqfjzDkyEPLv mattchung@Matts-Ma'
                   'cBook-Air.local')
            data = {
                'title': 'Deploy Key',
                'key': key
            }
            key = repository.create_key(**data)
            assert isinstance(key, github3.users.Key)

    def test_create_label(self):
        """Test the ability to create a label on a repository."""
        self.token_login()
        cassette_name = self.cassette_name('create_label')
        with self.recorder.use_cassette(cassette_name):
            repository = self.gh.repository('github3py', 'delete_contents')
            label = repository.create_label('fakelabel', 'fad8c7')
            label.delete()

        assert isinstance(label, github3.issues.label.Label)

    def test_create_milestone(self):
        """Test the ability to create a milestone on a repository."""
        self.token_login()
        cassette_name = self.cassette_name('create_milestone')
        with self.recorder.use_cassette(cassette_name):
            repository = self.gh.repository('github3py', 'delete_contents')
            milestone = repository.create_milestone('foo')
            milestone.delete()

        assert isinstance(milestone, github3.issues.milestone.Milestone)

    def test_create_project(self):
        """Test the ability to create a project on a repository."""
        self.token_login()
        cassette_name = self.cassette_name('create_repo_project')
        with self.recorder.use_cassette(cassette_name):
            repository = self.gh.repository('github3py', 'delete_contents')
            project = repository.create_project(
                'test-project', body='test body')
            project.delete()

        assert isinstance(project, github3.projects.Project)

    def test_create_pull(self):
        """Test the ability to create a pull request on a repository."""
        self.token_login()
        cassette_name = self.cassette_name('create_pull')
        with self.recorder.use_cassette(cassette_name):
            original_repository = self.gh.repository('github3py', 'github3.py')
            repository = original_repository.create_fork(
                organization='testgh3py',
            )
            pull_request = repository.create_pull(
                title='Update forked repo',
                base='master',
                head='testgh3py:develop',
                body='Testing the ability to create a pull request',
            )
            repository.delete()

        assert isinstance(pull_request, github3.pulls.ShortPullRequest)

    def test_create_pull_from_issue(self):
        """Verify creation of a pull request from an issue."""
        self.token_login()
        cassette_name = self.cassette_name('create_pull_from_issue')
        with self.recorder.use_cassette(cassette_name):
            repository = self.gh.repository('github3py', 'fork_this')
            issue = repository.create_issue('Test create pull from issue')
            pull_request = repository.create_pull_from_issue(
                issue=issue.number,
                base='master',
                head='sigmavirus24:master',
            )

        assert isinstance(pull_request, github3.pulls.ShortPullRequest)

    def test_create_ref(self):
        """Verify the ability to create a reference on a repository."""
        self.auto_login()
        cassette_name = self.cassette_name('create_ref')
        with self.recorder.use_cassette(cassette_name):
            repository = self.gh.repository('github3py', 'fork_this')
            master = repository.commit('master')
            ref = repository.create_ref(
                'refs/tags/test-tag-{}'.format(master.sha[:6]),
                master,
            )
            assert isinstance(ref, github3.git.Reference)
            ref.delete()

    def test_create_branch_ref(self):
        """Verify the ability to create a branch on a repository."""
        self.auto_login()
        cassette_name = self.cassette_name('create_branch_ref')
        with self.recorder.use_cassette(cassette_name):
            repository = self.gh.repository('github3py', 'fork_this')
            master = repository.commit('master')
            ref = repository.create_branch_ref(
                'test-branch-{}'.format(master.sha[:6]),
                master,
            )
            assert isinstance(ref, github3.git.Reference)
            ref.delete()

    def test_create_release(self):
        """Test the ability to create a release on a repository."""
        self.token_login()
        cassette_name = self.cassette_name('create_release')
        with self.recorder.use_cassette(cassette_name):
            repository = self.gh.repository('sigmavirus24', 'charade')
            assert repository is not None
            release = repository.create_release(
                '1.0.3.test', 'f1d4e150be7070adfbbdca164328d69723e096ec',
                'Test release'
                )
            release.delete()

        assert isinstance(release, github3.repos.release.Release)

    def test_create_status(self):
        """Test the ability to create a status object on a commit."""
        self.token_login()
        cassette_name = self.cassette_name('create_status')
        with self.recorder.use_cassette(cassette_name):
            repository = self.gh.repository('github3py', 'github3.py')
            status = repository.create_status(
                sha='24893ec07db2a12073703258f0089f105906d2e4',
                state='failure'
            )

        assert isinstance(status, github3.repos.status.Status)

    def test_create_tag(self):
        """Test the ability to create an annotated tag on a repository."""
        self.basic_login()
        cassette_name = self.cassette_name('create_tag')
        with self.recorder.use_cassette(cassette_name):
            repository = self.gh.repository('github3py', 'fork_this')
            assert repository is not None
            tag = repository.create_tag(
                tag='tag-name-redux',
                message='Test annotated tag creation',
                sha='5145c9682d46d714c31ae0b5fbe30a83039a96e5',
                obj_type='commit',
                tagger={
                    'name': 'Ian Cordasco',
                    'email': 'graffatcolmingov@gmail.com',
                    'date': '2015-11-01T14:09:00Z'
                }
            )

        assert isinstance(tag, github3.git.Tag)

    def test_delete(self):
        """Test that a repository can be deleted."""
        self.basic_login()
        cassette_name = self.cassette_name('delete')
        with self.recorder.use_cassette(cassette_name):
            repository = self.gh.create_repository('gh3test',
                                                   'delete-me-in-seconds')
            assert repository is not None
            assert repository.delete() is True

    def test_delete_key(self):
        """Test the ability to delete a key from a repository."""
        self.token_login()
        cassette_name = self.cassette_name('delete_key')
        with open('tests/id_rsa.pub', 'r') as fd:
            key_contents = fd.read()
        with self.recorder.use_cassette(cassette_name):
            repository = self.gh.repository('github3py', 'github3.py')
            key = repository.create_key('Key Name', key_contents)
            assert repository.delete_key(key.id) is True

    def test_delete_subscription(self):
        """Test the ability to delete a subscription from a repository."""
        self.token_login()
        cassette_name = self.cassette_name('delete_subscription')
        with self.recorder.use_cassette(cassette_name):
            repository = self.gh.create_repository('gh3-delete-me')
            repository.subscribe()
            assert repository.delete_subscription() is True

    def test_deployment(self):
        """Test that a deployment can be retrieved by its id."""
        cassette_name = self.cassette_name('deployment')
        with self.recorder.use_cassette(cassette_name):
            repository = self.gh.repository('sigmavirus24', 'github3.py')
            assert repository is not None
            deployment = repository.deployment(797)

        assert isinstance(deployment, github3.repos.deployment.Deployment)

    def test_deployments(self):
        """Test that a repository's deployments may be retrieved."""
        cassette_name = self.cassette_name('deployments')
        with self.recorder.use_cassette(cassette_name):
            repository = self.gh.repository('sigmavirus24', 'github3.py')
            assert repository is not None
            for d in repository.deployments():
                assert isinstance(d, github3.repos.deployment.Deployment)

    def test_directory_contents(self):
        """Test that a directory's contents can be retrieved."""
        cassette_name = self.cassette_name('directory_contents')
        with self.recorder.use_cassette(cassette_name):
            repository = self.gh.repository('sigmavirus24', 'github3.py')
            contents = repository.directory_contents('github3/search/')

        for (filename, content) in contents:
            assert content.name == filename
            assert isinstance(content, github3.repos.contents.Contents)

    def test_directory_contents_for_a_file(self):
        """Verify we raise a sensical exception for a directory's contents."""
        cassette_name = self.cassette_name('not_really_directory_contents')
        with self.recorder.use_cassette(cassette_name):
            repository = self.gh.repository('sigmavirus24', 'github3.py')
            with pytest.raises(github3.exceptions.UnprocessableResponseBody):
                repository.directory_contents('README.rst')

    def test_edit(self):
        """Test the ability to edit a repository."""
        self.token_login()
        cassette_name = self.cassette_name('edit')
        with self.recorder.use_cassette(cassette_name):
            repository = self.gh.repository('github3py', 'github3.py')
            assert repository.edit('github3py') is True

    def test_archive_a_repository(self):
        """Verify we can archive a repository."""
        self.token_login()
        cassette_name = self.cassette_name('archive_a_repository')
        with self.recorder.use_cassette(cassette_name):
            organization = self.gh.organization('testgh3py')
            repository = organization.create_repository('archive-me')
            assert repository.archived is False
            repository.edit(name='i-have-been-archived', archived=True)
            assert repository.archived is True
            repository.delete()

    def test_edit_has_projects(self):
        self.token_login()
        cassette_name = self.cassette_name('edit_has_projects')
        with self.recorder.use_cassette(cassette_name):
            repository = self.gh.repository('jacquerie', 'flask-shell-bpython')
            assert repository.has_projects is True
            repository.edit('flask-shell-bpython', has_projects=False)
            assert repository.has_projects is False

    def test_events(self):
        """Test that a user can iterate over the events from a repository."""
        cassette_name = self.cassette_name('events')
        with self.recorder.use_cassette(cassette_name):
            repository = self.gh.repository('sigmavirus24', 'github3.py')
            assert repository is not None
            events = list(repository.events(number=100))

        assert len(events) > 0
        for event in events:
            assert isinstance(event, github3.events.Event)

    def test_file_contents(self):
        """Test that a file's contents can be retrieved."""
        cassette_name = self.cassette_name('file_contents')
        with self.recorder.use_cassette(cassette_name):
            repository = self.gh.repository('sigmavirus24', 'github3.py')
            contents = repository.file_contents('github3/repos/repo.py')

        assert isinstance(contents, github3.repos.contents.Contents)
        assert contents.content is not None
        assert contents.decoded is not None

    def test_forks(self):
        """Test that a user can iterate over the forks of a repository."""
        cassette_name = self.cassette_name('forks')
        with self.recorder.use_cassette(cassette_name):
            repository = self.gh.repository('sigmavirus24', 'github3.py')
            assert repository is not None
            forks = list(repository.forks())

        assert len(forks) > 0
        for fork in forks:
            assert isinstance(fork, github3.repos.ShortRepository)

    def test_git_commit(self):
        """Test the ability to retrieve a commit from a repository."""
        cassette_name = self.cassette_name('git_commit')
        with self.recorder.use_cassette(cassette_name):
            repository = self.gh.repository('sigmavirus24', 'github3.py')
            commit = repository.git_commit(
                '9ea7482560c9e70c66019f7981aa1727caf888e0'
            )
        assert isinstance(commit, github3.git.Commit)

    def test_hook(self):
        """Test the ability to retrieve a hook from a repository."""
        self.token_login()
        cassette_name = self.cassette_name('hook')
        with self.recorder.use_cassette(cassette_name):
            repository = self.gh.repository('github3py', 'github3.py')
            hook_id = next(repository.hooks()).id
            hook = repository.hook(hook_id)
        assert isinstance(hook, github3.repos.hook.Hook)

    def test_hooks(self):
        """Test that a user can iterate over the hooks of a repository."""
        self.basic_login()
        cassette_name = self.cassette_name('hooks')
        with self.recorder.use_cassette(cassette_name):
            repository = self.gh.repository('github3py', 'fork_this')
            assert repository is not None
            hooks = list(repository.hooks())

        assert len(hooks) > 0
        for hook in hooks:
            assert isinstance(hook, github3.repos.hook.Hook)

    def test_ignore(self):
        """Test that a user can ignore the notifications on a repository."""
        self.basic_login()
        cassette_name = self.cassette_name('ignore')
        with self.recorder.use_cassette(cassette_name):
            repository = self.gh.repository('jnewland',
                                            'gmond_python_modules')
            assert repository is not None
            subscription = repository.ignore()
            assert subscription.ignored is True

    def test_invitations(self):
        """Test that a user can iterate over the invitations to a repo."""
        self.token_login()
        cassette_name = self.cassette_name('invitations')
        with self.recorder.use_cassette(cassette_name):
            repository = self.gh.repository('jacquerie', 'flask-shell-bpython')
            invitations = list(repository.invitations())

        assert len(invitations) > 0
        for invitation in invitations:
            assert isinstance(invitation, github3.repos.invitation.Invitation)

    def test_is_assignee(self):
        """
        Test the ability to check if a user can be assigned issues on a
        repository.
        """
        cassette_name = self.cassette_name('is_assignee')
        with self.recorder.use_cassette(cassette_name):
            repository = self.gh.repository('sigmavirus24', 'github3.py')
            is_assignee = repository.is_assignee('sigmavirus24')
        assert is_assignee is True

    def test_is_collaborator(self):
        """
        Test the ability to check if a user is a collaborator on a
        repository.
        """
        self.token_login()
        cassette_name = self.cassette_name('is_collaborator')
        with self.recorder.use_cassette(cassette_name):
            repository = self.gh.repository('sigmavirus24', 'github3.py')
            assert repository.is_collaborator('sigmavirus24') is True

    def test_issue(self):
        """Test the ability to retrieve an issue from a repository."""
        cassette_name = self.cassette_name('issue')
        with self.recorder.use_cassette(cassette_name):
            repository = self.gh.repository('sigmavirus24', 'github3.py')
            issue = repository.issue(525)
        assert isinstance(issue, github3.issues.issue.Issue)

    def test_issue_with_multiple_assignees(self):
        """Test the ability to retrieve an issue from a repository."""
        cassette_name = self.cassette_name('issue_multiple_assignees')
        with self.recorder.use_cassette(cassette_name):
            repository = self.gh.repository('sigmavirus24', 'github3.py')
            issue = repository.issue(637)
        assert isinstance(issue, github3.issues.issue.Issue)
        assert isinstance(issue.assignees, list)

    def test_imported_issue(self):
        """Test the ability to retrieve an imported issue by id."""
        self.token_login()
        cassette_name = self.cassette_name('imported_issue')
        with self.recorder.use_cassette(cassette_name):
            issue = {
                'title': 'foo',
                'body': 'bar',
                'created_at': '2014-03-16T17:15:42Z'
            }
            repository = self.gh.create_repository('testgh3py', 'test_import')
            imported_issue = repository.import_issue(**issue)
            imported_issue = repository.imported_issue(imported_issue.id)
            repository.delete()

        assert isinstance(imported_issue,
                          github3.repos.issue_import.ImportedIssue)

    def test_imported_issues(self):
        """Test the ability to retrieve imported issues."""
        self.token_login()
        cassette_name = self.cassette_name('imported_issues')
        with self.recorder.use_cassette(cassette_name):
            issues = [{
                'title': 'foo',
                'body': 'bar',
                'created_at': '2014-03-16T17:15:42Z',
                'comments': [{
                    'body': 'fake comments'
                }]
            }]
            repository = self.gh.create_repository('testgh3py', 'test_import')
            for issue in issues:
                repository.import_issue(**issue)
            imported_issues = list(repository.imported_issues())

        assert len(imported_issues) > 0
        for imported_issue in imported_issues:
            assert isinstance(imported_issue,
                              github3.repos.issue_import.ImportedIssue)

    def test_import_issue(self):
        """Test the ability to import an issue."""
        self.token_login()
        cassette_name = self.cassette_name('import_issue')
        with self.recorder.use_cassette(cassette_name):
            issue = {
                'title': 'foo',
                'body': 'bar',
                'created_at': '2014-03-16T17:15:42Z'
            }
            repository = self.gh.create_repository('testgh3py', 'test_import')
            imported_issue = repository.import_issue(**issue)
            repository.delete()

        assert isinstance(imported_issue,
                          github3.repos.issue_import.ImportedIssue)

    def test_import_issue_with_comments(self):
        """
        Test the ability to import an issue with comments on a repoitory.
        """
        self.token_login()
        cassette_name = self.cassette_name('import_issue_with_comments')
        with self.recorder.use_cassette(cassette_name):
            issue = {
                'title': 'foo',
                'body': 'bar',
                'created_at': '2014-03-16T17:15:42Z',
                'comments': [{
                    'body': 'fake comments'
                }]
            }
            repository = self.gh.create_repository(
                'testgh3py',
                'test_import_issue_with_comments',
            )
            imported_issue = repository.import_issue(**issue)
            repository.delete()

        assert isinstance(imported_issue,
                          github3.repos.issue_import.ImportedIssue)

    def test_issue_events(self):
        """Test that a user can iterate over issue events in a repo."""
        cassette_name = self.cassette_name('issue_events')
        with self.recorder.use_cassette(cassette_name):
            repository = self.gh.repository('sigmavirus24', 'github3.py')
            assert repository is not None
            events = list(repository.issue_events(number=50))

        for ev in events:
            assert isinstance(ev, github3.issues.event.RepositoryIssueEvent)

    def test_issues_sorts_ascendingly(self):
        """Test that issues will be returned in ascending order."""
        cassette_name = self.cassette_name('issues_ascending')
        with self.recorder.use_cassette(cassette_name):
            repository = self.gh.repository('sigmavirus24', 'betamax')
            assert repository is not None
            issues = list(repository.issues(direction='asc'))

        assert len(issues) > 0
        last_issue = None
        for issue in issues:
            assert isinstance(issue, github3.issues.ShortIssue)
            if last_issue:
                assert last_issue.number < issue.number
            last_issue = issue

    def test_issues_accepts_state_all(self):
        """Test that the state parameter accepts 'all'."""
        cassette_name = self.cassette_name('issues_state_all')
        with self.recorder.use_cassette(cassette_name):
            repository = self.gh.repository('sigmavirus24', 'betamax')
            assert repository is not None
            for issue in repository.issues(state='all'):
                assert issue.state in ('open', 'closed')

    def test_key(self):
        """Test the retrieval of a single key."""
        self.basic_login()
        cassette_name = self.cassette_name('key')
        with self.recorder.use_cassette(cassette_name):
            repository = self.gh.repository('github3py', 'fork_this')
            assert repository is not None
            key = ('ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDZn4/RGE9YQrfjq7wSr'
                   'YkdtKH3r1rEIkx/4Nv1AG/PqE4AWKSVzKkqhurnqKtctVCLtU9pNFIjl/'
                   'XvNluTW3zrfqKjgaDdiBtWwecWzSbQqugfzmwFqCE4smJkP8e7+e9Fd1k'
                   'GOGyqVJLBLfIUdEbHN3Ws40Z9OXgrJ/tiNdg1HHgAOjpknCMrQI8NDP9o'
                   '9CLuE/AfNVzRNOzpf/rrdZ4YW4kcDhbcQ8X7DGCnbvY9wUp3lDmSvVy6z'
                   'olYwLziYqsGjw0kLHvIzHdbGCjp+50iZSBrm29AlWa9eRsGskiUTIk6SA'
                   'Q8Fm5qKNkCtPYQ6YmjRiKyDtsMoqfjzDkyEPLv mattchung@Matts-Ma'
                   'cBook-Air.local')
            data = {
                'title': 'Deploy Key',
                'key': key
            }
            created_key = repository.create_key(**data)
            key = repository.key(created_key.id)
            key.delete()

        assert isinstance(key, github3.users.Key)

    def test_keys(self):
        """Test that the user can retrieve all deploy keys."""
        self.basic_login()
        cassette_name = self.cassette_name('keys')
        with self.recorder.use_cassette(cassette_name):
            repository = self.gh.repository('github3py', 'fork_this')
            assert repository is not None
            key = ('ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDZn4/RGE9YQrfjq7wSr'
                   'YkdtKH3r1rEIkx/4Nv1AG/PqE4AWKSVzKkqhurnqKtctVCLtU9pNFIjl/'
                   'XvNluTW3zrfqKjgaDdiBtWwecWzSbQqugfzmwFqCE4smJkP8e7+e9Fd1k'
                   'GOGyqVJLBLfIUdEbHN3Ws40Z9OXgrJ/tiNdg1HHgAOjpknCMrQI8NDP9o'
                   '9CLuE/AfNVzRNOzpf/rrdZ4YW4kcDhbcQ8X7DGCnbvY9wUp3lDmSvVy6z'
                   'olYwLziYqsGjw0kLHvIzHdbGCjp+50iZSBrm29AlWa9eRsGskiUTIk6SA'
                   'Q8Fm5qKNkCtPYQ6YmjRiKyDtsMoqfjzDkyEPLv mattchung@Matts-Ma'
                   'cBook-Air.local')
            data = {
                'title': 'Deploy Key',
                'key': key
            }
            created_key = repository.create_key(**data)
            keys = list(repository.keys())
            created_key.delete()

        assert len(keys) > 0
        for key in keys:
            assert isinstance(key, github3.users.Key)

    def test_label(self):
        """Test that a user can retrieve a repository's label."""
        cassette_name = self.cassette_name('label')
        with self.recorder.use_cassette(cassette_name):
            repository = self.gh.repository('sigmavirus24', 'github3.py')
            label = repository.label('bug')
        assert isinstance(label, github3.issues.label.Label)
        assert label.description is not None

    def test_labels(self):
        """Test that a user can retrieve a repository's labels."""
        cassette_name = self.cassette_name('labels')
        with self.recorder.use_cassette(cassette_name):
            repository = self.gh.repository('sigmavirus24', 'github3.py')
            assert repository is not None
            labels = list(repository.labels())

        assert len(labels) > 0
        for label in labels:
            assert isinstance(label, github3.issues.label.Label)

    def test_languages(self):
        """Test that a repository's languages can be retrieved."""
        cassette_name = self.cassette_name('languages')
        with self.recorder.use_cassette(cassette_name):
            repository = self.gh.repository('sigmavirus24', 'github3.py')
            assert repository is not None
            for l in repository.languages():
                assert 'ETag' not in l
                assert 'Last-Modified' not in l
                assert isinstance(l, tuple)

    def test_license(self):
        """Test that a repository's license can be retrieved."""
        cassette_name = self.cassette_name('license')
        with self.recorder.use_cassette(cassette_name):
            repository = self.gh.repository('github3py', 'github3.py')
            license = repository.license()
            assert isinstance(license, github3.licenses.RepositoryLicense)

    def test_mark_notifications(self):
        """Verify we can mark all notifications on a repository as read."""
        self.token_login()
        cassette_name = self.cassette_name('mark_notifications')
        with self.recorder.use_cassette(cassette_name):
            repository = self.gh.repository('github3py', 'github3.py')
            marked = repository.mark_notifications('2016-01-12T00:00:00Z')
        assert marked is True

    def test_merge(self):
        """Test the ability to perform a merge on a repository."""
        self.token_login()
        cassette_name = self.cassette_name('merge')
        with self.recorder.use_cassette(cassette_name):
            repository = self.gh.repository('github3py', 'fork_this')
            commit = repository.merge('master', 'new-branch')
        assert isinstance(commit, github3.repos.commit.ShortCommit)

    def test_milestone(self):
        """Test the ability to retrieve a milestone on a repository."""
        cassette_name = self.cassette_name('milestone')
        with self.recorder.use_cassette(cassette_name):
            repository = self.gh.repository('sigmavirus24', 'github3.py')
            assert repository is not None
            milestone = repository.milestone(7)
        assert isinstance(milestone, github3.issues.milestone.Milestone)

    def test_milestones(self):
        """Test the ability to retrieve the milestones in a repository."""
        cassette_name = self.cassette_name('milestones')
        with self.recorder.use_cassette(cassette_name):
            repository = self.gh.repository('sigmavirus24', 'github3.py')
            assert repository is not None
            milestones = list(repository.milestones())

        assert len(milestones) > 0
        for milestone in milestones:
            assert isinstance(milestone, github3.issues.milestone.Milestone)

    def test_network_events(self):
        """Test that a user can retrieve the events of a repo's network."""
        cassette_name = self.cassette_name('network_events')
        with self.recorder.use_cassette(cassette_name):
            repository = self.gh.repository('sigmavirus24', 'github3.py')
            assert repository is not None
            events = list(repository.network_events())

        assert len(events) > 0
        for event in events:
            assert isinstance(event, github3.events.Event)

    def test_notifications(self):
        """Test that a user can retrieve their repo notifications."""
        self.basic_login()
        cassette_name = self.cassette_name('notifications')
        with self.recorder.use_cassette(cassette_name):
            repository = self.gh.repository('github3py', 'fork_this')
            assert repository is not None
            notifications = list(repository.notifications())

        assert len(notifications) > 0
        for notification in notifications:
            assert isinstance(notification, github3.notifications.Thread)

    def test_original_license(self):
        """Test that a repository's license is present initially."""
        cassette_name = self.cassette_name('original_license')
        with self.recorder.use_cassette(cassette_name):
            repository = self.gh.repository('github3py', 'github3.py')
            assert repository is not None
            assert isinstance(repository.original_license,
                              github3.licenses.ShortLicense)

    def test_pull_request(self):
        """Test that a user can retrieve a pull request from a repo."""
        cassette_name = self.cassette_name('pull_request')
        with self.recorder.use_cassette(cassette_name):
            repository = self.gh.repository('sigmavirus24', 'github3.py')
            pull_request = repository.pull_request(546)

        assert isinstance(pull_request, github3.pulls.PullRequest)

    def test_pull_requests(self):
        """Test that a user can retrieve the pull requests from a repo."""
        cassette_name = self.cassette_name('pull_requests')
        with self.recorder.use_cassette(cassette_name):
            repository = self.gh.repository('sigmavirus24', 'github3.py')
            assert repository is not None
            pulls = list(repository.pull_requests())

        assert len(pulls) > 0
        for pull in pulls:
            assert isinstance(pull, github3.pulls.ShortPullRequest)

    def test_pull_requests_accepts_sort_and_direction(self):
        """Test that pull_requests now takes a sort parameter."""
        cassette_name = self.cassette_name('pull_requests_accept_sort')
        with self.recorder.use_cassette(cassette_name):
            repository = self.gh.repository('sigmavirus24', 'betamax')
            assert repository is not None
            last_pr = None
            for pr in repository.pull_requests(sort='updated',
                                               direction='asc'):
                assert pr is not None
                if last_pr:
                    assert last_pr.updated_at < pr.updated_at
                last_pr = pr

    def test_readme(self):
        """Test the ability to retrieve the README."""
        cassette_name = self.cassette_name('readme')
        with self.recorder.use_cassette(cassette_name):
            repository = self.gh.repository('sigmavirus24', 'github3.py')
            readme = repository.readme()

        assert isinstance(readme, github3.repos.contents.Contents)

    def test_ref(self):
        """Test the ability to retrieve a ref."""
        cassette_name = self.cassette_name('ref')
        with self.recorder.use_cassette(cassette_name):
            repository = self.gh.repository('sigmavirus24', 'github3.py')
            ref = repository.ref('tags/0.9.3')

        assert isinstance(ref, github3.git.Reference)

    def test_release(self):
        """Test the ability to retrieve a single release."""
        cassette_name = self.cassette_name('release')
        with self.recorder.use_cassette(cassette_name):
            repository = self.gh.repository('sigmavirus24', 'github3.py')
            assert repository is not None
            release = repository.release(76677)

        assert isinstance(release, github3.repos.release.Release)

    def test_latest_release(self):
        """Test the ability to retrieve the latest release."""
        cassette_name = self.cassette_name('latest_release')
        with self.recorder.use_cassette(cassette_name):
            repository = self.gh.repository('sigmavirus24', 'github3.py')
            assert repository is not None
            release = repository.latest_release()

        assert isinstance(release, github3.repos.release.Release)

    def test_release_from_tag(self):
        """Test the ability to retrieve a release by tag name."""
        cassette_name = self.cassette_name('release_from_tag')
        with self.recorder.use_cassette(cassette_name):
            repository = self.gh.repository('sigmavirus24', 'github3.py')
            assert repository is not None
            release = repository.release_from_tag('v0.7.1')

        assert isinstance(release, github3.repos.release.Release)

    def test_releases(self):
        """Test the ability to iterate over releases on a repository."""
        cassette_name = self.cassette_name('releases')
        with self.recorder.use_cassette(cassette_name):
            repository = self.gh.repository('sigmavirus24', 'github3.py')
            assert repository is not None
            for release in repository.releases():
                assert isinstance(release, github3.repos.release.Release)

    def test_refs(self):
        """Test the ability to retrieve the references from a repository."""
        self.token_login()
        cassette_name = self.cassette_name('refs')
        with self.recorder.use_cassette(cassette_name):
            repository = self.gh.repository('sigmavirus24', 'github3.py')
            assert repository is not None
            references = list(repository.refs())

        assert len(references) > 0
        for ref in references:
            assert isinstance(ref, github3.git.Reference)

    def test_refs_raises_unprocessable_exception(self):
        """Verify github3.exceptions.UnprocessableResponseBody is raised."""
        cassette_name = self.cassette_name('invalid_refs')
        with self.recorder.use_cassette(cassette_name):
            repository = self.gh.repository('sigmavirus24', 'github3.py')
            assert repository is not None
            with pytest.raises(exc.UnprocessableResponseBody):
                list(repository.refs('heads/develop'))

    def test_remove_collaborator(self):
        """Test the ability to remove a collaborator on a repository."""
        self.token_login()
        cassette_name = self.cassette_name('remove_collaborator')
        with self.recorder.use_cassette(cassette_name):
            repository = self.gh.repository('github3py', 'test_rename1')
            removed_collaborator = repository.remove_collaborator('littleboyd')

        assert removed_collaborator is True

    def test_replace_topics(self):
        """Test the ability to replace the topics of a repository."""
        self.token_login()
        cassette_name = self.cassette_name('replace_topics')
        with self.recorder.use_cassette(cassette_name):
            repository = self.gh.repository('jacquerie', 'flask-shell-bpython')
            topics = repository.replace_topics(['flask', 'bpython', 'python'])

        assert isinstance(topics, github3.repos.topics.Topics)
        assert len(topics.names) == 3

    def test_stargazers(self):
        """Test the ability to retrieve the stargazers on a repository."""
        cassette_name = self.cassette_name('stargazers')
        with self.recorder.use_cassette(cassette_name):
            repository = self.gh.repository('sigmavirus24', 'betamax')
            assert repository is not None
            stargazers = list(repository.stargazers())

        assert len(stargazers) > 0
        for user in stargazers:
            assert isinstance(user, github3.users.ShortUser)

    def test_statuses(self):
        """Test the ability to retrieve a commit's statuses."""
        cassette_name = self.cassette_name('statuses')
        with self.recorder.use_cassette(cassette_name):
            repository = self.gh.repository('pycqa', 'flake8')
            assert repository is not None
            statuses = list(repository.statuses(
                'f8344997267b8ca87a96c690a3515a443005b653'
            ))

        assert len(statuses) > 0
        for status in statuses:
            assert isinstance(status, github3.repos.status.Status)

    def test_subscribers(self):
        """Test the ability to retrieve a repository's subscribers."""
        cassette_name = self.cassette_name('subscribers')
        with self.recorder.use_cassette(cassette_name):
            repository = self.gh.repository('sigmavirus24', 'betamax')
            assert repository is not None
            subscribers = list(repository.subscribers())

        assert len(subscribers) > 0
        for user in subscribers:
            assert isinstance(user, github3.users.ShortUser)

    def test_subscribe(self):
        """Test the ability to subscribe to a repository's notifications."""
        self.basic_login()
        cassette_name = self.cassette_name('subscribe')
        with self.recorder.use_cassette(cassette_name):
            repository = self.gh.repository('vcr', 'vcr')
            assert repository is not None
            subscription = repository.subscribe()
            assert subscription.subscribed is True

    def test_subscription(self):
        """Test the ability to retreive a repository's subscription."""
        self.token_login()
        cassette_name = self.cassette_name('subscription')
        with self.recorder.use_cassette(cassette_name):
            repository = self.gh.repository('sigmavirus24', 'github3.py')
            assert repository is not None
            repository.subscribe()
            subscription = repository.subscription()
            repository.delete_subscription()

        assert isinstance(subscription,
                          github3.notifications.RepositorySubscription)

    def test_tag(self):
        """Test the ability to retrieve an annotated tag."""
        cassette_name = self.cassette_name('tag')
        with self.recorder.use_cassette(cassette_name):
            repository = self.gh.repository('sigmavirus24', 'github3.py')
            tag = repository.tag('bf1eca5702d6408ab8dbf395c49c2c903a116d33')

        assert isinstance(tag, github3.git.Tag)

    def test_tags(self):
        """Test the ability to retrieve a repository's tags."""
        cassette_name = self.cassette_name('tags')
        with self.recorder.use_cassette(cassette_name):
            repository = self.gh.repository('sigmavirus24', 'betamax')
            assert repository is not None
            tags = list(repository.tags())

        assert len(tags) > 0
        for tag in tags:
            assert isinstance(tag, github3.repos.tag.RepoTag)

    def test_teams(self):
        """Test the ability to retrieve teams assigned to a repo."""
        self.basic_login()
        cassette_name = self.cassette_name('teams')
        with self.recorder.use_cassette(cassette_name):
            repository = self.gh.repository('github3py', 'fork_this')
            assert repository is not None
            teams = list(repository.teams())

        assert len(teams) > 0
        for team in teams:
            assert isinstance(team, github3.orgs.ShortTeam)

    def test_topics(self):
        """Test the ability to retrieve topics from a repository."""
        cassette_name = self.cassette_name('topics')
        with self.recorder.use_cassette(cassette_name):
            repository = self.gh.repository('jacquerie', 'flask-shell-bpython')
            topics = repository.topics()

        assert isinstance(topics, github3.repos.topics.Topics)
        assert len(topics.names) == 3

    def test_tree(self):
        """Test the ability to retrieve a tree from a repository."""
        cassette_name = self.cassette_name('tree')
        with self.recorder.use_cassette(cassette_name):
            repository = self.gh.repository('sigmavirus24', 'github3.py')
            tree = repository.tree('52a3f30e05cf434285e775979f01f1a8355049a7')

        assert isinstance(tree, github3.git.Tree)
        assert len(tree.tree) == 18

    def test_tree_recursive(self):
        """Test the ability to retrieve a tree recursively."""
        cassette_name = self.cassette_name('tree_recursive')
        with self.recorder.use_cassette(cassette_name):
            repository = self.gh.repository('sigmavirus24', 'github3.py')
            tree = repository.tree(
                '52a3f30e05cf434285e775979f01f1a8355049a7', recursive=True)

        assert isinstance(tree, github3.git.Tree)
        assert len(tree.tree) == 275

    def test_weekly_commit_count(self):
        """
        Test the ability to retrieve the weekly commit count on a
        repository.
        """
        cassette_name = self.cassette_name('weekly_commit_count')
        with self.recorder.use_cassette(cassette_name):
            repository = self.gh.repository('sigmavirus24', 'github3.py')
            weekly_commit_count = repository.weekly_commit_count()

        assert isinstance(weekly_commit_count, dict)
        assert len(weekly_commit_count.get('owner')) == 52
        assert len(weekly_commit_count.get('all')) == 52


class TestContents(helper.IntegrationHelper):

    """Integration test for Contents object."""

    def test_delete(self):
        """Test the ability to delete content from a repository."""
        self.token_login()
        cassette_name = self.cassette_name('delete')
        with self.recorder.use_cassette(cassette_name):
            repository = self.gh.repository('github3py', 'delete_contents')
            repository.create_file('test.txt', 'Create test.txt', b'testing')
            content = repository.file_contents('test.txt')
            deleted = content.delete('Deleting test.txt from repository')

        assert deleted

    def test_update(self):
        """Test the ability to update a file's content from a repository."""
        self.token_login()
        cassette_name = self.cassette_name('update')
        with self.recorder.use_cassette(cassette_name):
            repository = self.gh.repository('github3py', 'delete_contents')
            repository.create_file('test.txt', 'Create test.txt', b'testing')
            content = repository.file_contents('test.txt')
            update = content.update(message='Updating test.txt',
                                    content=b'HELLO')
            assert isinstance(update, dict)
            assert isinstance(update['content'],
                              github3.repos.contents.Contents)
            assert isinstance(update['commit'], github3.git.Commit)

            # Clean-up
            update['content'].delete('Deleting test.txt from repository')


class TestHook(helper.IntegrationHelper):

    """Integration tests for Hook object."""

    def test_delete(self):
        self.token_login()
        cassette_name = self.cassette_name('delete')
        with self.recorder.use_cassette(cassette_name):
            repository = self.gh.repository('github3py', 'delete_contents')
            hook = repository.create_hook('web', config={
                'url': 'https://httpbin.org/post',
                'content_type': 'json',
            })
            deleted = hook.delete()

        assert deleted is True

    def test_edit(self):
        """Test the ability to edit a hook on a repository."""
        self.token_login()
        cassette_name = self.cassette_name('edit')
        with self.recorder.use_cassette(cassette_name):
            repository = self.gh.repository('github3py', 'delete_contents')
            hook = repository.create_hook('web', config={
                'url': 'https://httpbin.org/post',
                'content_type': 'json',
            })
            data = {
                'config': {
                    'url': 'https://requestb.in/15u72q01',
                    'content_type': 'json'
                },
                'events': ['pull_request'],
            }
            edited = hook.edit(**data)
            hook.delete()

        assert edited

    def test_ping(self):
        """Test the ability to ping a hook on a repository."""
        self.token_login()
        cassette_name = self.cassette_name('ping')
        with self.recorder.use_cassette(cassette_name):
            repository = self.gh.repository('github3py', 'delete_contents')
            hook = repository.create_hook('web', config={
                'url': 'https://httpbin.org/post',
                'content_type': 'json',
            })
            pinged = hook.ping()
            hook.delete()

        assert pinged

    def test_test(self):
        """Test the ability to test a hook on a repository."""
        self.token_login()
        cassette_name = self.cassette_name('test')
        with self.recorder.use_cassette(cassette_name):
            repository = self.gh.repository('github3py', 'delete_contents')
            hook = repository.create_hook('web', config={
                'url': 'https://httpbin.org/post',
                'content_type': 'json',
            })
            tested = hook.test()
            hook.delete()

        assert tested


class TestRepoComment(helper.IntegrationHelper):

    """Integration tests for RepoComment object."""

    def test_delete(self):
        """Test the ability to delete a repository comment."""
        self.token_login()
        cassette_name = self.cassette_name('delete')
        with self.recorder.use_cassette(cassette_name):
            repository = self.gh.repository('github3py', 'delete_contents')
            commit_comment = repository.create_comment(
                'Goodbye',
                '5bcffc5f7dacbbf2706fad0d8dfb74f109bd6a68',
            )
            comment = repository.commit_comment(commit_comment.id)
            deleted = comment.delete()

        assert deleted

    def test_edit(self):
        """Test the ability to update a repository comment."""
        self.token_login()
        cassette_name = self.cassette_name('edit')
        with self.recorder.use_cassette(cassette_name):
            repository = self.gh.repository('github3py', 'delete_contents')
            comment = repository.create_comment(
                'Goodbye',
                '5bcffc5f7dacbbf2706fad0d8dfb74f109bd6a68',
            )
            updated = comment.edit(body='Updated by integration test')
            comment.delete()

        assert updated


class TestRepoCommit(helper.IntegrationHelper):

    """Integration tests for RepoCommit object."""

    def test_diff(self):
        """Test the ability to retrieve a diff for a commit."""
        cassette_name = self.cassette_name('diff')
        with self.recorder.use_cassette(cassette_name):
            repository = self.gh.repository('sigmavirus24', 'github3.py')
            commit = repository.commit(
                '51cfbf8cbf98b0ba5006b3490f553bc05d4461e4'
            )
            diff = commit.diff()

        assert diff

    def test_patch(self):
        """Test the ability to retrieve a patch for a commit."""
        cassette_name = self.cassette_name('patch')
        with self.recorder.use_cassette(cassette_name):
            repository = self.gh.repository('sigmavirus24', 'github3.py')
            commit = repository.commit(
                '51cfbf8cbf98b0ba5006b3490f553bc05d4461e4'
            )
            patch = commit.patch()

        assert patch


class TestComparison(helper.IntegrationHelper):

    """Integration test for Comparison object."""

    def test_diff(self):
        """Test the ability to retrieve a diff for a comparison."""
        cassette_name = self.cassette_name('diff')
        with self.recorder.use_cassette(cassette_name):
            repository = self.gh.repository('sigmavirus24', 'github3.py')
            comparison = repository.compare_commits(base='master',
                                                    head='develop')
            diff = comparison.diff()

        assert diff

    def test_patch(self):
        """Test the ability to retrieve a diff for a comparison."""
        cassette_name = self.cassette_name('patch')
        with self.recorder.use_cassette(cassette_name):
            repository = self.gh.repository('sigmavirus24', 'github3.py')
            comparison = repository.compare_commits(base='master',
                                                    head='develop')
            patch = comparison.patch()

        assert patch
