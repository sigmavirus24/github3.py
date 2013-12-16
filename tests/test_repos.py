import os
import github3
from github3 import repos
from datetime import datetime
from tests.utils import (BaseCase, load)
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

        self.assertRaises(github3.GitHubError, self.repo.add_collaborator,
                          'foo')

        self.login()
        assert self.repo.add_collaborator(None) is False
        assert self.repo.add_collaborator('sigmavirus24')
        self.mock_assertions()

    def test_archive(self):
        headers = {'content-disposition': 'filename=foo'}
        self.response('archive', 200, **headers)
        self.get(self.api + 'tarball/master')
        self.conf.update({'stream': True})

        assert self.repo.archive(None) is False

        assert os.path.isfile('foo') is False
        assert self.repo.archive('tarball')
        assert os.path.isfile('foo')
        os.unlink('foo')
        self.mock_assertions()

        self.request.return_value.raw.seek(0)
        self.request.return_value._content_consumed = False

        assert os.path.isfile('path_to_file') is False
        assert self.repo.archive('tarball', 'path_to_file')
        assert os.path.isfile('path_to_file')
        os.unlink('path_to_file')

        self.request.return_value.raw.seek(0)
        self.request.return_value._content_consumed = False

        self.get(self.api + 'zipball/randomref')
        assert self.repo.archive('zipball', ref='randomref')
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
        assert isinstance(blob, github3.git.Blob)
        assert repr(blob).startswith('<Blob')
        self.mock_assertions()

    def test_branch(self):
        self.response('branch')
        self.get(self.api + 'branches/master')

        b = self.repo.branch('master')
        assert isinstance(b, repos.branch.Branch)
        self.mock_assertions()

        assert repr(b) == '<Repository Branch [master]>'

    def test_commit(self):
        self.response('commit')
        sha = '76dcc6cb4b9860034be81b7e58adc286a115aa97'
        self.get(self.api + 'commits/' + sha)

        assert isinstance(self.repo.commit(sha), repos.commit.RepoCommit)
        self.mock_assertions()

    def test_commit_comment(self):
        self.response('commit_comment')
        comment_id = 1380832
        self.get(self.api + 'comments/{0}'.format(comment_id))

        assert isinstance(self.repo.commit_comment(comment_id),
                          repos.comment.RepoComment)
        self.mock_assertions()

    def test_compare_commits(self):
        self.response('comparison')
        base = 'a811e1a270f65eecb65755eca38d888cbefcb0a7'
        head = '76dcc6cb4b9860034be81b7e58adc286a115aa97'
        self.get(self.api + 'compare/{0}...{1}'.format(base, head))

        assert isinstance(self.repo.compare_commits(base, head),
                          repos.comparison.Comparison)
        self.mock_assertions()

    def test_contents(self):
        self.response('contents')
        filename = 'setup.py'
        self.get(self.api + 'contents/' + filename)

        assert isinstance(self.repo.contents(filename),
                          repos.contents.Contents)
        self.mock_assertions()

        self.response('', 404)
        assert self.repo.contents(filename) is None

        self.response('contents', _iter=True)
        files = self.repo.contents(filename)
        assert isinstance(files, dict)

        self.mock_assertions()

    def test_contents_ref(self):
        self.response('contents')
        filename = 'setup.py'
        self.get(self.api + 'contents/' + filename)
        self.conf = {'params': {'ref': 'foo'}}

        assert isinstance(self.repo.contents(filename, ref='foo'),
                          repos.contents.Contents)
        self.mock_assertions()

    def test_create_blob(self):
        self.response('blob', 201)
        content = 'VGVzdCBibG9i\n'
        encoding = 'base64'
        sha = '30f2c645388832f70d37ab2b47eb9ea527e5ae7c'
        self.post(self.api + 'git/blobs')
        self.conf = {'data': {'content': content, 'encoding': encoding}}

        self.assertRaises(github3.GitHubError, self.repo.create_blob,
                          content, encoding)

        self.login()
        assert self.repo.create_blob(None, None) == ''
        assert self.repo.create_blob(content, encoding) == sha
        self.mock_assertions()

    def test_create_comment(self):
        self.response('commit_comment', 201)
        body = ('Late night commits are never a good idea. I refactored a '
                'bit. `User` objects and `Organization` objects share a lot '
                'of common attributes. I turned those common attributes into '
                'one `BaseAccount` class to make things simpler. ')
        sha = 'd41566090114a752eb3a87dbcf2473eb427ef0f3'
        self.post(self.api + 'commits/{0}/comments'.format(sha))
        self.conf = {'data': {'body': body, 'line': 1}}

        self.assertRaises(github3.GitHubError, self.repo.create_comment,
                          body, sha)

        self.login()
        assert self.repo.create_comment(None, None) is None
        assert self.repo.create_comment(body, sha, line=0) is None
        assert isinstance(self.repo.create_comment(body, sha),
                          repos.comment.RepoComment)
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

        self.assertRaises(github3.GitHubError, self.repo.create_commit, **data)

        self.login()
        assert self.repo.create_commit(None, None, None) is None
        assert isinstance(self.repo.create_commit(**data), github3.git.Commit)
        self.mock_assertions()

    def test_create_fork(self):
        self.response('repo', 202)
        self.conf = {'data': None}
        self.post(self.api + 'forks')

        self.assertRaises(github3.GitHubError, self.repo.create_fork)

        self.login()
        assert isinstance(self.repo.create_fork(), repos.Repository)
        self.mock_assertions()

        self.conf['data'] = {'organization': 'github3py'}
        assert isinstance(self.repo.create_fork('github3py'), repos.Repository)
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

        self.assertRaises(github3.GitHubError, self.repo.create_hook,
                          None, None)

        self.login()
        assert self.repo.create_hook(None, {'foo': 'bar'}) is None
        assert self.repo.create_hook('name', None) is None
        assert self.repo.create_hook('name', 'bar') is None
        self.not_called()

        h = self.repo.create_hook(**self.conf['data'])
        assert isinstance(h, repos.hook.Hook)
        self.mock_assertions()

    def test_create_issue(self):
        self.response('issue', 201)
        title = 'Construct _api attribute on our own'
        self.post(self.api + 'issues')
        self.conf = {'data': {'title': title}}

        self.assertRaises(github3.GitHubError, self.repo.create_issue, title)

        self.login()
        assert self.repo.create_issue(None) is None
        assert isinstance(self.repo.create_issue(title), github3.issues.Issue)
        self.mock_assertions()

        body = 'Fake body'
        #self.conf['data'].update(body=body)
        assert isinstance(self.repo.create_issue(title, body),
                          github3.issues.Issue)
        self.mock_assertions()

        assignee, mile, labels = 'sigmavirus24', 1, ['bug', 'enhancement']
        #self.conf['data'].update({'assignee': assignee, 'milestone': mile,
        #                          'labels': labels})
        issue = self.repo.create_issue(title, body, assignee, mile, labels)
        assert isinstance(issue, github3.issues.Issue)
        self.mock_assertions()

    def test_create_key(self):
        self.response('key', 201)
        self.post(self.api + 'keys')
        self.conf = {'data': {'key': 'ssh-rsa foobarbogus',
                              'title': 'Fake key'}}

        self.assertRaises(github3.GitHubError, self.repo.create_key,
                          **self.conf['data'])

        self.login()
        assert self.repo.create_key(None, None) is None
        self.not_called()
        assert isinstance(self.repo.create_key(**self.conf['data']),
                          github3.users.Key)
        self.mock_assertions()

    def test_create_label(self):
        self.response('label', 201)
        self.post(self.api + 'labels')
        self.conf = {'data': {'name': 'foo', 'color': 'f00f00'}}

        self.assertRaises(github3.GitHubError, self.repo.create_label,
                          **self.conf['data'])

        self.login()
        assert self.repo.create_label(None, None) is None
        self.not_called()
        assert isinstance(self.repo.create_label(**self.conf['data']),
                          github3.issues.label.Label)
        self.mock_assertions()

    def test_create_milestone(self):
        self.response('milestone', 201)
        self.post(self.api + 'milestones')
        self.conf = {'data': {'title': 'foo'}}

        self.assertRaises(github3.GitHubError, self.repo.create_milestone,
                          **self.conf['data'])

        self.login()
        assert self.repo.create_milestone(None) is None
        self.not_called()
        assert isinstance(self.repo.create_milestone('foo'),
                          github3.issues.milestone.Milestone)
        self.mock_assertions()

    def test_create_pull(self):
        self.response('pull', 201)
        self.post(self.api + 'pulls')
        self.conf = {'data': {'title': 'Fake title', 'base': 'master',
                              'head': 'feature_branch'}}

        self.assertRaises(github3.GitHubError, self.repo.create_pull,
                          **self.conf['data'])

        self.login()
        assert self.repo.create_pull(None, None, None) is None
        self.not_called()
        assert isinstance(self.repo.create_pull(**self.conf['data']),
                          github3.pulls.PullRequest)
        self.mock_assertions()

    def test_create_pull_from_issue(self):
        self.response('pull', 201)
        self.post(self.api + 'pulls')
        self.conf = {'data': {'issue': 1, 'base': 'master',
                              'head': 'feature_branch'}}

        self.assertRaises(github3.GitHubError,
                          self.repo.create_pull_from_issue,
                          **self.conf['data'])

        self.login()
        assert self.repo.create_pull_from_issue(0, 'foo', 'bar') is None
        self.not_called()
        pull = self.repo.create_pull_from_issue(**self.conf['data'])
        assert isinstance(pull, github3.pulls.PullRequest)
        self.mock_assertions()

    def test_create_ref(self):
        self.response('ref', 201)
        self.post(self.api + 'git/refs')
        self.conf = {'data': {'ref': 'refs/heads/master', 'sha': 'fakesha'}}

        self.assertRaises(github3.GitHubError, self.repo.create_ref,
                          'foo', 'bar')

        self.login()
        assert self.repo.create_ref('foo/bar', None) is None
        assert isinstance(self.repo.create_ref(**self.conf['data']),
                          github3.git.Reference)
        self.mock_assertions()

    def test_create_status(self):
        self.response('status', 201)
        self.post(self.api + 'statuses/fakesha')
        self.conf = {'data': {'state': 'success'}}

        self.assertRaises(github3.GitHubError, self.repo.create_status,
                          'fakesha', 'success')

        self.login()
        assert self.repo.create_status(None, None) is None
        s = self.repo.create_status('fakesha', 'success')
        assert isinstance(s, repos.status.Status)
        assert repr(s) > ''
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

        self.assertRaises(github3.GitHubError, self.repo.create_tag,
                          None, None, None, None, None)

        self.login()
        with patch.object(repos.Repository, 'create_ref'):
            assert self.repo.create_tag(None, None, None, None,
                                        None) is None
            tag = self.repo.create_tag(**data)
            assert isinstance(tag, github3.git.Tag)
            assert repr(tag).startswith('<Tag')
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

        self.assertRaises(github3.GitHubError, self.repo.create_tree, **data)

        self.login()
        assert self.repo.create_tree(None) is None
        assert self.repo.create_tree({'foo': 'bar'}) is None
        self.not_called()
        assert isinstance(self.repo.create_tree(**data), github3.git.Tree)
        self.mock_assertions()

    def test_delete(self):
        self.response('', 204)
        self.delete(self.api[:-1])
        self.conf = {}

        self.assertRaises(github3.GitHubError, self.repo.delete)

        self.login()
        assert self.repo.delete()
        self.mock_assertions()

    def test_delete_key(self):
        self.response('', 204)
        self.delete(self.api + 'keys/2')
        self.conf = {}

        self.assertRaises(github3.GitHubError, self.repo.delete_key, 2)

        self.login()
        assert self.repo.delete_key(-2) is False
        self.not_called()
        assert self.repo.delete_key(2)
        self.mock_assertions()

    def test_edit(self):
        self.response('repo')
        self.patch(self.api[:-1])
        self.conf = {'data': {'name': 'foo'}}

        self.assertRaises(github3.GitHubError, self.repo.edit, 'Foo')

        self.login()
        assert self.repo.edit(None) is False
        self.not_called()
        assert self.repo.edit('foo')
        self.mock_assertions()

        self.conf['data']['description'] = 'bar'
        assert self.repo.edit(**self.conf['data'])
        self.mock_assertions()

    def test_is_collaborator(self):
        self.response('', 204)
        self.get(self.api + 'collaborators/user')

        assert self.repo.is_collaborator(None) is False
        self.not_called()
        assert self.repo.is_collaborator('user')
        self.mock_assertions()

    def test_git_commit(self):
        self.response('git_commit')
        self.get(self.api + 'git/commits/fakesha')

        assert self.repo.git_commit(None) is None
        self.not_called()
        assert isinstance(self.repo.git_commit('fakesha'), github3.git.Commit)
        self.mock_assertions()

    def test_hook(self):
        self.response('hook')
        self.get(self.api + 'hooks/2')

        self.assertRaises(github3.GitHubError, self.repo.hook, 2)

        self.login()
        assert self.repo.hook(-2) is None
        self.not_called()
        assert isinstance(self.repo.hook(2), repos.hook.Hook)
        self.mock_assertions()

    def test_is_assignee(self):
        self.response('', 204)
        self.get(self.api + 'assignees/login')

        assert self.repo.is_assignee(None) is False
        self.not_called()
        assert self.repo.is_assignee('login')
        self.mock_assertions()

    def test_issue(self):
        self.response('issue')
        self.get(self.api + 'issues/2')

        assert self.repo.issue(-2) is None
        self.not_called()
        assert isinstance(self.repo.issue(2), github3.issues.Issue)
        self.mock_assertions()

    def test_key(self):
        self.response('key')
        self.get(self.api + 'keys/2')

        self.assertRaises(github3.GitHubError, self.repo.key, 2)

        self.login()
        assert self.repo.key(-2) is None
        self.not_called()
        assert isinstance(self.repo.key(2), github3.users.Key)
        self.mock_assertions()

    def test_label(self):
        self.response('label')
        self.get(self.api + 'labels/name')

        assert self.repo.label(None) is None
        self.not_called()
        assert isinstance(self.repo.label('name'), github3.issues.label.Label)
        self.mock_assertions()

    def test_iter_assignees(self):
        self.response('user', _iter=True)
        self.get(self.api + 'assignees')
        self.conf = {'params': {'per_page': 100}}

        u = next(self.repo.iter_assignees())
        assert isinstance(u, github3.users.User)
        self.mock_assertions()

    def test_iter_branches(self):
        self.response('branch', _iter=True)
        self.get(self.api + 'branches')
        self.conf = {'params': {'per_page': 100}}

        b = next(self.repo.iter_branches())
        assert isinstance(b, repos.branch.Branch)
        self.mock_assertions()

    def test_iter_comments(self):
        self.response('repo_comment', _iter=True)
        self.get(self.api + 'comments')
        self.conf = {'params': {'per_page': 100}}

        c = next(self.repo.iter_comments())
        assert isinstance(c, repos.comment.RepoComment)
        self.mock_assertions()

    def test_iter_comments_on_commit(self):
        self.response('repo_comment', _iter=True)
        self.get(self.api + 'commits/fakesha/comments')
        self.conf = {'params': {'per_page': 1}}

        c = next(self.repo.iter_comments_on_commit('fakesha'))
        assert isinstance(c, repos.comment.RepoComment)
        self.mock_assertions()

    def test_iter_commits(self):
        self.response('commit', _iter=True)
        self.get(self.api + 'commits')
        self.conf = {'params': {'per_page': 100}}

        c = next(self.repo.iter_commits())
        assert isinstance(c, repos.commit.RepoCommit)
        self.mock_assertions()

        self.conf = {'params': {'sha': 'fakesha', 'path': '/',
                                'per_page': 100}}
        c = next(self.repo.iter_commits('fakesha', '/'))
        self.mock_assertions()

        since = datetime(2013, 6, 1, 0, 0, 0)
        until = datetime(2013, 6, 2, 0, 0, 0)
        self.conf = {'params': {'since': '2013-06-01T00:00:00',
                                'until': '2013-06-02T00:00:00',
                                'per_page': 100}}
        c = next(self.repo.iter_commits(since=since, until=until))
        self.mock_assertions()

        since = '2013-06-01T00:00:00'
        until = '2013-06-02T00:00:00'
        self.conf = {'params': {'since': '2013-06-01T00:00:00',
                                'until': '2013-06-02T00:00:00',
                                'per_page': 100}}
        c = next(self.repo.iter_commits(since=since, until=until))
        self.mock_assertions()

    def test_iter_contributors(self):
        self.response('user', _iter=True)
        self.get(self.api + 'contributors')
        self.conf = {'params': {'per_page': 100}}

        u = next(self.repo.iter_contributors())
        assert isinstance(u, github3.users.User)
        self.mock_assertions()

        self.conf = {'params': {'anon': True, 'per_page': 100}}
        next(self.repo.iter_contributors(True))
        self.mock_assertions()

        next(self.repo.iter_contributors('true value'))
        self.mock_assertions()

    def test_iter_events(self):
        self.response('event', _iter=True)
        self.get(self.api + 'events')
        self.conf = {'params': {'per_page': 100}}

        e = next(self.repo.iter_events())
        assert isinstance(e, github3.events.Event)
        self.mock_assertions()

    def test_iter_forks(self):
        self.response('repo', _iter=True)
        self.get(self.api + 'forks')
        self.conf = {'params': {'per_page': 100}}

        r = next(self.repo.iter_forks())
        assert isinstance(r, repos.Repository)
        self.mock_assertions()

        self.conf['params']['sort'] = 'newest'
        forks_params = self.conf['params'].copy()
        forks_params.pop('per_page')
        next(self.repo.iter_forks(**forks_params))
        self.mock_assertions()

    def test_iter_hooks(self):
        self.response('hook', _iter=True)
        self.get(self.api + 'hooks')
        self.conf = {'params': {'per_page': 100}}

        self.assertRaises(github3.GitHubError, self.repo.iter_hooks)

        self.login()
        h = next(self.repo.iter_hooks())
        assert isinstance(h, repos.hook.Hook)
        self.mock_assertions()

    def test_iter_issues(self):
        self.response('issue', _iter=True)
        self.get(self.api + 'issues')
        params = {'per_page': 100}
        self.conf = {'params': params}

        i = next(self.repo.iter_issues())
        assert isinstance(i, github3.issues.Issue)
        self.mock_assertions()

        params['milestone'] = 'none'
        next(self.repo.iter_issues('none'))
        self.mock_assertions()

        params['state'] = 'open'

        request_params = params.copy()
        request_params.pop('per_page')
        next(self.repo.iter_issues(**request_params))
        self.mock_assertions()

    def test_iter_issue_events(self):
        self.response('issue_event', _iter=True)
        self.get(self.api + 'issues/events')
        self.conf = {'params': {'per_page': 100}}

        e = next(self.repo.iter_issue_events())
        assert isinstance(e, github3.issues.event.IssueEvent)
        self.mock_assertions()

    def test_iter_keys(self):
        self.response('key', _iter=True)
        self.get(self.api + 'keys')

        self.assertRaises(github3.GitHubError, self.repo.iter_keys)

        self.login()
        k = next(self.repo.iter_keys())
        assert isinstance(k, github3.users.Key)
        self.mock_assertions()

    def test_iter_labels(self):
        self.response('label', _iter=True)
        self.get(self.api + 'labels')

        l = next(self.repo.iter_labels())
        assert isinstance(l, github3.issues.label.Label)
        self.mock_assertions()

    def test_iter_languages(self):
        #: repos/:login/:repo/languages is just a dictionary, so _iter=False
        self.response('language')
        self.get(self.api + 'languages')

        l = next(self.repo.iter_languages())
        assert isinstance(l, tuple)
        self.assertNotIn('ETag', l)
        self.assertNotIn('Last-Modified', l)
        self.mock_assertions()

    def test_iter_milestones(self):
        self.response('milestone', _iter=True)
        self.get(self.api + 'milestones')

        m = next(self.repo.iter_milestones())
        assert isinstance(m, github3.issues.milestone.Milestone)
        self.mock_assertions()

    def test_iter_network_events(self):
        self.response('event', _iter=True)
        self.get(self.api.replace('repos', 'networks', 1) + 'events')

        e = next(self.repo.iter_network_events())
        assert isinstance(e, github3.events.Event)
        self.mock_assertions()

    def test_iter_notifications(self):
        self.response('notification', _iter=True)
        self.get(self.api + 'notifications')
        self.conf.update(params={'per_page': 100})

        self.assertRaises(github3.GitHubError, self.repo.iter_notifications)

        self.login()
        n = next(self.repo.iter_notifications())
        assert isinstance(n, github3.notifications.Thread)
        self.mock_assertions()

    def test_iter_pulls(self):
        self.response('pull', _iter=True)
        self.get(self.api + 'pulls')
        self.conf.update(params={'per_page': 100})

        p = next(self.repo.iter_pulls())
        assert isinstance(p, github3.pulls.PullRequest)
        self.mock_assertions()

        next(self.repo.iter_pulls('foo'))
        self.mock_assertions()

        self.conf.update(params={'state': 'open', 'per_page': 100})
        next(self.repo.iter_pulls('Open'))
        self.mock_assertions()

        self.conf.update(params={'head': 'user:branch', 'per_page': 100})
        next(self.repo.iter_pulls(head='user:branch'))
        self.mock_assertions()

        self.conf.update(params={'base': 'branch', 'per_page': 100})
        next(self.repo.iter_pulls(base='branch'))
        self.mock_assertions()

    def test_iter_refs(self):
        self.response('ref', _iter=True)
        self.get(self.api + 'git/refs')

        r = next(self.repo.iter_refs())
        assert isinstance(r, github3.git.Reference)
        self.mock_assertions()

        self.get(self.api + 'git/refs/subspace')
        r = next(self.repo.iter_refs('subspace'))
        assert isinstance(r, github3.git.Reference)
        self.mock_assertions()

    def test_iter_stargazers(self):
        self.response('user', _iter=True)
        self.get(self.api + 'stargazers')

        u = next(self.repo.iter_stargazers())
        assert isinstance(u, github3.users.User)
        self.mock_assertions()

    def test_iter_subscribers(self):
        self.response('user', _iter=True)
        self.get(self.api + 'subscribers')

        u = next(self.repo.iter_subscribers())
        assert isinstance(u, github3.users.User)
        self.mock_assertions()

    def test_iter_statuses(self):
        self.response('status', _iter=True)
        self.get(self.api + 'statuses/fakesha')

        with self.assertRaises(StopIteration):
            next(self.repo.iter_statuses(None))
        self.not_called()

        s = next(self.repo.iter_statuses('fakesha'))
        assert isinstance(s, repos.status.Status)
        self.mock_assertions()

    def test_iter_tags(self):
        self.response('tag', _iter=True)
        self.get(self.api + 'tags')

        t = next(self.repo.iter_tags())
        assert isinstance(t, repos.tag.RepoTag)
        self.mock_assertions()

        assert repr(t).startswith('<Repository Tag')
        assert str(t) > ''

    def test_iter_teams(self):
        self.response('team', _iter=True)
        self.get(self.api + 'teams')

        self.assertRaises(github3.GitHubError, self.repo.iter_teams)
        self.not_called()

        self.login()
        t = next(self.repo.iter_teams())
        assert isinstance(t, github3.orgs.Team)
        self.mock_assertions()

    def test_mark_notifications(self):
        self.response('', 205)
        self.put(self.api + 'notifications')
        self.conf = {'data': {'read': True}}

        self.assertRaises(github3.GitHubError, self.repo.mark_notifications)
        self.not_called()

        self.login()
        assert self.repo.mark_notifications()
        self.mock_assertions()

        assert self.repo.mark_notifications('2013-01-18T19:53:04Z')
        self.conf['data']['last_read_at'] = '2013-01-18T19:53:04Z'
        self.mock_assertions()

    def test_merge(self):
        self.response('commit', 201)
        self.post(self.api + 'merges')
        self.conf = {'data': {'base': 'master', 'head': 'sigma/feature'}}

        self.assertRaises(github3.GitHubError, self.repo.merge, 'foo', 'bar')
        self.not_called()

        self.login()
        assert isinstance(self.repo.merge('master', 'sigma/feature'),
                          repos.commit.RepoCommit)
        self.mock_assertions()

        self.conf['data']['commit_message'] = 'Commit message'
        self.repo.merge('master', 'sigma/feature', 'Commit message')
        self.mock_assertions()

    def test_milestone(self):
        self.response('milestone', 200)
        self.get(self.api + 'milestones/2')

        assert self.repo.milestone(0) is None
        self.not_called()

        assert isinstance(self.repo.milestone(2),
                          github3.issues.milestone.Milestone)
        self.mock_assertions()

    def test_parent(self):
        json = self.repo.to_json().copy()
        json['parent'] = json.copy()
        r = repos.Repository(json)
        assert isinstance(r.parent, repos.Repository)

    def test_pull_request(self):
        self.response('pull', 200)
        self.get(self.api + 'pulls/2')

        assert self.repo.pull_request(0) is None
        self.not_called()

        assert isinstance(self.repo.pull_request(2), github3.pulls.PullRequest)
        self.mock_assertions()

    def test_readme(self):
        self.response('readme', 200)
        self.get(self.api + 'readme')

        assert isinstance(self.repo.readme(), repos.contents.Contents)
        self.mock_assertions()

    def test_ref(self):
        self.response('ref', 200)
        self.get(self.api + 'git/refs/fakesha')

        assert self.repo.ref(None) is None
        self.not_called()

        assert isinstance(self.repo.ref('fakesha'), github3.git.Reference)
        self.mock_assertions()

    def test_remove_collaborator(self):
        self.response('', 204)
        self.delete(self.api + 'collaborators/login')

        self.assertRaises(github3.GitHubError, self.repo.remove_collaborator,
                          None)
        self.not_called()

        self.login()
        assert self.repo.remove_collaborator(None) is False
        self.not_called()

        assert self.repo.remove_collaborator('login')
        self.mock_assertions()

    def test_repr(self):
        assert repr(self.repo) == '<Repository [sigmavirus24/github3.py]>'

    def test_source(self):
        json = self.repo.to_json().copy()
        json['source'] = json.copy()
        r = repos.Repository(json)
        assert isinstance(r.source, repos.Repository)

    def test_set_subscription(self):
        self.response('subscription')
        self.put(self.api + 'subscription')
        self.conf = {'data': {'subscribed': True, 'ignored': False}}

        self.assertRaises(github3.GitHubError, self.repo.set_subscription,
                          True, False)
        self.not_called()

        self.login()
        s = self.repo.set_subscription(True, False)
        assert isinstance(s, github3.notifications.Subscription)
        self.mock_assertions()

    def test_subscription(self):
        self.response('subscription')
        self.get(self.api + 'subscription')

        self.assertRaises(github3.GitHubError, self.repo.subscription)
        self.not_called()

        self.login()
        s = self.repo.subscription()
        assert isinstance(s, github3.notifications.Subscription)
        self.mock_assertions()

    def test_tag(self):
        self.response('tag')
        self.get(self.api + 'git/tags/fakesha')

        assert self.repo.tag(None) is None
        self.not_called()

        assert isinstance(self.repo.tag('fakesha'), github3.git.Tag)
        self.mock_assertions()

    def test_tree(self):
        self.response('tree')
        self.get(self.api + 'git/trees/fakesha')

        assert self.repo.tree(None) is None
        self.not_called()

        assert isinstance(self.repo.tree('fakesha'), github3.git.Tree)
        self.mock_assertions()

    def test_update_label(self):
        self.response('label')
        self.patch(self.api + 'labels/Bug')
        self.conf = {'data': {'name': 'big_bug', 'color': 'fafafa'}}

        self.assertRaises(github3.GitHubError, self.repo.update_label,
                          'foo', 'bar')
        self.not_called()

        self.login()
        with patch.object(repos.Repository, 'label') as l:
            l.return_value = None
            assert self.repo.update_label('foo', 'bar') is False
            self.not_called()

        with patch.object(repos.Repository, 'label') as l:
            l.return_value = github3.issues.label.Label(load('label'), self.g)
            assert self.repo.update_label('big_bug', 'fafafa')

        self.mock_assertions()

    def test_equality(self):
        assert self.repo == repos.Repository(load('repo'))

    def test_create_file(self):
        self.response('create_content', 201)
        self.put(self.api + 'contents/setup.py')
        self.conf = {'data': {'message': 'Foo bar',
                              'content': 'Zm9vIGJhciBib2d1cw==',
                              'branch': 'develop',
                              'author': {'name': 'Ian', 'email': 'foo'},
                              'committer': {'name': 'Ian', 'email': 'foo'}}}

        self.assertRaises(github3.GitHubError, self.repo.create_file,
                          None, None, None)

        self.not_called()
        self.login()

        ret = self.repo.create_file('setup.py', 'Foo bar', b'foo bar bogus',
                                    'develop',
                                    {'name': 'Ian', 'email': 'foo'},
                                    {'name': 'Ian', 'email': 'foo'})
        assert isinstance(ret, dict)
        assert isinstance(ret['commit'], github3.git.Commit)
        assert isinstance(ret['content'], repos.contents.Contents)
        self.mock_assertions()

    def test_update_file(self):
        self.response('create_content', 200)
        self.put(self.api + 'contents/setup.py')
        self.conf = {
            'data': {
                'message': 'foo',
                'content': 'Zm9vIGJhciBib2d1cw==',
                'sha': 'ae02db',
            }
        }

        self.assertRaises(github3.GitHubError, self.repo.update_file,
                          None, None, None, None)

        self.not_called()
        self.login()

        ret = self.repo.update_file('setup.py', 'foo', b'foo bar bogus',
                                    'ae02db')
        assert isinstance(ret, dict)
        assert isinstance(ret['commit'], github3.git.Commit)
        assert isinstance(ret['content'], repos.contents.Contents)
        self.mock_assertions()

    def test_delete_file(self):
        self.response('create_content', 200)
        self.delete(self.api + 'contents/setup.py')
        self.conf = {'data': {'message': 'foo', 'sha': 'ae02db'}}

        self.assertRaises(github3.GitHubError, self.repo.delete_file,
                          'setup.py', None, None)

        self.not_called()
        self.login()
        ret = self.repo.delete_file('setup.py', 'foo', 'ae02db')
        assert isinstance(ret, github3.git.Commit)
        self.mock_assertions()

    def test_weekly_commit_count(self):
        self.response('weekly_commit_count', ETag='"foobarbogus"')
        self.request.return_value.headers['Last-Modified'] = 'foo'
        self.get(self.api + 'stats/participation')

        w = self.repo.weekly_commit_count()
        self.assertTrue(w.get('owner') is not None)
        self.assertTrue(w.get('all') is not None)

        self.mock_assertions()

        self.response('', 202)
        w = self.repo.weekly_commit_count()
        self.assertEqual(w, {})
        self.mock_assertions()

    def test_iter_commit_activity(self):
        self.response('commit_activity', _iter=True)
        self.get(self.api + 'stats/commit_activity')

        w = next(self.repo.iter_commit_activity())
        assert isinstance(w, dict)

        self.mock_assertions()

    def test_iter_contributor_statistics(self):
        self.response('contributor_statistics', _iter=True)
        self.get(self.api + 'stats/contributors')

        s = next(self.repo.iter_contributor_statistics())
        assert isinstance(s, repos.stats.ContributorStats)

        self.mock_assertions()

    def test_iter_code_frequency(self):
        self.response('code_frequency', _iter=True)
        self.get(self.api + 'stats/code_frequency')

        s = next(self.repo.iter_code_frequency())
        assert isinstance(s, list)

        self.mock_assertions()


class TestContents(BaseCase):
    def __init__(self, methodName='runTest'):
        super(TestContents, self).__init__(methodName)
        self.contents = repos.contents.Contents(load('readme'))
        self.api = self.contents._api

    def setUp(self):
        super(TestContents, self).setUp()
        self.contents = repos.contents.Contents(self.contents.to_json(),
                                                self.g)

    def test_equality(self):
        contents = repos.contents.Contents(load('readme'))
        assert self.contents == contents
        contents.sha = 'fakesha'
        assert self.contents != contents

    def test_git_url(self):
        assert self.contents.links['git'] == self.contents.git_url

    def test_html_url(self):
        assert self.contents.links['html'] == self.contents.html_url

    def test_repr(self):
        assert repr(self.contents) == '<Content [{0}]>'.format('README.rst')

    def test_delete(self):
        self.response('create_content', 200)
        self.delete(self.api)
        self.conf = {
            'data': {
                'message': 'foo',
                'sha': self.contents.sha,
            }
        }

        self.assertRaises(github3.GitHubError, self.contents.delete, None)

        self.not_called()
        self.login()

        c = self.contents.delete('foo')
        assert isinstance(c, github3.git.Commit)
        self.mock_assertions()

    def test_update(self):
        self.response('create_content', 200)
        self.put(self.api)
        self.conf = {
            'data': {
                'message': 'foo',
                'content': 'Zm9vIGJhciBib2d1cw==',
                'sha': self.contents.sha,
            }
        }

        self.assertRaises(github3.GitHubError, self.contents.update,
                          None, None)

        self.not_called()
        self.login()

        ret = self.contents.update('foo', b'foo bar bogus')
        assert isinstance(ret, github3.git.Commit)
        self.mock_assertions()


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
        assert self.hook == h
        h._uniq = 1
        assert self.hook != h

    def test_repr(self):
        assert repr(self.hook) == '<Hook [readthedocs]>'

    def test_delete(self):
        self.response('', 204)
        self.delete(self.api)

        self.assertRaises(github3.GitHubError, self.hook.delete)
        self.not_called()

        self.login()
        assert self.hook.delete()
        self.mock_assertions()

    def test_delete_subscription(self):
        self.response('', 204)
        self.delete(self.api + '/subscription')

        self.assertRaises(github3.GitHubError, self.hook.delete_subscription)
        self.not_called()

        self.login()
        assert self.hook.delete_subscription()
        self.mock_assertions()

    def test_edit(self):
        self.response('hook', 200)
        self.patch(self.api)
        data = {
            'config': {'push': 'http://example.com'},
            'events': ['push'],
            'add_events': ['fake_ev'],
            'rm_events': ['fake_ev'],
            'active': True,
        }
        self.conf = {'data': data.copy()}
        self.conf['data']['remove_events'] = data['rm_events']
        del(self.conf['data']['rm_events'])

        self.assertRaises(github3.GitHubError, self.hook.edit, **data)

        self.login()
        self.not_called()

        assert self.hook.edit(**data)
        self.mock_assertions()

    def test_edit_failed(self):
        self.response('', 404)
        self.patch(self.api)
        self.conf = {}

        self.login()
        assert self.hook.edit() is False
        self.mock_assertions()

    def test_test(self):
        # Funny name, no?
        self.response('', 204)
        self.post(self.api + '/tests')
        self.conf = {}

        self.assertRaises(github3.GitHubError, self.hook.test)
        self.not_called()

        self.login()
        assert self.hook.test()
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

        self.assertRaises(github3.GitHubError, self.comment.delete)

        self.not_called()
        self.login()

        assert self.comment.delete()
        self.mock_assertions()

    def test_repr(self):
        assert repr(self.comment).startswith('<Repository Comment')

    def test_update(self):
        self.post(self.api)
        self.response('repo_comment', 200)
        self.conf = {'data': {'body': 'This is a comment body'}}

        self.assertRaises(github3.GitHubError, self.comment.update, 'foo')

        self.login()
        assert self.comment.update(None) is False
        self.not_called()

        assert self.comment.update('This is a comment body')
        self.mock_assertions()


class TestRepoCommit(BaseCase):
    def __init__(self, methodName='runTest'):
        super(TestRepoCommit, self).__init__(methodName)
        self.commit = repos.commit.RepoCommit(load('commit'))
        self.api = ("https://api.github.com/repos/sigmavirus24/github3.py/"
                    "commits/76dcc6cb4b9860034be81b7e58adc286a115aa97")

    def test_equality(self):
        c = repos.commit.RepoCommit(load('commit'))
        assert self.commit == c
        c._uniq = 'fake'
        assert self.commit != c

    def test_repr(self):
        assert repr(self.commit).startswith('<Repository Commit')

    def test_diff(self):
        self.response('archive', 200)
        self.get(self.api)
        self.conf.update(headers={'Accept': 'application/vnd.github.diff'})

        assert self.commit.diff().startswith(b'archive_data')
        self.mock_assertions()

    def test_patch(self):
        self.response('archive', 200)
        self.get(self.api)
        self.conf.update(headers={'Accept': 'application/vnd.github.patch'})

        assert self.commit.patch().startswith(b'archive_data')
        self.mock_assertions()


class TestComparison(BaseCase):
    def __init__(self, methodName='runTest'):
        super(TestComparison, self).__init__(methodName)
        self.comp = repos.comparison.Comparison(load('comparison'))
        self.api = ("https://api.github.com/repos/sigmavirus24/github3.py/"
                    "compare/a811e1a270f65eecb65755eca38d888cbefcb0a7..."
                    "76dcc6cb4b9860034be81b7e58adc286a115aa97")

    def test_repr(self):
        assert repr(self.comp).startswith('<Comparison ')

    def test_equality(self):
        comp = repos.comparison.Comparison(load('comparison'))
        assert self.comp == comp
        comp.commits.pop(0)
        assert self.comp != comp

    def test_diff(self):
        self.response('archive', 200)
        self.get(self.api)
        self.conf.update(headers={'Accept': 'application/vnd.github.diff'})

        assert self.comp.diff().startswith(b'archive_data')
        self.mock_assertions()

    def test_patch(self):
        self.response('archive', 200)
        self.get(self.api)
        self.conf.update(headers={'Accept': 'application/vnd.github.patch'})

        assert self.comp.patch().startswith(b'archive_data')
        self.mock_assertions()
