"""

    Helper functions.

"""

from DateTime import DateTime
from zope.component import getMultiAdapter

def query_expired_revisit_content(portal, offset_days=0):
    """ Get objects whose revisit date is expiring.
    
    @param portal: Plone portal object
    
    @param offset_days: int object how much in the future 
        we get expiring items. By default this is 0 days to future.
    
    @return: LazyMap iterable of content whose revisit expires soon
    """
    
    past = DateTime (2001, 1, 1)

    now = DateTime() 
    future = now + offset_days
                
    results = portal.portal_catalog(revisit_date={'query':(past, future),'range': 'min:max'},
        sort_on='revisit_date',
        sort_order='reverse',
        show_inactive=True)
    
    return results
    
    
def expired_revisit_content_data(context, request, offset_days=0, view_limit=None):
    """ List the content items needing revisiting.
    
    @return: Iterable of dicts
    """

    portal = context.portal_url.getPortalObject()
    plone_view = getMultiAdapter((context, request), name=u'plone')

    getIcon = plone_view.getIcon
    toLocalizedTime = plone_view.toLocalizedTime        
    def format_contributors(contribs):
        """ 
        @return: String of comma separated list of all contributors
        """
        
        if len(contribs) == 0:
            return None
        
        return ", ".join(contribs)


    # Get items needing revisit
    brains = query_expired_revisit_content(portal, offset_days)
    if view_limit:
        brains = brains[:view_limit]
    
    
    # Resulting dict data
    items = []
    
        
    for brain in brains:
        
        # Gather info
        entry = {}
        
        obj = brain.getObject()
                    
        entry = {            
            "path" :        obj.absolute_url(),
            "title" :       obj.pretty_title_or_id(),
            "description" : obj.Description(),
            "icon" :        getIcon(obj).html_tag(),
            "creator" :     obj.Creator(),
            "contributors" : format_contributors(obj.Contributors()),
            "mod_date" :     toLocalizedTime(obj.ModificationDate()),
            "revisit_date" : toLocalizedTime(brain["revisit_date"]),
        }
        
        items.append(entry)
        
    return items
