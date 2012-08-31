import base
import github3
from base import expect
from datetime import datetime
from os import unlink
from github3.repos import (Repository, Branch, RepoCommit, RepoComment,
        Comparison, Contents, Download, Hook, RepoTag)
from github3.users import User, Key
from github3.git import Commit, Reference, Tag, Tree, Blob
from github3.issues import (Issue, IssueEvent, Label, Milestone)
from github3.events import Event
from github3.pulls import PullRequest


class TestRepository(base.BaseTest):
    def __init__(self, methodName='runTest'):
        super(TestRepository, self).__init__(methodName)
        self.repo = self.g.repository(self.sigm, self.todo)

    def test_repository(self):
        expect(self.repo).isinstance(Repository)

    def test_clone_url(self):
        expect(self.repo.clone_url).is_not_None()

    def test_created_at(self):
        expect(self.repo.created_at).isinstance(datetime)

    def test_forks(self):
        expect(self.repo.forks) > 0

    def test_is_collaborator(self):
        expect(self.repo.is_collaborator(self.sigm)).is_True()

    def test_git_clone(self):
        expect(self.repo.git_clone) != ''

    def test_homepage(self):
        expect(self.repo.homepage) != ''

    def test_html_url(self):
        expect(self.repo.html_url) != ''

    def test_id(self):
        expect(self.repo.id) > 0

    def test_language(self):
        expect(self.repo.language) != ''

    def test_mirror_url(self):
        expect(self.repo.mirror_url) != ''

    def test_name(self):
        expect(self.repo.name) == self.todo

    def test_open_issues(self):
        expect(self.repo.open_issues) >= 0

    def test_owner(self):
        expect(self.repo.owner).isinstance(User)

    def test_pushed_at(self):
        expect(self.repo.pushed_at).isinstance(datetime)

    def test_size(self):
        expect(self.repo.size) >= 0

    def test_ssh_url(self):
        expect(self.repo.ssh_url) != ''

    def test_svn_url(self):
        expect(self.repo.svn_url) != ''

    def test_updated_at(self):
        expect(self.repo.updated_at).isinstance(datetime)

    def test_watchers(self):
        expect(self.repo.watchers) >= 1

    # Methods
    def test_archive(self):
        expect(self.repo.archive('tarball', 'archive.tar.gz')).is_True()
        unlink('archive.tar.gz')

        #blob = repo.blob("sha"")
    def test_blob(self):
        expect(self.repo.blob(
            '2494c145b614f8c945d67cb456536f8b1903e672'
            )).isinstance(Blob)

    def test_branch(self):
        master = self.repo.branch('master')
        expect(master).isinstance(Branch)

    def test_commit(self):
        commit = self.repo.commit('04d55444a3ec06ca8d2aa0a5e333cdaf27113254')
        expect(commit).isinstance(RepoCommit)

    def test_commit_comment(self):
        comment = self.repo.commit_comment('766400')
        expect(comment).isinstance(RepoComment)

    def test_compare_commits(self):
        comp = self.repo.compare_commits(
                '04d55444a3ec06ca8d2aa0a5e333cdaf27113254',
                '731691616b71258c7ad7c141379856b5ebbab310')
        expect(comp).isinstance(Comparison)

    def test_contents(self):
        contents = self.repo.contents('todo.py')
        expect(contents).isinstance(Contents)

    def test_download(self):
        download = self.repo.download(248618)
        expect(download).isinstance(Download)

    def test_git_commit(self):
        sha = '04d55444a3ec06ca8d2aa0a5e333cdaf27113254'
        commit = self.repo.git_commit(sha)
        expect(commit).isinstance(Commit)
        expect(commit.sha) == sha

    def test_is_fork(self):
        expect(self.repo.is_fork()).is_False()

    def test_is_private(self):
        expect(self.repo.is_private()).is_False()

    def test_has_downloads(self):
        expect(self.repo.has_downloads()).is_True()

    def test_has_wiki(self):
        expect(self.repo.has_wiki()).is_True()

    def test_is_assignee(self):
        expect(self.repo.is_assignee(self.sigm)).is_True()

    def test_issue(self):
        issue = self.repo.issue(1)
        expect(issue).isinstance(Issue)
        expect(issue.title) == 'Change get_todos()?'

    def test_label(self):
        expect(self.repo.label('Bug')).isinstance(Label)

    def test_list_assignees(self):
        assignees = self.repo.list_assignees()
        self.expect_list_of_class(assignees, User)
        for a in assignees:
            if a.login == 'sigmavirus24':
                return
        self.fail('No user with login sigmavirus24')

    def test_list_branches(self):
        branches = self.repo.list_branches()
        self.expect_list_of_class(branches, Branch)
        for b in branches:
            if b.name == 'master':
                return
        self.fail('No branch named master')

    def test_list_comments(self):
        comments = self.repo.list_comments()
        self.expect_list_of_class(comments, RepoComment)
        for c in comments:
            if c.user.login in ('sigmavirus24', 'jvstein'):
                return
        self.fail('No commenter with login sigmavirus24 or jvstein')

    def test_list_comments_on_commit(self):
        comments = self.repo.list_comments_on_commit(
                '38c76375ae1a766b44c729b4b2ff0363312b6d13')
        self.expect_list_of_class(comments, RepoComment)
        for c in comments:
            if c.user.login in ('sigmavirus24', 'jvstein'):
                return
        self.fail('No commenter with login sigmavirus24 or jvstein')

    def test_list_commits(self):
        self.expect_list_of_class(self.repo.list_commits(), RepoCommit)

    def test_list_downloads(self):
        downloads = self.repo.list_downloads()
        self.expect_list_of_class(downloads, Download)
        for d in downloads:
            if d.name == 'todo.txt-python-0.3.zip':
                return
        self.fail('No download with name todo.txt-python-0.3.zip')

    def test_list_events(self):
        self.expect_list_of_class(self.repo.list_events(), Event)

    def test_list_forks(self):
        self.expect_list_of_class(self.repo.list_forks(), Repository)

    def test_list_issues(self):
        self.expect_list_of_class(self.repo.list_issues(), Issue)

    def test_list_issue_events(self):
        self.expect_list_of_class(self.repo.list_issue_events(), IssueEvent)

    def test_list_milestones(self):
        self.expect_list_of_class(self.repo.list_milestones(), Milestone)

    def test_list_network_events(self):
        self.expect_list_of_class(self.repo.list_network_events(), Event)

    def test_list_pulls(self):
        self.expect_list_of_class(self.repo.list_pulls(state='closed'),
                PullRequest)

    def test_list_refs(self):
        self.expect_list_of_class(self.repo.list_refs(), Reference)

    def test_list_tags(self):
        self.expect_list_of_class(self.repo.list_tags(), RepoTag)

    def test_list_watchers(self):
        self.expect_list_of_class(self.repo.list_watchers(), User)

    def test_milestone(self):
        expect(self.repo.milestone(1)).isinstance(Milestone)

    def test_pull_request(self):
        expect(self.repo.pull_request(2)).isinstance(PullRequest)

    def test_readme(self):
        expect(self.repo.readme()).isinstance(Contents)

    def test_ref(self):
        expect(self.repo.ref('tags/0.3')).isinstance(Reference)

    def test_tag(self):
        expect(self.repo.tag(
            '21501fd1630546af3ee4bc58ddef6604f6983607'
            )).isinstance(Tag)

    def test_tree(self):
        expect(self.repo.tree(
            '239bdbfa86adec94c0d13fb039796da3efe7c7db'
            )).isinstance(Tree)

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
            repo.pubsubhubub(
                    'subscribe',
                    'https://github.com/user/repo/events/push',
                    'https://httpbin.org/post'
                    )
            repo.remove_collaborator('foobarbogus')
            repo.update_label('Foo', 'abc123')
            repo.merge('development', 'master', 'Fails')

    def test_with_auth(self):
        if self.auth:
            repo = self._g.repository(self.sigm, self.todo)
            # Try somethings only I can test
            try:
                expect(repo.hook(74859)).isinstance(Hook)
            except github3.GitHubError:
                pass
            try:
                expect(repo.key(3069618)).isinstance(Key)
            except github3.GitHubError:
                pass
            try:
                expect(repo.pubsubhubbub(
                    'subscribe',
                    'https://github.com/sigmavirus24/github3.py/events',
                    'https://httpbin.org/post'
                    )).is_False()
            except github3.GitHubError:
                pass
            try:
                expect(repo.add_collaborator('jcordasc')).is_True()
            except github3.GitHubError:
                pass
            try:
                expect(repo.remove_collaborator('jcordasc')).is_True()
            except github3.GitHubError:
                pass


class TestBranch(base.BaseTest):
    def __init__(self, methodName='runTest'):
        super(TestBranch, self).__init__(methodName)
        repo = self.g.repository(self.sigm, self.todo)
        self.branch = repo.branch('master')

    def test_commit(self):
        expect(self.branch.commit).isinstance(Commit)

    def test_links(self):
        expect(self.branch.links).isinstance(dict)

    def test_name(self):
        expect(self.branch.name) == 'master'


class TestContents(base.BaseTest):
    def __init__(self, methodName='runTest'):
        super(TestContents, self).__init__(methodName)
        repo = self.g.repository(self.sigm, self.todo)
        self.contents = repo.contents('todo.py')

    def _test_str_(self, val):
        expect(val).is_not_None()
        expect(val) > ''
        expect(val).isinstance(base.str_test)

    def test_content(self):
        expect(len(self.contents.content)) > 0
        self._test_str_(self.contents.content)

    def test_decoded(self):
        expect(len(self.contents.decoded)) > 0
        self._test_str_(self.contents.content)

    def test_encoding(self):
        self._test_str_(self.contents.encoding)

    def test_git(self):
        self._test_str_(self.contents.git)

    def test_html(self):
        self._test_str_(self.contents.html)

    def test_name(self):
        self._test_str_(self.contents.name)

    def test_path(self):
        self._test_str_(self.contents.path)

    def test_sha(self):
        self._test_str_(self.contents.sha)

    def test_size(self):
        expect(self.contents.size) > 0

    def test_type(self):
        expect(self.contents.type) == 'file'


class TestDownload(base.BaseTest):
    def __init__(self, methodName='runTest'):
        super(TestDownload, self).__init__(methodName)
        repo = self.g.repository(self.sigm, self.todo)
        self.dl = repo.download(248618)

    def test_content_type(self):
        expect(self.dl.content_type) == 'application/zip'

    def test_description(self):
        expect(self.dl.description) == ('zip of the essential files for ' +
            'version 0.3')

    def test_download_count(self):
        expect(self.dl.download_count) > 0

    def test_html_url(self):
        assert self.dl.html_url.startswith(
                'https://github.com/downloads/sigmavirus24/Todo'), (
                        'Download HTML URL is invalid'
                        )

    def test_id(self):
        expect(self.dl.id) == 248618

    def test_name(self):
        expect(self.dl.name) == 'todo.txt-python-0.3.zip'

    def test_size(self):
        expect(self.dl.size) == 26624

    def test_requires_auth(self):
        with expect.raises(github3.GitHubError):
            self.dl.delete()


class TestHook(base.BaseTest):
    def __init__(self, methodName='runTest'):
        super(TestHook, self).__init__(methodName)
        if self.auth:
            repo = self._g.repository(self.sigm, self.todo)
            self.hook = repo.hook(74859)
        else:
            json = {
                'name': 'twitter',
                'url':
                'https://api.github.com/repos/sigmavirus24/Todo.txt-python/' +
                'hooks/74859',
                'created_at': '2011-09-05T18:19:50Z',
                'updated_at': '2012-03-08T17:03:25Z',
                'id': 74859,
                'active': False,
                'config': {'token': 'fake_token', 'secret': 'fake_secret'},
                'events': ['push'],
                'last_response': {'status': 'ok', 'message': '', 'code': 200}
                }
            self.hook = Hook(json)

    def test_config(self):
        expect(self.hook.config).isinstance(dict)
        assert 'token' in self.hook.config, (
                'token not in config')
        assert 'secret' in self.hook.config, (
                'secret not in config')

    def test_created_at(self):
        expect(self.hook.created_at).isinstance(datetime)

    def test_events(self):
        self.expect_list_of_class(self.hook.events, base.str_test)

    def test_id(self):
        expect(self.hook.id) == 74859

    def test_is_active(self):
        expect(self.hook.is_active()).is_False()

    def test_name(self):
        expect(self.hook.name) == 'twitter'

    def test_updated_at(self):
        expect(self.hook.updated_at).isinstance(datetime)

    def test_requires_auth(self):
        if self.auth:
            return
        with expect.raises(github3.GitHubError):
            self.hook.edit('tweeter', self.hook.config)
            self.hook.delete()
            self.hook.test()


class TestRepoTag(base.BaseTest):
    def __init__(self, methodName='runTest'):
        super(TestRepoTag, self).__init__(methodName)
        repo = self.g.repository(self.sigm, self.todo)
        self.tag = repo.list_tags()[0]

    def test_commit(self):
        expect(self.tag.commit).isinstance(dict)

    def test_name(self):
        expect(self.tag.name).isinstance(base.str_test)

    def test_tarball_url(self):
        expect(self.tag.tarball_url).isinstance(base.str_test)

    def test_zipball_url(self):
        expect(self.tag.zipball_url).isinstance(base.str_test)


def __test_files__(fd, sha):
    expect(fd.additions) >= 0
    expect(fd.deletions) >= 0
    expect(fd.changes) == fd.additions + fd.deletions
    expect(fd.filename).isinstance(base.str_test)
    expect(fd.blob_url).isinstance(base.str_test)
    expect(fd.raw_url).isinstance(base.str_test)
    expect(fd.sha).isinstance(base.str_test)
    if sha:
        expect(fd.sha) == sha
    expect(fd.status).isinstance(base.str_test)
    expect(fd.patch).isinstance(base.str_test)


class TestRepoCommit(base.BaseTest):
    def __init__(self, methodName='runTest'):
        super(TestRepoCommit, self).__init__(methodName)
        repo = self.g.repository(self.sigm, self.todo)
        self.commit = repo.commit('04d55444a3ec06ca8d2aa0a5e333cdaf27113254')
        self.sha = self.commit.sha

    def test_additions(self):
        expect(self.commit.additions) == 12

    def test_author(self):
        expect(self.commit.author).isinstance(User)

    def test_commit(self):
        expect(self.commit.commit).isinstance(Commit)

    def test_committer(self):
        expect(self.commit.committer).isinstance(User)

    def test_deletions(self):
        expect(self.commit.deletions) == 5

    def test_files(self):
        expect(self.commit.files).isinstance(list)
        expect(self.commit.files) > []
        self.expect_list_of_class(self.commit.files, type)
        for file in self.commit.files:
            __test_files__(file, self.sha)

    def test_total(self):
        expect(self.commit.total) == 17


class TestComparison(base.BaseTest):
    def __init__(self, methodName='runTest'):
        super(TestComparison, self).__init__(methodName)
        repo = self.g.repository(self.sigm, self.todo)
        self.comp = repo.compare_commits(
                '04d55444a3ec06ca8d2aa0a5e333cdaf27113254',
                '731691616b71258c7ad7c141379856b5ebbab310'
                )

    def test_ahead_by(self):
        expect(self.comp.ahead_by) > 0

    def test_base_commit(self):
        expect(self.comp.base_commit).isinstance(RepoCommit)

    def test_behind_by(self):
        expect(self.comp.behind_by) >= 0

    def test_commits(self):
        self.expect_list_of_class(self.comp.commits, RepoCommit)

    def test_diff_url(self):
        expect(self.comp.diff_url).isinstance(base.str_test)

    def test_files(self):
        expect(self.comp.files).isinstance(list)
        expect(self.comp.files) > []
        self.expect_list_of_class(self.comp.files, type)
        for file in self.comp.files:
            __test_files__(file, '')

    def test_html_url(self):
        expect(self.comp.html_url).isinstance(base.str_test)

    def test_patch_url(self):
        expect(self.comp.patch_url).isinstance(base.str_test)

    def test_permalink_url(self):
        expect(self.comp.permalink_url).isinstance(base.str_test)

    def test_status(self):
        expect(self.comp.status) == 'ahead'

    def test_total_commits(self):
        expect(self.comp.total_commits) == 18
