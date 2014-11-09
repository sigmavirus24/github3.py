from .helper import UnitHelper
from github3.null import NullObject

import pytest


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

    def test_instances_can_be_coerced_to_zero(self):
        assert int(self.instance) == 0
