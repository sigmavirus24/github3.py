from ..models import GitHubObject


class PagesInfo(GitHubObject):
    def __init__(self, info):
        super(PagesInfo, self).__init__(info)
        self._api = info.get('url')

        #: Status of the pages site, e.g., built
        self.status = info.get('status')

        #: CName used for the pages site
        self.cname = info.get('cname')

        #: Boolean indicating whether there is a custom 404 for the pages site
        self.custom_404 = info.get('custom_404')


class PagesBuild(GitHubObject):
    def __init__(self, build):
        super(PagesBuild, self).__init__(build)
        self._api = build.get('url')

        #: Status of the pages build, e.g., building
        self.status = build.get('status')

        #: Error dictionary containing the error message
        self.error = build.get('error')

        from ..users import User
        #: :class:`User <github3.users.User>` representing who pushed the
        #: commit
        self.pusher = User(build.get('pusher'))

        #: SHA of the commit that triggered the build
        self.commit = build.get('commit')

        #: Time the build took to finish
        self.duration = build.get('duration')

        #: Datetime the build was created
        self.created_at = self._strptime(build.get('created_at'))

        #: Datetime the build was updated
        self.updated_at = self._strptime(build.get('updated_at'))
