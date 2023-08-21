from wagtail import hooks
from wagtail.admin.userbar import BaseItem


class RefreshFromPlanningCenterLinkItem(BaseItem):
    template = "group/userbar_refresh_from_planningcenter.html"

    def __init__(self, page):
        self.page = page

    def attrs(self):
        return dir(self)


@hooks.register('construct_wagtail_userbar')
def add_refresh_from_planningcenter_link_item(request, items):
    return items.append(RefreshFromPlanningCenterLinkItem(page))
