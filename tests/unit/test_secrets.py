"""Secret unit tests."""

import pytest

import github3

from . import helper

get_secret_examlple_data = helper.create_example_data_helper("secret_example")
get_organization_secret_example_data = helper.create_example_data_helper(
    "organization_secret_example"
)


class TestRepositorySecrets(helper.UnitHelper):
    described_class = github3.actions.RepositorySecret
    example_data = get_secret_examlple_data()

    def test_repr(self):
        """Show that instance string is formatted properly."""
        assert repr(self.instance).startswith("<RepositorySecret")


class TestSharedOrganizationSecrets(helper.UnitHelper):
    described_class = github3.actions.SharedOrganizationSecret
    example_data = get_secret_examlple_data()

    def test_repr(self):
        """Show that instance string is formatted properly."""
        assert repr(self.instance).startswith("<SharedOrganizationSecret")


class TestOrganizationSecrets(helper.UnitHelper):
    described_class = github3.actions.OrganizationSecret
    example_data = get_organization_secret_example_data()

    def test_repr(self):
        """Show that instance string is formatted properly."""
        assert repr(self.instance).startswith("<OrganizationSecret")

    def test_set_selected_respositories(self):
        """
        Show that setting selected repositories does the proper HTTP request.
        """
        self.instance.set_selected_repositories([123])
        self.session.put.assert_called_once_with(
            self.instance.selected_repositories_url,
            json={"selected_repository_ids": [123]},
        )

    def test_set_selected_respositories_on_non_selected_visibility(self):
        """
        Show that setting selected respositories with a non-'selected'
        visibility results in a ValueError.
        """
        self.instance.visibility = "all"
        with pytest.raises(ValueError):
            self.instance.set_selected_repositories([123])

    def test_add_selected_repository(self):
        """
        Show that adding a selected repository does the proper HTTP request.
        """
        add_repo_url = "/".join(
            [self.instance.selected_repositories_url, str(123)]
        )
        _ = self.instance.add_selected_repository(123)

        self.session.put.assert_called_once_with(add_repo_url)

    def test_remove_selected_repository(self):
        """
        Show that deleting a selected repository does the proper HTTP request.
        """
        del_repo_url = "/".join(
            [self.instance.selected_repositories_url, str(123)]
        )
        _ = self.instance.remove_selected_repository(123)

        self.session.delete.assert_called_once_with(del_repo_url)

    def test_add_repository_on_non_selected_visibility(self):
        """
        Show that adding selected respositories with a non-'selected'
        visibility results in a ValueError.
        """
        self.instance.visibility = "all"
        with pytest.raises(ValueError):
            self.instance.add_selected_repository(123)
        self.instance.visibility = "private"
        with pytest.raises(ValueError):
            self.instance.add_selected_repository(123)

    def test_delete_repository_on_non_selected_visibility(self):
        """
        Show that deleting selected respositories with a non-'selected'
        visibility results in a ValueError.
        """
        self.instance.visibility = "all"
        with pytest.raises(ValueError):
            self.instance.remove_selected_repository(123)
        self.instance.visibility = "private"
        with pytest.raises(ValueError):
            self.instance.remove_selected_repository(123)


class TestOrganizationSecretIterators(helper.UnitIteratorHelper):
    described_class = github3.actions.OrganizationSecret
    example_data = get_organization_secret_example_data()

    def test_shared_repositories(self):
        """
        Show that listing selected respositories works.
        """
        i = self.instance.selected_repositories()
        self.get_next(i)

        self.session.get.assert_called_once_with(
            self.instance.selected_repositories_url,
            params={"per_page": 100},
            headers={},
        )
