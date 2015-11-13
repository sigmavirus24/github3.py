from .helper import UnitHelper
from .helper import create_example_data_helper
from .helper import create_url_helper

import github3

get_example_data = create_example_data_helper('license_example')
url_for = create_url_helper(
    'https://api.github.com/licenses/mit'
)


class TestLicenses(UnitHelper):
    described_class = github3.licenses.License
    example_data = get_example_data()

    def test_repr(self):
        """Show that instance string is formatted properly."""
        assert(repr(self.instance).startswith('<License'))
