"""

    Index revisit dates to portal_catalog

"""

import Missing

def index_revisit(obj, portal, vars=vars, **kwargs):
    """ A silly method for indexing things in a meaningless way
    
    """
    if hasattr(obj, "getField"):
        reindexField = obj.getField("revisitDate")
        if reindexField is not None:
            date = reindexField.get(obj)
            return date
        
    return Missing.Value 

from Products.CMFPlone.CatalogTool import registerIndexableAttribute

