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
from archetypes.schemaextender.interfaces import ISchemaExtender

class ExtensionDateField(ExtensionField, atapi.DateTimeField):
    """ Retrofitted date field """
    

class RevisitExtender(object):
    adapts(IBaseContent)
    implements(ISchemaExtender)


    fields = [
        ExtensionDateField("revisitDate",
            schemata="revisit",
            widget = atapi.CalendarWidget(
                label="Revisit date",
                description="When you are alarmed this content should be revisited (one month beforehand this date)",            
                show_hm=False,
            ),
        )
    ]

    def __init__(self, context):
        self.context = context

    def getFields(self):
        return self.fields    
    
