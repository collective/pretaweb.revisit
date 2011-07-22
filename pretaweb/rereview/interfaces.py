"""
    
    Define interfaces for your add-on.

"""

import zope.interface
from zope import schema


class IAddOnInstalled(zope.interface.Interface):
    """A layer specific for this add-on product.

    This interface is referred in browserlayers.xml.

    All views and viewlets register against this layer will appear on your Plone site 
    only when the add-on installer has been run.
    """



def contentTypesVocabulary ():
    return schema.vocabulary.SimpleVocabulary.fromValues(["apples", "oranges", "pares"])


class IRereviewSettings (zope.interface.Interface):

    defaultRereviewDaysWait = schema.Int(
            title=(u"Default number of days until rereview"),
            description=(u"The default length of time from when content was created until it's rereview date"),
            required=True,
            default=90 )

    defaultApplyToContent = schema.Set(
            title=(u"Apply default rereview to content types"),
            description=(u"The content types for which a review date will autmaticly be set"),
            default=set([]),
            required=False,
            value_type=schema.TextLine(title=u"Content Types"))

    
