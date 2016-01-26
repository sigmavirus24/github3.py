import os
import github3
import pytest
from github3 import repos
from tests.utils import (BaseCase, load, mock)

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
