# -*- coding: utf-8 -*-
"""Implementation of a branch on a repository."""
from __future__ import unicode_literals

from json import dumps

from . import commit
from .. import decorators
from .. import models
from ..exceptions import NotFoundError




class _Branch(models.GitHubCore):
    """A representation of a branch on a repository.

    See also https://developer.github.com/v3/repos/branches/

    This object has the following attributes:
    """

    # The Accept header will likely be removable once the feature is out of
    # preview mode. See http://git.io/v4O1e
    PREVIEW_HEADERS = {'Accept': 'application/vnd.github.loki-preview+json'}

    class_name = 'Repository Branch'

    def _update_attributes(self, branch):
        self.commit = commit.MiniCommit(branch['commit'], self)
        self.name = branch['name']
        base = self.commit.url.split('/commit', 1)[0]
        self._api = self._build_url('branches', self.name, base_url=base)

    def _repr(self):
        return '<{0} [{1}]>'.format(self.class_name, self.name)

    def latest_sha(self, differs_from=''):
        """Check if SHA-1 is the same as the remote branch.

        See https://git.io/vaqIw

        :param str differs_from:
            (optional), sha to compare against
        :returns:
            string of the SHA or None
        """
        # If-None-Match returns 200 instead of 304 value does not have quotes
        headers = {
            'Accept': 'application/vnd.github.v3.sha',
            'If-None-Match': '"{0}"'.format(differs_from)
        }
        base = self._api.split('/branches', 1)[0]
        url = self._build_url('commits', self.name, base_url=base)
        resp = self._get(url, headers=headers)
        if self._boolean(resp, 200, 304):
            return resp.content
        return None

    @decorators.requires_auth
    def protection(self):
        """Retrieve the protections enabled for this branch.

        See
        https://developer.github.com/v3/repos/branches/#get-branch-protection

        :returns:
            The protections enabled for this branch.
        :rtype:
            :class:`~github3.repos.branch.BranchProtection`
        """
        url = self._build_url('protection', base_url=self._api)
        headers_map = BranchProtection.PREVIEW_HEADERS_MAP
        headers = headers_map['required_approving_review_count']
        resp = self._get(url, headers=headers)
        try:
            json = self._json(resp, 200)
        except NotFoundError:
            json = {'url': url}
        return BranchProtection(json, self)

    @decorators.requires_auth
    def protect(self, enforce_admins=None, required_status_checks=None,
                required_pull_request_reviews=None, restrictions=None):
        """Enable force push protection and configure status check enforcement.

        Note: this is a shorthand method for `branch.protection().update()`

        See
        https://developer.github.com/v3/repos/branches/#get-branch-protection

        :param str enforce_admins:
            (optional), Specifies the enforce_admins level of the status checks.
            Must be one of 'off', 'non_admins', or 'everyone'. Use `None` or
            omit to use the already associated value.
        :param list required_status_checks:
            (optional), A list of strings naming status checks that must pass
            before merging. Use `None` or omit to use the already associated
            value.
        :param obj required_pull_request_reviews:
            (optional), Object representing the configuration of Request Pull
            Request Reviews settings. Use `None` or omit to use the already
            associated value.
        :param obj restrictions:
            (optional), Object representing the configuration of Restrictions.
            Use `None` or omit to use the already associated value.
        :returns:
            Returns branch protection instance
        :rtype:
            :class:`~github3.repos.branch.BranchProtection`
        """
        p = self.protection()
        p.u = p.update
        v = p.u(enforce_admins=enforce_admins,
                required_status_checks=required_status_checks,
                required_pull_request_reviews=required_pull_request_reviews,
                restrictions=restrictions)
        return v


    @decorators.requires_auth
    def unprotect(self):
        """Disable protection on this branch.
        :returns:
            If branch protection has been removed
        :rtype:
            bool
        """
        return self.protection().delete()


class Branch(_Branch):
    """The representation of a branch returned in a collection.

    GitHub's API returns different amounts of information about repositories
    based upon how that information is retrieved. This object exists to
    represent the limited amount of information returned for a specific
    branch in a collection. For example, you would receive this class when
    calling :meth:`~github3.repos.repo.Repository.branches`. To provide a
    clear distinction between the types of branches, github3.py uses different
    classes with different sets of attributes.

    This object has the same attributes as a
    :class:`~github3.repos.branch.ShortBranch` as well as the following:

    .. attribute:: links

        The dictionary of URLs returned by the API as ``_links``.

    .. attribute:: protected

        A boolean attribute that describes whether this branch is protected or
        not.

    .. attribute:: original_protection

        .. versionchanged:: 1.1.0

            To support a richer branch protection API, this is the new name
            for the information formerly stored under the attribute
            ``protection``.

        A dictionary with details about the protection configuration of this
        branch.

    .. attribute:: protection_url

        The URL to access and manage details about this branch's protection.
    """

    class_name = 'Repository Branch'

    def _update_attributes(self, branch):
        super(Branch, self)._update_attributes(branch)
        self.commit = commit.ShortCommit(branch['commit'], self)
        #: Returns '_links' attribute.
        self.links = branch['_links']
        #: Provides the branch's protection status.
        self.protected = branch['protected']
        self.original_protection = branch['protection']
        self.protection_url = branch['protection_url']
        if self.links and 'self' in self.links:
            self._api = self.links['self']


class ShortBranch(_Branch):
    """The representation of a branch returned in a collection.

    GitHub's API returns different amounts of information about repositories
    based upon how that information is retrieved. This object exists to
    represent the limited amount of information returned for a specific
    branch in a collection. For example, you would receive this class when
    calling :meth:`~github3.repos.repo.Repository.branches`. To provide a
    clear distinction between the types of branches, github3.py uses different
    classes with different sets of attributes.

    This object has the following attributes:

    .. attribute:: commit

        A :class:`~github3.repos.commit.MiniCommit` representation of the
        newest commit on this branch with the associated repository metadata.

    .. attribute:: name

        The name of this branch.
    """

    class_name = 'Short Repository Branch'
    _refresh_to = Branch


class BranchProtection(models.GitHubCore):
    """The representation of a branch's protection.

    .. seealso::

        `Branch protection API documentation`_
            GitHub's documentation of branch protection

    This object has the following attributes:

    .. attribute:: enforce_admins

        A :class:`~github3.repos.branch.ProtectionEnforceAdmins` instance
        representing whether required status checks are required for admins.

    .. attribute:: restrictions

        A :class:`~github3.repos.branch.ProtectionRestrictions` representing
        who can push to this branch. Team and user restrictions are only
        available for organization-owned repositories.

    .. attribute:: required_pull_request_reviews

        A :class:`~github3.repos.branch.ProtectionRequiredPullRequestReviews`
        representing the protection provided by requiring pull request
        reviews.

    .. attribute:: required_status_checks

        A :class:`~github3.repos.branch.ProtectionRequiredStatusChecks`
        representing the protection provided by requiring status checks.

    .. links
    .. _Branch protection API documentation:
        https://developer.github.com/v3/repos/branches/#get-branch-protection
    """

    PREVIEW_HEADERS_MAP = {
        'required_approving_review_count': {
            'Accept': 'application/vnd.github.luke-cage-preview+json',
        },
        'requires_signed_commits': {
            'Accept': 'application/vnd.github.zzzax-preview+json',
        },
        'nested_teams': {
            'Accept': 'application/vnd.github.hellcat-preview+json',
        },
    }

    def _update_attributes(self, protection):
        self._api = protection['url']

        def _set_conditional_attr(name, cls):
            value = protection.get(name)
            setattr(self, name, value)
            if getattr(self, name):
                setattr(self, name, cls(value, self))

        _set_conditional_attr('enforce_admins', ProtectionEnforceAdmins)
        _set_conditional_attr('restrictions', ProtectionRestrictions)
        _set_conditional_attr('required_pull_request_reviews',
                              ProtectionRequiredPullRequestReviews)
        _set_conditional_attr('required_status_checks',
                              ProtectionRequiredStatusChecks)

    @decorators.requires_auth
    def update(self, enforce_admins=None, required_status_checks=None,
               required_pull_request_reviews=None, restrictions=None):
        """Enable force push protection and configure status check enforcement.

        See http://git.io/v4Gvu

        :param str enforce_admins:
            (optional), Specifies the enforcement level of the status checks.
            Must be one of 'off', 'non_admins', or 'everyone'. Use `None` or
            omit to use the already associated value.
        :param list required_status_checks:
            (optional), A list of strings naming status checks that must pass
            before merging. Use `None` or omit to use the already associated
            value.
        :param obj required_pull_request_reviews:
            (optional), Object representing the configuration of Request Pull
            Request Reviews settings. Use `None` or omit to use the already
            associated value.
        :param obj restrictions:
            (optional), Object representing the configuration of Restrictions.
            Use `None` or omit to use the already associated value.
        :returns:
            Updated branch protection
        :rtype:
            :class:`~github3.repos.branch.BranchProtection`
        """
        edit = {
            'enabled': True,
            'enforce_admins':
                self.enforce_admins.enabled
                if self.enforce_admins is not None else False,
            'required_status_checks':
                self.required_status_checks.as_dict()
                if self.required_status_checks is not None else None,
            'required_pull_request_reviews':
                self.required_pull_request_reviews.as_dict()
                if self.required_pull_request_reviews is not None else None,
            'restrictions':
                self.restrictions.as_dict()
                if self.restrictions is not None else None
        }

        preview_headers = \
            self.PREVIEW_HEADERS_MAP['required_approving_review_count']
        json = self._json(self._put(self._api, data=dumps(edit),
                                    headers=preview_headers), 200)
        self._update_attributes(json)
        return self

    @decorators.requires_auth
    def delete(self):
        """
        Removes branch protection
        :return bool:
        """
        resp = self._delete(self._api)
        return self._boolean(resp, 204, 404)


class ProtectionEnforceAdmins(models.GitHubCore):
    """The representation of a sub-portion of branch protection.

    .. seealso::

        `Branch protection API documentation`_
            GitHub's documentation of branch protection

    This object has the following attributes:

    .. attribute:: enabled

        A boolean attribute indicating whether the ``enforce_admins``
        protection is enabled or disabled.


    .. links
    .. _Branch protection API documentation:
        https://developer.github.com/v3/repos/branches/#get-branch-protection
    .. _Admin enforcement of protected branch
        https://developer.github.com/v3/repos/branches/#get-admin-enforcement-of-protected-branch
    """

    def _update_attributes(self, protection):
        self._api = protection['url']
        self.enabled = protection['enabled']

    @decorators.requires_auth
    def enable(self):
        """Enable Admin enforcement for protected branch."""
        resp = self._post(self._api,
                          headers=BranchProtection.PREVIEW_HEADERS_MAP)
        return self._boolean(resp, 200, 404)

    @decorators.requires_auth
    def disable(self):
        """Disable Admin enforcement for protected branch."""
        resp = self._delete(self._api,
                            headers=BranchProtection.PREVIEW_HEADERS_MAP)
        return self._boolean(resp, 204, 404)


class ProtectionRestrictions(models.GitHubCore):
    """The representation of a sub-portion of branch protection.

    .. seealso::

        `Branch protection API documentation`_
            GitHub's documentation of branch protection

        `Branch restriction documentation`_
            GitHub's description of branch restriction

    This object has the following attributes:

    .. attribute:: original_teams

        List of :class:`~github3.orgs.ShortTeam` objects representing
        the teams allowed to push to the protected branch.

    .. attribute:: original_users

        List of :class:`~github3.users.ShortUser` objects representing
        the users allowed to push to the protected branch.

    .. attribute:: teams_url

        The URL to retrieve the list of teams allowed to push to the
        protected branch.

    .. attribute:: users_url

        The URL to retrieve the list of users allowed to push to the
        protected branch.


    .. links
    .. _Branch protection API documentation:
        https://developer.github.com/v3/repos/branches/#get-branch-protection
    .. _Branch restriction documentation:
        https://help.github.com/articles/about-branch-restrictions
    """

    def _update_attributes(self, protection):
        from .. import orgs, users
        self._api = protection['url']
        self.users_url = protection['users_url']
        self.teams_url = protection['teams_url']
        self.original_users = protection['users']
        if self.original_users:
            self.original_users = [
                users.ShortUser(user, self)
                for user in self.original_users
            ]

        self.original_teams = protection['teams']
        if self.original_teams:
            self.original_teams = [
                orgs.ShortTeam(team, self)
                for team in self.original_teams
            ]

    def teams(self, number=-1):
        """Retrieve an up-to-date listing of teams.

        :returns:
            An iterator of teams
        :rtype:
            :class:`~github3.orgs.ShortTeam`
        """
        from .. import orgs
        return self._iter(int(number), self.teams_url, orgs.ShortTeam)

    def users(self, number=-1):
        """Retrieve an up-to-date listing of users.

        :returns:
            An iterator of users
        :rtype:
            :class:`~github3.users.ShortUser`
        """
        from .. import users
        return self._iter(int(number), self.users_url, users.ShortUser)

    @decorators.requires_auth
    def add_teams(self, teams):
        """Add teams to the protected branch.

        See
        https://developer.github.com/v3/repos/branches/#add-team-restrictions-of-protected-branch

        :param list teams:
            The list of the team names to have access to interact with
            protected branch.
        :returns:
            True if successful, False otherwise.
        :rtype:
            bool
        """
        resp = self._post(self.teams_url, data=teams,
                          headers=BranchProtection.PREVIEW_HEADERS_MAP)
        json = self._json(resp, 200)
        return json

    @decorators.requires_auth
    def remove_teams(self, teams):
        """Remove teams from protected branch.

        See
        https://developer.github.com/v3/repos/branches/#remove-team-restrictions-of-protected-branch

        :param list teams:
            The list of the team names to stop having access to interact with
            protected branch.
        :returns:
            True if successful, False otherwise.
        :rtype:
            bool
        """
        resp = self._delete(self.teams_url, json=dumps(teams),
                            headers=BranchProtection.PREVIEW_HEADERS_MAP)
        return self._boolean(resp, 204, 404)

    @decorators.requires_auth
    def add_users(self, users):
        """Add users to protected branch.

        See
        https://developer.github.com/v3/repos/branches/#add-user-restrictions-of-protected-branch

        :param list users:
            The list of the user logins to have access to interact with
            protected branch.
        :returns:
            True if successful, False otherwise.
        :rtype:
            bool
        """
        resp = self._post(self.users_url, data=users,
                          headers=BranchProtection.PREVIEW_HEADERS_MAP)
        return self._boolean(resp, 200, 404)

    @decorators.requires_auth
    def remove_users(self, users):
        """Remove users from protected branch.

        See
        https://developer.github.com/v3/repos/branches/#remove-user-restrictions-of-protected-branch

        :param list users:
            The list of the user logins to stop having access to interact with
            protected branch.
        :returns:
            True if successful, False otherwise.
        :rtype:
            bool
        """
        resp = self._delete(self.users_url, json=dumps(users),
                            headers=BranchProtection.PREVIEW_HEADERS_MAP)
        return self._boolean(resp, 204, 404)

    @decorators.requires_auth
    def set_teams(self, teams):
        """Set the teams that will have access to protected branch.

        See
        https://developer.github.com/v3/repos/branches/#replace-team-restrictions-of-protected-branch

        :param list teams:
            The list of the team names to have access to interact with
            protected branch.
        :returns:
            True if successful, False otherwise.
        :rtype:
            bool
        """
        teams_resp = self._put(self.teams_url, json=dumps(teams),
                               headers=BranchProtection.PREVIEW_HEADERS_MAP)
        return self._boolean(teams_resp, 200, 404)

    @decorators.requires_auth
    def set_users(self, users):
        """Set users that will have access to protected branch.

        See
        https://developer.github.com/v3/repos/branches/#replace-user-restrictions-of-protected-branch

        :param list users:
            The list of the user logins to have access to interact with
            protected branch.
        :returns:
            True if successful, False otherwise.
        :rtype:
            bool
        """
        users_resp = self._put(self.users_url, json=dumps(users),
                               headers=BranchProtection.PREVIEW_HEADERS_MAP)
        return self._boolean(users_resp, 200, 404)

    @decorators.requires_auth
    def delete(self):
        """Completely remove restrictions of the protected branch.

        See
        https://developer.github.com/v3/repos/branches/#remove-user-restrictions-of-protected-branch

        :returns:
            True if successful, False otherwise.
        :rtype:
            bool
        """
        resp = self._delete(self._api,
                            headers=BranchProtection.PREVIEW_HEADERS_MAP)
        return self._boolean(resp, 204, 404)


class ProtectionRequiredPullRequestReviews(models.GitHubCore):
    """The representation of a sub-portion of branch protection.

    .. seealso::

        `Branch protection API documentation`_
            GitHub's documentation of branch protection.


    .. links
    .. _Branch protection API documentation:
        https://developer.github.com/v3/repos/branches/#get-branch-protection
    .. _Branch Required Pull Request Reviews
        https://developer.github.com/v3/repos/branches/#get-pull-request-review-enforcement-of-protected-branch
    """

    def _update_attributes(self, protection):
        self._api = protection['url']
        self.dismiss_stale_reviews = protection['dismiss_stale_reviews']
        # Use a temporary value to stay under line-length restrictions
        value = protection['require_code_owner_reviews']
        self.require_code_owner_reviews = value
        # Use a temporary value to stay under line-length restrictions
        value = protection['required_approving_review_count']
        self.required_approving_review_count = value
        if 'dismissal_restrictions' in protection:
            self.dismissal_restrictions = ProtectionRestrictions(
                protection['dismissal_restrictions'],
                self,
            )

    def set_required_code_owner_reviews(self, value):
        """Sets the mandatory requirement for code owner reviews.

        :param bool value:
            Do we require the code owner reviews.
        """
        self.require_code_owner_reviews = value

    def set_dismiss_stale_reviews(self, value):
        """Do we dismiss the stale reviews once the code is updated?

        :param bool value:
            Should we dismiss the stale reviews once the code is updated?
        """
        self.dismiss_stale_reviews = value

    def set_required_approving_review_count(self, value):
        """Sets how many approving reviews of the pull request are required
        in order for the Pull Request to be able to get merged.

        :param int value:
            How many approving reviews are required.
        """
        self.required_approving_review_count = value

    @decorators.requires_auth
    def update(self):
        """Updates the configuration for the Required Pull Request Reviews.

        :returns:
            A updated instance of the required pull request reviews.
        :rtype:
            :class:`~github3.repos.branch.ProtectionRequiredPullRequestReviews`
        """
        teams = []
        for team in self.dismissal_restrictions.original_teams:
            teams.append(team.slug)

        users = []
        for user in self.dismissal_restrictions.original_users:
            users.append(user.login)

        update_json = {
            'dismiss_stale_reviews': self.dismiss_stale_reviews,
            'require_code_owner_reviews': self.require_code_owner_reviews,
            'required_approving_review_count':
                self.required_approving_review_count,
            'dismissal_restrictions': {
                'teams': teams,
                'users': users
            }
        }
        resp = self._patch(self._api, json=update_json)
        json = self._json(resp, 200)
        return self._instance_or_null(
            json=json,
            instance_class=ProtectionRequiredPullRequestReviews
        )

    @decorators.requires_auth
    def delete(self):
        """Removes the Required Pull Request Reviews
        :returns:
            Whether the operation finished successfully or not
        :rtype:
            bool
        """
        resp = self._delete(self._api)
        return self._boolean(resp, 204, 404)


class ProtectionRequiredStatusChecks(models.GitHubCore):
    """The representation of a sub-portion of branch protection.

    .. seealso::

        `Branch protection API documentation`_
            GitHub's documentation of branch protection
        `Required Status Checks documentation`_
            GitHub's description of required status checks


    .. links
    .. _Branch protection API documentation:
        https://developer.github.com/v3/repos/branches/#get-branch-protection
    .. _Required Status Checks documentation:
        https://help.github.com/articles/about-required-status-checks
    .. _Required Status Checks API documentation:
        https://developer.github.com/v3/repos/branches/#get-required-status-checks-of-protected-branch
    """

    def _update_attributes(self, protection):
        self._api = protection['url']
        self.strict = protection['strict']
        self.original_contexts = protection['contexts']
        self.contexts_url = protection['contexts_url']

    @decorators.requires_auth
    def add_contexts(self, contexts):
        """Add contexts to the existing list of required contexts.

        See
        https://developer.github.com/v3/repos/branches/#add-required-status-checks-contexts-of-protected-branch

        :param list contexts:
            The list of contexts to append to the existing list.
        :returns:
            The updated list of contexts.
        :rtype:
            list
        """
        resp = self._post(self.contexts_url, data=contexts)
        json = self._json(resp, 200)
        return json

    @decorators.requires_auth
    def contexts(self):
        """Retrieve the list of contexts required as status checks.

        See
        https://developer.github.com/v3/repos/branches/#list-required-status-checks-contexts-of-protected-branch

        :returns:
            A list of context names which are required status checks.
        :rtype:
            list
        """
        resp = self._get(self.contexts_url)
        json = self._json(resp, 200)
        return json

    @decorators.requires_auth
    def remove_contexts(self, contexts):
        """Remove the specified contexts from the list of required contexts.

        See
        https://developer.github.com/v3/repos/branches/#remove-required-status-checks-contexts-of-protected-branch

        :param list contexts:
            The context names to remove
        :returns:
            The updated list of contexts required as status checks.
        :rtype:
            list
        """
        resp = self._delete(self.contexts_url, json=contexts)
        json = self._json(resp, 200)
        return json

    @decorators.requires_auth
    def replace_contexts(self, contexts):
        """Replace the existing contexts required as status checks.

        See
        https://developer.github.com/v3/repos/branches/#replace-required-status-checks-contexts-of-protected-branch

        :param list contexts:
            The names of the contexts to be required as status checks
        :returns:
            True if successful, False otherwise
        :rtype:
            bool
        """
        resp = self._put(self.contexts_url, json=contexts)
        json = self._json(resp, 200)
        return json

    @decorators.requires_auth
    def delete_contexts(self, contexts):
        """Delete the contexts required as status checks.

        See
        https://developer.github.com/v3/repos/branches/#replace-required-status-checks-contexts-of-protected-branch

        :param list contexts:
            The names of the contexts to be required as status checks
        :returns:
            The updated list of contexts required as status checks.
        :rtype:
            list
        """
        resp = self._delete(self.contexts_url, json=contexts)
        return self._boolean(resp, 204, 404)

    @decorators.requires_auth
    def update(self, strict=None, contexts=None):
        """Update required status checks for the branch.

        This requires admin or owner permissions to the repository and
        branch protection to be enabled.

        .. seealso::

            `API docs`_
                Descrption of how to update the required status checks.

        :param bool strict:
            Whether this should be strict protection or not.
        :param list contexts:
            A list of context names that should be required.
        :returns:
            A new instance of this class with the updated information
        :rtype:
            :class:`~github3.repos.branch.ProtectionRequiredStatusChecks`


        .. links
        .. _API docs:
            https://developer.github.com/v3/repos/branches/#update-required-status-checks-of-protected-branch
        """
        update_data = {}
        if strict is not None:
            update_data['strict'] = strict
        if contexts is not None:
            update_data['contexts'] = contexts
        if update_data:
            resp = self._patch(self.url, json=update_data)
            json = self._json(resp, 200)
            return json

    @decorators.requires_auth
    def delete(self):
        """Remove required status checks from this branch.

        See
        https://developer.github.com/v3/repos/branches/#remove-required-status-checks-of-protected-branch

        :returns:
            True if successful, False otherwise
        :rtype:
            bool
        """
        resp = self._delete(self.url)
        return self._boolean(resp, 204, 404)
