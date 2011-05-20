  # -*- extra stuff goes here -*- 
from zope.i18nmessageid import MessageFactory

try:
    from Products.CMFPlone.CatalogTool import registerIndexableAttribute
except:
    registerIndexableAttribute = None

rereviewMessageFactory = MessageFactory('pretaweb.rereview')

import indexing

def initialize(context):
    """Initializer called when used as a Zope 2 product."""
    if registerIndexableAttribute is not None:
        registerIndexableAttribute('revisit_date', indexing.index_revisit)
