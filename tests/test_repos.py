import base
import github3
from expecter import expect
from datetime import datetime
from os import unlink
from github3.repos import (Repository, Branch, RepoCommit, RepoComment,
        Comparison)
from github3.users import User
#from github3.issues import (Issue, Label, Milestone)
#from github3.events import Event


class TestRepos(base.BaseTest):
    def test_repository(self):
        repo = self.g.repository(self.sigm, self.todo)
        expect(repo).isinstance(Repository)

        # Attributes
        expect(repo.clone_url).is_not_None()
        expect(repo.created_at).isinstance(datetime)
        expect(repo.owner).isinstance(User)

        # Methods
        expect(repo.archive('tarball', 'archive.tar.gz')).is_True()
        unlink('archive.tar.gz')

        #blob = repo.blob("sha"")
        master = repo.branch('master')
        expect(master).isinstance(Branch)

        commit = repo.commit('04d55444a3ec06ca8d2aa0a5e333cdaf27113254')
        expect(commit).isinstance(RepoCommit)

        comment = repo.commit_comment('766400')
        expect(comment).isinstance(RepoComment)

        comp = repo.compare_commits(
                '04d55444a3ec06ca8d2aa0a5e333cdaf27113254',
                '731691616b71258c7ad7c141379856b5ebbab310')
        expect(comp).isinstance(Comparison)

        with expect.raises(github3.GitHubError):
            # It's going to fail anyway by default so the username is
            # unimportant
            repo.add_collaborator('sigmavirus24')
