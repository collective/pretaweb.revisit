import datetime

from Acquisition import aq_inner
from zope.interface import Interface
from zope.interface import implements
from zope import schema
from zope.component import getMultiAdapter
from zope.component import queryUtility
from zope.formlib import form
from zope.interface import implements
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from plone.app.portlets.portlets import base
from plone.portlets.interfaces import IPortletDataProvider
from plone.memoize.instance import memoize

from pretaweb.rereview import rereviewMessageFactory as _
from pretaweb.rereview.utils import query_revisit_content

class IRereviewPortlet(IPortletDataProvider):
    """A portlet


    """
    
    time_period = schema.Int(title=_(u"Time period"),
                                  description=_(u"How many days to future query content needing rereview"),
                                  required=True,
                                  default=30
                                  )


class Assignment(base.Assignment):
    """Portlet assignment.

    This is what is actually managed through the portlets UI and associated
    with columns.
    """

    implements(IRereviewPortlet)

    # TODO: Set default values for the configurable parameters here

    # some_field = u""

    # TODO: Add keyword parameters for configurable parameters here
    # def __init__(self, some_field=u''):
    #    self.some_field = some_field

    def __init__(self, time_period):
        self.time_period = time_period

    @property
    def title(self):
        return _(u"Rereview portlet")


class Renderer(base.Renderer):
    
    render = ViewPageTemplateFile('rereviewportlet.pt')
    
    @property
    def anonymous(self):
        context = aq_inner(self.context)
        portal_state = getMultiAdapter((context, self.request),
                                       name=u'plone_portal_state')
        return portal_state.anonymous()

    @property
    def available(self):
        return not self.anonymous and len(self._data())

    def review_items(self):
        return self._data()

    @memoize
    def _data(self):
        """ List the content items needing rereview.
        
        @return: Iterable of dicts
        """
        try:
            if self.anonymous:
                return []
            
            context = aq_inner(self.context)
            
            portal = context.portal_url.getPortalObject()
    
            timedelta = datetime.timedelta(days=self.data.time_period) 
    
            # Get items needing revisit
            brains = query_revisit_content(portal, timedelta)
            
            plone_view = getMultiAdapter((context, self.request), name=u'plone')
            getIcon = plone_view.getIcon
            toLocalizedTime = plone_view.toLocalizedTime        
            
            # Resulting dict data
            items = []
            
            def format_contributors(contribs):
                """ 
                @return: String of comma separated list of all contributors
                """
                
                if len(contribs) == 0:
                    return None
                
                return ", ".join(contribs)
                
            
            for brain in brains:
                
                # Gather info
                entry = {}
                
                obj = brain.getObject()
                            
                entry = {            
                    "path" : obj.absolute_url(),
                    "title" : obj.pretty_title_or_id(),
                    "description" : obj.Description(),
                    "icon" : getIcon(obj).html_tag(),
                    "creator" : obj.Creator(),
                    "contributors" : format_contributors(obj.Contributors()),
                    "mod_date" : toLocalizedTime(obj.ModificationDate()),
                    "revisit_date" : toLocalizedTime(brain["revisit_date"]),
                }
                
                items.append(entry)
                
            return items
        except Exception, e:
            # portlet manager swallos there
            import traceback
            traceback.print_exc()
            raise e


# NOTE: If this portlet does not have any configurable parameters, you can
# inherit from NullAddForm and remove the form_fields variable.

class AddForm(base.AddForm):
    """Portlet add form.

    This is registered in configure.zcml. The form_fields variable tells
    zope.formlib which fields to display. The create() method actually
    constructs the assignment that is being added.
    """
    form_fields = form.Fields(IRereviewPortlet)

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
    form_fields = form.Fields(IRereviewPortlet)
