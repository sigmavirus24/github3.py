import os
import github3
import pytest
from github3 import repos
from tests.utils import (BaseCase, load, mock)


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
