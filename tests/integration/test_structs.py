import github3
import pytest

from .helper import IntegrationHelper


class TestGitHubIterator(IntegrationHelper):
    def test_resets_etag(self):
        """Show that etag resets to None after refreshing the object."""
        cassette_name = self.cassette_name('resets_etag')
        with self.recorder.use_cassette(cassette_name):
            users_iter = self.gh.all_users(number=10)
            assert users_iter.etag is None
            next(users_iter)  # Make the request
            assert users_iter.etag is not None
            users_iter.refresh()
            assert users_iter.etag is None

    def test_catch_etags(self):
        """Show that etag gets during iteration."""
        cassette_name = self.cassette_name('catch_etags')
        with self.recorder.use_cassette(cassette_name):
            users_iter = self.gh.all_users(number=10)
            assert users_iter.etag is None
            next(users_iter)  # Make the request
            assert users_iter.etag is not None

    def test_catch_None(self):
        """Show that StopIteration is raised when response is empty."""
        cassette_name = self.cassette_name('catch_None')
        with self.recorder.use_cassette(cassette_name):
            orgs_iter = self.gh.organizations_with('itsmemattchung')
            with pytest.raises(StopIteration):
                next(orgs_iter)

    def test_count_reaches_0(self):
        """Tests __iter__ and while loop reaches 0."""
        cassette_name = self.cassette_name('count_reaches_0')
        with self.recorder.use_cassette(cassette_name):
            users_iter = self.gh.all_users(number=1)
            assert isinstance(next(users_iter), github3.users.ShortUser)
            with pytest.raises(StopIteration):
                next(users_iter)

    def test_next(self):
        """Test method returns next value."""
        cassette_name = self.cassette_name('next')
        with self.recorder.use_cassette(cassette_name):
            users_iter = self.gh.all_users(number=10)
            assert isinstance(next(users_iter), github3.users.ShortUser)
