"""

    Retrofit re-review dates to Archetypes schema.

"""


from zope.component import adapts
from zope.interface import implements

from Products.Archetypes.public import BooleanWidget
from Products.ATContentTypes.interface import IATDocument
from Products.Archetypes import public as atapi
from Products.Archetypes.interfaces import IBaseContent

from archetypes.schemaextender.field import ExtensionField
from archetypes.schemaextender.interfaces import ISchemaExtender, IOrderableSchemaExtender

class ExtensionDateField(ExtensionField, atapi.DateTimeField):
    """ Retrofitted date field """
    

class RevisitExtender(object):
    adapts(IBaseContent)
    implements(IOrderableSchemaExtender)


    fields = [
        ExtensionDateField("revisitDate",
            schemata="dates",
            widget = atapi.CalendarWidget(
                label="Revisit date",
                description="When you are alarmed this content should be revisited (one month beforehand this date)",            
                show_hm=False,
            ),
        )
    ]

    def __init__(self, context):
        self.context = context

    def getOrder(self, schematas):
        """ """
        # Let revisit date to be the last
        return schematas

    def getFields(self):
        return self.fields
    
