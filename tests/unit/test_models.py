import pytest

from github3.models import GitHubObject
from .helper import UnitHelper


class MyGetAttrTestClass(GitHubObject):
    """Subclass for testing getattr on GitHubObject."""

    def __init__(self, example_data, session=None):
        super(MyGetAttrTestClass, self).__init__(example_data)

    def _update_attributes(self, json_data):
        self.fake_attr = json_data.get('fake_attr')


class TestGitHubObject(UnitHelper):
    """Test methods on GitHubObject class."""

    described_class = MyGetAttrTestClass
    example_data = {
        'fake_attr': 'foo',
        'another_fake_attr': 'bar'
    }

    def test_exposes_attributes(self):
        """Verify JSON attributes are exposed even if not explicitly set."""
        assert self.instance.another_fake_attr == 'bar'

    def test_missingattribute(self):
        """Test AttributeError is raised when attribute is not in JSON."""
        with pytest.raises(AttributeError):
            self.instance.missingattribute
