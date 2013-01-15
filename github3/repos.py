"""
github3.repos
=============

This module contains the classes relating to repositories.

"""

from json import dumps
from base64 import b64decode
from collections import Callable
from github3.events import Event
from github3.issues import Issue, IssueEvent, Label, Milestone, issue_params
from github3.git import Blob, Commit, Reference, Tag, Tree
from github3.models import GitHubObject, GitHubCore, BaseComment, BaseCommit
from github3.pulls import PullRequest
from github3.users import User, Key
from github3.decorators import requires_auth
from github3.notifications import Subscription, Thread


class Repository(GitHubCore):
    """The :class:`Repository <Repository>` object. It represents how GitHub
    sends information about repositories.
    """
    def __init__(self, repo, session=None):
        super(Repository, self).__init__(repo, session)
        #: URL used to clone via HTTPS.
        self.clone_url = repo.get('clone_url', '')
        #: ``datetime`` object representing when the Repository was created.
        self.created_at = self._strptime(repo.get('created_at'))
        #: Description of the repository.
        self.description = repo.get('description', '')

        # The number of forks
        #: The number of forks made of this repository.
        self.forks = repo.get('forks', 0)

        #: Is this repository a fork?
        self.fork = repo.get('fork')

        #: Full name as login/name
        self.full_name = repo.get('full_name', '')

        # Clone url using git, e.g. git://github.com/sigmavirus24/github3.py
        #: Plain git url for an anonymous clone.
        self.git_url = repo.get('git_url', '')
        #: Whether or not this repository has downloads enabled
        self.has_downloads = repo.get('has_downloads')
        #: Whether or not this repository has an issue tracker
        self.has_issues = repo.get('has_issues')
        #: Whether or not this repository has the wiki enabled
        self.has_wiki = repo.get('has_wiki')

        # e.g. https://sigmavirus24.github.com/github3.py
        #: URL of the home page for the project.
        self.homepage = repo.get('homepage', '')

        # e.g. https://github.com/sigmavirus24/github3.py
        #: URL of the project at GitHub.
        self.html_url = repo.get('html_url', '')
        #: Unique id of the repository.
        self.id = repo.get('id', 0)
        #: Language property.
        self.language = repo.get('language', '')
        #: Mirror property.
        self.mirror_url = repo.get('mirror_url', '')

        # Repository name, e.g. github3.py
        #: Name of the repository.
        self.name = repo.get('name', '')

        # Number of open issues
        #: Number of open issues on the repository.
        self.open_issues = repo.get('open_issues', 0)

        # Repository owner's name
        #: :class:`User <github3.users.User>` object representing the
        #  repository owner.
        self.owner = User(repo.get('owner', {}), self._session)

        #: Is this repository private?
        self.private = repo.get('private')
        #: ``datetime`` object representing the last time commits were pushed
        #  to the repository.
        self.pushed_at = self._strptime(repo.get('pushed_at'))
        #: Size of the repository.
        self.size = repo.get('size', 0)

        # SSH url e.g. git@github.com/sigmavirus24/github3.py
        #: URL to clone the repository via SSH.
        self.ssh_url = repo.get('ssh_url', '')
        #: If it exists, url to clone the repository via SVN.
        self.svn_url = repo.get('svn_url', '')
        #: ``datetime`` object representing the last time the repository was
        #  updated.
        self.updated_at = self._strptime(repo.get('updated_at'))
        self._api = repo.get('url', '')

        # The number of watchers
        #: Number of users watching the repository.
        self.watchers = repo.get('watchers', 0)

        #: Parent of this fork, if it exists :class;`Repository`
        self.source = repo.get('source')
        if self.source:
            self.source = Repository(self.source, self)

        #: Parent of this fork, if it exists :class:`Repository`
        self.parent = repo.get('parent')
        if self.parent:
            self.parent = Repository(self.parent, self)

        #: default branch for the repository
        self.master_branch = repo.get('master_branch', '')

    def __repr__(self):
        return '<Repository [{0}]>'.format(self)

    def __str__(self):
        return self.full_name

    def _update_(self, repo):
        self.__init__(repo, self._session)

    def _create_pull(self, data):
        self._remove_none(data)
        json = None
        if data:
            url = self._build_url('pulls', base_url=self._api)
            json = self._json(self._post(url, data=dumps(data)), 201)
        return PullRequest(json, self._session) if json else None

    @requires_auth
    def add_collaborator(self, login):
        """Add ``login`` as a collaborator to a repository.

        :param str login: (required), login of the user
        :returns: bool -- True if successful, False otherwise
        """
        resp = False
        if login:
            url = self._build_url('collaborators', login, base_url=self._api)
            resp = self._boolean(self._put(url), 204, 404)
        return resp

    def archive(self, format, path='', ref='master'):
        """Get the tarball or zipball archive for this repo at ref.

        :param str format: (required), accepted values: ('tarball',
            'zipball')
        :param path: (optional), path where the file should be saved
            to, default is the filename provided in the headers and will be
            written in the current directory.
            it can take a file-like object as well
        :type path: str, file
        :param str ref: (optional)
        :returns: bool -- True if successful, False otherwise
        """
        resp = None
        written = False
        if format in ('tarball', 'zipball'):
            url = self._build_url(format, ref, base_url=self._api)
            resp = self._get(url, allow_redirects=True, stream=True)

        pre_opened = False
        if resp and self._boolean(resp, 200, 404):
            fd = None
            if path:
                if isinstance(getattr(path, 'write', None), Callable):
                    pre_opened = True
                    fd = path
                else:
                    fd = open(path, 'wb')
            else:
                header = resp.headers['content-disposition']
                i = header.find('filename=') + len('filename=')
                fd = open(header[i:], 'wb')
            for chunk in resp.iter_content():
                fd.write(chunk)

            if not pre_opened:
                fd.close()

            written = True
        return written

    def blob(self, sha):
        """Get the blob indicated by ``sha``.

        :param str sha: (required), sha of the blob
        :returns: :class:`Blob <github3.git.Blob>` if successful, otherwise
            None
        """
        url = self._build_url('git', 'blobs', sha, base_url=self._api)
        json = self._json(self._get(url), 200)
        return Blob(json) if json else None

    def branch(self, name):
        """Get the branch ``name`` of this repository.

        :param str name: (required), branch name
        :type name: str
        :returns: :class:`Branch <Branch>`
        """
        json = None
        if name:
            url = self._build_url('branches', name, base_url=self._api)
            json = self._json(self._get(url), 200)
        return Branch(json, self) if json else None

    def commit(self, sha):
        """Get a single (repo) commit. See :func:`git_commit` for the Git Data
        Commit.

        :param str sha: (required), sha of the commit
        :returns: :class:`RepoCommit <RepoCommit>` if successful, otherwise
            None
        """
        url = self._build_url('commits', sha, base_url=self._api)
        json = self._json(self._get(url), 200)
        return RepoCommit(json, self) if json else None

    def commit_comment(self, comment_id):
        """Get a single commit comment.

        :param int comment_id: (required), id of the comment used by GitHub
        :returns: :class:`RepoComment <RepoComment>` if successful, otherwise
            None
        """
        url = self._build_url('comments', str(comment_id), base_url=self._api)
        json = self._json(self._get(url), 200)
        return RepoComment(json, self) if json else None

    def compare_commits(self, base, head):
        """Compare two commits.

        :param str base: (required), base for the comparison
        :param str head: (required), compare this against base
        :returns: :class:`Comparison <Comparison>` if successful, else None
        """
        url = self._build_url('compare', base + '...' + head,
                              base_url=self._api)
        json = self._json(self._get(url), 200)
        return Comparison(json) if json else None

    def contents(self, path):
        """Get the contents of the file pointed to by ``path``.

        :param str path: (required), path to file, e.g.
            github3/repo.py
        :returns: :class:`Contents <Contents>` if successful, else None
        """
        url = self._build_url('contents', path, base_url=self._api)
        resp = self._get(url)
        if self._boolean(resp, 200, 404):
            return Contents(self._json(resp, 200))
        else:
            return None

    @requires_auth
    def create_blob(self, content, encoding):
        """Create a blob with ``content``.

        :param str content: (required), content of the blob
        :param str encoding: (required), ('base64', 'utf-8')
        :returns: string of the SHA returned
        """
        sha = ''
        if encoding in ('base64', 'utf-8') and content:
            url = self._build_url('git', 'blobs', base_url=self._api)
            data = {'content': content, 'encoding': encoding}
            json = self._json(self._post(url, data=dumps(data)), 201)
            if json:
                sha = json.get('sha')
        return sha

    @requires_auth
    def create_comment(self, body, sha, path='', position=1, line=1):
        """Create a comment on a commit.

        :param str body: (required), body of the message
        :param str sha: (required), commit id
        :param str path: (optional), relative path of the file to comment
            on
        :param str position: (optional), line index in the diff to comment on
        :param int line: (optional), line number of the file to comment on,
            default: 1
        :returns: :class:`RepoComment <RepoComment>` if successful else None
        """
        line = int(line)
        position = int(position)
        json = None
        if body and sha and line > 0:
            data = {'body': body, 'commit_id': sha, 'line': line,
                    'path': path, 'position': position}
            url = self._build_url('commits', sha, 'comments',
                                  base_url=self._api)
            json = self._json(self._post(url, data=dumps(data)), 201)
        return RepoComment(json, self) if json else None

    @requires_auth
    def create_commit(self, message, tree, parents, author={}, committer={}):
        """Create a commit on this repository.

        :param str message: (required), commit message
        :param str tree: (required), SHA of the tree object this
            commit points to
        :param list parents: (required), SHAs of the commits that were parents
            of this commit. If empty, the commit will be written as the root
            commit.  Even if there is only one parent, this should be an
            array.
        :param dict author: (optional), if omitted, GitHub will
            use the authenticated user's credentials and the current
            time. Format: {'name': 'Committer Name', 'email':
            'name@example.com', 'date': 'YYYY-MM-DDTHH:MM:SS+HH:00'}
        :param dict committer: (optional), if ommitted, GitHub will use the
            author parameters. Should be the same format as the author
            parameter.
        :returns: :class:`Commit <github3.git.Commit>` if successful, else
            None
        """
        json = None
        if message and tree and isinstance(parents, list):
            url = self._build_url('git', 'commits', base_url=self._api)
            data = {'message': message, 'tree': tree, 'parents': parents,
                    'author': author, 'committer': committer}
            json = self._json(self._post(url, data=dumps(data)), 201)
        return Commit(json, self) if json else None

    @requires_auth
    def create_fork(self, organization=None):
        """Create a fork of this repository.

        :param str organization: (required), login for organization to create
            the fork under
        :returns: :class:`Repository <Repository>` if successful, else None
        """
        url = self._build_url('forks', base_url=self._api)
        if organization:
            resp = self._post(url, data=dumps({'organization': organization}))
        else:
            resp = self._post(url)
        json = self._json(resp, 202)

        return Repository(json, self) if json else None

    @requires_auth
    def create_hook(self, name, config, events=['push'], active=True):
        """Create a hook on this repository.

        :param str name: (required), name of the hook
        :param dict config: (required), key-value pairs which act as settings
            for this hook
        :param list events: (optional), events the hook is triggered for
        :param bool active: (optional), whether the hook is actually
            triggered
        :returns: :class:`Hook <Hook>` if successful, else None
        """
        json = None
        if name and config and isinstance(config, dict):
            url = self._build_url('hooks', base_url=self._api)
            data = {'name': name, 'config': config, 'events': events,
                    'active': active}
            json = self._json(self._post(url, data=dumps(data)), 201)
        return Hook(json, self) if json else None

    @requires_auth
    def create_issue(self,
                     title,
                     body=None,
                     assignee=None,
                     milestone=None,
                     labels=None):
        """Creates an issue on this repository.

        :param str title: (required), title of the issue
        :param str body: (optional), body of the issue
        :param str assignee: (optional), login of the user to assign the
            issue to
        :param int milestone: (optional), number of the milestone to attribute
            this issue to (e.g. ``m`` is a Milestone object, ``m.number`` is
            what you pass here.)
        :param labels: (optional), labels to apply to this
            issue
        :type labels: list of strings
        :returns: :class:`Issue <github3.issues.Issue>` if successful, else
            None
        """
        issue = {'title': title, 'body': body, 'assignee': assignee,
                 'milestone': milestone, 'labels': labels}
        self._remove_none(issue)
        json = None

        if issue:
            url = self._build_url('issues', base_url=self._api)
            json = self._json(self._post(url, data=dumps(issue)), 201)

        return Issue(json, self) if json else None

    @requires_auth
    def create_key(self, title, key):
        """Create a deploy key.

        :param str title: (required), title of key
        :param str key: (required), key text
        :returns: :class:`Key <github3.users.Key>` if successful, else None
        """
        json = None
        if title and key:
            data = {'title': title, 'key': key}
            url = self._build_url('keys', base_url=self._api)
            json = self._json(self._post(url, data=dumps(data)), 201)
        return Key(json, self) if json else None

    @requires_auth
    def create_label(self, name, color):
        """Create a label for this repository.

        :param str name: (required), name to give to the label
        :param str color: (required), value of the color to assign to the
            label
        :returns: :class:`Label <github3.issues.Label>` if successful, else
            None
        """
        json = None
        if name and color:
            data = {'name': name, 'color': color.strip('#')}
            url = self._build_url('labels', base_url=self._api)
            json = self._json(self._post(url, data=dumps(data)), 201)
        return Label(json, self) if json else None

    @requires_auth
    def create_milestone(self, title, state=None, description=None,
                         due_on=None):
        """Create a milestone for this repository.

        :param str title: (required), title of the milestone
        :param str state: (optional), state of the milestone, accepted
            values: ('open', 'closed'), default: 'open'
        :param str description: (optional), description of the milestone
        :param str due_on: (optional), ISO 8601 formatted due date
        :returns: :class:`Milestone <github3.issues.Milestone>` if successful,
            else None
        """
        url = self._build_url('milestones', base_url=self._api)
        if state not in ('open', 'closed'):
            state = None
        data = {'title': title, 'state': state,
                'description': description, 'due_on': due_on}
        self._remove_none(data)
        json = None
        if data:
            json = self._json(self._post(url, data=dumps(data)), 201)
        return Milestone(json, self) if json else None

    @requires_auth
    def create_pull(self, title, base, head, body=None):
        """Create a pull request using commits from ``head`` and comparing
        against ``base``.

        :param str title: (required)
        :param str base: (required), e.g., 'username:branch', or a sha
        :param str head: (required), e.g., 'master', or a sha
        :param str body: (optional), markdown formatted description
        :returns: :class:`PullRequest <github3.pulls.PullRequest>` if
            successful, else None
        """
        data = {'title': title, 'body': body, 'base': base,
                'head': head}
        return self._create_pull(data)

    @requires_auth
    def create_pull_from_issue(self, issue, base, head):
        """Create a pull request from issue #``issue``.

        :param int issue: (required), issue number
        :param str base: (required), e.g., 'username:branch', or a sha
        :param str head: (required), e.g., 'master', or a sha
        :returns: :class:`PullRequest <github3.pulls.PullRequest>` if
            successful, else None
        """
        if issue > 0:
            data = {'issue': issue, 'base': base, 'head': head}
            return self._create_pull(data)
        return None

    @requires_auth
    def create_ref(self, ref, sha):
        """Create a reference in this repository.

        :param str ref: (required), fully qualified name of the reference,
            e.g. ``refs/heads/master``. If it doesn't start with ``refs`` and
            contain at least two slashes, GitHub's API will reject it.
        :param str sha: (required), SHA1 value to set the reference to
        :returns: :class:`Reference <github3.git.Reference>` if successful
            else None
        """
        json = None
        if ref and ref.count('/') >= 2 and sha:
            data = {'ref': ref, 'sha': sha}
            url = self._build_url('git', 'refs', base_url=self._api)
            json = self._json(self._post(url, data=dumps(data)), 201)
        return Reference(json, self) if json else None

    @requires_auth
    def create_status(self, sha, state, target_url='', description=''):
        """Create a status object on a commit.

        :param str sha: (required), SHA of the commit to create the status on
        :param str state: (required), state of the test; only the following
            are accepted: 'pending', 'success', 'error', 'failure'
        :param str target_url: (optional), URL to associate with this status.
        :param str description: (optional), short description of the status
        """
        json = {}
        if sha and state:
            data = {'state': state, 'target_url': target_url,
                    'description': description}
            url = self._build_url('statuses', sha, base_url=self._api)
            json = self._json(self._post(url, data=dumps(data)), 201)
        return Status(json) if json else None

    @requires_auth
    def create_tag(self, tag, message, sha, obj_type, tagger,
                   lightweight=False):
        """Create a tag in this repository.

        :param str tag: (required), name of the tag
        :param str message: (required), tag message
        :param str sha: (required), SHA of the git object this is tagging
        :param str obj_type: (required), type of object being tagged, e.g.,
            'commit', 'tree', 'blob'
        :param dict tagger: (required), containing the name, email of the
            tagger and the date it was tagged
        :param bool lightweight: (optional), if False, create an annotated
            tag, otherwise create a lightweight tag (a Reference).
        :returns: If lightweight == False: :class:`Tag <github3.git.Tag>` if
            successful, else None. If lightweight == True: :class:`Reference
            <Reference>`
        """
        if lightweight and tag and sha:
            return self.create_ref('refs/tags/' + tag, sha)

        json = None
        if tag and message and sha and obj_type and len(tagger) == 3:
            data = {'tag': tag, 'message': message, 'object': sha,
                    'type': obj_type, 'tagger': tagger}
            url = self._build_url('git', 'tags', base_url=self._api)
            json = self._json(self._post(url, data=dumps(data)), 201)
            if json:
                self.create_ref('refs/tags/' + tag, sha)
        return Tag(json) if json else None

    @requires_auth
    def create_tree(self, tree, base_tree=''):
        """Create a tree on this repository.

        :param list tree: (required), specifies the tree structure.
            Format: [{'path': 'path/file', 'mode':
            'filemode', 'type': 'blob or tree', 'sha': '44bfc6d...'}]
        :param str base_tree: (optional), SHA1 of the tree you want
            to update with new data
        :returns: :class:`Tree <github3.git.Tree>` if successful, else None
        """
        json = None
        if tree and isinstance(tree, list):
            data = {'tree': tree, 'base_tree': base_tree}
            url = self._build_url('git', 'trees', base_url=self._api)
            json = self._json(self._post(url, data=dumps(data)), 201)
        return Tree(json) if json else None

    @requires_auth
    def delete(self):
        """Delete this repository.

        :returns: bool -- True if successful, False otherwise
        """
        return self._boolean(self._delete(self._api), 204, 404)

    @requires_auth
    def delete_key(self, key_id):
        """Delete the key with the specified id from your deploy keys list.

        :returns: bool -- True if successful, False otherwise
        """
        if int(key_id) <= 0:
            return False
        url = self._build_url('keys', str(key_id), base_url=self._api)
        return self._boolean(self._delete(url), 204, 404)

    def download(self, id_num):
        """Get a single download object by its id.

        .. warning::

            On 2012-03-11, GitHub will be deprecating the Downloads API. This
            method will no longer work.

        :param int id_num: (required), id of the download
        :returns: :class:`Download <Download>` if successful, else None
        """
        json = None
        if int(id_num) > 0:
            url = self._build_url('downloads', str(id_num),
                                  base_url=self._api)
            json = self._json(self._get(url), 200)
        return Download(json, self) if json else None

    @requires_auth
    def edit(self,
             name,
             description=None,
             homepage=None,
             private=None,
             has_issues=None,
             has_wiki=None,
             has_downloads=None,
             default_branch=None):
        """Edit this repository.

        :param str name: (required), name of the repository
        :param str description: (optional), If not ``None``, change the
            description for this repository. API default: ``None`` - leave
            value unchanged.
        :param str homepage: (optional), If not ``None``, change the homepage
            for this repository. API default: ``None`` - leave value unchanged.
        :param bool private: (optional), If ``True``, make the repository
            private. If ``False``, make the repository public. API default:
            ``None`` - leave value unchanged.
        :param bool has_issues: (optional), If ``True``, enable issues for
            this repository. If ``False``, disable issues for this repository.
            API default: ``None`` - leave value unchanged.
        :param bool has_wiki: (optional), If ``True``, enable the wiki for
            this repository. If ``False``, disable the wiki for this
            repository. API default: ``None`` - leave value unchanged.
        :param bool has_downloads: (optional), If ``True``, enable downloads
            for this repository. If ``False``, disable downloads for this
            repository. API default: ``None`` - leave value unchanged.
        :param str default_branch: (optional), If not ``None``, change the
            default branch for this repository. API default: ``None`` - leave
            value unchanged.
        :returns: bool -- True if successful, False otherwise
        """
        edit = {'name': name, 'description': description, 'homepage': homepage,
                'private': private, 'has_issues': has_issues,
                'has_wiki': has_wiki, 'has_downloads': has_downloads,
                'default_branch': default_branch}
        self._remove_none(edit)
        json = None
        if edit:
            json = self._json(self._patch(self._api, data=dumps(edit)), 200)
            self._update_(json)
            return True
        return False

    def is_collaborator(self, login):
        """Check to see if ``login`` is a collaborator on this repository.

        :param str login: (required), login for the user
        :returns: bool -- True if successful, False otherwise
        """
        if login:
            url = self._build_url('collaborators', login, base_url=self._api)
            return self._boolean(self._get(url), 204, 404)
        return False

    def git_commit(self, sha):
        """Get a single (git) commit.

        :param str sha: (required), sha of the commit
        :returns: :class:`Commit <github3.git.Commit>` if successful,
            otherwise None
        """
        json = {}
        if sha:
            url = self._build_url('git', 'commits', sha, base_url=self._api)
            json = self._json(self._get(url), 200)
        return Commit(json, self) if json else None

    @requires_auth
    def hook(self, id_num):
        """Get a single hook.

        :param int id_num: (required), id of the hook
        :returns: :class:`Hook <Hook>` if successful, else None
        """
        json = None
        if int(id_num) > 0:
            url = self._build_url('hooks', str(id_num), base_url=self._api)
            json = self._json(self._get(url), 200)
        return Hook(json, self) if json else None

    def is_assignee(self, login):
        """Check if the user is a possible assignee for an issue on this
        repository.

        :returns: :class:`bool`
        """
        if not login:
            return False
        url = self._build_url('assignees', login, base_url=self._api)
        return self._boolean(self._get(url), 204, 404)

    def issue(self, number):
        """Get the issue specified by ``number``.

        :param int number: (required), number of the issue on this repository
        :returns: :class:`Issue <github3.issues.Issue>` if successful, else
            None
        """
        json = None
        if int(number) > 0:
            url = self._build_url('issues', str(number), base_url=self._api)
            json = self._json(self._get(url), 200)
        return Issue(json, self) if json else None

    @requires_auth
    def key(self, id_num):
        """Get the specified deploy key.

        :param int id_num: (required), id of the key
        :returns: :class:`Key <Key>` if successful, else None
        """
        json = None
        if int(id_num) > 0:
            url = self._build_url('keys', str(id_num), base_url=self._api)
            json = self._json(self._get(url), 200)
        return Key(json, self) if json else None

    def label(self, name):
        """Get the label specified by ``name``

        :param str name: (required), name of the label
        :returns: :class:`Label <github3.issues.Label>` if successful, else
            None
        """
        json = None
        if name:
            url = self._build_url('labels', name, base_url=self._api)
            json = self._json(self._get(url), 200)
        return Label(json, self) if json else None

    def iter_assignees(self, number=-1):
        """Iterate over all available assignees to which an issue may be
        assigned.

        :param int number: (optional), number of assignees to return. Default:
            -1 returns all available assignees
        :returns: list of :class:`User <github3.users.User>`\ s
        """
        url = self._build_url('assignees', base_url=self._api)
        return self._iter(int(number), url, User)

    def iter_branches(self, number=-1):
        """Iterate over the branches in this repository.

        :param int number: (optional), number of branches to return. Default:
            -1 returns all branches
        :returns: list of :class:`Branch <Branch>`\ es
        """
        url = self._build_url('branches', base_url=self._api)
        return self._iter(int(number), url, Branch)

    def iter_comments(self, number=-1):
        """Iterate over comments on all commits in the repository.

        :param int number: (optional), number of comments to return. Default:
            -1 returns all comments
        :returns: list of :class:`RepoComment <RepoComment>`\ s
        """
        url = self._build_url('comments', base_url=self._api)
        return self._iter(int(number), url, RepoComment)

    def iter_comments_on_commit(self, sha, number=1):
        """Iterate over comments for a single commit.

        :param sha: (required), sha of the commit to list comments on
        :type sha: str
        :param int number: (optional), number of comments to return. Default:
            -1 returns all comments
        :returns: list of :class:`RepoComment <RepoComment>`\ s
        """
        url = self._build_url('commits', sha, 'comments', base_url=self._api)
        return self._iter(int(number), url, RepoComment)

    def iter_commits(self, sha=None, path=None, author=None, number=-1):
        """Iterate over commits in this repository.

        :param str sha: (optional), sha or branch to start listing commits
            from
        :param str path: (optional), commits containing this path will be
            listed
        :param str author: (optional), GitHub login, real name, or email to
            filter commits by (using commit author)
        :param int number: (optional), number of comments to return. Default:
            -1 returns all comments

        :returns: list of :class:`RepoCommit <RepoCommit>`\ s
        """
        params = {'sha': sha, 'path': path, 'author': author}
        self._remove_none(params)
        url = self._build_url('commits', base_url=self._api)
        return self._iter(int(number), url, RepoCommit, params=params)

    def iter_contributors(self, anon=False, number=-1):
        """Iterate over the contributors to this repository.

        :param bool anon: (optional), True lists anonymous contributors as
            well
        :param int number: (optional), number of contributors to return.
            Default: -1 returns all contributors
        :returns: list of :class:`User <github3.users.User>`\ s
        """
        url = self._build_url('contributors', base_url=self._api)
        params = {}
        if anon:
            params = {'anon': True}
        return self._iter(int(number), url, User, params=params)

    def iter_downloads(self, number=-1):
        """Iterate over available downloads for this repository.

        .. warning::

            On 2012-03-11, GitHub will be deprecating the Downloads API. This
            method will no longer work.

        :param int number: (optional), number of downloads to return. Default:
            -1 returns all available downloads
        :returns: list of :class:`Download <Download>`\ s
        """
        url = self._build_url('downloads', base_url=self._api)
        return self._iter(int(number), url, Download)

    def iter_events(self, number=-1):
        """Iterate over events on this repository.

        :param int number: (optional), number of events to return. Default: -1
            returns all available events
        :returns: list of :class:`Event <github3.events.Event>`\ s
        """
        url = self._build_url('events', base_url=self._api)
        return self._iter(int(number), url, Event)

    def iter_forks(self, sort='', number=-1):
        """Iterate over forks of this repository.

        :param str sort: (optional), accepted values:
            ('newest', 'oldest', 'watchers'), API default: 'newest'
        :param int number: (optional), number of forks to return. Default: -1
            returns all forks
        :returns: list of :class:`Repository <Repository>`
        """
        url = self._build_url('forks', base_url=self._api)
        params = {}
        if sort in ('newest', 'oldest', 'watchers'):
            params = {'sort': sort}
        return self._iter(int(number), url, Repository, params=params)

    @requires_auth
    def iter_hooks(self, number=-1):
        """Iterate over hooks registered on this repository.

        :param int number: (optional), number of hoks to return. Default: -1
            returns all hooks
        :returns: list of :class:`Hook <Hook>`\ s
        """
        url = self._build_url('hooks', base_url=self._api)
        return self._iter(int(number), url, Hook)

    def iter_issues(self,
                    milestone=None,
                    state=None,
                    assignee=None,
                    mentioned=None,
                    labels=None,
                    sort=None,
                    direction=None,
                    since=None,
                    number=-1):
        """Iterate over issues on this repo based upon parameters passed.

        :param int milestone: (optional), 'none', or '*'
        :param str state: (optional), accepted values: ('open', 'closed')
        :param str assignee: (optional), 'none', '*', or login name
        :param str mentioned: (optional), user's login name
        :param str labels: (optional), comma-separated list of labels, e.g.
            'bug,ui,@high' :param sort: accepted values:
            ('created', 'updated', 'comments', 'created')
        :param str direction: (optional), accepted values: ('asc', 'desc')
        :param str since: (optional), ISO 8601 format: YYYY-MM-DDTHH:MM:SSZ
        :param int number: (optional), Number of issues to return.
            By default all issues are returned
        :returns: list of :class:`Issue <github3.issues.Issue>`\ s
        """
        url = self._build_url('issues', base_url=self._api)

        params = {'assignee': assignee, 'mentioned': mentioned}
        if milestone in ('*', 'none') or isinstance(milestone, int):
            params['milestone'] = milestone
        self._remove_none(params)
        params.update(issue_params(None, state, labels, sort, direction,
            since))  # nopep8

        return self._iter(int(number), url, Issue, params=params)

    def iter_issue_events(self, number=-1):
        """Iterates over issue events on this repository.

        :param int number: (optional), number of events to return. Default: -1
            returns all available events
        :returns: generator of
            :class:`IssueEvent <github3.issues.IssueEvent>`\ s
        """
        url = self._build_url('issues', 'events', base_url=self._api)
        return self._iter(int(number), url, IssueEvent)

    @requires_auth
    def iter_keys(self, number=-1):
        """Iterates over deploy keys on this repository.

        :param int number: (optional), number of keys to return. Default: -1
            returns all available keys
        :returns: generator of :class:`Key <github3.users.Key>`\ s
        """
        url = self._build_url('keys', base_url=self._api)
        return self._iter(int(number), url, Key)

    def iter_labels(self, number=-1):
        """Iterates over labels on this repository.

        :param int number: (optional), number of labels to return. Default: -1
            returns all available labels
        :returns: generator of :class:`Label <github3.issues.Label>`\ s
        """
        url = self._build_url('labels', base_url=self._api)
        return self._iter(int(number), url, Label)

    def iter_languages(self, number=-1):
        """Iterate over the programming languages used in the repository.

        :param int number: (optional), number of languages to return. Default:
            -1 returns all used languages
        :returns: list of tuples
        """
        url = self._build_url('languages', base_url=self._api)
        return self._iter(int(number), url, tuple)

    def iter_milestones(self, state=None, sort=None, direction=None,
                        number=-1):
        """Iterates over the milestones on this repository.

        :param str state: (optional), state of the milestones, accepted
            values: ('open', 'closed')
        :param str sort: (optional), how to sort the milestones, accepted
            values: ('due_date', 'completeness')
        :param str direction: (optional), direction to sort the milestones,
            accepted values: ('asc', 'desc')
        :param int number: (optional), number of milestones to return.
            Default: -1 returns all milestones
        :returns: generator of
            :class:`Milestone <github3.issues.Milestone>`\ s
        """
        url = self._build_url('milestones', base_url=self._api)
        accepted = {'state': ('open', 'closed'),
                    'sort': ('due_date', 'completeness'),
                    'direction': ('asc', 'desc')}
        params = {'state': state, 'sort': sort, 'direction': direction}
        for (k, v) in list(params.items()):
            if not (v and (v in accepted[k])):  # e.g., '' or None
                del params[k]
        if not params:
            params = None
        return self._iter(int(number), url, Milestone, params)

    def iter_network_events(self, number=-1):
        """Iterates over events on a network of repositories.

        :param int number: (optional), number of events to return. Default: -1
            returns all available events
        :returns: generator of :class:`Event <github3.events.Event>`\ s
        """
        base = self._api.replace('repos', 'networks', 1)
        url = self._build_url('events', base_url=base)
        return self._iter(int(number), url, Event)

    def iter_notifications(self, all=False, participating=False, since='',
                           number=-1):
        """Iterates over the notifications for this repository.

        :param bool all: (optional), show all notifications, including ones
            marked as read
        :param bool participating: (optional), show only the notifications the
            user is participating in directly
        :param str since: (optional), filters out any notifications updated
            before the given time. The time should be passed in as UTC in the
            ISO 8601 format: ``YYYY-MM-DDTHH:MM:SSZ``. Example:
            "2012-10-09T23:39:01Z".
        :returns: generator of :class:`Thread <github3.notifications.Thread>`
        """
        url = self._build_url('notifications', base_url=self._api)
        params = {'all': all, 'participating': participating, 'since': since}
        for (k, v) in list(params.items()):
            if not v:
                del params[k]
        return self._iter(int(number), url, Thread, params=params)

    def iter_pulls(self, state=None, number=-1):
        """List pull requests on repository.

        :param str state: (optional), accepted values: ('open', 'closed')
        :param int number: (optional), number of pulls to return. Default: -1
            returns all available pull requests
        :returns: generator of
            :class:`PullRequest <github3.pulls.PullRequest>`\ s
        """
        url = self._build_url('pulls', base_url=self._api)
        params = {}
        if state in ('open', 'closed'):
            params['state'] = state
        return self._iter(int(number), url, PullRequest, params=params)

    def iter_refs(self, subspace='', number=-1):
        """Iterates over references for this repository.

        :param str subspace: (optional), e.g. 'tags', 'stashes', 'notes'
        :param int number: (optional), number of refs to return. Default: -1
            returns all available refs
        :returns: generator of :class:`Reference <github3.git.Reference>`\ s
        """
        if subspace:
            args = ('git', 'refs', subspace)
        else:
            args = ('git', 'refs')
        url = self._build_url(*args, base_url=self._api)
        return self._iter(int(number), url, Reference)

    def iter_stargazers(self, number=-1):
        """List users who have starred this repository.

        :returns: generator of :class:`User <github3.users.User>`\ s
        """
        url = self._build_url('stargazers', base_url=self._api)
        return self._iter(int(number), url, User)

    def iter_subscribers(self, number=-1):
        """Iterates over users subscribed to this repository.

        :param int number: (optional), number of subscribers to return.
            Default: -1 returns all subscribers available
        :returns: generator of :class:`User <github3.users.User>`
        """
        url = self._build_url('subscribers', base_url=self._api)
        return self._iter(int(number), url, User)

    def iter_statuses(self, sha, number=-1):
        """Iterates over the statuses for a specific SHA.

        :param str sha: SHA of the commit to list the statuses of
        :param int number: (optional), return up to number statuses. Default:
            -1 returns all available statuses.
        :returns: generator of :class:`Status <Status>`
        """
        url = ''
        if sha:
            url = self._build_url('statuses', sha, base_url=self._api)
        return self._iter(int(number), url, Status)

    def iter_tags(self, number=-1):
        """Iterates over tags on this repository.

        :param int number: (optional), return up to at most number tags.
            Default: -1 returns all available tags.
        :returns: generator of :class:`RepoTag <RepoTag>`\ s
        """
        url = self._build_url('tags', base_url=self._api)
        return self._iter(int(number), url, RepoTag)

    @requires_auth
    def iter_teams(self, number=-1):
        """Iterates over teams with access to this repository.

        :param int number: (optional), return up to number Teams. Default: -1
            returns all Teams.
        :returns: generator of :class:`Team <github3.orgs.Team>`\ s
        """
        from github3.orgs import Team
        url = self._build_url('teams', base_url=self._api)
        return self._iter(int(number), url, Team)

    def mark_notifications(self, last_read=''):
        """Mark all notifications in this repository as read.

        :param str last_read: (optional), Describes the last point that
            notifications were checked. Anything updated since this time will
            not be updated. Default: Now. Expected in ISO 8601 format:
            ``YYYY-MM-DDTHH:MM:SSZ``. Example: "2012-10-09T23:39:01Z".
        :returns: bool
        """
        url = self._build_url('notifications', base_url=self._api)
        mark = {'read': True}
        if last_read:
            mark['last_read_at'] = last_read
        return self._boolean(self._put(url, data=dumps(mark)),
                             205, 404)

    def merge(self, base, head, message=''):
        """Perform a merge from ``head`` into ``base``.

        :param str base: (required), where you're merging into
        :param str head: (required), where you're merging from
        :param str message: (optional), message to be used for the commit
        :returns: :class:`RepoCommit <RepoCommit>`
        """
        url = self._build_url('merges', base_url=self._api)
        data = {'base': base, 'head': head, 'commit_message': message}
        json = self._json(self._post(url, data=dumps(data)), 201)
        return RepoCommit(json, self) if json else None

    def milestone(self, number):
        """Get the milestone indicated by ``number``.

        :param int number: (required), unique id number of the milestone
        :returns: :class:`Milestone <github3.issues.Milestone>`
        """
        url = self._build_url('milestones', str(number), base_url=self._api)
        json = self._json(self._get(url), 200)
        return Milestone(json, self) if json else None

    @requires_auth
    def pubsubhubbub(self, mode, topic, callback, secret=''):
        """Create/update a pubsubhubbub hook.

        :param str mode: (required), accepted values: ('subscribe',
            'unsubscribe')
        :param str topic: (required), form:
            https://github.com/:user/:repo/events/:event
        :param str callback: (required), the URI that receives the updates
        :param str secret: (optional), shared secret key that generates a
            SHA1 HMAC of the payload content.
        :returns: bool
        """
        from re import match
        m = match('https://github\.com/\w+/[\w\._-]+/events/\w+', topic)
        status = False
        if mode and topic and callback and m:
            data = [('hub.mode', mode), ('hub.topic', topic),
                    ('hub.callback', callback)]
            if secret:
                data.append(('hub.secret', secret))
            url = self._build_url('hub')
            h = {'Content-Type': None}
            status = self._boolean(self._post(url, data=data, headers=h), 204,
                                   404)
        return status

    def pull_request(self, number):
        """Get the pull request indicated by ``number``.

        :param int number: (required), number of the pull request.
        :returns: :class:`PullRequest <github3.pulls.PullRequest>`
        """
        json = None
        if int(number) > 0:
            url = self._build_url('pulls', str(number), base_url=self._api)
            json = self._json(self._get(url), 200)
        return PullRequest(json, self) if json else None

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

        :param str ref: (required)
        :type ref: str
        :returns: :class:`Reference <github3.git.Reference>`
        """
        url = self._build_url('git', 'refs', ref, base_url=self._api)
        json = self._json(self._get(url), 200)
        return Reference(json, self) if json else None

    @requires_auth
    def remove_collaborator(self, login):
        """Remove collaborator ``login`` from the repository.

        :param str login: (required), login name of the collaborator
        :returns: bool
        """
        resp = False
        if login:
            url = self._build_url('collaborators', login, base_url=self._api)
            resp = self._boolean(self._delete(url), 204, 404)
        return resp

    @requires_auth
    def set_subscription(self, subscribed, ignored):
        """Set the user's subscription for this repository

        :param bool subscribed: (required), determines if notifications should
            be received from this repository.
        :param bool ignored: (required), determines if notifications should be
            ignored from this repository.
        :returns: :class;`Subscription <Subscription>`
        """
        sub = {'subscribed': subscribed, 'ignored': ignored}
        url = self._build_url('subscription', base_url=self._api)
        json = self._json(self._put(url, data=dumps(sub)), 200)
        return Subscription(json, self) if json else None

    @requires_auth
    def subscription(self):
        """Return subscription for this Repository.

        :returns: :class:`Subscription <github3.notifications.Subscription>`
        """
        url = self._build_url('subscription', base_url=self._api)
        json = self._json(self._get(url), 200)
        return Subscription(json, self) if json else None

    def tag(self, sha):
        """Get an annotated tag.

        http://learn.github.com/p/tagging.html

        :param str sha: (required), sha of the object for this tag
        :returns: :class:`Tag <github3.git.Tag>`
        """
        url = self._build_url('git', 'tags', sha, base_url=self._api)
        json = self._json(self._get(url), 200)
        return Tag(json) if json else None

    def tree(self, sha):
        """Get a tree.

        :param str sha: (required), sha of the object for this tree
        :returns: :class:`Tree <github3.git.Tree>`
        """
        url = self._build_url('git', 'trees', sha, base_url=self._api)
        json = self._json(self._get(url), 200)
        return Tree(json, self) if json else None

    def update_label(self, name, color, new_name=''):
        """Update the label ``name``.

        :param str name: (required), name of the label
        :param str color: (required), color code
        :param str new_name: (optional), new name of the label
        :returns: bool
        """
        label = self.label(name)
        resp = False
        if label:
            upd = label.update
            resp = upd(new_name, color) if new_name else upd(name, color)
        return resp


class Branch(GitHubCore):
    """The :class:`Branch <Branch>` object. It holds the information GitHub
    returns about a branch on a :class:`Repository <Repository>`.
    """
    def __init__(self, branch, session=None):
        super(Branch, self).__init__(branch, session)
        #: Name of the branch.
        self.name = branch.get('name')
        #: Returns the branch's :class:`RepoCommit <RepoCommit>` or
        #  ``None``.
        self.commit = branch.get('commit')
        if self.commit:
            self.commit = RepoCommit(self.commit, self._session)
        #: Returns '_links' attribute.
        self.links = branch.get('_links', {})

    def __repr__(self):
        return '<Repository Branch [{0}]>'.format(self.name)


class Contents(GitHubObject):
    """The :class:`Contents <Contents>` object. It holds the information
    concerning any content in a repository requested via the API.
    """

    def __init__(self, content):
        super(Contents, self).__init__(content)
        # links
        self._api = content['_links'].get('self', '')
        #: Dictionary of links
        self.links = content.get('_links')

        # should always be 'base64'
        #: Returns encoding used on the content.
        self.encoding = content.get('encoding', '')

        # content, base64 encoded and decoded
        #: Base64-encoded content of the file.
        self.content = content.get('content', '')

        #: Decoded content of the file.
        self.decoded = self.content
        if self.encoding == 'base64':
            self.decoded = b64decode(self.content.encode())

        # file name, path, and size
        #: Name of the content.
        self.name = content.get('name', '')
        #: Path to the content.
        self.path = content.get('path', '')
        #: Size of the content
        self.size = content.get('size', 0)
        #: SHA string.
        self.sha = content.get('sha', '')

        # should always be 'file'
        #: Type of content.
        self.type = content.get('type', '')

    def __repr__(self):
        return '<Content [{0}]>'.format(self.path)

    def __str__(self):
        return self.decoded

    @property
    def git_url(self):
        """API URL for this blob"""
        return self.links['git']

    @property
    def html_url(self):
        """URL pointing to the content on GitHub."""
        return self.links['html']


class Download(GitHubCore):
    """The :class:`Download <Download>` object. It represents how GitHub sends
    information about files uploaded to the downloads section of a repository.

    .. warning::

        On 2013-03-11, this API will be deprecated by GitHub. There will also
        be a new version of github3.py to accompany this at that date.
    """

    def __init__(self, download, session=None):
        super(Download, self).__init__(download, session)
        self._api = download.get('url', '')
        #: URL of the download at GitHub.
        self.html_url = download.get('html_url', '')
        #: Unique id of the download on GitHub.
        self.id = download.get('id', 0)
        #: Name of the download.
        self.name = download.get('name', '')
        #: Description of the download.
        self.description = download.get('description', '')
        #: Size of the download.
        self.size = download.get('size', 0)
        #: How many times this particular file has been downloaded.
        self.download_count = download.get('download_count', 0)
        #: Content type of the download.
        self.content_type = download.get('content_type', '')

    def __repr__(self):
        return '<Download [{0}]>'.format(self.name)

    @requires_auth
    def delete(self):
        """Delete this download if authenticated"""
        return self._boolean(self._delete(self._api), 204, 404)

    def saveas(self, path=''):
        """Save this download to the path specified.

        :param str path: (optional), if no path is specified, it will be
            saved in the current directory with the name specified by GitHub.
            it can take a file-like object as well
        :returns: bool
        """
        if not path:
            path = self.name

        resp = self._get(self.html_url, allow_redirects=True, stream=True)
        if self._boolean(resp, 200, 404):
            if isinstance(getattr(path, 'write', None), Callable):
                file_like = True
                fd = path
            else:
                file_like = False
                fd = open(path, 'wb')
            for chunk in resp.iter_content():
                fd.write(chunk)
            if not file_like:
                fd.close()
            return True
        return False  # (No coverage)


class Hook(GitHubCore):
    """The :class:`Hook <Hook>` object. This handles the information returned
    by GitHub about hooks set on a repository."""

    def __init__(self, hook, session=None):
        super(Hook, self).__init__(hook, session)
        self._api = hook.get('url', '')
        #: datetime object representing when this hook was last updated.
        self.updated_at = None
        if hook.get('updated_at'):
            self.updated_at = self._strptime(hook.get('updated_at'))
        #: datetime object representing the date the hook was created.
        self.created_at = self._strptime(hook.get('created_at'))
        #: The name of the hook.
        self.name = hook.get('name')
        #: Events which trigger the hook.
        self.events = hook.get('events')
        #: Whether or not this Hook is marked as active on GitHub
        self.active = hook.get('active')
        #: Dictionary containing the configuration for the Hook.
        self.config = hook.get('config')
        #: Unique id of the hook.
        self.id = hook.get('id')

    def __repr__(self):
        return '<Hook [{0}]>'.format(self.name)

    def _update_(self, hook):
        self.__init__(hook, self._session)

    @requires_auth
    def delete(self):
        """Delete this hook.

        :returns: bool
        """
        return self._boolean(self._delete(self._api), 204, 404)

    @requires_auth
    def delete_subscription(self):
        """Delete the user's subscription to this repository.

        :returns: bool
        """
        url = self._build_url('subscription', base_url=self._api)
        return self._boolean(self._delete(url), 204, 404)

    @requires_auth
    def edit(self, name, config, events=[], add_events=[], rm_events=[],
             active=True):
        """Edit this hook.

        :param str name: (required), name of the service being called
        :param dict config: (required), key-value pairs of settings for this
            hook
        :param list events: (optional), which events should this be triggered
            for
        :param list add_events: (optional), events to be added to the list of
           events that this hook triggers for
        :param list rm_events: (optional), events to be remvoed from the list
            of events that this hook triggers for
        :param bool active: (optional), should this event be active
        :returns: bool
        """
        json = None
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

    @requires_auth
    def test(self):
        """Test this hook

        :returns: bool
        """
        url = self._build_url('tests', base_url=self._api)
        return self._boolean(self._post(url), 204, 404)


class RepoTag(GitHubObject):
    """The :class:`RepoTag <RepoTag>` object. This stores the information
    representing a tag that was created on a repository.
    """

    def __init__(self, tag):
        super(RepoTag, self).__init__(tag)
        #: Name of the tag.
        self.name = tag.get('name')
        #: URL for the GitHub generated zipball associated with the tag.
        self.zipball_url = tag.get('zipball_url')
        #: URL for the GitHub generated tarball associated with the tag.
        self.tarball_url = tag.get('tarball_url')
        #: Dictionary containing the SHA and URL of the commit.
        self.commit = tag.get('commit', {})

    def __repr__(self):
        return '<Repository Tag [{0}]>'.format(self)

    def __str__(self):
        return self.name


class RepoComment(BaseComment):
    """The :class:`RepoComment <RepoComment>` object. This stores the
    information about a comment on a file in a repository.
    """
    def __init__(self, comment, session=None):
        super(RepoComment, self).__init__(comment, session)
        #: Commit id on which the comment was made.
        self.commit_id = comment.get('commit_id')
        #: URL of the comment on GitHub.
        self.html_url = comment.get('html_url')
        #: The line number where the comment is located.
        self.line = comment.get('line')
        #: The path to the file where the comment was made.
        self.path = comment.get('path')
        #: The position in the diff where the comment was made.
        self.position = comment.get('position')
        #: datetime object representing when the comment was updated.
        self.updated_at = comment.get('updated_at')
        if self.updated_at:
            self.updated_at = self._strptime(self.updated_at)
        #: Login of the user who left the comment.
        self.user = None
        if comment.get('user'):
            self.user = User(comment.get('user'), self)

    def __repr__(self):
        return '<Repository Comment [{0}/{1}]>'.format(self.commit_id[:7],
                self.user.login or '')  # nopep8

    def _update_(self, comment):
        super(RepoComment, self)._update_(comment)
        self.__init__(comment, self._session)

    @requires_auth
    def update(self, body, sha, line, path, position):
        """Update this comment.

        :param str body: (required)
        :param str sha: (required), sha id of the commit to comment on
        :param int line: (required), line number to comment on
        :param str path: (required), relative path of the file you're
            commenting on
        :param int position: (required), line index in the diff to comment on
        :returns: bool
        """
        json = None
        if body and sha and path and line > 0 and position > 0:
            data = {'body': body, 'commit_id': sha, 'line': line,
                    'path': path, 'position': position}
            json = self._json(self._post(self._api, data=dumps(data)), 200)

        if json:
            self._update_(json)
            return True
        return False


class RepoCommit(BaseCommit):
    """The :class:`RepoCommit <RepoCommit>` object. This represents a commit as
    viewed by a :class:`Repository`. This is different from a Commit object
    returned from the git data section.
    """

    def __init__(self, commit, session=None):
        super(RepoCommit, self).__init__(commit, session)
        #: :class:`User <github3.users.User>` who authored the commit.
        self.author = commit.get('author')
        if self.author:
            self.author = User(self.author, self._session)
        #: :class:`User <github3.users.User>` who committed the commit.
        self.committer = commit.get('committer')
        if self.committer:
            self.committer = User(self.committer, self._session)
        #: :class:`Commit <github3.git.Commit>`.
        self.commit = commit.get('commit')
        if self.commit:
            self.commit = Commit(self.commit, self._session)

        self.sha = commit.get('sha')
        #: The number of additions made in the commit.
        self.additions = 0
        #: The number of deletions made in the commit.
        self.deletions = 0
        #: Total number of changes in the files.
        self.total = 0
        if commit.get('stats'):
            self.additions = commit['stats'].get('additions')
            self.deletions = commit['stats'].get('deletions')
            self.total = commit['stats'].get('total')

        #: The files that were modified by this commit.
        self.files = commit.get('files', [])

    def __repr__(self):
        return '<Repository Commit [{0}]>'.format(self.sha[:7])

    def diff(self):
        """Return the diff"""
        resp = self._get(self._api,
                         headers={'Accept': 'application/vnd.github.diff'})
        return resp.content if self._boolean(resp, 200, 404) else None

    def patch(self):
        """Return the patch"""
        resp = self._get(self._api,
                         headers={'Accept': 'application/vnd.github.patch'})
        return resp.content if self._boolean(resp, 200, 404) else None


class Comparison(GitHubCore):
    """The :class:`Comparison <Comparison>` object. This encapsulates the
    information returned by GitHub comparing two commit objects in a
    repository."""

    def __init__(self, compare):
        super(Comparison, self).__init__(compare)
        self._api = compare.get('url', '')
        #: URL to view the comparison at GitHub
        self.html_url = compare.get('html_url')
        #: Permanent link to this comparison.
        self.permalink_url = compare.get('permalink_url')
        #: URL to see the diff between the two commits.
        self.diff_url = compare.get('diff_url')
        #: Patch URL at GitHub for the comparison.
        self.patch_url = compare.get('patch_url')
        #: :class:`RepoCommit <RepoCommit>` object representing the base of
        #  comparison.
        self.base_commit = RepoCommit(compare.get('base_commit'), None)
        #: Behind or ahead.
        self.status = compare.get('status')
        #: Number of commits ahead by.
        self.ahead_by = compare.get('ahead_by')
        #: Number of commits behind by.
        self.behind_by = compare.get('behind_by')
        #: Number of commits difference in the comparison.
        self.total_commits = compare.get('total_commits')
        #: List of :class:`RepoCommit <RepoCommit>` objects.
        self.commits = [RepoCommit(com) for com in compare.get('commits')]
        #: List of dicts describing the files modified.
        self.files = compare.get('files', [])

    def __repr__(self):
        return '<Comparison of {0} commits>'.format(self.total_commits)

    def diff(self):
        """Return the diff"""
        resp = self._get(self._api,
                         headers={'Accept': 'application/vnd.github.diff'})
        return resp.content if self._boolean(resp, 200, 404) else None

    def patch(self):
        """Return the patch"""
        resp = self._get(self._api,
                         headers={'Accept': 'application/vnd.github.patch'})
        return resp.content if self._boolean(resp, 200, 404) else None


class Status(GitHubObject):
    """The :class:`Status <Status>` object. This represents information from
    the Repo Status API."""
    def __init__(self, status):
        super(Status, self).__init__(status)
        #: datetime object representing the creation of the status object
        self.created_at = self._strptime(status.get('created_at'))
        #: :class:`User <github3.users.User>` who created the object
        self.creator = User(status.get('creator'))
        #: Short description of the Status
        self.description = status.get('description')
        #: GitHub ID for the status object
        self.id = status.get('id')
        #: State of the status, e.g., 'success', 'pending', 'failed', 'error'
        self.state = status.get('state')
        #: URL to view more information about the status
        self.target_url = status.get('target_url')
        #: datetime object representing the last time the status was updated
        self.updated_at = None
        if status.get('updated_at'):
            self.updated_at = self._strptime(status.get('updated_at'))

    def __repr__(self):
        return '<Status [{s.id}:{s.state}]>'.format(s=self)
