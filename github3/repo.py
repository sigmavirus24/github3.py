"""
github3.repo
============

This module contains the class relating to repositories.

"""

from datetime import datetime
from json import dumps
from .issue import Issue, Label, Milestone, issue_params
from .git import Blob, Reference, Tag
from .models import GitHubCore, Error
from .pulls import PullRequest
from .user import User


class Repository(GitHubCore):
    """A class to represent how GitHub sends information about repositories."""
    def __init__(self, repo, session):
        super(Repository, self).__init__(session)
        # Clone url using Smart HTTP(s)
        self._https_clone = repo.get('clone_url')
        self._created = self._strptime(repo.get('created_at'))
        self._desc = repo.get('description')

        # The number of forks
        self._forks = repo.get('forks')

        # Is this repository a fork?
        self._is_fork = repo.get('fork')

        # Clone url using git, e.g. git://github.com/sigmavirus24/github3.py
        self._git_clone = repo.get('git_url')
        self._has_dl = repo.get('has_downloads')
        self._has_issues = repo.get('has_issues')
        self._has_wiki = repo.get('has_wiki')

        # e.g. https://sigmavirus24.github.com/github3.py
        self._homepg = repo.get('homepage')

        # e.g. https://github.com/sigmavirus24/github3.py
        self._url = repo.get('html_url')
        self._id = repo.get('id')
        self._lang = repo.get('lang')
        self._mirror = repo.get('mirror_url')

        # Repository name, e.g. github3.py
        self._name = repo.get('name')

        # Number of open issues
        self._open_issues = repo.get('open_issues')

        # Repository owner's name
        self._owner = User(repo.get('owner'), self._session)

        # Is this repository private?
        self._priv = repo.get('private')
        self._pushed = self._strptime(repo.get('pushed_at'))
        self._size = repo.get('size')

        # SSH url e.g. git@github.com/sigmavirus24/github3.py
        self._ssh = repo.get('ssh_url')
        self._svn = repo.get('svn_url')
        self._updated = self._strptime(repo.get('updated_at'))
        self._api = repo.get('url')

        # The number of watchers
        self._watch = repo.get('watchers')

    def __repr__(self):
        return '<Repository [%s/%s]>' % (self._owner.login, self._name)

    def _create_pull(self, data):
        if data:
            url = self._api + '/pulls'
            resp = self._post(url, data)
            if resp.status_code == 201:
                return PullRequest(resp.json, self._session)
            if resp.status_code >= 400:
                return Error(resp)
        return None

    def blob(self, sha):
        url = '{0}/git/blobs/{1}'.format(self._api, sha)
        resp = self._get(url)
        if resp.status_code == 200:
            return Blob(resp.json)
        if resp.status_code >= 400:
            return Error(resp)
        return None

    @property
    def clone_url(self):
        return self._https_clone

    def create_blob(self, content, encoding):
        """Create a blob with ``content``.

        :param content: (required), string, content of the blob
        :param encoding: (required), string, ('base64', 'utf-8')
        """
        if encoding in ('base64', 'utf-8') and content:
            url = self._api + '/git/blobs'
            data = dumps({'content': content, 'encoding': encoding})
            resp = self._post(url, data)
            if resp.status_code == 201:
                return resp.json.get('sha')
            if resp.status_code >= 400:
                return Error(resp)
        return None

    def create_commit(self, message, tree, parents, author={}, committer={}):
        """Create a commit on this repository.

        :param message: (required), string, commit message
        :param tree: (required), string, SHA of the tree object this
            commit points to
        :param parents: (required), list/array, SHAs of the commits that
            were parents of this commit. If empty, the commit will be
            written as the root commit. Even if there is only one
            parent, this should be an array.
        :param author: (optional), dictionary, if omitted, GitHub will
            use the authenticated user's credentials and the current
            time. Format: {'name': 'Committer Name', 'email':
            'name@example.com', 'date': 'YYYY-MM-DDTHH:MM:SS+HH:00'}
        :param committer: (optional), dictionary, if ommitted, GitHub
            will use the author parameters. Should be the same format as
            the author parameter.
        """
        if message and tree and isinstance(parents, list):
            url = self._api + '/git/commits'
            data = dumps({'message': message, 'tree': tree,
                'parents': parents, 'author': author,
                'committer': committer})
            resp = self._post(url, data)
            if resp.status_code == 201:
                return Commit(resp.json, self._session)
            if resp.status_code >= 400:
                return Error(resp)
        return None

    def create_issue(self,
        title,
        body=None,
        assignee=None,
        milestone=None,
        labels=[]):
        """Creates an issue on this repository."""
        issue = dumps({'title': title, 'body': body,
            'assignee': assignee, 'milestone': milestone,
            'labels': labels})
        url = self._api + '/issues'

        resp = self._post(url, issue)
        issue = None
        if resp.status_code == 201:
            issue = Issue(resp.json, self._session)

        return issue

    def create_label(self, name, color):
        label = None

        if color[0] == '#':
            color = color[1:]

        url = self._api + '/labels'
        resp = self._post(url, dumps({'name': name, 'color': color}))

        if resp.status_code == 201:
            label = Label(resp.json, self._session)
        elif resp.status_code >= 400:
            label = Error(resp)
        return label

    def create_milestone(self, title, state=None, description=None,
            due_on=None):
        url = self._api + '/milestones'
        mile = dumps({'title': title, 'state': state,
            'description': description, 'due_on': due_on})
        milestone = None

        resp = self._post(url, mile)
        if resp.status_code == 201:
            milestone = Milestone(resp.json, self._session)

        return milestone

    def create_pull(self, title, base, head, body=''):
        """Create a pull request using commits from ``head`` and comparing
        against ``base``.

        :param title: (required), string
        :param base: (required), string, e.g., 'username:branch', or a sha
        :param head: (required), string, e.g., 'master', or a sha
        :param body: (optional), string, markdown formatted description
        """
        data = dumps({'title': title, 'body': body, 'base': base,
            'head': head})
        return self._create_pull(data)

    def create_pull_from_issue(self, issue, base, head):
        """Create a pull request from issue #``issue``.

        :param issue: (required), int, issue number
        :param base: (required), string, e.g., 'username:branch', or a sha
        :param head: (required), string, e.g., 'master', or a sha
        """
        data = dumps({'issue': issue, 'base': base, 'head': head})
        return self._create_pull(data)

    def create_ref(self, ref, sha):
        """Create a reference in this repository.

        :param ref: (required), string, fully qualified name of the reference,
            e.g. ``refs/heads/master``. If it doesn't start with ``refs`` and
            contain at least two slashes, GitHub's API will reject it.
        :param sha: (required), string, SHA1 value to set the reference to
        """
        data = dumps({'ref': ref, 'sha': sha})
        url = self._api + '/git/refs'
        resp = self._post(url, data)
        if resp.status_code == 201:
            return Reference(resp.json, self._session)
        if resp.status_code >= 400:
            return Error(resp)
        return None

    def create_tag(self, tag, message, sha, obj_type, tagger,
            lightweight=False):
        """Create a tag in this repository.

        :param tag: (required), string, name of the tag
        :param message: (required), string, tag message
        :param sha: (required), string, SHA of the git object this is tagging
        :param obj_type: (required), string, type of object being tagged, e.g.,
            'commit', 'tree', 'blob'
        :param tagger: (required), dict, containing the name, email of the
            tagger and the date it was tagged
        :param lightweight: (optional), boolean, if False, create an annotated
            tag, otherwise create a lightweight tag (a Reference).
        """
        if lightweight and tag and sha:
            return self.create_ref('refs/tags/' + tag, sha)

        t = None
        if tag and message and sha and obj_type and len(tagger) == 3:
            data = dumps({'tag': tag, 'message': message, 'object': sha,
                'type': obj_type, 'tagger': tagger})
            url = self._api + '/git/tags'
            resp = self._post(url, data)
            if resp.status_code == 201:
                t = Tag(resp.json)
                self.create_ref('refs/tags/' + tag, sha)
            elif resp.status_code >= 400:
                t = Error(resp)
        return t

    def create_tree(self, tree, base_tree=''):
        """Create a tree on this repository.

        :param tree: (required), array of hash objects specifying the
            tree structure. Format: [{'path': 'path/file', 'mode':
            'filemode', 'type': 'blob or tree', 'sha': '44bfc6d...'}]
        :param base_tree: (optional), string, SHA1 of the tree you want
            to update with new data
        """
        if tree and isinstance(tree, list):
            data = dumps({'tree': tree, 'base_tree': base_tree})
            url = self._api + '/git/trees'
            resp = self._post(url, data)
            if resp.status_code == 201:
                return Tree(resp.json)
            if resp.status_code >= 400:
                return Error(resp)
        return None

    @property
    def created_at(self):
        return self._created

    @property
    def description(self):
        return self._desc

    def fork(self, organization=None):
        """Create a fork of this repository.

        :param organization: login for organization to create the fork
            under"""
        url = self._api + '/forks'
        if organization:
            resp = self._post(url, dumps({'org': organization}))
        else:
            resp = self._post(url)

        if resp.status_code == 202:
            return Repository(resp.json, self._session)

        return None

    @property
    def forks(self):
        return self._forks

    def is_fork(self):
        return self._is_fork

    def is_private(self):
        return self._priv

    @property
    def git_clone(self):
        return self._git_clone

    def has_downloads(self):
        return self._has_dl

    def has_wiki(self):
        return self._has_wiki

    @property
    def homepage(self):
        return self._homepg

    @property
    def html_url(self):
        return self._url

    @property
    def id(self):
        return self._id

    def issue(self, number):
        if number > 0:
            url = '{0}/issues/{1}'.format(self._api, str(number))
            resp = self._get(url)
            if resp.status_code == 200:
                return Issue(resp.json, self._session)

        return None

    def label(self, name):
        if name:
            url = '{0}/labels/{1}'.format(self._api, name)
            resp = self._get(url)
            if resp.status_code == 200:
                return Label(resp.json, self._session)

        return None

    @property
    def language(self):
        return self._lang

    def list_issues(self,
        milestone=None,
        state=None,
        assignee=None,
        mentioned=None,
        labels=None,
        sort=None,
        direction=None,
        since=None):
        """List issues on this repo based upon parameters passed.

        :param milestone: must be an integer, 'none', or '*'
        :param state: accepted values: ('open', 'closed')
        :param assignee: 'none', '*', or login name
        :param mentioned: user's login name
        :param labels: comma-separated list of labels, e.g. 'bug,ui,@high'
        :param sort: accepted values:
            ('created', 'updated', 'comments', 'created')
        :param direction: accepted values: ('open', 'closed')
        :param since: ISO 8601 format: YYYY-MM-DDTHH:MM:SSZ
        """
        url = self._api + '/issues'

        params = []
        if milestone in ('*', 'none') or isinstance(milestone, int):
            params.append('milestone=%s' % str(milestone).lower())
            # str(None) = 'None' which is invalid, so .lower() it to make it
            # work.

        if assignee:
            params.append('assignee=%s' % assignee)

        if mentioned:
            params.append('mentioned=%s' % mentioned)

        tmp = issue_params(None, state, labels, sort, direction, since)

        params = '&'.join(params) if params else None
        params = '{0}&{1}'.format(tmp, params) if params else tmp

        if params:
            url = '{0}?{1}'.format(url, params)

        resp = self._get(url)
        issues = []
        if resp.status_code == 200:
            for issue in resp.json:
                issues.append(Issue(issue, self._session))

        return issues

    def list_labels(self):
        url = self._api + '/labels'
        resp = self._get(url)

        labels = []
        if resp.status_code == 200:
            for label in resp.json:
                labels.append(Label(label, self._session))

        return labels

    def list_milestones(self, state=None, sort=None, direction=None):
        url = self._api + '/milestones'

        params = []
        if state in ('open', 'closed'):
            params.append('state=%s' % state)

        if sort in ('due_date', 'completeness'):
            params.append('sort=%s' % sort)

        if direction in ('asc', 'desc'):
            params.append('direction=%s' % direction)

        if params:
            params = '&'.join(params)
            url = '{0}?{1}'.format(url, params)

        resp = self._get(url)
        milestones = []
        if resp.status_code == 200:
            for mile in resp.json:
                milestones.append(Milestone(mile, self._session))

        return milestones

    def list_pulls(self, state=None):
        if state in ('open', 'closed'):
            url = '{0}/pulls?state={1}'.format(self._api, state)
        else:
            url = self._api + '/pulls'

        resp = self._get(url)
        pulls = []
        if resp.status_code == 200:
            for pull in resp.json:
                pulls.append(PullRequest(pull, self._session))

        return pulls

    def list_refs(self, subspace=''):
        """List references for this repository.

        :param subspace: (optional), string, e.g. 'tags', 'stashes', 'notes'
        """
        if subspace:
            url = self._api + '/git/refs/' + subspace
        else:
            url = self._api + '/git/refs'
        resp = self._get(url)
        refs = []
        if resp.status_code == 200:
            for ref in resp.json:
                refs.append(Reference(ref, self._session))
        return refs

    def milestone(self, number):
        url = '{0}/milestones/{1}'.format(self._api, str(number))
        resp = self._session.get(url)
        if resp.status_code == 200:
            return Milestone(resp.json, self._session)
        return None

    @property
    def mirror(self):
        return self._mirror

    @property
    def name(self):
        return self._name

    @property
    def open_issues(self):
        return self._open_issues

    @property
    def owner(self):
        return self._owner

    def pull_request(self, number):
        if int(number) > 0:
            url = '{0}/pulls/{1}'.format(self._api, str(number))
            resp = self._get(url)
            if resp.status_code == 200:
                return PullRequest(resp.json, self._session)
        return None

    @property
    def pushed_at(self):
        return self._pushed

    def ref(self, ref):
        """Get a reference pointed to by ``ref``.

        The most common will be branches and tags. For a branch, you must
        specify 'heads/branchname' and for a tag, 'tags/tagname'. Essentially,
        the system should return any reference you provide it in the namespace,
        including notes and stashes (provided they exist on the server).
        """
        url = self._api + '/git/refs/' + ref
        resp = self._get(url)
        if resp.status_code == 200:
            return Reference(resp.json, self._session)
        if resp.status_code >= 400:
            return Error(resp)
        return None

    @property
    def size(self):
        return self._size

    @property
    def ssh_url(self):
        return self._ssh

    @property
    def svn_url(self):
        return self._svn

    def tag(self, sha):
        """Get an annotated tag.

        http://learn.github.com/p/tagging.html
        """
        url = self._api + '/git/tags/' + sha
        resp = self._get(url)
        if resp.status_code == 200:
            return Tag(resp.json)
        if resp.status_code >= 400:
            return Error(resp)
        return None

    def tree(self, sha):
        url = '{0}/git/trees/{1}'.format(self._api, sha)
        resp = self._get(url)
        if resp.status_code == 200:
            return Tree(resp.json, self._session)
        if resp.status_code >= 400:
            return Error(resp)
        return None

    @property
    def updated_at(self):
        return self._updated

    def update_label(self, name, color, new_name=''):
        label = self.get_label(name)

        if label:
            if not new_name:
                return label.update(name, color)
            return label.update(new_name, color)

        # label == None
        return False

    @property
    def watchers(self):
        return self._watchers
