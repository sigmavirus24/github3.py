import os
import github3
from github3 import repos
from tests.utils import (expect, BaseCase, load)
from mock import patch, mock_open


class TestRepository(BaseCase):
    def __init__(self, methodName='runTest'):
        super(TestRepository, self).__init__(methodName)
        self.repo = repos.Repository(load('repo'))

    def setUp(self):
        super(TestRepository, self).setUp()
        self.repo = repos.Repository(self.repo.to_json(), self.g)
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

        self.request.return_value.raw.seek(0)
        self.request.return_value._content_consumed = False

        o = mock_open()
        with patch('{0}.open'.format(__name__), o, create=True):
            with open('archive', 'wb+') as fd:
                self.repo.archive('tarball', fd)

        o.assert_called_once_with('archive', 'wb+')
        fd = o()
        fd.write.assert_called_once_with(b'archive_data')

    def test_blob(self):
        self.response('blob')
        sha = '3ceb856e2f14e9669fed6384e58c9a1590a2314f'
        self.get(self.api + 'git/blobs/' + sha)

        blob = self.repo.blob(sha)
        expect(blob).isinstance(github3.git.Blob)
        expect(repr(blob).startswith('<Blob')).is_True()
        self.mock_assertions()

    def test_branch(self):
        self.response('branch')
        self.get(self.api + 'branches/master')

        b = self.repo.branch('master')
        expect(b).isinstance(repos.branch.Branch)
        self.mock_assertions()

        expect(repr(b)) == '<Repository Branch [master]>'

    def test_commit(self):
        self.response('commit')
        sha = '76dcc6cb4b9860034be81b7e58adc286a115aa97'
        self.get(self.api + 'commits/' + sha)

        expect(self.repo.commit(sha)).isinstance(repos.commit.RepoCommit)
        self.mock_assertions()

    def test_commit_comment(self):
        self.response('commit_comment')
        comment_id = 1380832
        self.get(self.api + 'comments/{0}'.format(comment_id))

        expect(self.repo.commit_comment(comment_id)
               ).isinstance(repos.comment.RepoComment)
        self.mock_assertions()

    def test_compare_commits(self):
        self.response('comparison')
        base = 'a811e1a270f65eecb65755eca38d888cbefcb0a7'
        head = '76dcc6cb4b9860034be81b7e58adc286a115aa97'
        self.get(self.api + 'compare/{0}...{1}'.format(base, head))

        expect(self.repo.compare_commits(base, head)
               ).isinstance(repos.comparison.Comparison)
        self.mock_assertions()

    def test_contents(self):
        self.response('contents')
        filename = 'setup.py'
        self.get(self.api + 'contents/' + filename)

        expect(self.repo.contents(filename)).isinstance(
            repos.contents.Contents)
        self.mock_assertions()

        self.response('', 404)
        expect(self.repo.contents(filename)).is_None()

    def test_contents_ref(self):
        self.response('contents')
        filename = 'setup.py'
        self.get(self.api + 'contents/' + filename)
        self.conf = {'params': {'ref': 'foo'}}

        expect(self.repo.contents(filename, ref='foo')).isinstance(
            repos.contents.Contents)
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
        self.conf = {'data': {'body': body, 'commit_id': sha, 'line': 1}}

        with expect.githuberror():
            self.repo.create_comment(body, sha)

        self.login()
        expect(self.repo.create_comment(None, None)).is_None()
        expect(self.repo.create_comment(body, sha, line=0)).is_None()
        expect(self.repo.create_comment(body, sha)
               ).isinstance(repos.comment.RepoComment)
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
        expect(self.repo.create_fork()).isinstance(repos.Repository)
        self.mock_assertions()

        self.conf['data'] = {'organization': 'github3py'}
        expect(self.repo.create_fork('github3py')
               ).isinstance(repos.Repository)
        self.mock_assertions()

    def test_create_hook(self):
        self.response('hook', 201)
        self.post(self.api + 'hooks')
        self.conf = {
            'data': {
                'name': 'Hookname',
                'config': {
                    'foo': 'bar'
                }
            }
        }

        with expect.githuberror():
            self.repo.create_hook(None, None)

        self.login()
        expect(self.repo.create_hook(None, {'foo': 'bar'})).is_None()
        expect(self.repo.create_hook('name', None)).is_None()
        expect(self.repo.create_hook('name', 'bar')).is_None()
        self.not_called()

        h = self.repo.create_hook(**self.conf['data'])
        expect(h).isinstance(repos.hook.Hook)
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
            github3.issues.label.Label)
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
            github3.issues.milestone.Milestone)
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
        s = self.repo.create_status('fakesha', 'success')
        expect(s).isinstance(repos.status.Status)
        expect(repr(s)) > ''
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
        with patch.object(repos.Repository, 'create_ref'):
            expect(self.repo.create_tag(None, None, None, None,
                                        None)).is_None()
            tag = self.repo.create_tag(**data)
            expect(tag).isinstance(github3.git.Tag)
            expect(repr(tag).startswith('<Tag')).is_True()
        self.mock_assertions()

        with patch.object(repos.Repository, 'create_ref') as cr:
            self.repo.create_tag('tag', '', 'fakesha', '', '',
                                 lightweight=True)
            cr.assert_called_once_with('refs/tags/tag', 'fakesha')

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
        expect(self.repo.download(2)).isinstance(repos.download.Download)
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
        expect(self.repo.hook(2)).isinstance(repos.hook.Hook)
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
        expect(self.repo.label('name')).isinstance(github3.issues.label.Label)
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
        expect(b).isinstance(repos.branch.Branch)
        self.mock_assertions()

    def test_iter_comments(self):
        self.response('repo_comment', _iter=True)
        self.get(self.api + 'comments')
        self.conf = {'params': None}

        c = next(self.repo.iter_comments())
        expect(c).isinstance(repos.comment.RepoComment)
        self.mock_assertions()

    def test_iter_comments_on_commit(self):
        self.response('repo_comment', _iter=True)
        self.get(self.api + 'commits/fakesha/comments')
        self.conf = {'params': None}

        c = next(self.repo.iter_comments_on_commit('fakesha'))
        expect(c).isinstance(repos.comment.RepoComment)
        self.mock_assertions()

    def test_iter_commits(self):
        self.response('commit', _iter=True)
        self.get(self.api + 'commits')
        self.conf = {'params': {}}

        c = next(self.repo.iter_commits())
        expect(c).isinstance(repos.commit.RepoCommit)
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
        expect(d).isinstance(repos.download.Download)
        self.mock_assertions()

    def test_iter_events(self):
        self.response('event', _iter=True)
        self.get(self.api + 'events')
        self.conf = {'params': None}

        e = next(self.repo.iter_events())
        expect(e).isinstance(github3.events.Event)
        self.mock_assertions()

    def test_iter_forks(self):
        self.response('repo', _iter=True)
        self.get(self.api + 'forks')
        self.conf = {'params': {}}

        r = next(self.repo.iter_forks())
        expect(r).isinstance(repos.Repository)
        self.mock_assertions()

        self.conf['params']['sort'] = 'newest'
        next(self.repo.iter_forks(**self.conf['params']))
        self.mock_assertions()

    def test_iter_hooks(self):
        self.response('hook', _iter=True)
        self.get(self.api + 'hooks')
        self.conf = {'params': None}

        with expect.githuberror():
            self.repo.iter_hooks()

        self.login()
        h = next(self.repo.iter_hooks())
        expect(h).isinstance(repos.hook.Hook)
        self.mock_assertions()

    def test_iter_issues(self):
        self.response('issue', _iter=True)
        self.get(self.api + 'issues')
        params = {}
        self.conf = {'params': params}

        i = next(self.repo.iter_issues())
        expect(i).isinstance(github3.issues.Issue)
        self.mock_assertions()

        params['milestone'] = 'none'
        next(self.repo.iter_issues('none'))
        self.mock_assertions()

        params['state'] = 'open'
        next(self.repo.iter_issues(**params))
        self.mock_assertions()

    def test_iter_issue_events(self):
        self.response('issue_event', _iter=True)
        self.get(self.api + 'issues/events')
        self.conf = {'params': None}

        e = next(self.repo.iter_issue_events())
        expect(e).isinstance(github3.issues.event.IssueEvent)
        self.mock_assertions()

    def test_iter_keys(self):
        self.response('key', _iter=True)
        self.get(self.api + 'keys')

        with expect.githuberror():
            self.repo.iter_keys()

        self.login()
        k = next(self.repo.iter_keys())
        expect(k).isinstance(github3.users.Key)
        self.mock_assertions()

    def test_iter_labels(self):
        self.response('label', _iter=True)
        self.get(self.api + 'labels')

        l = next(self.repo.iter_labels())
        expect(l).isinstance(github3.issues.label.Label)
        self.mock_assertions()

    def test_iter_languages(self):
        #: repos/:login/:repo/languages is just a dictionary, so _iter=False
        self.response('language')
        self.get(self.api + 'languages')

        l = next(self.repo.iter_languages())
        expect(l).isinstance(tuple)
        self.mock_assertions()

    def test_iter_milestones(self):
        self.response('milestone', _iter=True)
        self.get(self.api + 'milestones')

        m = next(self.repo.iter_milestones())
        expect(m).isinstance(github3.issues.milestone.Milestone)
        self.mock_assertions()

    def test_iter_network_events(self):
        self.response('event', _iter=True)
        self.get(self.api.replace('repos', 'networks', 1) + 'events')

        e = next(self.repo.iter_network_events())
        expect(e).isinstance(github3.events.Event)
        self.mock_assertions()

    def test_iter_notifications(self):
        self.response('notification', _iter=True)
        self.get(self.api + 'notifications')
        self.conf.update(params={})

        with expect.githuberror():
            self.repo.iter_notifications()

        self.login()
        n = next(self.repo.iter_notifications())
        expect(n).isinstance(github3.notifications.Thread)
        self.mock_assertions()

    def test_iter_pulls(self):
        self.response('pull', _iter=True)
        self.get(self.api + 'pulls')
        self.conf.update(params={})

        p = next(self.repo.iter_pulls())
        expect(p).isinstance(github3.pulls.PullRequest)
        self.mock_assertions()

        next(self.repo.iter_pulls('foo'))
        self.mock_assertions()

        self.conf.update(params={'state': 'open'})
        next(self.repo.iter_pulls('Open'))
        self.mock_assertions()

    def test_iter_refs(self):
        self.response('ref', _iter=True)
        self.get(self.api + 'git/refs')

        r = next(self.repo.iter_refs())
        expect(r).isinstance(github3.git.Reference)
        self.mock_assertions()

        self.get(self.api + 'git/refs/subspace')
        r = next(self.repo.iter_refs('subspace'))
        expect(r).isinstance(github3.git.Reference)
        self.mock_assertions()

    def test_iter_stargazers(self):
        self.response('user', _iter=True)
        self.get(self.api + 'stargazers')

        u = next(self.repo.iter_stargazers())
        expect(u).isinstance(github3.users.User)
        self.mock_assertions()

    def test_iter_subscribers(self):
        self.response('user', _iter=True)
        self.get(self.api + 'subscribers')

        u = next(self.repo.iter_subscribers())
        expect(u).isinstance(github3.users.User)
        self.mock_assertions()

    def test_iter_statuses(self):
        self.response('status', _iter=True)
        self.get(self.api + 'statuses/fakesha')

        with expect.raises(StopIteration):
            next(self.repo.iter_statuses(None))
            self.not_called()

        s = next(self.repo.iter_statuses('fakesha'))
        expect(s).isinstance(repos.status.Status)
        self.mock_assertions()

    def test_iter_tags(self):
        self.response('tag', _iter=True)
        self.get(self.api + 'tags')

        t = next(self.repo.iter_tags())
        expect(t).isinstance(repos.tag.RepoTag)
        self.mock_assertions()

        expect(repr(t).startswith('<Repository Tag')).is_True()
        expect(str(t) > '').is_True()

    def test_iter_teams(self):
        self.response('team', _iter=True)
        self.get(self.api + 'teams')

        with expect.githuberror():
            self.repo.iter_teams()
            self.not_called()

        self.login()
        t = next(self.repo.iter_teams())
        expect(t).isinstance(github3.orgs.Team)
        self.mock_assertions()

    def test_mark_notifications(self):
        self.response('', 205)
        self.put(self.api + 'notifications')
        self.conf = {'data': {'read': True}}

        with expect.githuberror():
            self.repo.mark_notifications()
        self.not_called()

        self.login()
        expect(self.repo.mark_notifications()).is_True()
        self.mock_assertions()

        expect(self.repo.mark_notifications('2013-01-18T19:53:04Z')).is_True()
        self.conf['data']['last_read_at'] = '2013-01-18T19:53:04Z'
        self.mock_assertions()

    def test_merge(self):
        self.response('commit', 201)
        self.post(self.api + 'merges')
        self.conf = {'data': {'base': 'master', 'head': 'sigma/feature'}}

        with expect.githuberror():
            self.repo.merge('foo', 'bar')
        self.not_called()

        self.login()
        expect(self.repo.merge('master', 'sigma/feature')).isinstance(
            repos.commit.RepoCommit)
        self.mock_assertions()

        self.conf['data']['commit_message'] = 'Commit message'
        self.repo.merge('master', 'sigma/feature', 'Commit message')
        self.mock_assertions()

    def test_milestone(self):
        self.response('milestone', 200)
        self.get(self.api + 'milestones/2')

        expect(self.repo.milestone(0)).is_None()
        self.not_called()

        expect(self.repo.milestone(2)).isinstance(
            github3.issues.milestone.Milestone)
        self.mock_assertions()

    def test_parent(self):
        json = self.repo.to_json().copy()
        json['parent'] = json.copy()
        r = repos.Repository(json)
        expect(r.parent).isinstance(repos.Repository)

    def test_pull_request(self):
        self.response('pull', 200)
        self.get(self.api + 'pulls/2')

        expect(self.repo.pull_request(0)).is_None()
        self.not_called()

        expect(self.repo.pull_request(2)).isinstance(github3.pulls.PullRequest)
        self.mock_assertions()

    def test_readme(self):
        self.response('readme', 200)
        self.get(self.api + 'readme')

        expect(self.repo.readme()).isinstance(repos.contents.Contents)
        self.mock_assertions()

    def test_ref(self):
        self.response('ref', 200)
        self.get(self.api + 'git/refs/fakesha')

        expect(self.repo.ref(None)).is_None()
        self.not_called()

        expect(self.repo.ref('fakesha')).isinstance(github3.git.Reference)
        self.mock_assertions()

    def test_remove_collaborator(self):
        self.response('', 204)
        self.delete(self.api + 'collaborators/login')

        with expect.githuberror():
            self.repo.remove_collaborator(None)
        self.not_called()

        self.login()
        expect(self.repo.remove_collaborator(None)).is_False()
        self.not_called()

        expect(self.repo.remove_collaborator('login')).is_True()
        self.mock_assertions()

    def test_repr(self):
        expect(repr(self.repo)) == '<Repository [sigmavirus24/github3.py]>'

    def test_source(self):
        json = self.repo.to_json().copy()
        json['source'] = json.copy()
        r = repos.Repository(json)
        expect(r.source).isinstance(repos.Repository)

    def test_set_subscription(self):
        self.response('subscription')
        self.put(self.api + 'subscription')
        self.conf = {'data': {'subscribed': True, 'ignored': False}}

        with expect.githuberror():
            self.repo.set_subscription(True, False)
        self.not_called()

        self.login()
        s = self.repo.set_subscription(True, False)
        expect(s).isinstance(github3.notifications.Subscription)
        self.mock_assertions()

    def test_subscription(self):
        self.response('subscription')
        self.get(self.api + 'subscription')

        with expect.githuberror():
            self.repo.subscription()
        self.not_called()

        self.login()
        s = self.repo.subscription()
        expect(s).isinstance(github3.notifications.Subscription)
        self.mock_assertions()

    def test_tag(self):
        self.response('tag')
        self.get(self.api + 'git/tags/fakesha')

        expect(self.repo.tag(None)).is_None()
        self.not_called()

        expect(self.repo.tag('fakesha')).isinstance(github3.git.Tag)
        self.mock_assertions()

    def test_tree(self):
        self.response('tree')
        self.get(self.api + 'git/trees/fakesha')

        expect(self.repo.tree(None)).is_None()
        self.not_called()

        expect(self.repo.tree('fakesha')).isinstance(github3.git.Tree)
        self.mock_assertions()

    def test_update_label(self):
        self.response('label', 200)
        self.patch(self.api + 'labels/bug')
        self.conf = {'data': {'name': 'big_bug', 'color': 'fafafa'}}

        with expect.githuberror():
            self.repo.update_label('foo', 'bar')
        self.not_called()

        self.login()
        with patch.object(repos.Repository, 'label') as l:
            l.return_value = None
            expect(self.repo.update_label('foo', 'bar')).is_False()
            self.not_called()

        with patch.object(repos.Repository, 'label') as l:
            l.return_value = github3.issues.label.Label(load('label'), self.g)
            expect(self.repo.update_label('big_bug', 'fafafa')).is_True()

        self.mock_assertions()

    def test_equality(self):
        expect(self.repo) == repos.Repository(load('repo'))


class TestContents(BaseCase):
    def __init__(self, methodName='runTest'):
        super(TestContents, self).__init__(methodName)
        self.contents = repos.contents.Contents(load('readme'))

    def test_git_url(self):
        expect(self.contents.links['git']) == self.contents.git_url

    def test_html_url(self):
        expect(self.contents.links['html']) == self.contents.html_url

    def test_repr(self):
        expect(repr(self.contents)) == '<Content [{0}]>'.format('README.rst')

    def test_str(self):
        expect(str(self.contents)) == self.contents.decoded


class TestDownload(BaseCase):
    def __init__(self, methodName='runTest'):
        super(TestDownload, self).__init__(methodName)
        self.dl = repos.download.Download(load('download'))
        self.api = ("https://api.github.com/repos/sigmavirus24/github3.py/"
                    "downloads/338893")

    def setUp(self):
        super(TestDownload, self).setUp()
        self.dl = repos.download.Download(self.dl.to_json(), self.g)

    def test_repr(self):
        expect(repr(self.dl)) == '<Download [kr.png]>'

    def test_delete(self):
        self.response('', 204)
        self.delete(self.api)

        with expect.githuberror():
            self.dl.delete()
        self.not_called()

        self.login()
        expect(self.dl.delete()).is_True()
        self.mock_assertions()

    def test_saveas(self):
        self.response('archive', 200)
        self.get(self.dl.html_url)

        o = mock_open()
        with patch('{0}.open'.format(__name__), o, create=True):
            with open('archive', 'wb+') as fd:
                expect(self.dl.saveas(fd)).is_True()

        o.assert_called_once_with('archive', 'wb+')
        fd = o()
        fd.write.assert_called_once_with(b'archive_data')
        self.mock_assertions()

        self.request.return_value.raw.seek(0)
        self.request.return_value._content_consumed = False

        self.dl.saveas()
        expect(os.path.isfile(self.dl.name)).is_True()
        os.unlink(self.dl.name)
        expect(os.path.isfile(self.dl.name)).is_False()

        self.request.return_value.raw.seek(0)
        self.request.return_value._content_consumed = False

        self.dl.saveas('tmp')
        expect(os.path.isfile('tmp')).is_True()
        os.unlink('tmp')
        expect(os.path.isfile('tmp')).is_False()

        self.response('', 404)
        expect(self.dl.saveas()).is_False()


class TestHook(BaseCase):
    def __init__(self, methodName='runTest'):
        super(TestHook, self).__init__(methodName)
        self.hook = repos.hook.Hook(load('hook'))
        self.api = ("https://api.github.com/repos/sigmavirus24/github3.py/"
                    "hooks/292492")

    def setUp(self):
        super(TestHook, self).setUp()
        self.hook = repos.hook.Hook(self.hook.to_json(), self.g)

    def test_equality(self):
        h = repos.hook.Hook(load('hook'))
        expect(self.hook) == h
        h.id = 1
        expect(self.hook) != h

    def test_repr(self):
        expect(repr(self.hook)) == '<Hook [readthedocs]>'

    def test_delete(self):
        self.response('', 204)
        self.delete(self.api)

        with expect.githuberror():
            self.hook.delete()
        self.not_called()

        self.login()
        expect(self.hook.delete()).is_True()
        self.mock_assertions()

    def test_delete_subscription(self):
        self.response('', 204)
        self.delete(self.api + '/subscription')

        with expect.githuberror():
            self.hook.delete_subscription()
        self.not_called()

        self.login()
        expect(self.hook.delete_subscription()).is_True()
        self.mock_assertions()

    def test_edit(self):
        self.response('hook', 200)
        self.patch(self.api)
        data = {
            'name': 'hookname',
            'config': {'push': 'http://example.com'},
            'events': ['push'],
            'add_events': ['fake_ev'],
            'rm_events': ['fake_ev'],
            'active': True,
        }
        self.conf = {'data': data.copy()}
        self.conf['data']['remove_events'] = data['rm_events']
        del(self.conf['data']['rm_events'])

        with expect.githuberror():
            self.hook.edit(**data)

        self.login()
        expect(self.hook.edit(None, None, None)).is_False()
        expect(self.hook.edit('True', None, None)).is_False()
        expect(self.hook.edit(None, 'True', None)).is_False()
        expect(self.hook.edit(None, None, {})).is_False()
        self.not_called()

        expect(self.hook.edit(**data)).is_True()
        self.mock_assertions()

    def test_test(self):
        # Funny name, no?
        self.response('', 204)
        self.post(self.api + '/tests')
        self.conf = {}

        with expect.githuberror():
            self.hook.test()
        self.not_called()

        self.login()
        expect(self.hook.test()).is_True()
        self.mock_assertions()


class TestRepoComment(BaseCase):
    def __init__(self, methodName='runTest'):
        super(TestRepoComment, self).__init__(methodName)
        self.comment = repos.comment.RepoComment(load('repo_comment'))
        self.api = ("https://api.github.com/repos/sigmavirus24/github3.py/"
                    "comments/1380832")

    def setUp(self):
        super(TestRepoComment, self).setUp()
        self.comment = repos.comment.RepoComment(self.comment.to_json(),
                                                 self.g)

    def test_delete(self):
        self.response('', 204)
        self.delete(self.api)

        with expect.githuberror():
            self.comment.delete()

        self.not_called()
        self.login()

        expect(self.comment.delete()).is_True()
        self.mock_assertions()

    def test_repr(self):
        expect(repr(self.comment).startswith('<Repository Comment'))

    def test_update(self):
        self.post(self.api)
        self.response('repo_comment', 200)
        self.conf = {'data': {'body': 'This is a comment body'}}

        with expect.githuberror():
            self.comment.update('foo')

        self.login()
        expect(self.comment.update(None)).is_False()
        self.not_called()

        expect(self.comment.update('This is a comment body')).is_True()
        self.mock_assertions()


class TestRepoCommit(BaseCase):
    def __init__(self, methodName='runTest'):
        super(TestRepoCommit, self).__init__(methodName)
        self.commit = repos.commit.RepoCommit(load('commit'))
        self.api = ("https://api.github.com/repos/sigmavirus24/github3.py/"
                    "commits/76dcc6cb4b9860034be81b7e58adc286a115aa97")

    def test_equality(self):
        c = repos.commit.RepoCommit(load('commit'))
        expect(self.commit) == c
        c.sha = 'fake'
        expect(self.commit) != c

    def test_repr(self):
        expect(repr(self.commit).startswith('<Repository Commit')).is_True()

    def test_diff(self):
        self.response('archive', 200)
        self.get(self.api)
        self.conf.update(headers={'Accept': 'application/vnd.github.diff'})

        expect(self.commit.diff().startswith(b'archive_data')).is_True()
        self.mock_assertions()

    def test_patch(self):
        self.response('archive', 200)
        self.get(self.api)
        self.conf.update(headers={'Accept': 'application/vnd.github.patch'})

        expect(self.commit.patch().startswith(b'archive_data')).is_True()
        self.mock_assertions()


class TestComparison(BaseCase):
    def __init__(self, methodName='runTest'):
        super(TestComparison, self).__init__(methodName)
        self.comp = repos.comparison.Comparison(load('comparison'))
        self.api = ("https://api.github.com/repos/sigmavirus24/github3.py/"
                    "compare/a811e1a270f65eecb65755eca38d888cbefcb0a7..."
                    "76dcc6cb4b9860034be81b7e58adc286a115aa97")

    def test_repr(self):
        expect(repr(self.comp).startswith('<Comparison ')).is_True()

    def test_diff(self):
        self.response('archive', 200)
        self.get(self.api)
        self.conf.update(headers={'Accept': 'application/vnd.github.diff'})

        expect(self.comp.diff().startswith(b'archive_data')).is_True()
        self.mock_assertions()

    def test_patch(self):
        self.response('archive', 200)
        self.get(self.api)
        self.conf.update(headers={'Accept': 'application/vnd.github.patch'})

        expect(self.comp.patch().startswith(b'archive_data')).is_True()
        self.mock_assertions()
