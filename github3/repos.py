"""
github3.repos
=============

This module contains the class relating to repositories.

"""

from base64 import b64decode
from json import dumps
from .events import Event
from .issues import Issue, IssueEvent, Label, Milestone, issue_params
from .git import Blob, Commit, Reference, Tag, Tree
from .models import GitHubObject, GitHubCore, BaseComment, BaseCommit
from .pulls import PullRequest
from .users import User, Key


class Repository(GitHubCore):
    """The :class:`Repository <Repository>` object. It represents how GitHub
    sends information about repositories.
    """
    def __init__(self, repo, session=None):
        super(Repository, self).__init__(repo, session)
        self._update_(repo)

    def __repr__(self):
        return '<Repository [{0}/{1}]>'.format(self._owner.login, self._name)

    def _update_(self, repo):
        self._json_data = repo
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

    def _create_pull(self, data):
        json = None
        if data:
            url = self._build_url('pulls', self._api)
            json = self._json(self._post(url, data), 201)
        return PullRequest(json, self._session) if json else None

    @GitHubCore.requires_auth
    def add_collaborator(self, login):
        """Add ``login`` as a collaborator to a repository.

        :param login: (required), login of the user
        :type login: str
        :returns: bool -- True if successful, False otherwise
        """
        resp = False
        if login:
            url = self._api + '/collaborators/' + login
            resp = self._put(url)
        return resp

    def archive(self, format, path='', ref='master'):
        """Get the tarball or zipball archive for this repo at ref.

        :param format: (required), accepted values: ('tarball',
            'zipball')
        :type format: str
        :param path: (optional), path where the file should be saved
            to, default is the filename provided in the headers and will be
            written in the current directory
        :type path: str
        :param ref: (optional)
        :type ref: str
        :returns: bool -- True if successful, False otherwise
        """
        resp = None
        written = False
        if format in ('tarball', 'zipball'):
            url = self._build_url(format, ref, base_url=self._api)
            resp = self._get(url, allow_redirects=True)

        if resp.ok and path:
            with open(path, 'wb') as fd:
                fd.write(resp.content)
                written = True
        elif resp:
            header = resp.headers['content-disposition']
            i = header.find('filename=') + len('filename=')
            with open(header[i:], 'wb') as fd:
                fd.write(resp.content)
                written = True
        return written

    def blob(self, sha):
        """Get the blob indicated by ``sha``.

        :param sha: (required), sha of the blob
        :type sha: str
        :returns: :class:`Blob <github3.git.Blob>` if successful, otherwise
            None
        """
        url = self._build_url('git', 'blobs', sha, base_url=self._api)
        json = self._json(self._get(url), 200)
        return Blob(json) if json else None

    def branch(self, name):
        """Get the branch ``name`` of this repository.

        :param name: (required), branch name
        :type name: str
        :returns: :class:`Branch <Branch>`
        """
        json = None
        if name:
            url = self._build_url('branches', name, base_url=self._api)
            json = self._json(self._get(url), 200)
        return Branch(json, self) if json else None

    @property
    def clone_url(self):
        """URL used to clone via HTTPS."""
        return self._https_clone

    def commit(self, sha):
        """Get a single (repo) commit. See :func:`git_commit` for the Git Data
        Commit.

        :param sha: (required), sha of the commit
        :type sha: str
        :returns: :class:`RepoCommit <RepoCommit>` if successful, otherwise
            None
        """
        url = self._build_url('commits', sha, base_url=self._api)
        json = self._json(self._get(url), 200)
        return RepoCommit(json, self) if json else None

    def commit_comment(self, comment_id):
        """Get a single commit comment.

        :param comment_id: (required), id of the comment used by GitHub
        :type comment_id: int
        :returns: :class:`RepoComment <RepoComment>` if successful, otherwise
            None
        """
        url = self._build_url('comments', str(comment_id), base_url=self._api)
        json = self._json(self._get(url), 200)
        return RepoComment(json, self) if json else None

    def compare_commits(self, base, head):
        """Compare two commits.

        :param base: (required), base for the comparison
        :type base: str
        :param head: (required), compare this against base
        :type head: str
        :returns: :class:`Comparison <Comparison>` if successful, else None
        """
        url = self._build_url('compare', base + '...' + head,
                base_url=self._api)
        json = self._json(self._get(url), 200)
        return Comparison(json) if json else None

    def contents(self, path):
        """Get the contents of the file pointed to by ``path``.

        :param path: (required), path to file, e.g.
            github3/repo.py
        :type path: str
        :returns: :class:`Contents <Contents>` if successful, else None
        """
        url = self._build_url('contents', path, base_url=self._api)
        json = self._json(self._get(url), 200)
        return Contents(json) if json else None

    @GitHubCore.requires_auth
    def create_blob(self, content, encoding):
        """Create a blob with ``content``.

        :param content: (required), content of the blob
        :type content: str
        :param encoding: (required), ('base64', 'utf-8')
        :type encoding: str
        :returns: string of the SHA returned
        """
        sha = ''
        if encoding in ('base64', 'utf-8') and content:
            url = self._build_url('git', 'blobs', base_url=self._api)
            data = dumps({'content': content, 'encoding': encoding})
            json = self._json(self._post(url, data), 201)
            if json:
                sha = json.get('sha')
        return sha

    @GitHubCore.requires_auth
    def create_comment(self, body, sha, path, position, line=1):
        """Create a comment on a commit.

        :param body: (required), body of the message
        :type body: str
        :param sha: (required), commit id
        :type sha: str
        :param path: (required), relative path of the file to comment
            on
        :type path: str
        :param position: (required), line index in the diff to comment on
        :type position: int
        :param line: (optional), line number of the file to comment on,
            default: 1
        :type line: int
        :returns: :class:`RepoComment <RepoComment>` if successful else None
        """
        line = int(line)
        position = int(position)
        json = None
        if body and sha and line > 0 and path and position > 0:
            data = dumps({'body': body, 'commit_id': sha, 'line': line,
                'path': path, 'position': position})
            url = self._build_url('commits', sha, 'comments',
                    base_url=self._api)
            json = self._json(self._post(url, data), 201)
        return RepoComment(json, self) if json else None

    @GitHubCore.requires_auth
    def create_commit(self, message, tree, parents, author={}, committer={}):
        """Create a commit on this repository.

        :param message: (required), commit message
        :type message: str
        :param tree: (required), SHA of the tree object this
            commit points to
        :type tree: str
        :param parents: (required), SHAs of the commits that were parents of
            this commit. If empty, the commit will be written as the root
            commit.  Even if there is only one parent, this should be an
            array.
        :type parents: list
        :param author: (optional), if omitted, GitHub will
            use the authenticated user's credentials and the current
            time. Format: {'name': 'Committer Name', 'email':
            'name@example.com', 'date': 'YYYY-MM-DDTHH:MM:SS+HH:00'}
        :type author: dict
        :param committer: (optional), if ommitted, GitHub will use the author
            parameters. Should be the same format as the author parameter.
        :type commiter: dict
        :returns: :class:`Commit <github3.git.Commit>` if successful, else
            None
        """
        json = None
        if message and tree and isinstance(parents, list):
            url = self._build_url('git', 'commits', base_url=self._api)
            data = dumps({'message': message, 'tree': tree, 'parents': parents,
                'author': author, 'committer': committer})
            json = self._json(self._post(url, data), 201)
        return Commit(json, self) if json else None

    @GitHubCore.requires_auth
    def create_download(self, name, path, description='',
            content_type='text/plain'):
        """Create a new download on this repository.

        I do not require you provide the size in bytes because it can be
        determined by the operating system.

        :param str name: (required), name of the file as it will appear
        :param path: (required), path to the file
        :type path: str
        :param description: (optional), description of the file
        :type description: str
        :param content_type: (optional), e.g. 'text/plain'
        :type content_type: str
        :returns: :class:`Download <Download>` if successful, else None
        """
        json = None
        if name and path:
            url = self._build_url('downloads', base_url=self._api)
            from os import stat
            info = stat(path)
            data = dumps({'name': name, 'size': info.st_size,
                'description': description, 'content_type': content_type})
            json = self._json(self._post(url, data), 201)

        if not json:
            return None

        form = [('key', json.get('path')),
            ('acl', json.get('acl')),
            ('success_action_status', '201'),
            ('Filename', json.get('name')),
            ('AWSAccessKeyId', json.get('accesskeyid')),
            ('Policy', json.get('policy')),
            ('Signature', json.get('signature')),
            ('Content-Type', json.get('mime_type'))]
        file = [('file', open(path, 'rb').read())]
        resp = self._post(json.get('s3_url'), data=form, files=file,
                auth=tuple())

        return Download(json, self) if self._boolean(resp, 201, 404) else None

    @GitHubCore.requires_auth
    def create_fork(self, organization=None):
        """Create a fork of this repository.

        :param organization: (required), login for organization to create the
            fork under
        :type organization: str
        :returns: :class:`Repository <Repository>` if successful, else None
        """
        url = self._build_url('forks', base_url=self._api)
        if organization:
            resp = self._post(url, dumps({'org': organization}))
        else:
            resp = self._post(url)
        json = self._json(resp, 202)

        return Repository(json, self) if json else None

    @GitHubCore.requires_auth
    def create_hook(self, name, config, events=['push'], active=True):
        """Create a hook on this repository.

        :param name: (required), name of the hook
        :type name: str
        :param config: (required), key-value pairs which act as settings
            for this hook
        :type config: dict
        :param events: (optional), events the hook is triggered for
        :type events: list
        :param active: (optional), whether the hook is actually
            triggered
        :type active: bool
        :returns: :class:`Hook <Hook>` if successful, else None
        """
        json = None
        if name and config and isinstance(config, dict):
            url = self._build_url('hooks', base_url=self._api)
            data = dumps({'name': name, 'config': config, 'events': events,
                'active': active})
            json = self._json(self._post(url, data), 201)
        return Hook(json, self) if json else None

    @GitHubCore.requires_auth
    def create_issue(self,
        title,
        body=None,
        assignee=None,
        milestone=None,
        labels=[]):
        """Creates an issue on this repository.

        :param title: (required), title of the issue
        :type title: str
        :param body: (optional), body of the issue
        :type body: str
        :param assignee: (optional), login of the user to assign the
            issue to
        :type assignee: str
        :param milestone: (optional), milestone to attribute this issue
            to
        :type milestone: str
        :param labels: (optional), labels to apply to this
            issue
        :type labels: list of strings
        :returns: :class:`Issue <github3.issue.Issue>` if successful, else
            None
        """
        issue = dumps({'title': title, 'body': body, 'assignee': assignee,
            'milestone': milestone, 'labels': labels})
        url = self._build_url('issues', base_url=self._api)

        json = self._json(self._post(url, issue), 201)
        return Issue(json, self) if json else None

    @GitHubCore.requires_auth
    def create_key(self, title, key):
        """Create a deploy key.

        :param title: (required), title of key
        :type title: str
        :param key: (required), key text
        :type key: str
        :returns: :class:`Key <github3.user.Key>` if successful, else None
        """
        data = dumps({'title': title, 'key': key})
        url = self._build_url('keys', base_url=self._api)
        json = self._json(self._post(url, data), 201)
        return Key(json, self) if json else None

    @GitHubCore.requires_auth
    def create_label(self, name, color):
        """Create a label for this repository.

        :param name: (required), name to give to the label
        :type name: str
        :param color: (required), value of the color to assign to the
            label
        :type color: str
        :returns: :class:`Label <github3.issue.Label>` if successful, else
            None
        """
        data = dumps({'name': name, 'color': color.strip('#')})
        url = self._build_url('labels', base_url=self._api)
        json = self._json(self._post(url, data), 201)
        return Label(json, self) if json else None

    @GitHubCore.requires_auth
    def create_milestone(self, title, state=None, description=None,
            due_on=None):
        """Create a milestone for this repository.

        :param title: (required), title of the milestone
        :type title: str
        :param state: (optional), state of the milestone, accepted
            values: ('open', 'closed'), default: 'open'
        :type state: str
        :param description: (optional), description of the milestone
        :type description: str
        :param due_on: (optional), ISO 8601 formatted due date
        :type due_on: str
        :returns: :class:`Milestone <github3.issue.Milestone>` if successful,
            else None
        """
        url = self._build_url('milestones', base_url=self._api)
        if state not in ('open', 'closed'):
            state = 'open'
        data = dumps({'title': title, 'state': state,
            'description': description, 'due_on': due_on})
        json = self._json(self._post(url, data), 201)
        return Milestone(json, self) if json else None

    @GitHubCore.requires_auth
    def create_pull(self, title, base, head, body=''):
        """Create a pull request using commits from ``head`` and comparing
        against ``base``.

        :param title: (required)
        :type title: str
        :param base: (required), e.g., 'username:branch', or a sha
        :type base: str
        :param head: (required), e.g., 'master', or a sha
        :type head: str
        :param body: (optional), markdown formatted description
        :type body: str
        :returns: :class:`PullRequest <github3.pulls.PullRequest>` if
            successful, else None
        """
        data = dumps({'title': title, 'body': body, 'base': base,
            'head': head})
        return self._create_pull(data)

    @GitHubCore.requires_auth
    def create_pull_from_issue(self, issue, base, head):
        """Create a pull request from issue #``issue``.

        :param issue: (required), issue number
        :type issue: int
        :param base: (required), e.g., 'username:branch', or a sha
        :type base: str
        :param head: (required), e.g., 'master', or a sha
        :type head: str
        :returns: :class:`PullRequest <github3.pulls.PullRequest>` if
            successful, else None
        """
        data = dumps({'issue': issue, 'base': base, 'head': head})
        return self._create_pull(data)

    @GitHubCore.requires_auth
    def create_ref(self, ref, sha):
        """Create a reference in this repository.

        :param ref: (required), fully qualified name of the reference,
            e.g. ``refs/heads/master``. If it doesn't start with ``refs`` and
            contain at least two slashes, GitHub's API will reject it.
        :type ref: str
        :param sha: (required), SHA1 value to set the reference to
        :type sha: str
        :returns: :class:`Reference <github3.git.Reference>` if successful
            else None
        """
        data = dumps({'ref': ref, 'sha': sha})
        url = self._build_url('git', 'refs', base_url=self._api)
        json = self._json(self._post(url, data), 201)
        return Reference(json, self) if json else None

    @GitHubCore.requires_auth
    def create_tag(self, tag, message, sha, obj_type, tagger,
            lightweight=False):
        """Create a tag in this repository.

        :param tag: (required), name of the tag
        :type tag: str
        :param message: (required), tag message
        :type message: str
        :param sha: (required), SHA of the git object this is tagging
        :type sha: str
        :param obj_type: (required), type of object being tagged, e.g.,
            'commit', 'tree', 'blob'
        :type obj_type: str
        :param tagger: (required), containing the name, email of the
            tagger and the date it was tagged
        :type tagger: dict
        :param lightweight: (optional), if False, create an annotated
            tag, otherwise create a lightweight tag (a Reference).
        :type lightweight: bool
        :returns: If lightweight == False: :class:`Tag <github3.git.Tag>` if
            successful, else None. If lightweight == True: :class:`Reference
            <Reference>`
        """
        if lightweight and tag and sha:
            return self.create_ref('refs/tags/' + tag, sha)

        json = None
        if tag and message and sha and obj_type and len(tagger) == 3:
            data = dumps({'tag': tag, 'message': message, 'object': sha,
                'type': obj_type, 'tagger': tagger})
            url = self._build_url('git', 'tags', base_url=self._api)
            json = self._json(self._post(url, data), 201)
            if json:
                self.create_ref('refs/tags/' + tag, sha)
        return Tag(json) if json else None

    @GitHubCore.requires_auth
    def create_tree(self, tree, base_tree=''):
        """Create a tree on this repository.

        :param tree: (required), specifies the tree structure.
            Format: [{'path': 'path/file', 'mode':
            'filemode', 'type': 'blob or tree', 'sha': '44bfc6d...'}]
        :type tree: list of dicts
        :param base_tree: (optional), SHA1 of the tree you want
            to update with new data
        :type base_tree: str
        :returns: :class:`Tree <github3.git.Tree>` if successful, else None
        """
        json = None
        if tree and isinstance(tree, list):
            data = dumps({'tree': tree, 'base_tree': base_tree})
            url = self._build_url('git', 'trees', base_url=self._api)
            json = self._json(self._post(url, data), 201)
        return Tree(json) if json else None

    @property
    def created_at(self):
        """``datetime`` object representing when the Repository was created."""
        return self._created

    @GitHubCore.requires_auth
    def delete(self):
        """Delete this repository.

        :returns: bool -- True if successful, False otherwise
        """
        return self._boolean(self._delete(self._api), 204, 404)

    @property
    def description(self):
        """Description of the repository."""
        return self._desc

    def download(self, id_num):
        """Get a single download object by its id.

        :param id_num: (required), id of the download
        :type id_num: int
        :returns: :class:`Download <Download>` if successful, else None
        """
        json = None
        if int(id_num) > 0:
            url = self._build_url('downloads', str(id_num),
                    base_url=self._api)
            json = self._json(self._get(url), 200)
        return Download(json, self) if json else None

    @GitHubCore.requires_auth
    def edit(self,
        name,
        description='',
        homepage='',
        private=False,
        has_issues=True,
        has_wiki=True,
        has_downloads=True):
        """Edit this repository.

        :param name: (required), name of the repository
        :type name: str
        :param description: (optional)
        :type description: str
        :param homepage: (optional)
        :type homepage: str
        :param private: (optional), If ``True``, create a
            private repository. API default: ``False``
        :type private: bool
        :param has_issues: (optional), If ``True``, enable
            issues for this repository. API default: ``True``
        :type has_issues: bool
        :param has_wiki: (optional), If ``True``, enable the
            wiki for this repository. API default: ``True``
        :type has_wiki: bool
        :param has_downloads: (optional), If ``True``, enable
            downloads for this repository. API default: ``True``
        :type has_downloads: bool
        :returns: bool -- True if successful, False otherwise
        """
        data = dumps({'name': name, 'description': description,
            'homepage': homepage, 'private': private,
            'has_issues': has_issues, 'has_wiki': has_wiki,
            'has_downloads': has_downloads})
        json = self._json(self._patch(self._api, data=data), 200)
        if json:
            self._update_(json)
            return True
        return False

    @property
    def forks(self):
        """The number of forks made of this repository."""
        return self._forks

    def is_collaborator(self, login):
        """Check to see if ``login`` is a collaborator on this repository.

        :param login: (required), login for the user
        :type login: str
        :returns: bool -- True if successful, False otherwise
        """
        if login:
            url = self._build_url('collaborators', login, base_url=self._api)
            return self._boolean(self._get(url), 204, 404)
        return False

    def is_fork(self):
        """Checks if this repository is a fork.

        :returns: bool
        """
        return self._is_fork

    def is_private(self):
        """Checks if this repository is private.

        :returns: bool
        """
        return self._priv

    def git_commit(self, sha):
        """Get a single (git) commit.

        :param sha: (required), sha of the commit
        :type sha: str
        :returns: :class:`Commit <github3.git.Commit>` if successful,
            otherwise None
        """
        url = self._build_url('git', 'commits', sha, base_url=self._api)
        json = self._json(self._get(url), 200)
        return Commit(json, self) if json else None

    @property
    def git_clone(self):
        """Plain git url for an anonymous clone."""
        return self._git_clone

    def has_downloads(self):
        """Checks if this repository has downloads.

        :returns: bool
        """
        return self._has_dl

    def has_wiki(self):
        """Checks if this repository has a wiki.

        :returns: bool
        """
        return self._has_wiki

    @property
    def homepage(self):
        """URL of the home page for the project."""
        return self._homepg

    @GitHubCore.requires_auth
    def hook(self, id_num):
        """Get a single hook.

        :param id_num: (required), id of the hook
        :type id_num: int
        :returns: :class:`Hook <Hook>` if successful, else None
        """
        json = None
        if int(id_num) > 0:
            url = self._build_url('hooks', str(id_num), base_url=self._api)
            json = self._json(self._get(url), 200)
        return Hook(json, self) if json else None

    @property
    def html_url(self):
        """URL of the project at GitHub."""
        return self._url

    @property
    def id(self):
        """Unique id of the repository."""
        return self._id

    def is_assignee(self, login):
        """Check if the user is a possible assignee for an issue on this
        repository.

        :returns: :class:`bool`
        """
        url = self._build_url('assignees', login, base_url=self._api)
        return self._boolean(self._get(url), 204, 404)

    def issue(self, number):
        """Get the issue specified by ``number``.

        :param number: (required), number of the issue on this repository
        :type number: int
        :returns: :class:`Issue <github3.issue.Issue>` if successful, else
            None
        """
        json = None
        if int(number) > 0:
            url = self._build_url('issues', str(number), base_url=self._api)
            json = self._json(self._get(url), 200)
        return Issue(json, self) if json else None

    @GitHubCore.requires_auth
    def key(self, id_num):
        """Get the specified deploy key.

        :param id_num: (required), id of the key
        :type id_num: int
        :returns: :class:`Key <Key>` if successful, else None
        """
        json = None
        if int(id_num) > 0:
            url = self._build_url('keys', str(id_num), base_url=self._api)
            json = self._json(self._get(url), 200)
        return Key(json, self) if json else None

    def label(self, name):
        """Get the label specified by ``name``

        :param name: (required), name of the label
        :type name: str
        :returns: :class:`Label <github3.issue.Label>` if successful, else
            None
        """
        json = None
        if name:
            url = self._build_url('labels', name, base_url=self._api)
            json = self._json(self._get(url), 200)
        return Label(json, self) if json else None

    @property
    def language(self):
        """Language property."""
        return self._lang

    def list_assignees(self):
        """List all available assignees to which an issue may be assigned.

        :returns: list of :class:`User <github3.user.User>`\ s
        """
        url = self._build_url('assignees', base_url=self._api)
        json = self._json(self._get(url), 200)
        return [User(u, self) for u in json]

    def list_branches(self):
        """List the branches in this repository.

        :returns: list of :class:`Branch <Branch>`\ es
        """
        # Paginate?
        url = self._build_url('branches', base_url=self._api)
        json = self._json(self._get(url), 200)
        return [Branch(b, self) for b in json]

    def list_comments(self):
        """List comments on all commits in the repository.

        :returns: list of :class:`RepoComment <RepoComment>`\ s
        """
        # Paginate?
        url = self._build_url('comments', base_url=self._api)
        json = self._json(self._get(url), 200)
        return [RepoComment(comment, self) for comment in json]

    def list_comments_on_commit(self, sha):
        """List comments for a single commit.

        :param sha: (required), sha of the commit to list comments on
        :type sha: str
        :returns: list of :class:`RepoComment <RepoComment>`\ s
        """
        # Paginate?
        json = []
        if sha:
            url = self._build_url('commits', sha, 'comments',
                    base_url=self._api)
            json = self._json(self._get(url), 200)
        return [RepoComment(comm, self) for comm in json]

    def list_commits(self):
        """List commits in this repository.

        :returns: list of :class:`RepoCommit <RepoCommit>`\ s
        """
        # Paginate
        url = self._build_url('commits', base_url=self._api)
        json = self._json(self._get(url), 200)
        return [RepoCommit(commit, self) for commit in json]

    def list_contributors(self, anon=False):
        """List the contributors to this repository.

        :param anon: (optional), True lists anonymous contributors as well
        :type anon: bool
        :returns: list of :class:`User <github3.user.User>`\ s
        """
        # Paginate
        url = self._build_url('contributors', base_url=self._api)
        params = {}
        if anon:
            params = {'anon': anon}
        json = self._json(self._get(url, params=params), 200)
        return [User(c, self) for c in json]

    def list_downloads(self):
        """List available downloads for this repository.

        :returns: list of :class:`Download <Download>`\ s
        """
        # Paginate?
        url = self._build_url('downloads', base_url=self._api)
        json = self._json(self._get(url), 200)
        return [Download(dl, self) for dl in json]

    def list_events(self):
        """List events on this repository.

        :returns: list of :class:`Event <github3.event.Event>`\ s
        """
        # Paginate
        url = self._build_url('events', base_url=self._api)
        json = self._json(self._get(url), 200)
        return [Event(e, self) for e in json]

    def list_forks(self, sort=''):
        """List forks of this repository.

        :param sort: (optional), accepted values:
            ('newest', 'oldest', 'watchers'), API default: 'newest'
        :type sort: str
        :returns: list of :class:`Repository <Repository>`
        """
        # Paginate?
        url = self._build_url('forks', base_url=self._api)
        params = {}
        if sort in ('newest', 'oldest', 'watchers'):
            params = {'sort': sort}
        json = self._json(self._get(url, params=params), 200)
        return [Repository(r, self) for r in json]

    @GitHubCore.requires_auth
    def list_hooks(self):
        """List hooks registered on this repository.

        :returns: list of :class:`Hook <Hook>`\ s
        """
        # Paginate?
        url = self._build_url('hooks', base_url=self._api)
        json = self._json(self._get(url), 200)
        return [Hook(h, self) for h in json]

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

        :param milestone: (optional), 'none', or '*'
        :type milestone: int
        :param state: (optional), accepted values: ('open', 'closed')
        :type state: str
        :param assignee: (optional), 'none', '*', or login name
        :type assignee: str
        :param mentioned: (optional), user's login name
        :type mentioned: str
        :param labels: (optional), comma-separated list of labels, e.g.
            'bug,ui,@high' :param sort: accepted values:
            ('created', 'updated', 'comments', 'created')
        :type labels: str
        :param direction: (optional), accepted values: ('open', 'closed')
        :type direction: str
        :param since: (optional), ISO 8601 format: YYYY-MM-DDTHH:MM:SSZ
        :type since: str
        :returns: list of :class:`Issue <github3.issue.Issue>`\ s
        """
        # Paginate
        url = self._build_url('issues', base_url=self._api)

        params = {}
        if milestone in ('*', 'none') or isinstance(milestone, int):
            params['milestone'] = str(milestone).lower()
            # str(None) = 'None' which is invalid, so .lower() it to make it
            # work.

        if assignee:
            params['assignee'] = assignee

        if mentioned:
            params['mentioned'] = mentioned

        params.update(issue_params(None, state, labels, sort, direction,
            since))

        request = self._get(url, params=params)

        json = self._json(request, 200)
        return [Issue(i, self) for i in json]

    def list_issue_events(self):
        """List issue events on this repository.

        :returns: list of :class:`IssueEvent <github3.issues.IssueEvent>`\ s
        """
        # Paginate
        url = self._build_url('issues', 'events', base_url=self._api)
        json = self._json(self._get(url), 200)
        return [IssueEvent(e, self) for e in json]

    @GitHubCore.requires_auth
    def list_keys(self):
        """List deploy keys on this repository.

        :returns: list of :class:`Key <github3.user.Key>`\ s
        """
        # Paginate?
        url = self._build_url('keys', base_url=self._api)
        json = self._json(self._get(url), 200)
        return [Key(k, self._session) for k in json]

    def list_labels(self):
        """List labels on this repository.

        :returns: list of :class:`Label <github3.issue.Label>`\ s
        """
        # Paginate?
        url = self._build_url('labels', base_url=self._api)
        json = self._json(self._get(url), 200)
        return [Label(label, self) for label in json]

    def list_languages(self):
        """List the programming languages used in the repository.

        :returns: list of tuples
        """
        # Paginate?
        url = self._build_url('languages', base_url=self._api)
        json = self._json(self._get(url), 200)
        return [(k, v) for k, v in json.items()]

    def list_milestones(self, state=None, sort=None, direction=None):
        """List the milestones on this repository.

        :param state: (optional), state of the milestones, accepted
            values: ('open', 'closed')
        :type state: str
        :param sort: (optional), how to sort the milestones, accepted
            values: ('due_date', 'completeness')
        :type sort: str
        :param direction: (optional), direction to sort the milestones,
            accepted values: ('asc', 'desc')
        :type direction: str
        :returns: list of :class:`Milestone <github3.issue.Milestone>`\ s
        """
        # Paginate?
        url = self._build_url('milestones', base_url=self._api)

        params = {}
        if state in ('open', 'closed'):
            params['state'] = state

        if sort in ('due_date', 'completeness'):
            params['sort'] = sort

        if direction in ('asc', 'desc'):
            params['direction'] = direction

        json = self._json(self._get(url, params=params), 200)
        return [Milestone(mile, self) for mile in json]

    def list_network_events(self):
        """Lists events on a network of repositories.

        :returns: list of :class:`Event <github3.event.Event>`\ s
        """
        # Paginate
        base = self._api.replace('repos', 'networks', 1)
        url = self._build_url('events', base_url=base)
        json = self._json(self._get(url), 200)
        return [Event(e, self) for e in json]

    def list_pulls(self, state=None):
        """List pull requests on repository.

        :param state: (optional), accepted values: ('open', 'closed')
        :type state: str
        :returns: list of :class:`PullRequest <github3.pulls.PullRequest>`\ s
        """
        # Paginate
        url = self._build_url('pulls', base_url=self._api)
        params = {}
        if state in ('open', 'closed'):
            params['state'] = state
        json = self._json(self._get(url, params=params), 200)
        return [PullRequest(pull, self) for pull in json]

    def list_refs(self, subspace=''):
        """List references for this repository.

        :param subspace: (optional), e.g. 'tags', 'stashes', 'notes'
        :type subspace: str
        :returns: list of :class:`Reference <github3.git.Reference>`\ s
        """
        # Paginate?
        if subspace:
            args = ('git', 'refs', subspace)
        else:
            args = ('git', 'refs')
        url = self._build_url(*args, base_url=self._api)
        json = self._json(self._get(url), 200)
        return [Reference(r, self) for r in json]

    def list_tags(self):
        """List tags on this repository.

        :returns: list of :class:`RepoTag <RepoTag>`\ s
        """
        url = self._build_url('tags', base_url=self._api)
        json = self._json(self._get(url), 200)
        return [RepoTag(tag) for tag in json]

    def list_teams(self):
        """List teams with access to this repository.

        :returns: list of dicts
        """
        url = self._build_url('teams', base_url=self._api)
        return self._json(self._get(url), 200)

    def list_watchers(self):
        """List watchers of this repository.

        :returns: list of :class:`User <github3.user.User>`\ s
        """
        url = self._build_url('watchers', base_url=self._api)
        json = self._json(self._get(url), 200)
        return [User(u, self) for u in json]

    def milestone(self, number):
        """Get the milestone indicated by ``number``.

        :param number: (required), unique id number of the milestone
        :type number: int
        :returns: :class:`Milestone <github3.issue.Milestone>`
        """
        url = self._build_url('milestones', str(number), base_url=self._api)
        json = self._json(self._get(url), 200)
        return Milestone(json, self) if json else None

    @property
    def mirror_url(self):
        """Mirror property."""
        return self._mirror

    @property
    def name(self):
        """Name of the repository."""
        return self._name

    @property
    def open_issues(self):
        """Number of open issues on the repository."""
        return self._open_issues

    @property
    def owner(self):
        """:class:`User <github3.user.User>` object representing the
        repository owner."""
        return self._owner

    @GitHubCore.requires_auth
    def pubsubhubbub(self, mode, topic, callback, secret=''):
        """Create/update a pubsubhubbub hook.

        :param mode: (required), accepted values: ('subscribe', 'unsubscribe')
        :type mode: str
        :param topic: (required), form:
            https://github.com/:user/:repo/events/:event
        :type topic: str
        :param callback: (required), the URI that receives the updates
        :type callback: str
        :param secret: (optional), shared secret key that generates a
            SHA1 HMAC of the payload content.
        :type secret: str
        :returns: bool
        """
        from re import match
        m = match('https://github\.com/\w+/\w+/events/\w+', topic)
        status = False
        if mode and topic and callback and m:
            data = {'hub.mode': mode, 'hub.topic': topic,
                    'hub.callback': callback, 'hub.secret': secret}
            url = self._build_url('hub')
            status = self._boolean(self._post(url, data), 201, 404)
        return status

    def pull_request(self, number):
        """Get the pull request indicated by ``number``.

        :param number: (required), number of the pull request.
        :type number: int
        :returns: :class:`PullRequest <github3.pulls.PullRequest>`
        """
        json = None
        if int(number) > 0:
            url = self._build_url('pulls', str(number), base_url=self._api)
            json = self._json(self._get(url), 200)
        return PullRequest(json, self) if json else None

    @property
    def pushed_at(self):
        """``datetime`` object representing the last time commits were pushed
        to the repository."""
        return self._pushed

    def readme(self):
        """Get the README for this repository.

        :returns: :class:`Contents <Contents>`
        """
        url = self._build_url('readme', base_url=self._api)
        json = self._json(self._get(url), 200)
        return Contents(json) if json else None

    def ref(self, ref):
        """Get a reference pointed to by ``ref``.

        The most common will be branches and tags. For a branch, you must
        specify 'heads/branchname' and for a tag, 'tags/tagname'. Essentially,
        the system should return any reference you provide it in the namespace,
        including notes and stashes (provided they exist on the server).

        :param ref: (required)
        :type ref: str
        :returns: :class:`Reference <github3.git.Reference>`
        """
        url = self._build_url('git', 'refs', ref, base_url=self._api)
        json = self._json(self._get(url), 200)
        return Reference(json, self) if json else None

    @GitHubCore.requires_auth
    def remove_collaborator(self, login):
        """Remove collaborator ``login`` from the repository.

        :param login: (required), login name of the collaborator
        :type login: str
        :returns: bool
        """
        resp = False
        if login:
            url = self._build_url('collaborators', login, base_url=self._api)
            resp = self._boolean(self._delete(url), 204, 404)
        return resp

    @property
    def size(self):
        """Size of the repository."""
        return self._size

    @property
    def ssh_url(self):
        """URL to clone the repository via SSH."""
        return self._ssh

    @property
    def svn_url(self):
        """If it exists, url to clone the repository via SVN."""
        return self._svn

    def tag(self, sha):
        """Get an annotated tag.

        http://learn.github.com/p/tagging.html

        :param sha: (required), sha of the object for this tag
        :type sha: str
        :returns: :class:`Tag <github3.git.Tag>`
        """
        url = self._build_url('git', 'tags', sha, base_url=self._api)
        json = self._json(self._get(url), 200)
        return Tag(json) if json else None

    def tree(self, sha):
        """Get a tree.

        :param sha: (required), sha of the object for this tree
        :type sha: str
        :returns: :class:`Tree <github3.git.Tree>`
        """
        url = self._build_url('git', 'trees', sha, base_url=self._api)
        json = self._json(self._get(url), 200)
        return Tree(json, self) if json else None

    @property
    def updated_at(self):
        """``datetime`` object representing the last time the repository was
        updated."""
        return self._updated

    def update_label(self, name, color, new_name=''):
        """Update the label ``name``.

        :param name: (required), name of the label
        :type name: str
        :param color: (required), color code
        :type color: str
        :param new_name: (optional), new name of the label
        :type new_name: str
        :returns: bool
        """
        label = self.get_label(name)
        resp = False
        if label:
            upd = label.update
            resp = upd(new_name, color) if new_name else upd(name, color)
        return resp

    @property
    def watchers(self):
        """Number of users watching the repository."""
        return self._watch


class Branch(GitHubCore):
    """The :class:`Branch <Branch>` object. It holds the information GitHub
    returns about a branch on a :class:`Repository <Repository>`.
    """
    def __init__(self, branch, session=None):
        super(Branch, self).__init__(branch, session)
        self._name = branch.get('name')
        self._commit = None
        if branch.get('commit'):
            self._commit = Commit(branch.get('commit'), self._session)
        self._links = branch.get('_links', {})

    def __repr__(self):
        return '<Repository Branch [{0}]>'.format(self._name)

    @property
    def commit(self):
        """Returns the branch commit."""
        return self._commit

    @property
    def links(self):
        """Returns '_links' attribute."""
        return self._links

    @property
    def name(self):
        """Name of the branch."""
        return self._name


class Contents(GitHubObject):
    """The :class:`Contents <Contents>` object. It holds the information
    concerning any content in a repository requested via the API.
    """

    def __init__(self, content):
        super(Contents, self).__init__(content)
        # links
        self._api = content['_links'].get('self')
        self._links = content.get('_links')

        # should always be 'base64'
        self._enc = content.get('encoding')

        # content, base64 encoded and decoded
        self._content = content.get('content')
        if self._enc == 'base64':
            self._dec = b64decode(self._content.encode())
        else:
            self._dec = self._b64

        # file name, path, and size
        self._name = content.get('name')
        self._path = content.get('path')
        self._sz = content.get('size')

        self._sha = content.get('sha')

        # should always be 'file'
        self._type = content.get('type')

    def __repr__(self):
        return '<Content [{0}]>'.format(self.path)

    @property
    def content(self):
        """Base64-encoded content of the file."""
        return self._content

    @property
    def decoded(self):
        """Decoded content of the file."""
        return self._dec

    @property
    def encoding(self):
        """Returns encoding used on the content."""
        return self._enc

    @property
    def git(self):
        """API URL for this blob"""
        return self._links['git']

    @property
    def html(self):
        """URL pointing to the content on GitHub."""
        return self._links['html']

    @property
    def links(self):
        """Dictionary of links"""
        return self._links

    @property
    def name(self):
        """Name of the content."""
        return self._name

    @property
    def path(self):
        """Path to the content."""
        return self._path

    @property
    def sha(self):
        """SHA string."""
        return self._sha

    @property
    def size(self):
        """Size of the content"""
        return self._sz

    @property
    def type(self):
        """Type of content."""
        return self._type


class Download(GitHubCore):
    """The :class:`Download <Download>` object. It represents how GitHub sends
    information about files uploaded to the downloads section of a repository.
    """

    def __init__(self, download, session=None):
        super(Download, self).__init__(download, session)
        self._api = download.get('url')
        self._html = download.get('html_url')
        self._id = download.get('id')
        self._name = download.get('name')
        self._desc = download.get('description')
        self._sz = download.get('size')
        self._dlct = download.get('download_count')
        self._type = download.get('content_type')

    def __repr__(self):
        return '<Download [{0}]>'.format(self.name)

    @property
    def content_type(self):
        """Content type of the download."""
        return self._type

    @GitHubCore.requires_auth
    def delete(self):
        """Delete this download if authenticated"""
        return self._boolean(self._delete(self._api), 204, 404)

    @property
    def description(self):
        """Description of the download."""
        return self._desc

    @property
    def download_count(self):
        """How many times this particular file has been downloaded."""
        return self._dlct

    @property
    def html_url(self):
        """URL of the download at GitHub."""
        return self._html

    @property
    def id(self):
        """Unique id of the download on GitHub."""
        return self._id

    @property
    def name(self):
        """Name of the download."""
        return self._name

    def saveas(self, path=''):
        """Save this download to the path specified.

        :param path: (optional), if no path is specified, it will be
            saved in the current directory with the name specified by GitHub.
        :type path: str
        :returns: bool
        """
        if not path:
            path = self.name

        resp = self._get(self.html_url, allow_redirects=True)
        if self._boolean(resp, 200, 404):
            with open(path, 'wb') as fd:
                fd.write(resp.content)
                return True
        return False

    @property
    def size(self):
        """Size of the download."""
        return self._sz


class Hook(GitHubCore):
    """The :class:`Hook <Hook>` object. This handles the information returned
    by GitHub about hooks set on a repository."""

    def __init__(self, hook, session=None):
        super(Hook, self).__init__(hook, session)
        self._update_(hook)

    def __repr__(self):
        return '<Hook [{0}]>'.format(self._name)

    def _update_(self, hook):
        self._json_data = hook
        self._api = hook.get('url')
        self._updated = None
        if hook.get('updated_at'):
            self._updated = self._strptime(hook.get('updated_at'))
        self._created = self._strptime(hook.get('created_at'))
        self._name = hook.get('name')
        self._events = hook.get('events')
        self._active = hook.get('active')
        self._config = hook.get('config')
        self._id = hook.get('id')

    @property
    def config(self):
        """Dictionary containing the configuration for the Hook."""
        return self._config

    @property
    def created_at(self):
        """datetime object representing the date the hook was created."""
        return self._created

    @GitHubCore.requires_auth
    def delete(self):
        """Delete this hook.

        :returns: bool
        """
        return self._boolean(self._delete(self._api), 204, 404)

    @GitHubCore.requires_auth
    def edit(self, name, config, events=[], add_events=[], rm_events=[],
            active=True):
        """Edit this hook.

        :param name: (required), name of the service being called
        :type name: str
        :param config: (required), key-value pairs of settings for this
            hook
        :type config: dict
        :param events: (optional), which events should this be triggered
            for
        :type events: list
        :param add_events: (optional), events to be added to the list of
            events that this hook triggers for
        :type add_events: list
        :param rm_events: (optional), events to be remvoed from the list
            of events that this hook triggers for
        :type rm_events: list
        :param active: (optional), should this event be active
        :type active: bool
        :returns: bool
        """
        if name and config and isinstance(config, dict):
            data = {'name': name, 'config': config, 'active': active}
            if events:
                data['events'] = events

            if add_events:
                data['add_events'] = add_events

            if rm_events:
                data['remove_events'] = rm_events

            json = self._json(self._patch(self._api, data=dumps(data)), 200)

        if json:
            self._update_(json)
            return True
        return False

    @property
    def events(self):
        """Events which trigger the hook."""
        return self._events

    @property
    def id(self):
        """Unique id of the hook."""
        return self._id

    def is_active(self):
        """Checks whether the hook is marked as active on GitHub or not.

        :returns: bool
        """
        return self._active

    @property
    def name(self):
        """The name of the hook."""
        return self._name

    @GitHubCore.requires_auth
    def test(self):
        """Test this hook

        :returns: bool
        """
        return self._boolean(self._post(self._api + '/test'), 204, 404)

    @property
    def updated_at(self):
        """datetime object representing when this hook was last updated."""
        return self._updated


class RepoTag(GitHubObject):
    """The :class:`RepoTag <RepoTag>` object. This stores the information
    representing a tag that was created on a repository.
    """

    def __init__(self, tag):
        super(RepoTag, self).__init__(tag)
        self._name = tag.get('name')
        self._zip = tag.get('zipball_url')
        self._tar = tag.get('tarball_url')
        self._commit = tag.get('commit', {})

    def __repr__(self):
        return '<Repository Tag [{0}]>'.format(self._name)

    @property
    def commit(self):
        """Dictionary containing the SHA and URL of the commit."""
        return self._commit

    @property
    def name(self):
        """Name of the tag."""
        return self._name

    @property
    def tarball_url(self):
        """URL for the GitHub generated tarball associated with the tag."""
        return self._tar

    @property
    def zipball_url(self):
        """URL for the GitHub generated zipball associated with the tag."""
        return self._zip


class RepoComment(BaseComment):
    """The :class:`RepoComment <RepoComment>` object. This stores the
    information about a comment on a file in a repository.
    """

    def __init__(self, comment, session=None):
        super(RepoComment, self).__init__(comment, session)
        self._update_(comment)

    def __repr__(self):
        return '<Repository Comment [{0}]>'.format(self._user.login)

    def _update_(self, comment):
        super(RepoComment, self)._update_(comment)
        self._cid = comment.get('commit_id')
        self._html = comment.get('html_url')
        self._line = comment.get('line')
        self._path = comment.get('path')
        self._pos = comment.get('position')
        self._updated = comment.get('updated_at')
        self._user = None
        if comment.get('user'):
            self._user = User(comment.get('user'), self)

    @property
    def commit_id(self):
        """Commit id on which the comment was made."""
        return self._cid

    @property
    def html_url(self):
        """URL of the comment on GitHub."""
        return self._html

    @property
    def line(self):
        """The line number where the comment is located."""
        return self._line

    @property
    def path(self):
        """The path to the file where the comment was made."""
        return self._path

    @property
    def position(self):
        """The position in the diff where the comment was made."""
        return self._pos

    @GitHubCore.requires_auth
    def update(self, body, sha, line, path, position):
        """Update this comment.

        :param body: (required)
        :type body: str
        :param sha: (required), sha id of the commit to comment on
        :type sha: str
        :param line: (required), line number to comment on
        :type line: int
        :param path: (required), relative path of the file you're
            commenting on
        :type path: str
        :param position: (required), line index in the diff to comment on
        :type position: int
        :returns: bool
        """
        json = None
        if body and sha and path and line > 0 and position > 0:
            data = dumps({'body': body, 'commit_id': sha, 'line': line,
                'path': path, 'position': position})
            json = self._json(self._post(self._api, data), 200)

        if json:
            self._update_(json)
            return True
        return False

    @property
    def updated_at(self):
        """datetime object representing when the comment was updated."""
        return self._updated

    @property
    def user(self):
        """Login of the user who left the comment."""
        return self._user


class RepoCommit(BaseCommit):
    """The :class:`RepoCommit <RepoCommit>` object. This represents a commit as
    viewed by a :class:`Repository`. This is different from a Commit object
    returned from the git data section.
    """

    def __init__(self, commit, session=None):
        super(RepoCommit, self).__init__(commit, session)
        self._author = User(commit.get('author'), self._session)
        self._committer = User(commit.get('committer'), self._session)
        self._commit = Commit(commit.get('commit'), self._session)

        if commit.get('stats'):
            self._addts = commit['stats'].get('additions')
            self._delts = commit['stats'].get('deletions')
            self._total = commit['stats'].get('total')
        else:
            self._addts = self._delts = self._total = 0

        self._files = []
        if commit.get('files'):
            append = self._files.append
            for f in commit.get('files'):
                append(type('RepoCommit File', (object, ), f))

    def __repr__(self):
        return '<Repository Commit [{0}]>'.format(self._sha)

    @property
    def additions(self):
        """The number of additions made in the commit."""
        return self._addts

    @property
    def author(self):
        """:class:`User <github3.user.User>` who authored the commit."""
        return self._author

    @property
    def commit(self):
        """:class:`Commit <github3.git.Commit>`."""
        return self._commit

    @property
    def committer(self):
        """:class:`User <github3.user.User>` who committed the commit."""
        return self._committer

    @property
    def deletions(self):
        """The number of deletions made in the commit."""
        return self._delts

    @property
    def files(self):
        """The files that were modified by this commit."""
        return self._files

    @property
    def total(self):
        """Total number of changes in the files."""
        return self._total


class Comparison(GitHubObject):
    """The :class:`Comparison <Comparison>` object. This encapsulates the
    information returned by GitHub comparing two commit objects in a
    repository."""

    def __init__(self, compare):
        super(Comparison, self).__init__(compare)
        self._api = compare.get('api')
        self._html = compare.get('html_url')
        self._perma = compare.get('permalink_url')
        self._diff = compare.get('diff_url')
        self._patch = compare.get('patch_url')
        self._base = RepoCommit(compare.get('base_commit'), None)
        self._stat = compare.get('status')
        self._ahead_by = compare.get('ahead_by')
        self._behind = compare.get('behind_by')
        self._ttl_commits = compare.get('total_commits')
        self._commits = [RepoCommit(com, None) for com in
                compare.get('commits')]
        self._files = []
        if compare.get('files'):
            append = self._files.append
            for f in compare.get('files'):
                append(type('Comparison File', (object, ), f))

    def __repr__(self):
        return '<Comparison of {0} commits>'.format(self.total_commits)

    @property
    def ahead_by(self):
        """Number of commits ahead by."""
        return self._ahead_by

    @property
    def base_commit(self):
        """:class:`RepoCommit <RepoCommit>` object representing the base of
        comparison.
        """
        return self._base

    @property
    def behind_by(self):
        """Number of commits behind by."""
        return self._behind

    @property
    def commits(self):
        """List of :class:`RepoCommit <RepoCommit>` objects."""
        return self._commits

    @property
    def diff_url(self):
        """URL to see the diff between the two commits."""
        return self._diff

    @property
    def files(self):
        """List of objects describing the files modified."""
        return self._files

    @property
    def html_url(self):
        """URL to view the comparison at GitHub."""
        return self._html

    @property
    def patch_url(self):
        """Patch URL at GitHub for the comparison."""
        return self._patch

    @property
    def permalink_url(self):
        """Permanent link to this comparison."""
        return self._perma

    @property
    def status(self):
        """Behind or ahead."""
        return self._stat

    @property
    def total_commits(self):
        """Number of commits difference in the comparison."""
        return self._ttl_commits
