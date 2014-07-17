from github3.orgs import Organization

from .helper import UnitIteratorHelper


def url_for(path=''):
    """Simple function to generate URLs with the base Org URL."""
    if path:
        path = '/' + path.strip('/')
    return 'https://api.github.com/orgs/hapy' + path


class TestOrganizationIterator(UnitIteratorHelper):
    described_class = Organization

    example_data = {
        'url': url_for()
    }

    def test_members(self):
        """Show that one can iterate over all members."""
        i = self.instance.members()
        self.get_next(i)

        self.session.get.assert_called_once_with(
            url_for('members'),
            params={'per_page': 100},
            headers={}
        )
