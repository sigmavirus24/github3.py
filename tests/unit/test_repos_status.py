import github3

from .helper import (UnitHelper, create_example_data_helper)

get_combined_status_example_data = \
    create_example_data_helper('repos_combined_status_example')


class TestCombinedStatus(UnitHelper):

    """Commit unit test."""

    described_class = github3.repos.status.CombinedStatus
    example_data = get_combined_status_example_data()

    def test_repr(self):
        assert repr(self.instance).startswith('<CombinedStatus')

    def test_statuses(self):
        assert len(self.instance.statuses) == self.instance.total_count
