import github3
import re
from .base import expect, BaseTest, str_test, expect_str
from datetime import datetime
from os import unlink, listdir
from github3.repos import (Repository, Branch, RepoCommit, RepoComment,
        Comparison, Contents, Download, Hook, RepoTag, Status)
from github3.users import User, Key
from github3.git import Commit, Reference, Tag, Tree, Blob
from github3.issues import (Issue, IssueEvent, Label, Milestone)
from github3.events import Event
from github3.pulls import PullRequest
from github3.orgs import Team


class TestRepository(BaseTest):
    def __init__(self, methodName='runTest'):
        super(TestRepository, self).__init__(methodName)
        self.repo = self.g.repository(self.sigm, self.todo)
        self.requests_repo = self.g.repository(self.kr, 'requests')
        self.fork = self.g.repository(self.sigm, 'requests')
        if self.auth:
            self.alt_repo = self._g.repository(self.gh3py, self.test_repo)
            self.auth_todo = self._g.repository(self.sigm, self.todo)

    def test_repository(self):
        expect(self.repo).isinstance(Repository)
        expect_str(repr(self.repo))
        expect(repr(self.repo)) != ''
        self.repo._update_(self.repo.to_json())

    def test_clone_url(self):
        expect(self.repo.clone_url).is_not_None()

    def test_created_at(self):
        expect(self.repo.created_at).isinstance(datetime)

    def test_forks(self):
        expect(self.requests_repo.forks) > 0

    def test_is_collaborator(self):
        expect(self.repo.is_collaborator(self.sigm)).is_True()
        expect(self.repo.is_collaborator('')).is_False()

    def test_git_url(self):
        expect(self.repo.git_url) != ''

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
        expect(self.requests_repo.watchers) >= 1

    def test_source(self):
        if self.fork.source:
            expect(self.fork.source).isinstance(Repository)

    def test_parent(self):
        if self.fork.parent:
            expect(self.fork.parent).isinstance(Repository)

    def test_master_branch(self):
        expect(self.repo.master_branch) == 'master'
        expect(self.requests_repo.master_branch) == 'develop'

    # Methods
    def test_archive(self):
        expect(self.repo.archive('tarball', 'archive.tar.gz')).is_True()
        unlink('archive.tar.gz')
        expect(self.repo.archive('tarball')).is_True()
        reg = re.compile('{0}-{1}-.*\.tar\.gz'.format(self.sigm, self.todo))
        for f in listdir('.'):
            if reg.match(f):
                unlink(f)

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
        comment = self.requests_repo.commit_comment('270904')
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
        download = self.repo.download(316176)
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

    def test_has_issues(self):
        expect(self.repo.has_issues()).is_True()

    def test_has_downloads(self):
        expect(self.repo.has_downloads()).is_True()

    def test_has_wiki(self):
        expect(self.repo.has_wiki()).is_True()

    def test_is_assignee(self):
        expect(self.repo.is_assignee(self.sigm)).is_True()

    def test_issue(self):
        issue = self.requests_repo.issue(1)
        expect(issue).isinstance(Issue)
        expect(issue.title) == 'Cookie support?'

    def test_label(self):
        expect(self.requests_repo.label('Bug')).isinstance(Label)

    def test_list_assignees(self):
        assignees = self.repo.list_assignees()
        expect(assignees).list_of(User)
        for a in assignees:
            if a.login == 'sigmavirus24':
                return
        self.fail('No user with login sigmavirus24')

    def test_iter_assignees(self):
        assignees = [a for a in self.repo.iter_assignees()]
        expect(assignees).list_of(User)
        for a in assignees:
            if a.login == 'sigmavirus24':
                return
        self.fail('No user with login sigmavirus24')

    def test_list_branches(self):
        branches = self.repo.list_branches()
        expect(branches).list_of(Branch)
        for b in branches:
            if b.name == 'master':
                return
        self.fail('No branch named master')

    def test_iter_branches(self):
        expect(next(self.repo.iter_branches())).isinstance(Branch)

    def test_list_comments(self):
        comments = self.requests_repo.list_comments()
        expect(comments).list_of(RepoComment)
        for c in comments:
            if c.user.login == self.kr:
                return
        self.fail('No commenter with login kennethreitz')

    def test_iter_comments(self):
        expect(next(self.requests_repo.iter_comments())
                ).isinstance(RepoComment)

    def test_list_comments_on_commit(self):
        comments = self.requests_repo.list_comments_on_commit(
                '10280c697dcfd3d334f1c9c381a11c324bb550bc')
        expect(comments).list_of(RepoComment)
        for c in comments:
            if c.user.login in 'brunobord':
                return
        self.fail('No commenter with login brunobord')

    def test_iter_comments_on_commit(self):
        comment = next(self.requests_repo.iter_comments_on_commit(
            '10280c697dcfd3d334f1c9c381a11c324bb550bc'
            ))
        expect(comment).isinstance(RepoComment)

    def test_list_commits(self):
        expect(self.repo.list_commits()).list_of(RepoCommit)

    def test_iter_commits(self):
        expect(next(self.repo.iter_commits())).isinstance(RepoCommit)

    def test_list_contributors(self):
        expect(self.repo.list_contributors()).list_of(User)

    def test_iter_contributors(self):
        expect(next(self.repo.iter_contributors())).isinstance(User)

    def test_list_downloads(self):
        downloads = self.repo.list_downloads()
        expect(downloads).list_of(Download)
        for d in downloads:
            if d.name == 'todo.txt-python-0.3.zip':
                return
        self.fail('No download with name todo.txt-python-0.3.zip')

    def test_iter_downloads(self):
        expect(next(self.repo.iter_downloads())).isinstance(Download)

    def test_list_events(self):
        expect(self.repo.list_events()).list_of(Event)

    def test_iter_events(self):
        expect(next(self.repo.iter_events())).isinstance(Event)

    def test_list_forks(self):
        expect(self.repo.list_forks()).list_of(Repository)
        expect(self.repo.list_forks('oldest')).list_of(Repository)

    def test_iter_forks(self):
        expect(next(self.repo.iter_forks())).isinstance(Repository)
        expect(next(self.repo.iter_forks('oldest'))).isinstance(Repository)

    def test_iter_issues(self):
        expect(next(self.repo.iter_issues())).isinstance(Issue)
        expect(next(self.requests_repo.iter_issues(milestone='*'))).isinstance(
                Issue)

    def test_list_issues(self):
        expect(self.repo.list_issues()).list_of(Issue)

    def test_iter_issue_events(self):
        expect(next(self.repo.iter_issue_events())).isinstance(IssueEvent)

    def test_list_issue_events(self):
        expect(self.repo.list_issue_events()).list_of(IssueEvent)

    def test_iter_keys(self):
        if not self.auth:
            return
        expect([k for k in self.alt_repo.iter_keys()]).list_of(Key)

    def test_list_keys(self):
        if not self.auth:
            return
        expect(self.alt_repo.list_keys()).list_of(Key)

    def test_iter_labels(self):
        expect(next(self.repo.iter_labels(1))).isinstance(Label)

    def test_list_labels(self):
        expect(self.repo.list_labels()).list_of(Label)

    def test_list_languages(self):
        expect(self.repo.list_languages()).list_of(tuple)

    def test_iter_milestones(self):
        expect(next(
            self.requests_repo.iter_milestones(
                'open', '', ''))).isinstance(Milestone)

    def test_list_milestones(self):
        expect(self.repo.list_milestones()).list_of(Milestone)

    def test_iter_network_events(self):
        expect(next(self.repo.iter_network_events())).isinstance(Event)

    def test_list_network_events(self):
        expect(self.repo.list_network_events()).list_of(Event)

    def test_iter_pulls(self):
        expect(
              next(self.requests_repo.iter_pulls(state='closed'))
              ).isinstance(PullRequest)

    def test_list_pulls(self):
        expect(
              self.requests_repo.list_pulls(state='closed')
              ).list_of(PullRequest)

    def test_iter_refs(self):
        expect(next(self.repo.iter_refs())).isinstance(Reference)

    def test_list_refs(self):
        expect(self.repo.list_refs()).list_of(Reference)

    def test_iter_stargazers(self):
        expect(next(self.repo.iter_stargazers())).isinstance(User)

    def test_list_stargazers(self):
        expect(self.repo.list_stargazers()).list_of(User)

    def test_iter_subscribers(self):
        expect(next(self.repo.iter_subscribers())).isinstance(User)

    def test_list_subscribers(self):
        expect(self.repo.list_subscribers()).list_of(User)

    def test_iter_statuses(self):
        expect(next(self.repo.iter_statuses(
            '04d55444a3ec06ca8d2aa0a5e333cdaf27113254', 1
            ))).isinstance(Status)
        with expect.raises(StopIteration):
            next(self.repo.iter_statuses('', 1))

    def test_list_statuses(self):
        statuses = self.repo.list_statuses(
                '04d55444a3ec06ca8d2aa0a5e333cdaf27113254'
                )
        if statuses:
            expect(statuses).list_of(Status)

    def test_iter_tags(self):
        expect(next(self.repo.iter_tags())).isinstance(RepoTag)

    def test_list_tags(self):
        expect(self.repo.list_tags()).list_of(RepoTag)

    def test_list_teams(self):
        if not self.auth:
            return
        expect(self.alt_repo.list_teams()).list_of(Team)

    def test_iter_teams(self):
        if not self.auth:
            return
        expect(next(self.alt_repo.iter_teams(1))).isinstance(Team)

    def test_list_watchers(self):
        self.assertRaises(DeprecationWarning, self.repo.list_watchers)

    def test_milestone(self):
        expect(self.requests_repo.milestone(15)).isinstance(Milestone)

    def test_pull_request(self):
        expect(self.requests_repo.pull_request(833)).isinstance(PullRequest)

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
        repo = self.requests_repo
        self.raisesGHE(repo.add_collaborator, self.sigm)
        self.raisesGHE(repo.create_blob, 'Foo bar bogus', 'utf-8')
        self.raisesGHE(repo.create_comment, 'Foo bar bogus',
                'e8b7f5ad567faae369460f186ee0d82c90ccfbd1',
                'todo.py', 5, 10)
        #repo.create_commit
        self.raisesGHE(repo.create_download, 'file_to_download', '/tmp/foo')
        self.raisesGHE(repo.create_fork, self.gh3py)
        self.raisesGHE(repo.create_hook, 'Hook', {'foo': 'bar'})
        self.raisesGHE(repo.create_issue, 'New issue')
        self.raisesGHE(repo.create_key, 'Key', 'foobarbogus')
        self.raisesGHE(repo.create_label, 'Foo bar', 'abc123')
        self.raisesGHE(repo.create_milestone, 'milestone')
        self.raisesGHE(repo.create_pull, 'PR',
                '04d55444a3ec06ca8d2aa0a5e333cdaf27113254',
                '731691616b71258c7ad7c141379856b5ebbab310')
        self.raisesGHE(repo.create_tag, 'fake_tag', 'fake tag message',
                '731691616b71258c7ad7c141379856b5ebbab310', 'commit',
                {'name': 'Ian Cordasco',
                 'email': 'graffatcolmingov@gmail.com'})
        self.raisesGHE(repo.create_tree, {'path': 'tests/test_fake.py',
            'mode': '100644', 'type': 'blob',
            'sha': '731691616b71258c7ad7c141379856b5ebbab310'})
        self.raisesGHE(repo.delete)
        self.raisesGHE(repo.edit, 'todo.py', '#', 'http://git.io/todo.py')
        self.raisesGHE(repo.hook, 74859)
        self.raisesGHE(repo.key, 1234)
        self.raisesGHE(repo.list_keys)
        self.raisesGHE(repo.iter_keys, 1)
        self.raisesGHE(repo.list_teams)
        self.raisesGHE(repo.iter_teams, 1)
        self.raisesGHE(repo.pubsubhubbub,
                'subscribe',
                'https://github.com/user/repo/events/push',
                'https://httpbin.org/post'
                )
        self.raisesGHE(repo.remove_collaborator, 'foobarbogus')
        self.raisesGHE(repo.update_label, 'Foo', 'abc123')
        self.raisesGHE(repo.merge, 'development', 'master', 'Fails')

    # Try somethings only I should be able to do hence the try/except blocks
    def test_create_blob(self):
        if not self.auth:
            return
        content = 'foo bar bogus'
        sha = self.alt_repo.create_blob(content, 'utf-8')
        expect_str(sha)
        blob = self.alt_repo.blob(sha)
        expect(blob).isinstance(Blob)
        expect(self.alt_repo.create_blob('', '')) == ''

    def test_create_comment(self):
        if not self.auth:
            return
        sha = '499faa66a0f56235ee55bf295bac2f2f3c3f0a04'
        body = 'Spelling error: reposity -> repository'
        path = 'README.md'
        line = pos = 4
        comment = self.alt_repo.create_comment(body, sha, path, pos, line)
        expect(comment).isinstance(RepoComment)
        comment.delete()

    def test_create_download(self):
        if not self.auth:
            return
        dl = self.alt_repo.create_download('test_dls.py', __file__)
        expect(dl).isinstance(Download)
        dl.delete()
        expect(self.alt_repo.create_download('', '')).is_None()

    def test_create_fork_org(self):
        if not self.auth:
            return
        try:
            r = self.auth_todo.create_fork(self.gh3py)
            expect(r).isinstance(Repository)
            r.delete()
        except github3.GitHubError:
            pass

    def test_create_fork(self):
        if not self.auth:
            return
        repo = self._g.repository(self.gh3py, 'fork_this')
        r = repo.create_fork()
        expect(r).isinstance(Repository)
        r.delete()

    def test_create_hook(self):
        if not self.auth:
            return
        hook = self.alt_repo.create_hook('web',
                {'url': 'http://httpbin.org/post'})
        expect(hook).isinstance(Hook)
        hook.delete()

    def test_create_key(self):
        if not self.auth:
            return
        try:
            key = self.alt_repo.create_key('test_key', (
                  'ssh-rsa AAAAB3NzaC1yc2EAAAABIwAAAQEAxGTCJTMYmsBhLL0PQ2RwLp3'
                  'sgcJ8uz6RqOrlB/6lKzIXYOcvdaHqEEF9G+1xlJck7kA8pSNR9AkEWP2uoy'
                  '1tJVp4nUVzPYKSrkoMppzA34vT+iqW/H4rRCADxIRillvpXZB2CWQ8fbRlD'
                  '9Mjreh0L2A4NPKSmGxs5XfZXD9lWPb1+U6oQrZYG2h1ulyI7rt+adWOhfP2'
                  'UYq6V5JSdNDi4r1nGxBccZgguiL7XNjl9TSsgr8QKmAacubyNEwIrmQIS9h'
                  'ipKg3k10VcqfVmSzF1GuzDUKFfIHU/zyd6aJ0emAqgft/fho+BkrXBihhxf'
                  '/Qbi5fi4Ipx3VFcLrdiOBbOQ==')
                  )
            expect(key).isinstance(Key)
            self.alt_repo.delete_key(key.id)
        except github3.GitHubError:
            pass

    def test_edit(self):
        if not self.auth:
            return
        old = {'name': self.alt_repo.name,
                'description': self.alt_repo.description,
                'homepage': self.alt_repo.homepage,
                'has_issues': self.alt_repo.has_issues(),
                'has_wiki': self.alt_repo.has_wiki(),
                'has_downloads': self.alt_repo.has_downloads(),
                }
        expect(self.alt_repo.edit(self.alt_repo.name,
            'Test editing of github3.py', 'www.example.com', False, False,
            False)).is_True()
        expect(self.alt_repo.edit(**old)).is_True()

    def test_pubsubhubub(self):
        if not self.auth:
            return
        try:
            expect(self.auth_todo.pubsubhubbub('subscribe',
                'https://github.com/sigmavirus24/github3.py/events',
                'https://httpbin.org/post'
                )).is_False()
        except github3.GitHubError:
            pass

    def test_hook(self):
        if not self.auth:
            return
        try:
            expect(self.auth_todo.hook(424033)).isinstance(Hook)
        except github3.GitHubError:
            pass

    def test_deploy_key(self):
        if not self.auth:
            return
        try:
            expect(self.auth_todo.key(3199081)).isinstance(Key)
        except github3.GitHubError:
            pass

    def test_add_remove_collab(self):
        if not self.auth:
            return
        repo = self.auth_todo
        # Try somethings only I can test
        try:
            expect(repo.add_collaborator('gh3test')).is_True()
        except github3.GitHubError:
            pass
        try:
            expect(repo.remove_collaborator('gh3test')).is_True()
        except github3.GitHubError:
            pass


class TestBranch(BaseTest):
    def __init__(self, methodName='runTest'):
        super(TestBranch, self).__init__(methodName)
        repo = self.g.repository(self.sigm, self.todo)
        self.branch = repo.branch('master')

    def test_commit(self):
        expect(self.branch.commit).isinstance(RepoCommit)

    def test_links(self):
        expect(self.branch.links).isinstance(dict)

    def test_name(self):
        expect(self.branch.name) == 'master'


class TestContents(BaseTest):
    def __init__(self, methodName='runTest'):
        super(TestContents, self).__init__(methodName)
        repo = self.g.repository(self.sigm, self.todo)
        self.contents = repo.contents('todo.py')

    def _test_str_(self, val):
        expect(val).is_not_None()
        expect(val) > ''
        expect_str(val)

    def test_content(self):
        expect(len(self.contents.content)) > 0
        self._test_str_(self.contents.content)

    def test_decoded(self):
        expect(len(self.contents.decoded)) > 0
        self._test_str_(self.contents.content)

    def test_encoding(self):
        self._test_str_(self.contents.encoding)

    def test_git_url(self):
        self._test_str_(self.contents.git_url)

    def test_html(self):
        self._test_str_(self.contents.html_url)

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


class TestDownload(BaseTest):
    def __init__(self, methodName='runTest'):
        super(TestDownload, self).__init__(methodName)
        repo = self.g.repository(self.sigm, self.todo)
        self.dl = repo.download(316176)

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
        expect(self.dl.id) == 316176

    def test_name(self):
        expect(self.dl.name) == 'todo.txt-python-0.3.zip'

    def test_size(self):
        expect(self.dl.size) == 23552

    def test_requires_auth(self):
        with expect.raises(github3.GitHubError):
            self.dl.delete()


class TestHook(BaseTest):
    def __init__(self, methodName='runTest'):
        super(TestHook, self).__init__(methodName)
        if self.auth:
            repo = self._g.repository(self.sigm, self.todo)
            self.hook = repo.hook(424182)
        else:
            json = {
                'name': 'twitter',
                'url':
                'https://api.github.com/repos/sigmavirus24/Todo.txt-python/' +
                'hooks/74859',
                'created_at': '2011-09-05T18:19:50Z',
                'updated_at': '2012-03-08T17:03:25Z',
                'id': 424182,
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
        expect(self.hook.events).list_of(str_test)

    def test_id(self):
        expect(self.hook.id) == 424182

    def test_is_active(self):
        expect(self.hook.is_active()).is_False()

    def test_name(self):
        expect(self.hook.name) == 'twitter'

    def test_updated_at(self):
        expect(self.hook.updated_at).isinstance(datetime)

    def test_requires_auth(self):
        if self.auth:
            return
        self.raisesGHE(self.hook.edit, 'tweeter', self.hook.config)
        self.raisesGHE(self.hook.delete)
        self.raisesGHE(self.hook.test)


class TestRepoTag(BaseTest):
    def __init__(self, methodName='runTest'):
        super(TestRepoTag, self).__init__(methodName)
        repo = self.g.repository(self.sigm, self.todo)
        self.tag = repo.list_tags()[0]

    def test_commit(self):
        expect(self.tag.commit).isinstance(dict)

    def test_name(self):
        expect_str(self.tag.name)

    def test_tarball_url(self):
        expect_str(self.tag.tarball_url)

    def test_zipball_url(self):
        expect_str(self.tag.zipball_url)


def __test_files__(fd, sha):
    expect(fd['additions']) >= 0
    expect(fd['deletions']) >= 0
    expect(fd['changes']) == fd['additions'] + fd['deletions']
    expect_str(fd['filename'])
    expect_str(fd['blob_url'])
    expect_str(fd['raw_url'])
    expect_str(fd['sha'])
    expect_str(fd['status'])
    expect_str(fd['patch'])


class TestRepoCommit(BaseTest):
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
        expect(self.commit.files).list_of(dict)
        for fd in self.commit.files:
            __test_files__(fd, self.sha)

    def test_total(self):
        expect(self.commit.total) == 17


class TestComparison(BaseTest):
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
        expect(self.comp.commits).list_of(RepoCommit)

    def test_diff_url(self):
        expect_str(self.comp.diff_url)

    def test_files(self):
        expect(self.comp.files).isinstance(list)
        expect(self.comp.files) > []
        expect(self.comp.files).list_of(dict)
        for file in self.comp.files:
            __test_files__(file, '')

    def test_html_url(self):
        expect_str(self.comp.html_url)

    def test_patch_url(self):
        expect_str(self.comp.patch_url)

    def test_permalink_url(self):
        expect_str(self.comp.permalink_url)

    def test_status(self):
        expect(self.comp.status) == 'ahead'

    def test_total_commits(self):
        expect(self.comp.total_commits) == 18


class TestStatus(BaseTest):
    def __init__(self, methodName='runTest'):
        super(TestStatus, self).__init__(methodName)
        repo = self.g.repository(self.sigm, 'c_libs')
        statuses = repo.list_statuses(
                '60fc424765753121d0173073fec22a1c9a6d758b'
                )
        self.status = statuses[0]

    def test_status(self):
        expect(self.status).isinstance(Status)
        expect_str(repr(self.status))
        expect(repr(self.status)) != ''

    def test_created_at(self):
        expect(self.status.created_at).isinstance(datetime)

    def test_creator(self):
        expect(self.status.creator).isinstance(User)
        expect(self.status.creator.login) == self.sigm

    def test_description(self):
        expect_str(self.status.description)
        expect(self.status.description) == 'Testing github3.py'

    def test_id(self):
        expect(self.status.id) == 259373

    def test_state(self):
        expect_str(self.status.state)
        expect(self.status.state) == 'success'

    def test_target_url(self):
        expect_str(self.status.target_url)
        expect(self.status.target_url) == ('https://github.com/sigmavirus24/'
            'github3.py')

    def test_updated_at(self):
        expect(self.status.updated_at).isinstance(datetime)
