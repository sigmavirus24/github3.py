"""
github3.github
==============

This module contains the main GitHub session object.

"""

from requests import session
from json import dumps
from .event import Event
from .gist import Gist
from .issue import Issue, issue_params
from .legacy import LegacyIssue, LegacyRepo, LegacyUser
from .models import GitHubCore
from .org import Organization
from .repo import Repository
from .user import User, Key


class GitHub(GitHubCore):
    """Stores all the session information."""
    def __init__(self):
        super(GitHub, self).__init__()
        self._session = session()
        # Only accept JSON responses
        self._session.headers.update(
                {'Accept': 'application/vnd.github.full+json'})
        # Only accept UTF-8 encoded data
        self._session.headers.update({'Accept-Charset': 'utf-8'})
        # Identify who we are
        self._session.config['base_headers'].update(
                {'User-Agent': 'github3.py/pre-alpha'})

    def __repr__(self):
        return '<GitHub at 0x%x>' % id(self)

    def _list_follow(self, which):
        url = self._github_url + '/user/' + which
        json = self._get(url)
        return [User(f, self._session) for f in json]

    def authorization(self, id_num):
        """Get information about authorization ``id``.

        :param id_num: (required), unique id of the authorization
        :type id_num: int
        :returns: :class:`Authorization <Authorization>`
        """
        json = None
        if int(id_num) > 0:
            url = self._github_url + '/authorizations/{0}'.format(id_num)
            json = self._get(url)
        return Authorization(json, self._session) if json else None

    def authorize(self, login, password, scopes, note='', note_url=''):
        """Obtain an authorization token from the GitHub API for the GitHub 
        API.
        
        :param login: (required)
        :type login: str
        :param password: (required)
        :type password: str
        :param scopes: (required), areas you want this token to apply to,
            i.e., 'gist', 'user'
        :type scopes: list of strings
        :param note: (optional), note about the authorization
        :type note: str
        :param note_url: (optional), URL pointing to a note
        :type note_url: str
        :returns: :class:`Authorization <Authorization>`
        """
        json = None
        auth = self._session.auth or (login and password)
        if isinstance(scopes, list) and scopes and auth:
            url = self._github_url + '/authorizations'
            data = dumps({'scopes': scopes, 'note': note,
                'note_url': note_url})
            if self._session.auth:
                json = self._post(url, data=data)
            else:
                ses = session()
                ses.auth = (login, password)
                req = ses.post(url, data=data)
                json = req.json if req.ok else {}
        return Authorization(json, self._session) if json else None

    def create_gist(self, description, files, public=True):
        """Create a new gist.

        If no login was provided, it will be anonymous.

        :param description: (required), description of gist
        :type description: str
        :param files: (required), file names with associated dictionaries for
            content, e.g. ``{'spam.txt': {'content': 'File contents ...'}}``
        :type files: dict
        :param public: (optional), make the gist public if True
        :type public: bool
        :returns: :class:`Gist <github3.gist.Gist>`
        """
        new_gist = {'description': description, 'public': public,
                'files': files}

        url = self._github_url + '/gists'
        json = self._post(url, dumps(new_gist))
        return Gist(json, self._session) if json else None

    def create_issue(self,
        owner,
        repository,
        title,
        body=None,
        assignee=None,
        milestone=None,
        labels=[]):
        """Create an issue on the project 'repository' owned by 'owner'
        with title 'title'.

        body, assignee, milestone, labels are all optional.

        :param owner: (required), login of the owner
        :type owner: str
        :param repository: (required), repository name
        :type repository: str
        :param title: (required), Title of issue to be created
        :type title: str
        :param body: (optional), The text of the issue, markdown
            formatted
        :type body: str
        :param assignee: (optional), Login of person to assign
            the issue to
        :type assignee: str
        :param milestone: (optional), Which milestone to assign
            the issue to
        :type milestone: str
        :param labels: (optional), List of label names.
        :type labels: list
        :returns: :class:`Issue <github3.issue.Issue>`
        """
        repo = None
        if owner and repository and title:
            repo = self.repository(owner, repository)

        if repo:
            return repo.create_issue(title, body, assignee, milestone,
                    labels)

        # Regardless, something went wrong. We were unable to create the
        # issue
        return None

    def create_key(self, title, key):
        """Create a new key for the authenticated user.
        
        :param title: (required), key title
        :type title: str
        :param key: (required), actual key contents
        :type key: str or file
        :returns: :class:`Key <github3.user.Key>`
        """
        created = None

        if title and key:
            url = self._github_url + '/user/keys'
            json = self._post(url, {'title': title, 'key': key})
            if json:
                created = Key(resp.json, self._session)
        return created

    def create_repo(self,
        name,
        description='',
        homepage='',
        private=False,
        has_issues=True,
        has_wiki=True,
        has_downloads=True):
        """Create a repository for the authenticated user.

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
        :returns: :class:`Repository <github3.repo.Repository>`
        """
        url = self._github_url + '/user/repos'
        data = dumps({'name': name, 'description': description,
            'homepage': homepage, 'private': private,
            'has_issues': has_issues, 'has_wiki': has_wiki,
            'has_downloads': has_downloads})
        json = self._post(url, data)
        return Repository(json, self._session) if json else None

    def delete_key(self, key_id):
        """Delete user key pointed to by ``key_id``.

        :param key_id: (required), unique id used by Github
        :type: int
        :returns: bool
        """
        key = self.get_key(key_id)
        if key:
            return key.delete()
        return False

    def follow(self, login):
        """Make the authenticated user follow login.
        
        :param login: (required), user to follow
        :type login: str
        :returns: bool
        """
        resp = False
        if login:
            url = '{0}/user/following/{1}'.format(self._github_url,
                    login)
            resp = self._put(url)
        return resp

    def get_key(self, id_num):
        """Gets the authenticated user's key specified by id_num.
        
        :param id_num: (required), unique id of the key
        :type id_num: int
        :returns: :class:`Key <github3.user.Key>`
        """
        json = None
        if int(id_num) > 0:
            url = '{0}/user/keys/{1}'.format(self._github_url,
                    str(id_num))
            json = self._get(url)
        return Key(json, self._session) if json else None

    def gist(self, id_num):
        """Gets the gist using the specified id number.
        
        :param id_num: (required), unique id of the gist
        :type id_num: int
        :returns: :class:`Gist <github3.gist.Gist>`
        """
        url = '{0}/gists/{1}'.format(self._github_url, str(id_num))
        json = self._get(url)
        return Gist(json, self._session) if json else None

    def is_following(self, login):
        """Check if the authenticated user is following login.
        
        :param login: (required), login of the user to check if the
            authenticated user is checking
        :type login: str
        :returns: bool
        """
        json = None
        if login:
            url = '{0}/user/following/{1}'.format(self._github_url, login)
            json = self._session.get(url).status_code == 204
        return True if json else False

    def is_watching(self, login, repo):
        """Check if the authenticated user is following login/repo.
        
        :param login: (required), owner of repository
        :type login: str
        :param repo: (required), name of repository
        :type repo: str
        :returns: bool
        """
        json = None
        if login and repo:
            url = '/'.join([self._github_url, 'user/watched', login, repo])
            json = self._session.get(url).status_code == 204
        return True if json else False

    def issue(self, owner, repository, number):
        """Fetch issue #:number: from https://github.com/:owner:/:repository:
            
        :param owner: (required), owner of the repository
        :type owner: str
        :param repository: (required), name of the repository
        :type repository: str
        :param number: (required), issue number
        :type number: int
        :return: :class:`Issue <github3.issue.Issue>`
        """
        repo = self.repository(owner, repository)
        if repo:
            return repo.issue(number)
        return None

    def list_authorizations(self):
        """List authorizations for the authenticated user.

        :returns: list of :class:`Authorization <Authorization>`\ s
        """
        url = self._github_url + '/authorizations'
        json = self._get(url)
        return [Authorization(a, self._session) for a in json]

    def list_emails(self):
        """List email addresses for the authenticated user.
        
        :returns: list of dicts
        """
        url = self._github_url + '/user/emails'
        return self._get(url) or []

    def list_events(self):
        """List public events.
        
        :returns: list of :class:`Event <github3.event.Event>`\ s
        """
        json = self._get(self._github_url + '/events')
        return [Event(ev, self._session) for ev in json]

    def list_followers(self, login=None):
        """If login is provided, return a list of followers of that
        login name; otherwise return a list of followers of the
        authenticated user.
        
        :param login: (optional), login of the user to check
        :type login: str
        :returns: list of :class:`User <github3.user.User>`\ s
        """
        if login:
            return self.user(login).list_followers()
        return self._list_follow('followers')

    def list_following(self, login=None):
        """If login is provided, return a list of users being followed
        by login; otherwise return a list of people followed by the
        authenticated user.
        
        :param login: (optional), login of the user to check
        :type login: str
        :returns: list of :class:`User <github3.user.User>`\ s
        """
        if login:
            return self.user(login).list_following()
        return self._list_follow('following')

    def list_gists(self, username=None):
        """If no username is specified, GET /gists, otherwise GET
        /users/:username/gists
        
        :param login: (optional), login of the user to check
        :type login: str
        :returns: list of :class:`Gist <github3.gist.Gist>`\ s
        """
        url = [self._github_url]
        if username:
            url.extend(['users', username, 'gists'])
        else:
            url.append('gists')
        url = '/'.join(url)

        json = self._get(url)
        ses = self._session
        return [Gist(gist, ses) for gist in json]

    def list_issues(self,
        owner=None,
        repository=None,
        filter=None,
        state=None,
        labels=None,
        sort=None,
        direction=None,
        since=None):
        """If no parameters are provided, this gets the issues for the
        authenticated user. All parameters are optional with the
        exception that owner and repository must be supplied together.

        :param filter: accepted values:
            ('assigned', 'created', 'mentioned', 'subscribed')
            api-default: 'assigned'
        :type filter: str
        :param state: accepted values: ('open', 'closed')
            api-default: 'open'
        :type state: str
        :param labels: comma-separated list of label names, e.g.,
            'bug,ui,@high'
        :type labels: str
        :param sort: accepted values: ('created', 'updated', 'comments')
            api-default: created
        :type sort: str
        :param direction: accepted values: ('asc', 'desc')
            api-default: desc
        :type direction: str
        :param since: ISO 8601 formatted timestamp, e.g.,
            2012-05-20T23:10:27Z
        :type since: str
        :returns: list of :class:`Issue <github3.issue.Issue>`\ s
        """
        url = [self._github_url]
        if owner and repository:
            repo = self.repository(owner, repository)
            issues = repo.list_issues()
        else:
            url.append('issues')
            url = '/'.join(url)
            params = issue_params(filter, state, labels, sort, direction,
                    since)
            if params:
                url = '{0}?{1}'.format(url, params)

            json = self._get(url)
            ses = self._session
            issues = [Issue(issue, ses) for issue in json]
        return issues

    def list_keys(self):
        """List public keys for the authenticated user.
        
        :returns: list of :class:`Key <github3.user.Key>`\ s
        """
        url = self._github_url + '/user/keys'
        json = self._get(url)
        ses = self._session
        return [Key(key, ses) for key in json]

    def list_orgs(self, login=None):
        """List public organizations for login if provided; otherwise
        list public and private organizations for the authenticated
        user.
        
        :param login: (optional), user whose orgs you wish to list
        :type login: str
        :returns: list of :class:`Organization <github3.org.Organization>`\ s
        """
        url = [self._github_url]
        if login:
            url.extend(['users', login, 'orgs'])
        else:
            url.extend(['user', 'orgs'])
        url = '/'.join(url)

        json = self._get(url)
        ses = self._session
        return [Organization(org, ses) for org in json]

    def list_repos(self, login=None, type='', sort='', direction=''):
        """List public repositories for the specified ``login`` or all 
        repositories for the authenticated user if ``login`` is not 
        provided.

        :param login: (optional)
        :type login: str
        :param type: (optional), accepted values:
            ('all', 'owner', 'public', 'private', 'member')
            API default: 'all'
        :type type: str
        :param sort: (optional), accepted values:
            ('created', 'updated', 'pushed', 'full_name')
            API default: 'created'
        :type sort: str
        :param direction: (optional), accepted values:
            ('asc', 'desc'), API default: 'asc' when using 'full_name',
            'desc' otherwise
        :type direction: str
        :returns: list of :class:`Repository <github3.repo.Repository>`
            objects
        """
        url = [self._github_url]
        if login:
            url.extend(['users', login, 'repos'])
        else:
            url.extend(['user', 'repos'])
        url = '/'.join(url)
        
        params = {}
        if type in ('all', 'owner', 'public', 'private', 'member'):
            params.update(type=type)
        if not login:
            if sort in ('created', 'updated', 'pushed', 'full_name'):
                params.update(sort=sort)
            if direction in ('asc', 'desc'):
                params.update(direction=direction)

        json = self._get(url, params=params)
        ses = self._session
        return [Repository(repo, ses) for repo in json]

    def list_watching(self, login=None):
        """List the repositories being watched by ``login`` if provided or the
        repositories being watched by the authenticated user.

        :param login: (optional)
        :type login: str
        :returns: list of :class:`Repository <github3.repo.Repository>`
            objects
        """
        if login:
            url = self._github_url + '/users/' + login + '/watched'
        else:
            url = self._github_url + '/user/watched'
        json = self._get(url)
        return [Repository(repo, self._session) for repo in json]

    def login(self, username=None, password=None, token=None):
        """Logs the user into GitHub for protected API calls.
        
        :param username: (optional)
        :type username: str
        :param password: (optional)
        :type password: str
        :param token: (optional)
        :type token: str
        """
        if username and password:
            self._session.auth = (username, password)
        elif token:
            self._session.headers.update({
                'Authorization': 'token ' + token
                })

    def markdown(self, text, mode='', context='', raw=False):
        """Render an arbitrary markdown document.

        :param text: (required), the text of the document to render
        :type text: str
        :param mode: (optional), 'markdown' or 'gfm'. 
        :type mode: str
        :param context: (optional), only important when using mode 'gfm',
            this is the repository to use as the context for the rendering
        :type context: str
        :param raw: (optional), renders a document like a README.md, no gfm, no
            context
        :type raw: bool
        :returns: str -- HTML formatted text
        """
        url = self._github_url + '/markdown'
        if raw:
            url = '/'.join([url, '/raw'])

        data = {}
        if text:
            data['text'] = text

        if mode in ('markdown', 'gfm'):
            data['mode'] = mode

        if context:
            data['context'] = context

        if data:
            data = dumps(data)
            req = self._session.post(url, data=data)
            if req.ok:
                return req.content
        return ''

    def organization(self, login):
        """Returns a Organization object for the login name
        
        :param login: (required), login name of the org
        :type login: str
        :returns: :class:`Organization <org.Organization>`
        """
        url = '{0}/orgs/{1}'.format(self._github_url, login)
        json = self._get(url)
        return Organization(json, self._session) if json else None

    def repository(self, owner, repository):
        """Returns a Repository object for the specified combination of
        owner and repository
        
        :param owner: (required)
        :type owner: str
        :param repository: (required)
        :type repository: str
        :returns: :class:`Repository <github3.repo.Repository>`
        """
        url = '/'.join([self._github_url, 'repos', owner, repository])
        json = self._get(url)
        return Repository(json, self._session) if json else None

    def search_issues(self, owner, repo, state, keyword):
        """Find issues by state and keyword.

        :param owner: (required)
        :type owner: str
        :param repo: (required)
        :type repo: str
        :param state: (required), accepted values: ('open', 'closed')
        :type state: str
        :param keyword: (required), what to search for
        :type keyword: str
        :returns: list of :class:`LegacyIssue <github3.legacy.LegacyIssue>`\ s
        """
        url = self._github_url + '/legacy/issues/search/{0}/{1}/{2}/{3}'.format(
                owner, repo, state, keyword)
        json = self._get(url)
        issues = json.get('issues', [])
        return [LegacyIssue(l, self._session) for l in issues]

    def search_repos(self, keyword, **params):
        """Search all repositories by keyword.

        :param keyword: (required)
        :type keyword: str
        :param params: (optional), filter by language and/or start_page
        :type params: dict
        :returns: list of :class:`LegacyRepo <github3.legacy.LegacyRepo>`\ s
        """
        url = self._github_url + '/legacy/repos/search/{0}'.format(keyword)
        json = self._get(url, params=params)
        repos = json.get('repositories', [])
        return [LegacyRepo(r, self._session) for r in repos]

    def search_users(self, keyword):
        """Search all users by keyword.

        :param keyword: (required)
        :type keyword: str
        :returns: list of :class:`LegacyUser <github3.legacy.LegacyUser>`\ s
        """
        url = self._github_url + '/legacy/user/search/{0}'.format(keyword)
        json = self._get(url)
        users = json.get('users', [])
        return [LegacyUser(u, self._session) for u in users]

    def search_email(self, email):
        """Search users by email.

        :param email: (required)
        :type keyword: str
        :returns: :class:`LegacyUser <github3.legacy.LegacyUser>`
        """
        url = self._github_url + '/legacy/user/email/{0}'.format(email)
        json = self._get(url)
        u = json.get('user', {})
        return LegacyUser(u, self._session) if u else None

    def unfollow(self, login):
        """Make the authenticated user stop following login
        
        :param login: (required)
        :type login: str
        :returns: bool
        """
        resp = False
        if login:
            url = '{0}/user/following/{1}'.format(self._github_url,
                    login)
            resp = self._delete(url)
        return resp

    def update_user(self, name=None, email=None, blog=None,
            company=None, location=None, hireable=False, bio=None):
        """If authenticated as this user, update the information with
        the information provided in the parameters. All parameters are
        optional.

        :param name: e.g., 'John Smith', not login name
        :type name: str
        :param email: e.g., 'john.smith@example.com'
        :type email: str
        :param blog: e.g., 'http://www.example.com/jsmith/blog'
        :type blog: str
        :param company: company name
        :type company: str
        :param location: where you are located
        :type location: str
        :param hireable: defaults to False
        :type hireable: bool
        :param bio: GitHub flavored markdown
        :type bio: str
        :returns: bool
        """
        user = self.user()
        if user:
            return user.update(name, email, blog, company, location,
                    hireable, bio)
        return False

    def user(self, login=None):
        """Returns a User object for the specified login name if
        provided. If no login name is provided, this will return a User
        object for the authenticated user.
        
        :param login: (optional)
        :type login: str
        :returns: :class:`User <github3.user.User>`
        """
        url = [self._github_url]
        if login:
            url.extend(['users', login])
        else:
            url.append('user')
        url = '/'.join(url)

        json = self._get(url)
        return User(json, self._session) if json else None

    def watch(self, login, repo):
        """Make user start watching login/repo.
        
        :param login: (required), owner of repository
        :type login: str
        :param repo: (required), name of repository
        :type repo: str
        :returns: bool
        """
        resp = False
        if login and repo:
            url = self._github_url + '/user/watched/' + login + '/' + repo
            resp = self._put(url)
        return resp

    def unwatch(self, login, repo):
        """Make user stop watching login/repo.

        :param login: (required), owner of repository
        :type login: str
        :param repo: (required), name of repository
        :type repo: str
        :returns: bool
        """
        resp = False
        if login and repo:
            url = self._github_url + '/user/watched/' + login + '/' + repo
            resp = self._delete(url)
        return resp


class Authorization(GitHubCore):
    """The :class:`Authorization <Authorization>` object."""
    def __init__(self, auth, session):
        super(Authorization, self).__init__(session)
        self._update_(auth)

    def __repr__(self):
        return '<Authorization [%s]>' % self._app.get('name', '')

    def _update_(self, auth):
        self._app = auth.get('app', {})
        self._token = auth.get('token', '')
        self._note_url = auth.get('note_url', '')
        self._note = auth.get('note', '')
        self._scopes = auth.get('scopes', [])
        self._api = auth.get('url', '')
        self._id = auth.get('id', 0)
        self._created = None
        if auth.get('created_at'):
            self._created = self._strptime(auth.get('created_at'))
        self._updated = None
        if auth.get('updated_at'):
            self._updated = self._strptime(auth.get('updated_at'))

    @property
    def app(self):
        """Details about the application"""
        return self._app

    @property
    def created_at(self):
        """datetime object representing when the authorization was created."""
        return self._created

    def delete(self):
        """delete this authorization"""
        return self._delete(self._api)

    @property
    def id(self):
        """Unique id of the authorization"""
        return self._id

    @property
    def note(self):
        """Note about the authorization"""
        return self._note

    @property
    def note_url(self):
        """URL about the note"""
        return self._note_url

    @property
    def scopes(self):
        """List of scopes this applies to"""
        return self._scopes

    @property
    def token(self):
        """Returns the Authorization token"""
        return self._token

    def update(self, scopes=[], add_scopes=[], rm_scopes=[], note='',
            note_url=''):
        """Update this authorization.

        :param scopes: (optional), replaces the authorization scopes with these
        :type scopes: list
        :param add_scopes: (optional), scopes to be added
        :type add_scopes: list
        :param rm_scopes: (optional), scopes to be removed
        :type rm_scopes: list
        :param note: (optional), new note about authorization
        :type note: str
        :param note_url: (optional), new note URL about this authorization
        :type note_url: str
        :returns: bool
        """
        success = False
        if scopes:
            json = self._get(self._api, data={'scopes': scopes})
            self._update_(json)
            success = True
        if new_scopes:
            json = self._get(self._api, data={'add_scopes': add_scopes})
            self._update_(json)
            success = True
        if rm_scopes:
            json = self._get(self._api, data={'remove_scopes': rm_scopes})
            self._update_(json)
            success = True
        if note or note_url:
            json = self._get(self._api, data={'note': note,
                'note_url': note_url})
            self._update_(json)
            success = True
        return success

    @property
    def updated_at(self):
        """datetime object representing when the authorization was created."""
        return self._updated
