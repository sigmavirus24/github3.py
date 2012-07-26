import base
from expecter import expect
import github3
from github3 import Commit, Blob, Reference, Tag, Tree, Hash, GitObject


class TestGit(base.BaseTest):
    def setUp(self):
        super(TestGit, self).setUp()
        self.todor = self.g.repository(self.sigm, self.todo)

    def test_blob(self):
        r = self.todor
        blob = r.blob('f737918b90118a6aea991f89f444b150a2360393')
        expect(blob).isinstance(Blob)
        self.assertAreNotNone(blob, 'content', 'decoded', 'encoding', 'sha',
                'sized')

        with expect.raises(github3.GitHubError):
            r.create_blob('Foo bar bogus', 'utf-8')

    def test_commit(self):
        r = self.todor
        commit = r.commit('04d55444a3ec06ca8d2aa0a5e333cdaf27113254')
        expect(commit).isinstance(Commit)
        self.assertAreNotNone(commit, 'author', 'committer', 'tree',
                'message', 'parents', 'sha')

    def test_tag(self):
        r = self.todor
        tag = r.tag('6a53c72920c15e196d9a91302bdee2acbe6b44c')
        expect(tag).isinstance(Tag)
        self.assertAreNotNone(tag, 'message', 'object', 'tag', 'tagger',
                'sha')

    def test_tree_and_hash(self):
        r = self.todor
        tree = r.tree('31e862095dffa60744f1ce16a431ea040381f053')
        expect(tree).isinstance(Tree)
        self.assertAreNotNone(tree, 'sha', 'message', 'object', 'tag',
                'tagger')
        expect(tree.object).isinstance(GitObject)
        hashes = tree.tree  # Odd access, right?
        for h in hashes:
            expect(h).isinstance(Hash)

    def test_refs(self):
        r = self.todor
        ref = r.ref('heads/development')
        expect(ref).isinstance(Reference)
