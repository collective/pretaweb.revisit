"""

    Helper functions.

"""

import datetime
from DateTime import DateTime

from Products.ATContentTypes.utils import DT2dt, dt2DT

def query_revisit_content(portal, future_delta=datetime.timedelta(days=0)):
    """ Get objects whose revisit date is expiring.
    
    @param portal: Plone portal object
    
    @param future_delta: datetime.timedelta object how much in the future 
        we get expiring items. By default this is 30 days to future.
    
    @return: LazyMap iterable of content whose revisit expires soon
    """
    
    past = DateTime (2001, 1, 1)

    now = datetime.datetime.now()
    future = now + future_delta    
    future_tuple = future.timetuple()[:3]
    future = DateTime(*future_tuple) 
                
    results = portal.portal_catalog(revisit_date={'query':(past, future),'range': 'min:max'},
        sort_on='revisit_date',
        sort_order='reverse',
        show_inactive=True)
    
    return results
    
    
