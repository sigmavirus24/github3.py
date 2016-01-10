import os
import github3
import pytest
from github3 import repos
from tests.utils import (BaseCase, load, mock)


class TestRepository(BaseCase):
    def __init__(self, methodName='runTest'):
        super(TestRepository, self).__init__(methodName)
        self.repo = repos.Repository(load('repo'))

    def setUp(self):
        super(TestRepository, self).setUp()
        self.repo = repos.Repository(self.repo.as_dict(), self.g)
        self.api = 'https://api.github.com/repos/sigmavirus24/github3.py/'

    def test_create_pull_from_issue(self):
        self.response('pull', 201)
        self.post(self.api + 'pulls')
        self.conf = {'data': {'issue': 1, 'base': 'master',
                              'head': 'feature_branch'}}

        self.assertRaises(github3.GitHubError,
                          self.repo.create_pull_from_issue,
                          **self.conf['data'])

        self.login()
        pull = self.repo.create_pull_from_issue(**self.conf['data'])
        assert isinstance(pull, github3.pulls.PullRequest)
        self.mock_assertions()

    def test_create_status(self):
        self.response('status', 201)
        self.post(self.api + 'statuses/fakesha')
        self.conf = {'data': {'state': 'success'}}

        self.assertRaises(github3.GitHubError, self.repo.create_status,
                          'fakesha', 'success')

        self.login()
        s = self.repo.create_status('fakesha', 'success')
        assert isinstance(s, repos.status.Status)
        assert repr(s) > ''
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

    def test_delete_subscription(self):
        self.response('', 204)
        self.delete(self.api + 'subscription')

        self.assertRaises(github3.GitHubError, self.repo.delete_subscription)
        self.not_called()

        self.login()
        assert self.repo.delete_subscription()
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

        assert isinstance(self.repo.git_commit('fakesha'), github3.git.Commit)
        self.mock_assertions()

    def test_hook(self):
        self.response('hook')
        self.get(self.api + 'hooks/2')

        self.assertRaises(github3.GitHubError, self.repo.hook, 2)

        self.login()
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

        assert isinstance(self.repo.issue(2), github3.issues.Issue)
        self.mock_assertions()

    def test_label(self):
        self.response('label')
        self.get(self.api + 'labels/name')

        assert isinstance(self.repo.label('name'), github3.issues.label.Label)
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

        assert isinstance(self.repo.milestone(2),
                          github3.issues.milestone.Milestone)
        self.mock_assertions()

    def test_parent(self):
        json = self.repo.as_dict().copy()
        json['parent'] = json.copy()
        r = repos.Repository(json)
        assert isinstance(r.parent, repos.Repository)

    def test_permissions(self):
        json = load('repo')
        permissions = {"admin": True, "push": True, "pull": True}
        assert json['permissions'] == permissions
        assert self.repo.permissions == permissions

    def test_pull_request(self):
        self.response('pull', 200)
        self.get(self.api + 'pulls/2')

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
        json = self.repo.as_dict().copy()
        json['source'] = json.copy()
        r = repos.Repository(json)
        assert isinstance(r.source, repos.Repository)

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

        assert isinstance(self.repo.tag('fakesha'), github3.git.Tag)
        self.mock_assertions()

    def test_tree(self):
        self.response('tree')
        self.get(self.api + 'git/trees/fakesha')

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
        with mock.patch.object(repos.Repository, 'label') as l:
            l.return_value = None
            assert self.repo.update_label('foo', 'bar') is False
            self.not_called()

        with mock.patch.object(repos.Repository, 'label') as l:
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


class TestContents(BaseCase):
    def __init__(self, methodName='runTest'):
        super(TestContents, self).__init__(methodName)
        self.contents = repos.contents.Contents(load('readme'))
        self.api = self.contents._api

    def setUp(self):
        super(TestContents, self).setUp()
        self.contents = repos.contents.Contents(self.contents.as_dict(),
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

    @pytest.mark.xfail
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

    @pytest.mark.xfail
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
        self.hook = repos.hook.Hook(self.hook.as_dict(), self.g)

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

    def test_ping(self):
        # Funny name, no?
        self.response('', 204)
        self.post(self.api + '/pings')
        self.conf = {}

        self.assertRaises(github3.GitHubError, self.hook.ping)
        self.not_called()

        self.login()
        assert self.hook.ping()
        self.mock_assertions()


class TestRepoComment(BaseCase):
    def __init__(self, methodName='runTest'):
        super(TestRepoComment, self).__init__(methodName)
        self.comment = repos.comment.RepoComment(load('repo_comment'))
        self.api = ("https://api.github.com/repos/sigmavirus24/github3.py/"
                    "comments/1380832")

    def setUp(self):
        super(TestRepoComment, self).setUp()
        self.comment = repos.comment.RepoComment(self.comment.as_dict(),
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


class TestAsset(BaseCase):
    def __init__(self, methodName='runTest'):
        super(TestAsset, self).__init__(methodName)
        self.asset = repos.release.Asset(load('asset'))
        self.api = ("https://api.github.com/repos/sigmavirus24/github3.py/"
                    "releases/assets/37945")

    def test_repr(self):
        assert repr(self.asset) == '<Asset [github3.py-0.7.1.tar.gz]>'

    @pytest.mark.xfail
    def test_download(self):
        headers = {'content-disposition': 'filename=foo'}
        self.response('archive', 200, **headers)
        self.get(self.api)
        self.conf.update({
            'stream': True,
            'allow_redirects': False,
            'headers': {'Accept': 'application/octet-stream'}
            })

        # 200, to default location
        assert os.path.isfile('foo') is False
        assert self.asset.download()
        assert os.path.isfile('foo')
        os.unlink('foo')
        self.mock_assertions()

        self.request.return_value.raw.seek(0)
        self.request.return_value._content_consumed = False

        # 200, to path
        assert os.path.isfile('path_to_file') is False
        assert self.asset.download('path_to_file')
        assert os.path.isfile('path_to_file')
        os.unlink('path_to_file')
        self.mock_assertions()

        self.request.return_value.raw.seek(0)
        self.request.return_value._content_consumed = False

        # 200, to file-like object
        o = mock.mock_open()
        with mock.patch('{0}.open'.format(__name__), o, create=True):
            with open('download', 'wb+') as fd:
                self.asset.download(fd)
        o.assert_called_once_with('download', 'wb+')
        fd = o()
        fd.write.assert_called_once_with(b'archive_data')
        self.mock_assertions()

        self.request.return_value.raw.seek(0)
        self.request.return_value._content_consumed = False

        # 302, to file-like object
        r = self.request.return_value
        target = 'http://github.s3.example.com/foo'
        self.response('', 302, location=target)
        self.get(target)
        self.request.side_effect = [self.request.return_value, r]
        self.conf['headers'].update({
            'Authorization': None,
            'Content-Type': None,
            })
        del self.conf['allow_redirects']
        o = mock.mock_open()
        with mock.patch('{0}.open'.format(__name__), o, create=True):
            with open('download', 'wb+') as fd:
                self.asset.download(fd)
        o.assert_called_once_with('download', 'wb+')
        fd = o()
        fd.write.assert_called_once_with(b'archive_data')
        self.mock_assertions()

        # 404
        self.response('', 404)
        self.request.side_effect = None
        assert self.asset.download() is False
