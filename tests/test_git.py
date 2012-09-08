from base import BaseTest, expect, expect_str
import github3
from github3.git import (Commit, Blob, Reference, Tag, Tree, Hash, GitObject)


class TestGit(BaseTest):
    def setUp(self):
        super(TestGit, self).setUp()
        self.todor = self.g.repository(self.sigm, self.todo)
        self.gh3r = self.g.repository(self.sigm, 'github3.py')


class TestBlob(BaseTest):
    def __init__(self, methodName='runTest'):
        super(TestBlob, self).__init__(methodName)
        self.r = self.g.repository(self.sigm, self.todo)
        self.blob = self.r.blob('f737918b90118a6aea991f89f444b150a2360393')

    def test_blob(self):
        expect(self.blob).isinstance(Blob)
        expect_str(repr(self.blob))

    def test_content(self):
        expect_str(self.blob.content)

    def test_decoded(self):
        expect_str(self.blob.decoded)

    def test_encoding(self):
        expect_str(self.blob.encoding)

    def test_sha(self):
        expect_str(self.blob.sha)

    def test_size(self):
        expect_str(self.blob.size)


class TestCommit(BaseTest):
    def __init__(self, methodName='runTest'):
        r = self.g.repository(self.sigm, self.todo)
        self.commit = r.git_commit('8b0704374914f03a54b89d938de1c09d5831824e')

    def test_commit(self):
        expect(self.commit).isinstance(Commit)
        expect_str(repr(self.commit))

    def test_author(self):
        expect(self.commit.author).is_not_None()

    def test_committer(self):
        expect(self.commit.author).is_not_None()

    def test_tree(self):
        expect(self.commit.tree).isinstance(Tree)

    def test_message(self):
        expect_str(self.commit.message)

    def test_parents(self):
        expect(self.commit.parents).isinstance(list)
        self.expect_list_of_class(self.commit.parents, dict)

    def test_sha(self):
        expect_str(self.commit.sha)


class TestTag(BaseTest):
    def __init__(self, methodName='runTest'):
        super(TestTag, self).__init__(methodName)
        r = self.g.repository(self.sigm, 'github3.py')
        self.tag = r.tag('495404cbf4918f46a428b268104de37893dad449')

    def test_tag(self):
        expect(self.tag).isinstance(Tag)
        expect_str(repr(self.tag))

    def test_message(self):
        expect_str(self.tag.message)

    def test_object(self):
        expect(self.tag.object).isinstance(GitObject)

    def test_tagname(self):
        expect_str(self.tag.tag)

    def test_tagger(self):
        expect(self.tag.tagger).isinstance(dict)

    def test_sha(self):
        expect_str(self.tag.sha)


class TestTreeHash(BaseTest):
    def __init__(self, methodName='runTest'):
        super(TestTreeHash, self).__init__(methodName)
        r = self.g.repository(self.sigm, self.todo)
        self.tree = r.tree('31e862095dffa60744f1ce16a431ea040381f053')
        self.hashes = self.tree.tree
        self.hash = self.hashes[0]

    def test_tree(self):
        expect(self.tree).isinstance(Tree)
        expect_str(repr(self.tree))

    def test_tree_sha(self):
        expect_str(self.sha)

    def test_tree_recurse(self):
        expect(self.tree.recurse()).isinstance(Tree)

    def test_hash(self):
        for h in self.hashes:
            expect(h).isinstance(Hash)

    def test_hash_mode(self):
        expect_str(self.hash.mode)

    def test_hash_path(self):
        expect_str(self.hash.path)

    def test_hash_size(self):
        expect(self.hash.size) >= 0

    def test_hash_type(self):
        expect_str(self.hash.type)

    def test_hash_url(self):
        expect_str(self.hash.url)


class TestReference(BaseTest):
    def __init__(self, methodName='runTest'):
        super(TestReference, self).__init__(methodName)
        r = self.g.repository(self.sigm, self.todo)
        self.ref = r.ref('heads/development')

    def test_reference(self):
        expect(self.ref).isinstance(Reference)
        expect_str(repr(self.ref))

    def test_object(self):
        expect(self.ref.object).isinstance(GitObject)
        expect_str(repr(self.ref.object))

    def test_ref(self):
        expect_str(self.ref.ref)

    def test_requires_auth(self):
        with expect.raises(github3.GitHubError):
            self.ref.delete()
            self.ref.update('31e862095dffa60744f1ce16a431ea040381f053')

    def test_with_auth(self):
        if not self.auth:
            return
        r = self._g.repository(self.gh3py, self.test_repo)
        ref = r.create_ref('refs/tags/test_refs',
                '5bd14b07155cf555bda5b8081ba6dc4ac5e645dd')
        expect(ref.update(
            '82b8dd20e95ea34f3d46349a8731d6f18866f8af'
            )).isinstance(bool)
        expect(ref.delete()).is_True()
