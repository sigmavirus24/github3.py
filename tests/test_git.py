import base
from expecter import expect
import github3
from github3 import Commit, Blob, Reference, Tag, Tree, Hash


class TestGit(base.BaseTest):
    def setUp(self):
        super(TestGit, self).setUp()
        self.todor = self.g.repository(self.sigm, self.todo)
        self.gh3r = self.g.repository(self.sigm, 'github3.py')

    def test_blob(self):
        r = self.todor
        blob = r.blob('f737918b90118a6aea991f89f444b150a2360393')
        expect(blob).isinstance(Blob)
        self.assertAreNotNone(blob, 'content', 'decoded', 'encoding', 'sha',
                'size')

        with expect.raises(github3.GitHubError):
            r.create_blob('Foo bar bogus', 'utf-8')

    def test_commit(self):
        r = self.todor
        commit = r.git_commit('8b0704374914f03a54b89d938de1c09d5831824e')
        expect(commit).isinstance(Commit)
        self.assertAreNotNone(commit, 'author', 'committer', 'tree', 'message',
                'parents', 'sha')

    def test_tag(self):
        r = self.gh3r
        tag = r.tag('495404cbf4918f46a428b268104de37893dad449')
        expect(tag).isinstance(Tag)
        self.assertAreNotNone(tag, 'message', 'object', 'tag', 'tagger',
                'sha')

    def test_tree_and_hash(self):
        r = self.todor
        tree = r.tree('31e862095dffa60744f1ce16a431ea040381f053')
        expect(tree).isinstance(Tree)
        self.assertAreNotNone(tree, 'sha', 'tree')
        expect(tree.recurse()).isinstance(Tree)
        hashes = tree.tree  # Odd access, right?
        for h in hashes:
            expect(h).isinstance(Hash)
            self.assertAreNotNone(h, 'mode', 'path', 'sha', 'size', 'type',
                    'url')

    def test_refs(self):
        r = self.todor
        ref = r.ref('heads/development')
        expect(ref).isinstance(Reference)
        self.assertAreNotNone(ref, 'object', 'ref')

        with expect.raises(github3.GitHubError):
            ref.delete()
            ref.update('31e862095dffa60744f1ce16a431ea040381f053')
