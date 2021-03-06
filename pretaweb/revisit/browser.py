
from zope.publisher.browser import BrowserView

from utils import expired_revisit_content_data

class FullRevisitListView (BrowserView):

    def revisit_items (self):
        offset_days = int(self.request.get("offset_days", "7"))
        return expired_revisit_content_data (
                self.context,
                self.request,
                offset_days  )
                


