import base
import github3
from base import expect
from datetime import datetime
from os import unlink
from github3.repos import (Repository, Branch, RepoCommit, RepoComment,
        Comparison, Contents, Download, Hook, RepoTag)
from github3.users import User, Key
from github3.git import Commit, Reference
from github3.issues import (Issue, Label, Milestone)
from github3.events import Event
from github3.pulls import PullRequest


class TestRepository(base.BaseTest):
    def setUp(self):
        super(TestRepository, self).setUp()
        self.repo = self.g.repository(self.sigm, self.todo)

    def test_repository(self):
        expect(self.repo).isinstance(Repository)

    def test_attributess(self):
        repo = self.repo
        expect(repo.clone_url).is_not_None()
        expect(repo.created_at).isinstance(datetime)
        expect(repo.forks) > 0
        expect(repo.is_collaborator(self.sigm)).is_True()
        expect(repo.git_clone) != ''
        expect(repo.homepage) != ''
        expect(repo.owner).isinstance(User)
        expect(repo.html_url) != ''
        expect(repo.id) > 0
        expect(repo.language) != ''

    def test_methods(self):
        repo = self.repo
        expect(repo.archive('tarball', 'archive.tar.gz')).is_True()
        unlink('archive.tar.gz')

        #blob = repo.blob("sha"")
        master = repo.branch('master')
        expect(master).isinstance(Branch)

        commit = repo.commit('04d55444a3ec06ca8d2aa0a5e333cdaf27113254')
        expect(commit).isinstance(RepoCommit)

        comment = repo.commit_comment('766400')
        expect(comment).isinstance(RepoComment)

        comp = repo.compare_commits(
                '04d55444a3ec06ca8d2aa0a5e333cdaf27113254',
                '731691616b71258c7ad7c141379856b5ebbab310')
        expect(comp).isinstance(Comparison)

        contents = repo.contents('todo.py')
        expect(contents).isinstance(Contents)

        download = repo.download(248618)
        expect(download).isinstance(Download)

        commit = repo.git_commit('04d55444a3ec06ca8d2aa0a5e333cdaf27113254')
        expect(commit).isinstance(Commit)

        expect(repo.is_fork()).is_False()
        expect(repo.is_private()).is_False()
        expect(repo.has_downloads()).is_True()
        expect(repo.has_wiki()).is_True()

        expect(repo.is_assignee(self.sigm)).is_True()
        expect(repo.issue(1)).isinstance(Issue)
        expect(repo.label('Bug')).isinstance(Label)
        expect(repo.milestone(1)).isinstance(Milestone)

        self.expect_list_of_class(repo.list_assignees(), User)
        self.expect_list_of_class(repo.list_branches(), Branch)
        self.expect_list_of_class(repo.list_comments(), RepoComment)
        comments = repo.list_comments_on_commit(
                '38c76375ae1a766b44c729b4b2ff0363312b6d13')
        self.expect_list_of_class(comments, RepoComment)
        self.expect_list_of_class(repo.list_commits(), RepoCommit)
        self.expect_list_of_class(repo.list_downloads(), Download)
        self.expect_list_of_class(repo.list_events(), Event)
        self.expect_list_of_class(repo.list_forks(), Repository)
        self.expect_list_of_class(repo.list_issues(), Issue)
        self.expect_list_of_class(repo.list_issue_events(), Event)
        self.expect_list_of_class(repo.list_milestones(), Milestone)
        self.expect_list_of_class(repo.list_network_events(), Event)
        self.expect_list_of_class(repo.list_pulls(state='closed'),
                PullRequest)
        self.expect_list_of_class(repo.list_refs(), Reference)
        self.expect_list_of_class(repo.list_tags(), RepoTag)
        self.expect_list_of_class(repo.list_watchers(), User)
        # XXX: next up list_hooks() -> requires_auth

    def test_requires_auth(self):
        repo = self.repo
        with expect.raises(github3.GitHubError):
            # It's going to fail anyway by default so the username is
            # unimportant
            repo.add_collaborator(self.sigm)
            repo.create_blob('Foo bar bogus', 'utf-8')
            repo.create_comment('Foo bar bogus',
                    'e8b7f5ad567faae369460f186ee0d82c90ccfbd1',
                    'todo.py', 5, 10)
            #repo.create_commit
            repo.create_download('file_to_download', '/tmp/foo')
            repo.create_fork(self.gh3py)
            repo.create_hook('Hook', {'foo': 'bar'})
            repo.create_issue('New issue')
            repo.create_key('Key', 'foobarbogus')
            repo.create_label('Foo bar', 'abc123')
            repo.create_milestone('milestone')
            repo.create_pull('PR',
                    '04d55444a3ec06ca8d2aa0a5e333cdaf27113254',
                    '731691616b71258c7ad7c141379856b5ebbab310')
            repo.create_tag('fake_tag', 'fake tag message',
                    '731691616b71258c7ad7c141379856b5ebbab310', 'commit',
                    {'name': 'Ian Cordasco',
                     'email': 'graffatcolmingov@gmail.com'})
            repo.create_tree({'path': 'tests/test_fake.py',
                'mode': '100644', 'type': 'blob',
                'sha': '731691616b71258c7ad7c141379856b5ebbab310'})
            repo.delete()
            repo.edit('todo.py', '#', 'http://git.io/todo.py')
            repo.hook(74859)
            repo.key(1234)
            repo.list_keys()
            repo.list_teams()

        if self.auth:
            repo = self._g.repository(self.sigm, self.todo)
            # Try somethings only I can test
            try:
                expect(repo.hook(74859)).isinstance(Hook)
                expect(repo.key(3069618)).isinstance(Key)
            except github3.GitHubError:
                pass
