"""

    Index revisit dates to portal_catalog

"""

import Missing
from Products.ATContentTypes.interface import IATContentType

def _index_revisit(obj, portal=None, vars=vars, **kwargs):
    """ A silly method for indexing things in a meaningless way
    
    """
    if hasattr(obj, "getField"):
        reindexField = obj.getField("revisitDate")
        if reindexField is not None:
            date = reindexField.get(obj)
            return date
        
    return Missing.Value 

try:
    from plone.indexer.decorator import indexer
except:
    index_revisit = _index_revisit
else:
    index_revisit = indexer(IATContentType)(_index_revisit)
