from .helper import UnitHelper, mock
from github3.structs import GitHubIterator


class TestGitHubIterator(UnitHelper):
    described_class = GitHubIterator

    def after_setup(self):
        self.count = self.instance.count = -1
        self.cls = self.instance.cls = object

    def create_instance_of_described_class(self):
        self.url = 'https://api.github.com/users'

        def _klass(*args):
            return args

        klass = _klass
        instance = self.described_class(count=-1, url=self.url, cls=klass,
                                        session=self.session)
        return instance

    def test_refresh(self):
        """Show that __iter__ is called when refreshing."""
        with mock.patch.object(GitHubIterator, '__iter__') as i:
            self.instance.refresh()
            assert i.called is True

    def test_refresh_conditional(self):
        """Show that __iter__ is called when refreshing."""
        with mock.patch.object(GitHubIterator, '__iter__') as i:
            self.instance.refresh(True)
            assert i.called is True

    def test_sets_per_page_to_100(self):
        """Test that the Iterator defaults the per_page parameter to 100"""
        self.session.get.return_value = mock.Mock(status_code=200,
                                                  json=lambda: [],
                                                  links={})

        for i in self.instance:
            break

        self.session.get.assert_called_once_with(
            self.url, params={'per_page': 100}, headers={}
            )

    def test_stores_headers_properly(self):
        headers = {'Accept': 'foo'}
        session, url, count, cls = self.session, self.url, self.count, self.cls
        i = GitHubIterator(count, url, cls, session, headers=headers)
        assert i.headers != {}
        assert i.headers.get('Accept') == 'foo'

    def test_stores_etag_properly(self):
        session, url, count, cls = self.session, self.url, self.count, self.cls
        i = GitHubIterator(count, url, cls, session, etag='"foobarbogus"')
        assert i.headers != {}
        assert i.headers.get('If-None-Match') == '"foobarbogus"'

    def test_str(self):
        """Show that instance string is formatted correctly."""
        assert str(self.instance).startswith('<GitHubIterator')
