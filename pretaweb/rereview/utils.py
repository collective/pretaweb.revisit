"""

    Helper functions.

"""

import datetime

from Products.ATContentTypes.utils import DT2dt, dt2DT

def query_revisit_content(portal, future_delta=datetime.timedelta(days=30)):
    """ Get objects whose revisit date is expiring.
    
    @param portal: Plone portal object
    
    @param future_delta: datetime.timedelta object how much in the future 
        we get expiring items. By default this is 30 days to future.
    
    @return: LazyMap iterable of content whose revisit expires soon
    """
    
    now = datetime.datetime.now()
        
    past = datetime.datetime(2000, 1, 1)
    past = dt2DT(past)
    
    future = now + future_delta    
    future = dt2DT(future)
                
    results = portal.portal_catalog(revisit_date={'query':(past, future),'range': 'min:max'}, show_inactive=True)
    
    return results
    
    