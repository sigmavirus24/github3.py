from .helper import UnitHelper
from github3.structs import GitHubIterator, NullObject

import mock
import pytest


class TestGitHubIterator(UnitHelper):
    described_class = GitHubIterator

    def setUp(self):
        super(TestGitHubIterator, self).setUp()
        self.count = -1
        self.cls = object

    def create_instance_of_described_class(self):
        self.url = 'https://api.github.com/users'
        klass = lambda *args: args
        instance = self.described_class(count=-1, url=self.url, cls=klass,
                                        session=self.session)
        return instance

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


class TestNullObject(UnitHelper):
    described_class = NullObject

    def create_instance_of_described_class(self):
        return self.described_class()

    def test_returns_empty_list(self):
        assert list(self.instance) == []

    def test_contains_nothing(self):
        assert 'foo' not in self.instance

    def test_returns_itself_when_called(self):
        assert self.instance('foo', 'bar', 'bogus') is self.instance

    def test_returns_empty_string(self):
        assert str(self.instance) == ''

    def test_allows_arbitrary_attributes(self):
        assert self.instance.attr is self.instance

    def test_allows_arbitrary_attributes_to_be_set(self):
        self.instance.attr = 'new'
        assert self.instance.attr is self.instance

    def test_provides_an_api_to_check_if_it_is_null(self):
        assert self.instance.is_null()

    def test_stops_iteration(self):
        with pytest.raises(StopIteration):
            next(self.instance)

    def test_next_raises_stops_iteration(self):
        with pytest.raises(StopIteration):
            self.instance.next()

    def test_getitem_returns_itself(self):
        assert self.instance['attr'] is self.instance

    def test_setitem_sets_nothing(self):
        self.instance['attr'] = 'attr'
        assert self.instance['attr'] is self.instance

    def test_turns_into_unicode(self):
        unicode_str = b''.decode('utf-8')
        try:
            assert unicode(self.instance) == unicode_str
        except NameError:
            assert str(self.instance) == unicode_str

    def test_instances_are_falsey(self):
        if self.instance:
            pytest.fail()
