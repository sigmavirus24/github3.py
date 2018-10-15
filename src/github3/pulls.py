# -*- coding: utf-8 -*-
"""This module contains all the classes relating to pull requests."""
from __future__ import unicode_literals

from collections import OrderedDict
from json import dumps

from uritemplate import URITemplate

from . import models
from . import users
from .repos import commit as rcommit
from .repos import contents
from .repos import status
from .decorators import requires_auth
from .issues import Issue
from .issues.comment import IssueComment


class PullDestination(models.GitHubCore):
    """The object that represents a pull request destination.

    This is the base class for the :class:`~github3.pulls.Head` and
    :class:`~github3.pulls.Base` objects. Each has identical attributes to
    this object.

    Please see GitHub's `Pull Request Documentation`_ for more information.

    .. _Pull Request Documentation:
        http://developer.github.com/v3/pulls/#get-a-single-pull-request

    .. attribute:: ref

        The full reference string for the git object

    .. attribute:: label

        The label for the destination (e.g., 'master', 'mybranch')

    .. attribute:: user

        If provided, a :class:`~github3.users.ShortUser` instance representing
        the owner of the destination

    .. attribute:: sha

        The SHA of the commit at the head of the destination

    .. attribute:: repository

        A :class:`~github3.repos.repo.ShortRepository` representing the
        repository containing this destination

    .. attribute:: repo

        A tuple containing the login and repository name, e.g.,
        ('sigmavirus24', 'github3.py')

        This attribute is generated by github3.py and may be deprecated in the
        future.
    """

    direction = None

    def _update_attributes(self, dest):
        from .repos.repo import ShortRepository
        self.ref = dest['ref']
        self.label = dest['label']
        self.user = dest.get('user')
        if self.user:
            self.user = users.ShortUser(self.user, self)
        self.sha = dest['sha']
        self._repo_name = ''
        self._repo_owner = ''
        repo = dest.get('repo')
        if repo:
            self._repo_name = repo.get('name')
            self._repo_owner = repo['owner']['login']
            self.repository = ShortRepository(repo, self)
        self.repo = (self._repo_owner, self._repo_name)

    def _repr(self):
        return '<{0} [{1}]>'.format(self.direction, self.label)


class Head(PullDestination):
    """An object representing the Head destination of a pull request.

    See :class:`~github3.pulls.PullDestination` for more details.
    """

    destination = 'Head'


class Base(PullDestination):
    """An object representing the Base destination of a pull request.

    See :class:`~github3.pulls.PullDestination` for more details.
    """

    destination = 'Base'


class PullFile(models.GitHubCore):
    """The object that represents a file in a pull request.

    Please see GitHub's `Pull Request Files Documentation`_ for more
    information.

    .. _Pull Request Files Documentation:
        http://developer.github.com/v3/pulls/#list-pull-requests-files

    .. attribute:: additions_count

        The number of additions made to this file

    .. attribute:: blob_url

        The API resource used to retrieve the blob for this file

    .. attribute:: changes_count

        The number of changes made to this file

    .. attribute:: contents_url

        The API resource to view the raw contents of this file

    .. attribute:: deletions_count

        The number of deletions made to this file

    .. attribute:: filename

        The name of this file

    .. attribute:: patch

        The patch generated by this

        .. note::

            If the patch is larger than a specific size it may be missing
            from GitHub's response. The attribute will be set to ``None``
            in this case.

    .. attribute:: raw_url

        The API resource to view the raw diff of this file

    .. attribute:: sha

        The SHA of the commit that this file belongs to

    .. attribute:: status

        The string with the status of the file, e.g., 'added'
    """

    def _update_attributes(self, pfile):
        self.sha = pfile['sha']
        self.filename = pfile['filename']
        self.status = pfile['status']
        self.additions_count = pfile['additions']
        self.deletions_count = pfile['deletions']
        self.changes_count = pfile['changes']
        self.blob_url = pfile['blob_url']
        self.raw_url = pfile['raw_url']
        self.patch = pfile.get('patch')
        self.contents_url = pfile['contents_url']

    def _repr(self):
        return '<Pull Request File [{0}]>'.format(self.filename)

    def contents(self):
        """Return the contents of the file.

        :returns:
            An object representing the contents of this file
        :rtype:
            :class:`~github3.repos.contents.Contents`
        """
        json = self._json(self._get(self.contents_url), 200)
        return self._instance_or_null(contents.Contents, json)


class _PullRequest(models.GitHubCore):
    """The :class:`PullRequest <PullRequest>` object.

    Please see GitHub's `PullRequests Documentation`_ for more information.

    .. _PullRequests Documentation:
        http://developer.github.com/v3/pulls/
    """

    class_name = '_PullRequest'

    def _update_attributes(self, pull):
        from . import orgs
        self._api = pull['url']
        self.assignee = pull['assignee']
        if self.assignee is not None:
            self.assignee = users.ShortUser(self.assignee, self)
        self.assignees = [users.ShortUser(a, self) for a in pull['assignees']]
        self.base = Base(pull['base'], self)
        self.body = pull['body']
        self.body_html = pull['body_html']
        self.body_text = pull['body_text']
        self.closed_at = self._strptime(pull['closed_at'])
        self.comments_url = pull['comments_url']
        self.commits_url = pull['commits_url']
        self.created_at = self._strptime(pull['created_at'])
        self.diff_url = pull['diff_url']
        self.head = Head(pull['head'], self)
        self.html_url = pull['html_url']
        self.id = pull['id']
        self.issue_url = pull['issue_url']
        self.links = pull['_links']
        self.merge_commit_sha = pull['merge_commit_sha']
        self.merged_at = self._strptime(pull['merged_at'])
        self.number = pull['number']
        self.patch_url = pull['patch_url']
        requested_reviewers = pull.get('requested_reviewers', [])
        self.requested_reviewers = [
            users.ShortUser(r, self) for r in requested_reviewers]
        requested_teams = pull.get('requested_teams', [])
        self.requested_teams = [
            orgs.ShortTeam(t, self) for t in requested_teams]
        self.review_comment_urlt = URITemplate(pull['review_comment_url'])
        self.review_comments_url = pull['review_comments_url']
        self.repository = None
        if self.base:
            self.repository = self.base.repository
        self.state = pull['state']
        self.statuses_url = pull['statuses_url']
        self.title = pull['title']
        self.updated_at = self._strptime(pull['updated_at'])
        self.user = users.ShortUser(pull['user'], self)

    def _repr(self):
        return '<{0} [#{1}]>'.format(self.class_name, self.number)

    @requires_auth
    def close(self):
        """Close this Pull Request without merging.

        :returns:
            True if successful, False otherwise
        :rtype:
            bool
        """
        return self.update(self.title, self.body, 'closed')

    @requires_auth
    def create_comment(self, body):
        """Create a comment on this pull request's issue.

        :param str body:
            (required), comment body
        :returns:
            the comment that was created on the pull request
        :rtype:
            :class:`~github3.issues.comment.IssueComment`
        """
        url = self.comments_url
        json = None
        if body:
            json = self._json(self._post(url, data={'body': body}), 201)
        return self._instance_or_null(IssueComment, json)

    @requires_auth
    def create_review_comment(self, body, commit_id, path, position):
        """Create a review comment on this pull request.

        .. note::

            All parameters are required by the GitHub API.

        :param str body:
            The comment text itself
        :param str commit_id:
            The SHA of the commit to comment on
        :param str path:
            The relative path of the file to comment on
        :param int position:
            The line index in the diff to comment on.
        :returns:
            The created review comment.
        :rtype:
            :class:`~github3.pulls.ReviewComment`
        """
        url = self._build_url('comments', base_url=self._api)
        data = {'body': body, 'commit_id': commit_id, 'path': path,
                'position': int(position)}
        json = self._json(self._post(url, data=data), 201)
        return self._instance_or_null(ReviewComment, json)

    @requires_auth
    def create_review_requests(self, reviewers=None, team_reviewers=None):
        """Ask for reviews on this pull request.

        :param list reviewers:
            The users to which request a review
        :param list team_reviewers:
            The teams to which request a review
        :returns:
            The pull request on which the reviews were requested
        :rtype:
            :class:`~github3.pulls.ShortPullRequest`
        """
        url = self._build_url('requested_reviewers', base_url=self._api)
        data = {}
        if reviewers is not None:
            data['reviewers'] = [getattr(r, 'login', r) for r in reviewers]
        if team_reviewers is not None:
            data['team_reviewers'] = [
                getattr(t, 'slug', t) for t in team_reviewers]
        json = self._json(self._post(url, data=data), 201)
        return self._instance_or_null(ShortPullRequest, json)

    @requires_auth
    def create_review(self, body, commit_id=None, event=None, comments=None):
        """Create a review comment on this pull request.

        .. warning::

            If you do not specify ``event``, GitHub will default it
            to ``PENDING`` which means that your review will need to
            be submitted after creation. (See also
            :meth:`~github3.pulls.PullReview.submit`.)

        :param str body:
            The comment text itself, required when using COMMENT or
            REQUEST_CHANGES.
        :param str commit_id:
            The SHA of the commit to comment on
        :param str event:
            The review action you want to perform. Actions include
            APPROVE, REQUEST_CHANGES or COMMENT. By leaving this blank
            you set the action to PENDING and will need to submit the
            review. Leaving blank may result in a 422 error response
            which will need to be handled.
        :param list comments:
            Array of draft review comment objects. Please see Github's
            `Create a pull request review documentation`_ for details
            on review comment objects. At the time of writing these
            were a dictionary with 3 keys: `path`, `position` and
            `body`.

            .. _Create a pull request review documentation:
                https://developer.github.com/v3/pulls/reviews/#create-a-pull-request-review

        :returns:
            The created review.
        :rtype:
            :class:`~github3.pulls.PullReview`
        """
        if comments is None:
            comments = []
        url = self._build_url('reviews', base_url=self._api)
        data = {'body': body, 'comments': comments}
        if commit_id is not None:
            data['commit_id'] = commit_id
        if event is not None:
            data['event'] = event
        json = self._json(self._post(url, data=data), 200)
        return self._instance_or_null(PullReview, json)

    @requires_auth
    def delete_review_requests(self, reviewers=None, team_reviewers=None):
        """Cancel review requests on this pull request.

        :param list reviewers:
            The users whose review is no longer requested
        :param list team_reviewers:
            The teams whose review is no longer requested
        :returns:
            True if successful, False otherwise
        :rtype:
            bool
        """
        url = self._build_url('requested_reviewers', base_url=self._api)
        data = {}
        if reviewers is not None:
            data['reviewers'] = [getattr(r, 'login', r) for r in reviewers]
        if team_reviewers is not None:
            data['team_reviewers'] = [
                getattr(t, 'slug', t) for t in team_reviewers]
        return self._boolean(self._delete(url, data=dumps(data)), 200, 404)

    def diff(self):
        """Return the diff.

        :returns:
            representation of the diff
        :rtype:
            bytes
        """
        resp = self._get(self._api,
                         headers={'Accept': 'application/vnd.github.diff'})
        return resp.content if self._boolean(resp, 200, 404) else b''

    def is_merged(self):
        """Check to see if the pull request was merged.

        .. versionchanged:: 1.0.0

            This now always makes a call to the GitHub API. To avoid that,
            check :attr:`merged` before making this call.

        :returns:
            True if merged, False otherwise
        :rtype:
            bool
        """
        url = self._build_url('merge', base_url=self._api)
        return self._boolean(self._get(url), 204, 404)

    def issue(self):
        """Retrieve the issue associated with this pull request.

        :returns:
            the issue object that this pull request builds upon
        :rtype:
            :class:`~github3.issues.Issue`
        """
        json = self._json(self._get(self.issue_url), 200)
        return self._instance_or_null(Issue, json)

    def commits(self, number=-1, etag=None):
        """Iterate over the commits on this pull request.

        :param int number:
            (optional), number of commits to return. Default: -1 returns all
            available commits.
        :param str etag:
            (optional), ETag from a previous request to the same endpoint
        :returns:
            generator of repository commit objects
        :rtype:
            :class:`~github3.repos.commit.ShortCommit`
        """
        url = self._build_url('commits', base_url=self._api)
        return self._iter(int(number), url, rcommit.ShortCommit, etag=etag)

    def files(self, number=-1, etag=None):
        """Iterate over the files associated with this pull request.

        :param int number:
            (optional), number of files to return. Default: -1 returns all
            available files.
        :param str etag:
            (optional), ETag from a previous request to the same endpoint
        :returns: generator of pull request files
        :rtype: :class:`~PullFile`
        """
        url = self._build_url('files', base_url=self._api)
        return self._iter(int(number), url, PullFile, etag=etag)

    def issue_comments(self, number=-1, etag=None):
        """Iterate over the issue comments on this pull request.

        In this case, GitHub leaks implementation details. Pull Requests are
        really just Issues with a diff. As such, comments on a pull request
        that are not in-line with code, are technically issue comments.

        :param int number:
            (optional), number of comments to return. Default: -1 returns all
            available comments.
        :param str etag:
            (optional), ETag from a previous request to the same endpoint
        :returns:
            generator of non-review comments on this pull request
        :rtype:
            :class:`~github3.issues.comment.IssueComment`
        """
        comments = self.links.get('comments', {})
        url = comments.get('href')
        return self._iter(int(number), url, IssueComment, etag=etag)

    @requires_auth
    def merge(self, commit_message=None, sha=None, merge_method='merge'):
        """Merge this pull request.

        .. versionchanged:: 1.0.0

            The boolean ``squash`` parameter has been replaced with
            ``merge_method`` which requires a string.

        :param str commit_message:
            (optional), message to be used for the merge commit
        :param str sha:
            (optional), SHA that pull request head must match to merge.
        :param str merge_method: (optional), Change the merge method.
            Either 'merge', 'squash' or 'rebase'. Default is 'merge'.
        :returns:
            True if successful, False otherwise
        :rtype:
            bool
        :returns: bool
        """
        parameters = {'merge_method': merge_method}
        if sha:
            parameters['sha'] = sha
        if commit_message is not None:
            parameters['commit_message'] = commit_message
        url = self._build_url('merge', base_url=self._api)
        json = self._json(self._put(url, data=dumps(parameters)), 200)
        if not json:
            return False
        return json['merged']

    def patch(self):
        """Return the patch.

        :returns:
            bytestring representation of the patch
        :rtype:
            bytes
        """
        resp = self._get(self._api,
                         headers={'Accept': 'application/vnd.github.patch'})
        return resp.content if self._boolean(resp, 200, 404) else b''

    @requires_auth
    def reopen(self):
        """Re-open a closed Pull Request.

        :returns:
            True if successful, False otherwise
        :rtype:
            bool
        """
        return self.update(self.title, self.body, state='open')

    def review_comments(self, number=-1, etag=None):
        """Iterate over the review comments on this pull request.

        :param int number:
            (optional), number of comments to return. Default: -1 returns all
            available comments.
        :param str etag:
            (optional), ETag from a previous request to the same endpoint
        :returns:
            generator of review comments
        :rtype:
            :class:`~github3.pulls.ReviewComment`
        """
        url = self._build_url('comments', base_url=self._api)
        return self._iter(int(number), url, ReviewComment, etag=etag)

    def review_requests(self):
        """Retrieve the review requests associated with this pull request.

        :returns:
            review requests associated with this pull request
        :rtype:
            :class:`~github3.pulls.ReviewRequests`
        """
        url = self._build_url('requested_reviewers', base_url=self._api)
        json = self._json(self._get(url), 200)
        return self._instance_or_null(ReviewRequests, json)

    def reviews(self, number=-1, etag=None):
        """Iterate over the reviews associated with this pull request.

        :param int number:
            (optional), number of reviews to return. Default: -1 returns all
            available files.
        :param str etag:
            (optional), ETag from a previous request to the same endpoint
        :returns:
            generator of reviews for this pull request
        :rtype:
            :class:`~github3.pulls.PullReview`
        """
        url = self._build_url('reviews', base_url=self._api)
        return self._iter(int(number), url, PullReview, etag=etag)

    def statuses(self, number=-1, etag=None, most_recent=True):
        """Iterate over the statuses associated with this pull request.

        :param int number:
            (optional), number of statuses to return. Default: -1 returns all
            available statuses.
        :param str etag:
            (optional), ETag from a previous request to the same endpoint
        :param str etag:
            (optional), defaults to True, If true only returns the most recent
            status of each context type else returns all statuses
        :returns:
            generator of statuses for this pull request
        :rtype:
            :class:`~github3.repos.Status`
        """
        statuses = self._iter(number, self.statuses_url, status.Status,  etag=etag)
        if not most_recent:
            return statuses
        else:
            statuses_by_context = OrderedDict()
            for status in statuses:
                statuses_by_context[status.context] = status
        return statuses_by_context.values()

    @requires_auth
    def update(self, title=None, body=None, state=None, base=None,
               maintainer_can_modify=None):
        """Update this pull request.

        :param str title:
            (optional), title of the pull
        :param str body:
            (optional), body of the pull request
        :param str state:
            (optional), one of ('open', 'closed')
        :param str base:
            (optional), Name of the branch on the current repository that the
            changes should be pulled into.
        :param bool maintainer_can_modify:
            (optional), Indicates whether a maintainer is allowed to modify the
            pull request or not.
        :returns:
            True if successful, False otherwise
        :rtype:
            bool
        """
        data = {
            'title': title,
            'body': body,
            'state': state,
            'base': base,
            'maintainer_can_modify': maintainer_can_modify,
        }
        json = None
        self._remove_none(data)

        if data:
            json = self._json(self._patch(self._api, data=dumps(data)), 200)

        if json:
            self._update_attributes(json)
            return True
        return False


class PullRequest(_PullRequest):
    """Object for the full representation of a PullRequest.

    GitHub's API returns different amounts of information about prs based
    upon how that information is retrieved. This object exists to represent
    the full amount of information returned for a specific pr. For example,
    you would receive this class when calling
    :meth:`~github3.github.GitHub.pull_request`. To provide a clear
    distinction between the types of prs, github3.py uses different classes
    with different sets of attributes.

    .. versionchanged:: 1.0.0

    This object has all of the same attributes as
    :class:`~github3.pulls.ShortPullRequest` as well as the following:

    .. attribute:: additions_count

        The number of lines of code added in this pull request.

    .. attribute:: deletions_count

        The number of lines of code deleted in this pull request.

    .. attribute:: comments_count

        The number of comments left on this pull request.

    .. attribute:: commits_count

        The number of commits included in this pull request.

    .. attribute:: mergeable

        A boolean attribute indicating whether GitHub deems this pull request
        is mergeable.

    .. attribute:: mergeable_state

        A string indicating whether this would be a 'clean' or 'dirty' merge.

    .. attribute:: merged

        A boolean attribute indicating whether the pull request has been merged
        or not.

    .. attribute:: merged_by

        An instance of :class:`~github3.users.ShortUser` to indicate the user
        who merged this pull request. If this hasn't been merged or if
        :attr:`mergeable` is still being decided by GitHub this will be
        ``None``.

    .. attribute:: review_comments_count

        The number of review comments on this pull request.
    """

    class_name = 'Pull Request'

    def _update_attributes(self, pull):
        super(PullRequest, self)._update_attributes(pull)
        self.additions_count = pull['additions']
        self.deletions_count = pull['deletions']
        self.comments_count = pull['comments']
        self.commits_count = pull['commits']
        self.mergeable = pull['mergeable']
        self.mergeable_state = pull['mergeable_state']
        self.merged = pull['merged']
        self.merged_by = pull['merged_by']
        if self.merged_by is not None:
            self.merged_by = users.ShortUser(self.merged_by, self)
        self.review_comments_count = pull['review_comments']


class ShortPullRequest(_PullRequest):
    """Object for the shortened representation of a PullRequest.

    GitHub's API returns different amounts of information about prs based
    upon how that information is retrieved. Often times, when iterating over
    several prs, GitHub will return less information. To provide a clear
    distinction between the types of Pull Requests, github3.py uses different
    classes with different sets of attributes.

    .. versionadded:: 1.0.0

    The attributes available on this object are:

    .. attribute:: url

        The URL that describes this exact pull request.

    .. attribute:: assignee

        .. deprecated:: 1.0.0

            Use :attr:`assignees` instead.

        The assignee of the pull request, if present, represented as an
        instance of :class:`~github3.users.ShortUser`

    .. attribute:: assignees

        .. versionadded:: 1.0.0

        A list of the assignees of the pull request. If not empty, a list
        of instances of :class:`~github3.users.ShortUser`.

    .. attribute:: base

        A :class:`~github3.pulls.Base` object representing the base pull
        request destination.

    .. attribute:: body

        The Markdown formatted body of the pull request message.

    .. attribute:: body_html

        The HTML formatted body of the pull request mesage.

    .. attribute:: body_text

        The plain-text formatted body of the pull request message.

    .. attribute:: closed_at

        A :class:`~datetime.datetime` object representing the date and time
        when this pull request was closed.

    .. attribute:: comments_url

        The URL to retrieve the comments on this pull request from the API.

    .. attribute:: commits_url

        The URL to retrieve the commits in this pull request from the API.

    .. attribute:: created_at

        A :class:`~datetime.datetime` object representing the date and time
        when this pull request was created.

    .. attribute:: diff_url

        The URL to retrieve the diff for this pull request via the API.

    .. attribute:: head

        A :class:`~github3.pulls.Head` object representing the head pull
        request destination.

    .. attribute:: html_url

        The URL one would use to view this pull request in the browser.

    .. attribute:: id

        The unique ID of this pull request across all of GitHub.

    .. attribute:: issue_url

        The URL of the resource that represents this pull request as an issue.

    .. attribute:: links

        A dictionary provided by ``_links`` in the API response.

        .. versionadded:: 1.0.0

    .. attribute:: merge_commit_sha

        If unmerged, holds the sha of the commit to test mergability.
        If merged, holds commit sha of the merge commit, squashed commit on
        the base branch or the commit that the base branch was updated to
        after rebasing the PR.

    .. attribute:: merged_at

        A :class:`~datetime.datetime` object representing the date and time
        this pull request was merged. If this pull request has not been merged
        then this attribute will be ``None``.

    .. attribute:: number

        The number of the pull request on the repository.

    .. attribute:: patch_url

        The URL to retrieve the patch for this pull request via the API.

    .. attribute:: repository

        A :class:`~github3.repos.repo.ShortRepository` from the :attr:`base`
        instance.

    .. attribute:: requested_reviewers

        A list of :class:`~github3.users.ShortUser` from which a review was
        requested.

    .. attribute:: requested_teams

       A list of :class:`~github3.orgs.ShortTeam` from which a review was
       requested.

    .. attribute:: review_comment_urlt

        A URITemplate instance that expands to provide the review comment URL
        provided a number.

    .. attribute:: review_comments_url

        The URl to retrieve all review comments on this pull request from the
        API.

    .. attribute:: state

        The current state of this pull request.

    .. attribute:: title

        The title of this pull request.

    .. attribute:: updated_at

        A :class:`~datetime.datetime` instance representing the date and time
        when this pull request was last updated.

    .. attribute:: user

        A :class:`~github3.users.ShortUser` instance representing who opened
        this pull request.
    """

    class_name = 'Short Pull Request'
    _refresh_to = PullRequest


class PullReview(models.GitHubCore):
    """Object representing a Pull Request Review returned by the API.

    Please see GitHub's `Pull Review Documentation`_ for more information.

    .. _PullReview Documentation:
        https://developer.github.com/v3/pulls/reviews/

    .. attribute:: id

        The unique ID of this pull request review.

    .. attribute:: author_association

        .. versionadded:: 1.0.0

        The relationship of this review's author to the project.

    .. attribute:: body

        The Markdown formatted body of this review.

    .. attribute:: body_html

        .. versionadded:: 1.0.0

        The HTML formatted body of this review.

    .. attribute:: body_text

        .. versionadded:: 1.0.0

        The plain-text formatted body of this review.

    .. attribute:: commit_id

        The SHA of the commit that the review was left on.

    .. attribute:: html_url

        .. versionadded:: 1.0.0

        The URL to view this pull request in a browser.

    .. attribute:: pull_request_url

        The URL to retrieve the pull request via the API.

    .. attribute:: state

        The state of this review, e.g., the option specified in the review
        dialog by the author.

    .. attribute:: submitted_at

        A :class:`~datetime.datetime` object representing the date and time
        this review was submitted.

    .. attribute:: user

        A :class:`~github3.users.ShortUser` instance representing the author
        of this review.
    """

    def _update_attributes(self, review):
        self.id = review['id']
        self.author_association = review['author_association']
        self.body = review['body']
        self.body_html = review['body_html']
        self.body_text = review['body_text']
        self.commit_id = review['commit_id']
        self.html_url = review['html_url']
        self.user = users.ShortUser(review['user'], self)
        self.state = review['state']
        self.submitted_at = self._strptime(review.get('submitted_at'))
        self.pull_request_url = review['pull_request_url']

    def _repr(self):
        return '<Pull Request Review [{0}]>'.format(self.id)

    @requires_auth
    def submit(self, body, event=None):
        """Submit a pull request review.

        :param str body:
            The body text of the pull request review.
        :param str event:
            The review action you want to perform. Actions include
            APPROVE, REQUEST_CHANGES or COMMENT. By leaving this blank
            you set the action to PENDING and will need to submit the
            review. Leaving blank will result in a 422 error response
            which will need to be handled.
        :returns:
            True if successful, False otherwise
        :rtype:
            bool
        """
        url = self._build_url('reviews', self.id, 'events',
                              base_url=self.pull_request_url)
        data = {'body': body}
        if event is not None:
            data['event'] = event
        json = self._json(self._post(url, data=data), 200)
        if json:
            self._update_attributes(json)
            return True
        return False


class ReviewComment(models.GitHubCore):
    """Object representing review comments left on a pull request.

    Please see GitHub's `Pull Comments Documentation`_ for more information.

    .. _Pull Comments Documentation:
        http://developer.github.com/v3/pulls/comments/

    .. attribute:: id

        The unique identifier for this comment across all GitHub review
        comments.

    .. attribute:: author_association

        The role of the author of this comment on the repository.

    .. attribute:: body

        The Markdown formatted body of this comment.

    .. attribute:: body_html

        The HTML formatted body of this comment.

    .. attribute:: body_text

        The plain text formatted body of this comment.

    .. attribute:: commit_id

        The SHA of current commit this comment was left on.

    .. attribute:: created_at

        A :class:`~datetime.datetime` instance representing the date and time
        this comment was created.

    .. attribute:: diff_hunk

        A string representation of the hunk of the diff where the comment was
        left.

    .. attribute:: html_url

        The URL to view this comment in the webbrowser.

    .. attribute:: links

        A dictionary of relevant URLs usually returned in the ``_links``
        attribute.

    .. attribute:: original_commit_id

        The SHA of the original commit this comment was left on.

    .. attribute:: original_position

        The original position within the diff that this comment was left on.

    .. attribute:: pull_request_url

        The URL to retrieve the pull request via the API.

    .. attribute:: updated_at

        A :class:`~datetime.datetime` instance representing the date and time
        this comment was updated.

    .. attribute:: user

        A :class:`~github3.users.ShortUser` instance representing the author
        of this comment.

    """

    def _update_attributes(self, comment):
        self._api = comment['url']
        self.id = comment['id']
        self.author_association = comment['author_association']
        self.body = comment['body']
        self.body_html = comment['body_html']
        self.body_text = comment['body_text']
        self.commit_id = comment['commit_id']
        self.created_at = self._strptime(comment['created_at'])
        self.diff_hunk = comment['diff_hunk']
        self.html_url = comment['html_url']
        self.links = comment['_links']
        self.original_commit_id = comment['original_commit_id']
        self.original_position = comment['original_position']
        self.path = comment['path']
        self.position = comment['position']
        self.pull_request_url = comment['pull_request_url']
        self.updated_at = self._strptime(comment['updated_at'])
        self.user = users.ShortUser(comment['user'], self)

    def _repr(self):
        return '<Review Comment [{0}]>'.format(self.user.login)

    @requires_auth
    def delete(self):
        """Delete this comment.

        :returns:
            True if successful, False otherwise
        :rtype:
            bool
        """
        return self._boolean(self._delete(self._api), 204, 404)

    @requires_auth
    def edit(self, body):
        """Edit this comment.

        :param str body:
            (required), new body of the comment, Markdown formatted
        :returns:
            True if successful, False otherwise
        :rtype:
            bool
        """
        if body:
            json = self._json(self._patch(self._api,
                                          data=dumps({'body': body})), 200)
            if json:
                self._update_attributes(json)
                return True
        return False

    @requires_auth
    def reply(self, body):
        """Reply to this review comment with a new review comment.

        :param str body:
            The text of the comment.
        :returns:
            The created review comment.
        :rtype:
            :class:`~github3.pulls.ReviewComment`
        """
        url = self._build_url('comments', base_url=self.pull_request_url)
        index = self._api.rfind('/') + 1
        in_reply_to = int(self._api[index:])
        json = self._json(self._post(url, data={
            'body': body, 'in_reply_to': in_reply_to
        }), 201)
        return self._instance_or_null(ReviewComment, json)


class ReviewRequests(models.GitHubCore):
    """Object representing review requests in the GitHub API.

    .. attribute:: teams

        The list of teams that were requested a review

    .. attribute:: users

        The list of users that were requested a review

    Please see GitHub's `Review Request Documentation`_ for more information.

    .. _Review Request Documentation:
       https://developer.github.com/v3/pulls/review_requests/
    """
    def _update_attributes(self, requests):
        from . import orgs
        self.teams = [orgs.ShortTeam(t, self) for t in requests['teams']]
        self.users = [users.ShortUser(u, self) for u in requests['users']]

    def _repr(self):
        return '<Review Requests [users: {0}, teams: {1}]>'.format(
            len(self.users), len(self.teams))
