
from Acquisition import aq_inner

from plone.app.portlets.portlets import base
from plone.portlets.interfaces import IPortletDataProvider
from plone.memoize.instance import memoize

from pretaweb.revisit import revisitMessageFactory as _
from pretaweb.revisit.utils import expired_revisit_content_data

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from zope.interface import implements
from zope import schema
from zope.component import getMultiAdapter
from zope.formlib import form

class IRevisitPortlet(IPortletDataProvider):
    """A portlet


    """
    
    offset_days = schema.Int(title=_(u"Time period"),
                                  description=_(u"How many days to future query content needing revisit"),
                                  required=True,
                                  default=30
                                  )

    view_limit = schema.Int(title=_(u"Max Items"),
                                  description=_(u"Maximum number of items to display"),
                                  required=True,
                                  default=5
                                  )


class Assignment(base.Assignment):
    """Portlet assignment.

    This is what is actually managed through the portlets UI and associated
    with columns.
    """

    implements(IRevisitPortlet)

    # TODO: Set default values for the configurable parameters here

    # some_field = u""

    # TODO: Add keyword parameters for configurable parameters here
    # def __init__(self, some_field=u''):
    #    self.some_field = some_field

    def __init__(self, offset_days, view_limit):
        self.offset_days = offset_days
        self.view_limit = view_limit


    @property
    def title(self):
        return _(u"Revisit portlet")


class Renderer(base.Renderer):
    
    render = ViewPageTemplateFile('revisitportlet.pt')
    
    @property
    def anonymous(self):
        context = aq_inner(self.context)
        portal_state = getMultiAdapter((context, self.request),
                                       name=u'plone_portal_state')
        return portal_state.anonymous()

    @property
    def available(self):
        return not self.anonymous and len(self._data())

    def revisit_items(self):
        return self._data()

    def full_revisit_link (self):

        return self.context.portal_url() + "/full_revisit_list?offset_days=" + str(self.data.offset_days)

    @memoize
    def _data(self):
        """ List the content items needing revisit.
        
        @return: Iterable of dicts
        """
        if self.anonymous:
            return []

        try:
            data = expired_revisit_content_data (
                    self.context,
                    self.request, 
                    self.data.offset_days,
                    self.data.view_limit  )

        except Exception, e:
            # portlet manager swallos there
            import traceback
            traceback.print_exc()
            raise e

        return data


# NOTE: If this portlet does not have any configurable parameters, you can
# inherit from NullAddForm and remove the form_fields variable.

class AddForm(base.AddForm):
    """Portlet add form.

    This is registered in configure.zcml. The form_fields variable tells
    zope.formlib which fields to display. The create() method actually
    constructs the assignment that is being added.
    """
    form_fields = form.Fields(IRevisitPortlet)

    def create(self, data):
        return Assignment(**data)


# NOTE: IF this portlet does not have any configurable parameters, you can
# remove this class definition and delete the editview attribute from the
# <plone:portlet /> registration in configure.zcml

class EditForm(base.EditForm):
    """Portlet edit form.

    This is registered with configure.zcml. The form_fields variable tells
    zope.formlib which fields to display.
    """
    form_fields = form.Fields(IRevisitPortlet)



