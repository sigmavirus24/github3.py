# -*- coding: utf-8 -*-
from datetime import datetime
from github3.models import GitHubCore
from github3.users import User


def alternate_week(week):
    return {
        'start of week': datetime.fromtimestamp(int(week['w'])),
        'additions': week['a'],
        'deletions': week['d'],
        'commits': week['c'],
    }


class ContributorStats(GitHubCore):

    """This object provides easy access to information returned by the
    statistics section of the API.

    See http://developer.github.com/v3/repos/statistics/ for specifics.

    """

    def __init__(self, stats_object, session=None):
        super(ContributorStats, self).__init__(stats_object, session)
        #: Contributor in particular that this relates to
        self.author = User(stats_object.get('author', {}), session)
        #: Total number of commits authored by ``author``.
        self.total = stats_object.get('total')
        #: List of weekly dictionaries.
        self.weeks = stats_object.get('weeks', [])
        #: Alternative collection of weekly dictionaries
        #: This provides a datetime object and easy to remember keys for each
        #: element in the list. 'w' -> 'start of week', 'a' -> 'Number of additions',
        #: 'd' -> 'Number of deletions', 'c' -> 'Number of commits'
        self.alt_weeks = [alternate_week(w) for w in self.weeks]

    def __repr__(self):
        return '<Contributor Statistics [{0}]>'.format(self.author)
