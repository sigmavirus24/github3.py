from json import dumps
from github3.decorators import requires_auth
from github3.issues.label import Label
from github3.models import GitHubCore
from github3.users import User


class Milestone(GitHubCore):
    """The :class:`Milestone <Milestone>` object. This is a small class to
    handle information about milestones on repositories and issues.

    See also: http://developer.github.com/v3/issues/milestones/
    """
    def __init__(self, mile, session=None):
        super(Milestone, self).__init__(mile, session)
        self._api = mile.get('url', '')
        #: Identifying number associated with milestone.
        self.number = mile.get('number')
        #: State of the milestone, e.g., open or closed.
        self.state = mile.get('state')
        #: Title of the milestone, e.g., 0.2.
        self.title = mile.get('title')
        #: Description of this milestone.
        self.description = mile.get('description')
        #: :class:`User <github3.users.User>` object representing the creator
        #  of the milestone.
        self.creator = User(mile.get('creator'), self._session)
        #: Number of issues associated with this milestone which are still
        #  open.
        self.open_issues = mile.get('open_issues')
        #: The number of closed issues associated with this milestone.
        self.closed_issues = mile.get('closed_issues')
        #: datetime object representing when the milestone was created.
        self.created_at = self._strptime(mile.get('created_at'))
        #: datetime representing when this milestone is due.
        self.due_on = None
        if mile.get('due_on'):
            self.due_on = self._strptime(mile.get('due_on'))

    def __repr__(self):
        return '<Milestone [{0}]>'.format(self)

    def __str__(self):
        return self.title

    def _update_(self, mile):
        self.__init__(mile, self._session)

    @requires_auth
    def delete(self):
        """Delete this milestone.

        :returns: bool
        """
        return self._boolean(self._delete(self._api), 204, 404)

    def iter_labels(self, number=-1):
        """Iterate over the labels for every issue associated with this
        milestone.

        :param int number: (optional), number of labels to return. Default: -1
            returns all available labels.
        :returns: generator of :class:`Label <Label>`\ s
        """
        url = self._build_url('labels', base_url=self._api)
        return self._iter(int(number), url, Label)

    @requires_auth
    def update(self, title, state='', description='', due_on=''):
        """Update this milestone.

        state, description, and due_on are optional

        :param str title: (required), new title of the milestone
        :param str state: (optional), ('open', 'closed')
        :param str description: (optional)
        :param str due_on: (optional), ISO 8601 time format:
            YYYY-MM-DDTHH:MM:SSZ
        :returns: bool
        """
        data = {'title': title, 'state': state,
                'description': description, 'due_on': due_on}
        json = None

        if title:
            json = self._json(self._patch(self._api, data=dumps(data)), 200)
        if json:
            self._update_(json)
            return True
        return False
