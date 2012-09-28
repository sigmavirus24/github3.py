TODO
====

High priority
-------------

(In order of priority)

unittests
~~~~~~~~~

- We're currently at ~92% coverage. I want to get each module close to if not 
  above 90% coverage before December. 100% by next year (at the latest).

  + The major hurtle now are github3.github and github3.repos. Both contain 
    functions/functionality that will be very difficult to design test cases 
    for, e.g., creating a pull request, creating a pull request from an 
    existing issue, creating a commit object, etc.

.. links

iterability
~~~~~~~~~~~

- Replace all of the ``list_(.*)`` methods with ``iter_\1`` functions.

github3.api
~~~~~~~~~~~

- Add anonymous functionality for more areas of the API

Low priority
------------

(In order of priority)

logging
~~~~~~~

I need to determine if there is a desire for logging and where it would be 
most useful. I would probably take a cue from urllib3 in this instance.

Plan
====

- Finish unittests
- Design basic generator functionality to replace the ``list_*`` functions.

    ::

      def iter_issues(self, milestone=None, state=None, assignee=None,
          mentioned=None, labels=None, sort=None, direction=None,
          since=None, count=-1):
          """Iterates over issues on this repo based upon parameters passed.

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
          :param int count: (optional), numer of issues to iterate over, -1
              iterates over all issues
          """
          def issues_left():
              return count == -1 or count > 0

          url = self._build_url('issues', base_url=self._api)

          params = {}
          if milestone in ('*', 'none') or isinstance(milestone, int):
              params['milestone'] = str(milestone).lower()

          if assignee:
              params['assignee'] = assignee

          if mentioned:
              params['mentioned'] = mentioned

          params.update(issue_params(None, state, labels, sort, direction,
              since))

          count = int(count)

          while issues_left() and url:
              response = self._get(url)
              json = self._json(response, 200)
              for i in json:
                  yield Issue(i, self)
                  count -= 1
                  if count == 0:
                      break

              rel_next = response.links.get('rel_next', {})
              url = rel_next.get('url', '')

  Naturally, ``issues_left()`` will not be nested into each iterator,  but for 
  the purposes of this example, it is easier to define it there.
