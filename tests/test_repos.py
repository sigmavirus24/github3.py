import os
import github3
from tests.utils import (expect, BaseCase, load)
from mock import patch


class TestRepository(BaseCase):
    def __init__(self, methodName='runTest'):
        super(TestRepository, self).__init__(methodName)
        self.repo = github3.repos.Repository(load('repo'))

    def setUp(self):
        super(TestRepository, self).setUp()
        self.repo = github3.repos.Repository(self.repo.to_json(), self.g)
        self.api = 'https://api.github.com/repos/sigmavirus24/github3.py/'

    def test_add_collaborator(self):
        self.response('', 204)
        self.put(self.api + 'collaborators/sigmavirus24')
        self.conf = {'data': None}

        with expect.githuberror():
            self.repo.add_collaborator('foo')

        self.login()
        expect(self.repo.add_collaborator(None)).is_False()
        expect(self.repo.add_collaborator('sigmavirus24')).is_True()
        self.mock_assertions()

    def test_archive(self):
        headers = {'content-disposition': 'filename=foo'}
        self.response('archive', 200, **headers)
        self.get(self.api + 'tarball/master')
        self.conf.update({'stream': True})

        expect(self.repo.archive(None)).is_False()

        expect(os.path.isfile('foo')).is_False()
        expect(self.repo.archive('tarball')).is_True()
        expect(os.path.isfile('foo')).is_True()
        os.unlink('foo')
        self.mock_assertions()

        self.request.return_value.raw.seek(0)
        self.request.return_value._content_consumed = False

        expect(os.path.isfile('path_to_file')).is_False()
        expect(self.repo.archive('tarball', 'path_to_file')).is_True()
        expect(os.path.isfile('path_to_file')).is_True()
        os.unlink('path_to_file')

        self.request.return_value.raw.seek(0)
        self.request.return_value._content_consumed = False

        self.get(self.api + 'zipball/randomref')
        expect(self.repo.archive('zipball', ref='randomref')).is_True()
        os.unlink('foo')

    def test_blob(self):
        self.response('blob')
        sha = '3ceb856e2f14e9669fed6384e58c9a1590a2314f'
        self.get(self.api + 'git/blobs/' + sha)

        expect(self.repo.blob(sha)).isinstance(github3.git.Blob)
        self.mock_assertions()

    def test_branch(self):
        self.response('branch')
        self.get(self.api + 'branches/master')

        expect(self.repo.branch('master')).isinstance(github3.repos.Branch)
        self.mock_assertions()

    def test_commit(self):
        self.response('commit')
        sha = '76dcc6cb4b9860034be81b7e58adc286a115aa97'
        self.get(self.api + 'commits/' + sha)

        expect(self.repo.commit(sha)).isinstance(github3.repos.RepoCommit)
        self.mock_assertions()

    def test_commit_comment(self):
        self.response('commit_comment')
        comment_id = 1380832
        self.get(self.api + 'comments/{0}'.format(comment_id))

        expect(self.repo.commit_comment(comment_id)
               ).isinstance(github3.repos.RepoComment)
        self.mock_assertions()

    def test_compare_commits(self):
        self.response('comparison')
        base = 'a811e1a270f65eecb65755eca38d888cbefcb0a7'
        head = '76dcc6cb4b9860034be81b7e58adc286a115aa97'
        self.get(self.api + 'compare/{0}...{1}'.format(base, head))

        expect(self.repo.compare_commits(base, head)
               ).isinstance(github3.repos.Comparison)
        self.mock_assertions()

    def test_contents(self):
        self.response('contents')
        filename = 'setup.py'
        self.get(self.api + 'contents/' + filename)

        expect(self.repo.contents(filename)).isinstance(github3.repos.Contents)
        self.mock_assertions()

    def test_create_blob(self):
        self.response('blob', 201)
        content = 'VGVzdCBibG9i\n'
        encoding = 'base64'
        sha = '30f2c645388832f70d37ab2b47eb9ea527e5ae7c'
        self.post(self.api + 'git/blobs')
        self.conf = {'data': {'content': content, 'encoding': encoding}}

        with expect.githuberror():
            self.repo.create_blob(content, encoding)

        self.login()
        expect(self.repo.create_blob(None, None)) == ''
        expect(self.repo.create_blob(content, encoding)) == sha
        self.mock_assertions()

    def test_create_comment(self):
        self.response('commit_comment', 201)
        body = ('Late night commits are never a good idea. I refactored a '
                'bit. `User` objects and `Organization` objects share a lot '
                'of common attributes. I turned those common attributes into '
                'one `BaseAccount` class to make things simpler. ')
        sha = 'd41566090114a752eb3a87dbcf2473eb427ef0f3'
        self.post(self.api + 'commits/{0}/comments'.format(sha))
        self.conf = {
            'data': {
                'body': body, 'commit_id': sha, 'line': 1, 'path': '',
                'position': 1
            }
        }

        with expect.githuberror():
            self.repo.create_comment(body, sha)

        self.login()
        expect(self.repo.create_comment(None, None)).is_None()
        expect(self.repo.create_comment(body, sha, line=0)).is_None()
        expect(self.repo.create_comment(body, sha)
               ).isinstance(github3.repos.RepoComment)
        self.mock_assertions()

    def test_create_commit(self):
        self.response('commit', 201)
        data = {'message': 'My commit message',
                'author': {
                    'name': 'Ian Cordasco',
                    'email': 'foo@example.com',
                    'date': '2008-07-09T16:13:30+12:00',
                },
                'committer': {},
                'parents': [
                    '7d1b31e74ee336d15cbd21741bc88a537ed063a0'
                ],
                'tree': '827efc6d56897b048c772eb4087f854f46256132',
                }
        self.conf = {'data': data}
        self.post(self.api + 'git/commits')

        with expect.githuberror():
            self.repo.create_commit(**data)

        self.login()
        expect(self.repo.create_commit(None, None, None)).is_None()
        expect(self.repo.create_commit(**data)).isinstance(github3.git.Commit)
        self.mock_assertions()

    def test_create_fork(self):
        self.response('repo', 202)
        self.conf = {'data': None}
        self.post(self.api + 'forks')

        with expect.githuberror():
            self.repo.create_fork()

        self.login()
        expect(self.repo.create_fork()).isinstance(github3.repos.Repository)
        self.mock_assertions()

        self.conf['data'] = {'organization': 'github3py'}
        expect(self.repo.create_fork('github3py')
               ).isinstance(github3.repos.Repository)
        self.mock_assertions()

    def test_create_issue(self):
        self.response('issue', 201)
        title = 'Construct _api attribute on our own'
        self.post(self.api + 'issues')
        self.conf = {'data': {'title': title}}

        with expect.githuberror():
            self.repo.create_issue(title)

        self.login()
        expect(self.repo.create_issue(None)).is_None()
        expect(self.repo.create_issue(title)).isinstance(github3.issues.Issue)
        self.mock_assertions()

        body = 'Fake body'
        #self.conf['data'].update(body=body)
        expect(self.repo.create_issue(title, body)
               ).isinstance(github3.issues.Issue)
        self.mock_assertions()

        assignee, mile, labels = 'sigmavirus24', 1, ['bug', 'enhancement']
        #self.conf['data'].update({'assignee': assignee, 'milestone': mile,
        #                          'labels': labels})
        expect(self.repo.create_issue(title, body, assignee, mile, labels)
               ).isinstance(github3.issues.Issue)
        self.mock_assertions()

    def test_create_key(self):
        self.response('key', 201)
        self.post(self.api + 'keys')
        self.conf = {'data': {'key': 'ssh-rsa foobarbogus',
                              'title': 'Fake key'}}

        with expect.githuberror():
            self.repo.create_key(**self.conf['data'])

        self.login()
        expect(self.repo.create_key(None, None)).is_None()
        self.not_called()
        expect(self.repo.create_key(**self.conf['data'])).isinstance(
            github3.users.Key)
        self.mock_assertions()

    def test_create_label(self):
        self.response('label', 201)
        self.post(self.api + 'labels')
        self.conf = {'data': {'name': 'foo', 'color': 'f00f00'}}

        with expect.githuberror():
            self.repo.create_label(**self.conf['data'])

        self.login()
        expect(self.repo.create_label(None, None)).is_None()
        self.not_called()
        expect(self.repo.create_label(**self.conf['data'])).isinstance(
            github3.issues.Label)
        self.mock_assertions()

    def test_create_milestone(self):
        self.response('milestone', 201)
        self.post(self.api + 'milestones')
        self.conf = {'data': {'title': 'foo'}}

        with expect.githuberror():
            self.repo.create_milestone(**self.conf['data'])

        self.login()
        expect(self.repo.create_milestone(None)).is_None()
        self.not_called()
        expect(self.repo.create_milestone('foo')).isinstance(
            github3.issues.Milestone)
        self.mock_assertions()

    def test_create_pull(self):
        self.response('pull', 201)
        self.post(self.api + 'pulls')
        self.conf = {'data': {'title': 'Fake title', 'base': 'master',
                              'head': 'feature_branch'}}

        with expect.githuberror():
            self.repo.create_pull(**self.conf['data'])

        self.login()
        expect(self.repo.create_pull(None, None, None)).is_None()
        self.not_called()
        expect(self.repo.create_pull(**self.conf['data'])).isinstance(
            github3.pulls.PullRequest)
        self.mock_assertions()

    def test_create_pull_from_issue(self):
        self.response('pull', 201)
        self.post(self.api + 'pulls')
        self.conf = {'data': {'issue': 1, 'base': 'master',
                              'head': 'feature_branch'}}

        with expect.githuberror():
            self.repo.create_pull_from_issue(**self.conf['data'])

        self.login()
        expect(self.repo.create_pull_from_issue(0, 'foo', 'bar')).is_None()
        self.not_called()
        expect(self.repo.create_pull_from_issue(**self.conf['data'])
               ).isinstance(github3.pulls.PullRequest)
        self.mock_assertions()

    def test_create_ref(self):
        self.response('ref', 201)
        self.post(self.api + 'git/refs')
        self.conf = {'data': {'ref': 'refs/heads/master', 'sha': 'fakesha'}}

        with expect.githuberror():
            self.repo.create_ref('foo', 'bar')

        self.login()
        expect(self.repo.create_ref('foo/bar', None)).is_None()
        expect(self.repo.create_ref(**self.conf['data'])).isinstance(
            github3.git.Reference)
        self.mock_assertions()

    def test_create_status(self):
        self.response('status', 201)
        self.post(self.api + 'statuses/fakesha')
        self.conf = {'data': {'state': 'success'}}

        with expect.githuberror():
            self.repo.create_status('fakesha', 'success')

        self.login()
        expect(self.repo.create_status(None, None)).is_None()
        expect(self.repo.create_status('fakesha', 'success')).isinstance(
            github3.repos.Status)
        self.mock_assertions()

    def test_create_tag(self):
        self.response('tag', 201)
        self.post(self.api + 'git/tags')
        data = {
            'tag': '0.3', 'message': 'Fake message', 'object': 'fakesha',
            'type': 'commit', 'tagger': {
                'name': 'Ian Cordasco', 'date': 'Not a UTC date',
                'email': 'graffatcolmingov@gmail.com'
            }
        }
        self.conf = {'data': data.copy()}
        data['obj_type'] = data['type']
        data['sha'] = data['object']
        del(data['type'], data['object'])

        with expect.githuberror():
            self.repo.create_tag(None, None, None, None, None)

        self.login()
        with patch.object(github3.repos.Repository, 'create_ref'):
            expect(self.repo.create_tag(None, None, None, None,
                                        None)).is_None()
            expect(self.repo.create_tag(**data)).isinstance(github3.git.Tag)
        self.mock_assertions()

    def test_create_tree(self):
        self.response('tree', 201)
        self.post(self.api + 'git/trees')
        data = {'tree': [{'path': 'file1', 'mode': '100755',
                          'type': 'tree',
                          'sha': '75b347329e3fc87ac78895ca1be58daff78872a1'}],
                'base_tree': ''}
        self.conf = {'data': data}

        with expect.githuberror():
            self.repo.create_tree(**data)

        self.login()
        expect(self.repo.create_tree(None)).is_None()
        expect(self.repo.create_tree({'foo': 'bar'})).is_None()
        self.not_called()
        expect(self.repo.create_tree(**data)).isinstance(github3.git.Tree)
        self.mock_assertions()

    def test_delete(self):
        self.response('', 204)
        self.delete(self.api[:-1])
        self.conf = {}

        with expect.githuberror():
            self.repo.delete()

        self.login()
        expect(self.repo.delete()).is_True()
        self.mock_assertions()

    def test_delete_key(self):
        self.response('', 204)
        self.delete(self.api + 'keys/2')
        self.conf = {}

        with expect.githuberror():
            self.repo.delete_key(2)

        self.login()
        expect(self.repo.delete_key(-2)).is_False()
        self.not_called()
        expect(self.repo.delete_key(2)).is_True()
        self.mock_assertions()

    def test_download(self):
        self.response('download')
        self.get(self.api + 'downloads/2')

        expect(self.repo.download(-2)).is_None()
        self.not_called()
        expect(self.repo.download(2)).isinstance(github3.repos.Download)
        self.mock_assertions()

    def test_edit(self):
        self.response('repo')
        self.patch(self.api[:-1])
        self.conf = {'data': {'name': 'foo'}}

        with expect.githuberror():
            self.repo.edit('Foo')

        self.login()
        expect(self.repo.edit(None)).is_False()
        self.not_called()
        expect(self.repo.edit('foo')).is_True()
        self.mock_assertions()

        self.conf['data']['description'] = 'bar'
        expect(self.repo.edit(**self.conf['data'])).is_True()
        self.mock_assertions()

    def test_is_collaborator(self):
        self.response('', 204)
        self.get(self.api + 'collaborators/user')

        expect(self.repo.is_collaborator(None)).is_False()
        self.not_called()
        expect(self.repo.is_collaborator('user')).is_True()
        self.mock_assertions()

    def test_git_commit(self):
        self.response('git_commit')
        self.get(self.api + 'git/commits/fakesha')

        expect(self.repo.git_commit(None)).is_None()
        self.not_called()
        expect(self.repo.git_commit('fakesha')).isinstance(github3.git.Commit)
        self.mock_assertions()

    def test_hook(self):
        self.response('hook')
        self.get(self.api + 'hooks/2')

        with expect.githuberror():
            self.repo.hook(2)

        self.login()
        expect(self.repo.hook(-2)).is_None()
        self.not_called()
        expect(self.repo.hook(2)).isinstance(github3.repos.Hook)
        self.mock_assertions()

    def test_is_assignee(self):
        self.response('', 204)
        self.get(self.api + 'assignees/login')

        expect(self.repo.is_assignee(None)).is_False()
        self.not_called()
        expect(self.repo.is_assignee('login')).is_True()
        self.mock_assertions()

    def test_issue(self):
        self.response('issue')
        self.get(self.api + 'issues/2')

        expect(self.repo.issue(-2)).is_None()
        self.not_called()
        expect(self.repo.issue(2)).isinstance(github3.issues.Issue)
        self.mock_assertions()

    def test_key(self):
        self.response('key')
        self.get(self.api + 'keys/2')

        with expect.githuberror():
            self.repo.key(2)

        self.login()
        expect(self.repo.key(-2)).is_None()
        self.not_called()
        expect(self.repo.key(2)).isinstance(github3.users.Key)
        self.mock_assertions()

    def test_label(self):
        self.response('label')
        self.get(self.api + 'labels/name')

        expect(self.repo.label(None)).is_None()
        self.not_called()
        expect(self.repo.label('name')).isinstance(github3.issues.Label)
        self.mock_assertions()

    def test_iter_assignees(self):
        self.response('user', _iter=True)
        self.get(self.api + 'assignees')
        self.conf = {'params': None}

        u = next(self.repo.iter_assignees())
        expect(u).isinstance(github3.users.User)
        self.mock_assertions()

    def test_iter_branches(self):
        self.response('branch', _iter=True)
        self.get(self.api + 'branches')
        self.conf = {'params': None}

        b = next(self.repo.iter_branches())
        expect(b).isinstance(github3.repos.Branch)
        self.mock_assertions()

    def test_iter_comments(self):
        self.response('repo_comment', _iter=True)
        self.get(self.api + 'comments')
        self.conf = {'params': None}

        c = next(self.repo.iter_comments())
        expect(c).isinstance(github3.repos.RepoComment)
        self.mock_assertions()

    def test_iter_comments_on_commit(self):
        self.response('repo_comment', _iter=True)
        self.get(self.api + 'commits/fakesha/comments')
        self.conf = {'params': None}

        c = next(self.repo.iter_comments_on_commit('fakesha'))
        expect(c).isinstance(github3.repos.RepoComment)
        self.mock_assertions()

    def test_iter_commits(self):
        self.response('commit', _iter=True)
        self.get(self.api + 'commits')
        self.conf = {'params': {}}

        c = next(self.repo.iter_commits())
        expect(c).isinstance(github3.repos.RepoCommit)
        self.mock_assertions()

        self.conf = {'params': {'sha': 'fakesha', 'path': '/'}}
        c = next(self.repo.iter_commits('fakesha', '/'))
        self.mock_assertions()

    def test_iter_contributors(self):
        self.response('user', _iter=True)
        self.get(self.api + 'contributors')
        self.conf = {'params': {}}

        u = next(self.repo.iter_contributors())
        expect(u).isinstance(github3.users.User)
        self.mock_assertions()

        self.conf = {'params': {'anon': True}}
        next(self.repo.iter_contributors(True))
        self.mock_assertions()

        next(self.repo.iter_contributors('true value'))
        self.mock_assertions()

    def test_iter_downloads(self):
        self.response('download', _iter=True)
        self.get(self.api + 'downloads')
        self.conf = {'params': None}

        d = next(self.repo.iter_downloads())
        expect(d).isinstance(github3.repos.Download)
        self.mock_assertions()

    def test_iter_events(self):
        self.response('event', _iter=True)
        self.get(self.api + 'events')
        self.conf = {'params': None}

        e = next(self.repo.iter_events())
        expect(e).isinstance(github3.repos.Event)
        self.mock_assertions()

    def test_iter_forks(self):
        self.response('repo', _iter=True)
        self.get(self.api + 'forks')
        self.conf = {'params': {}}

        r = next(self.repo.iter_forks())
        expect(r).isinstance(github3.repos.Repository)
        self.mock_assertions()

        self.conf['params']['sort'] = 'newest'
