"""

    Index revisit dates to portal_catalog

"""

import Missing
from plone.indexer.decorator import indexer
from Products.ATContentTypes.interface import IATContentType

@indexer(IATContentType)
def index_revisit(obj, portal=None, vars=vars, **kwargs):
    """ A silly method for indexing things in a meaningless way
    
    """
    if hasattr(obj, "getField"):
        reindexField = obj.getField("revisitDate")
        if reindexField is not None:
            date = reindexField.get(obj)
            return date
        
    return Missing.Value 


