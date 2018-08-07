"""Unit tests for the github3.gists module."""
import pytest
import github3

from . import helper

gist_example_data = helper.create_example_data_helper('gist_example')
gist_example_issue_883 = helper.create_example_data_helper(
    'gist_example_issue_883'
)
gist_example_short_data = helper.create_example_data_helper(
    'gist_example_short'
)
gist_history_example_data = helper.create_example_data_helper(
    'gist_history_example'
)
gist_comment_example_data = helper.create_example_data_helper(
    'gist_comment_example'
)
gist_file_example_data = helper.create_example_data_helper(
    'gist_file_example'
)

url_for = helper.create_url_helper(
    'https://api.github.com/gists/e20f1e6c9ca010cabc523a7356217f5a'
)


class TestGist(helper.UnitHelper):
    """Test regular Gist methods."""

    described_class = github3.gists.Gist
    example_data = gist_example_data()

    def test_create_comment(self):
        """Show that a user can create a comment."""
        self.instance.create_comment('some comment text')

        self.post_called_with(url_for('comments'),
                              data={'body': 'some comment text'})

    def test_create_comment_requires_a_body(self):
        """Show that a user cannot create an empty comment."""
        self.instance.create_comment(None)

        assert self.session.post.called is False

    def test_delete(self):
        """Show that a user can delete a gist."""
        self.instance.delete()

        self.session.delete.assert_called_once_with(url_for())

    def test_edit(self):
        """Show that a user can edit a gist."""
        desc = 'description'
        files = {'file': {'content': 'foo content bar'}}
        self.instance.edit(desc, files)

        self.patch_called_with(url_for(), data={desc: desc, 'files': files})

    def test_edit_requires_changes(self):
        """Show that a user must change something to edit a gist."""
        self.instance.edit()

        assert self.session.patch.called is False

    def test_fork(self):
        """Show that a user can fork a gist."""
        self.instance.fork()

        self.session.post.assert_called_once_with(url_for('forks'), None)

    def test_history(self):
        """Show that a user can get a gist's history."""
        history = self.instance.history[0]
        assert isinstance(history, github3.gists.history.GistHistory)
        assert repr(history).startswith('<Gist History')

    def test_file(self):
        """Show that each file object is an instance of GistFile."""
        _file = list(self.instance.files.values())[0]
        assert isinstance(_file, github3.gists.file.GistFile)

    def test_is_starred(self):
        """Show that a user can check if they starred a gist."""
        self.instance.is_starred()

        self.session.get.assert_called_once_with(url_for('star'))

    def test_star(self):
        """Show that a user can star a gist."""
        self.instance.star()

        self.session.put.assert_called_once_with(url_for('star'))

    def test_unstar(self):
        """Show that a user can unstar a gist."""
        self.instance.unstar()

        self.session.delete.assert_called_once_with(url_for('star'))

    def test_to_str(self):
        """Show that a str(gist) is the same as the gist's id."""
        assert str(self.instance) == str(self.instance.id)


class TestGistIssue883(helper.UnitHelper):

    """Unit tests for the Gist object about issue 883."""

    described_class = github3.gists.Gist
    example_data = gist_example_issue_883()

    def test_owner_is_not_required(self):
        """Show that a gist does not always have an owner."""
        assert 'owner' not in self.instance.as_dict()


class TestGistRequiresAuth(helper.UnitRequiresAuthenticationHelper):
    """Test Gist methods which require authentication."""

    described_class = github3.gists.Gist
    example_data = gist_example_data()

    def test_create_comment(self):
        """Show that a user needs to authenticate to create a comment."""
        with pytest.raises(github3.GitHubError):
            self.instance.create_comment('foo')

    def test_delete(self):
        """Show that a user needs to authenticate to delete a gist."""
        with pytest.raises(github3.GitHubError):
            self.instance.delete()

    def test_edit(self):
        """Show that a user needs to authenticate to edit a gist."""
        with pytest.raises(github3.GitHubError):
            self.instance.edit()

    def test_fork(self):
        """Show that a user needs to authenticate to fork a gist."""
        with pytest.raises(github3.GitHubError):
            self.instance.fork()

    def test_is_starred(self):
        """Show that a user needs to auth to check if they starred a gist."""
        with pytest.raises(github3.GitHubError):
            self.instance.is_starred()

    def test_star(self):
        """Show that a user needs to be authenticated to star a gist."""
        with pytest.raises(github3.GitHubError):
            self.instance.star()

    def test_unstar(self):
        """Show that a user needs to be authenticated to unstar a gist."""
        with pytest.raises(github3.GitHubError):
            self.instance.unstar()


class TestGistIterators(helper.UnitIteratorHelper):
    """Test Gist methods that return Iterators."""

    described_class = github3.gists.Gist
    example_data = gist_example_data()

    def test_comments(self):
        """Show a user can iterate over the comments on a gist."""
        i = self.instance.comments()
        self.get_next(i)

        self.session.get.assert_called_once_with(
            url_for('comments'),
            params={'per_page': 100},
            headers={}
        )

    def test_commits(self):
        """Show a user can iterate over the commits on a gist."""
        i = self.instance.commits()
        self.get_next(i)

        self.session.get.assert_called_once_with(
            url_for('commits'),
            params={'per_page': 100},
            headers={}
        )

    def test_files(self):
        """Show that iterating over a gist's files does not make a request."""
        files = list(self.instance.files.values())
        assert len(files) > 0

        assert self.session.get.called is False

    def test_forks(self):
        """Show that a user can iterate over a gist's forks."""
        i = self.instance.forks()
        self.get_next(i)

        self.session.get.assert_called_once_with(
            url_for('forks'),
            params={'per_page': 100},
            headers={}
        )


class TestGistHistory(helper.UnitHelper):
    """Test Gist History."""

    described_class = github3.gists.history.GistHistory
    example_data = gist_history_example_data()

    def test_equality(self):
        """Show that two instances of a GistHistory are equal."""
        history = github3.gists.history.GistHistory(
            gist_history_example_data(),
            self.session
        )
        assert self.instance == history
        history._uniq = 'foo'
        assert self.instance != history

    def test_gist(self):
        """Verify we retrieve a Gist for this point in history."""
        self.instance.gist()

        self.session.get.assert_called_once_with(self.instance.url)


class TestGistComment(helper.UnitHelper):
    """Test Gist Comments."""

    described_class = github3.gists.comment.GistComment
    example_data = gist_comment_example_data()

    def test_equality(self):
        """Show that two instances of a GistComment are equal."""
        comment = github3.gists.comment.GistComment(
            gist_comment_example_data(),
            self.session
        )
        assert self.instance == comment
        comment._uniq = '1'
        assert self.instance != comment

    def test_repr(self):
        """Excercise the GistComment repr."""
        assert repr(self.instance).startswith('<Gist Comment')


class TestGistFile(helper.UnitHelper):
    """Test Gist File."""

    described_class = github3.gists.file.GistFile
    example_data = gist_file_example_data()

    def test_get_file_content_from_raw_url(self):
        """Verify the request made to retrieve a GistFile's content."""
        self.instance.content()

        self.session.get.assert_called_once_with(self.instance.raw_url)
