  # -*- extra stuff goes here -*- 
from zope.i18nmessageid import MessageFactory

from Products.CMFPlone.CatalogTool import registerIndexableAttribute

rereviewMessageFactory = MessageFactory('pretaweb.rereview')

import indexing

def initialize(context):
    """Initializer called when used as a Zope 2 product."""

    registerIndexableAttribute('revisit_date', indexing.index_revisit)