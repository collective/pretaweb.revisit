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
                label="Review Date",
                description="When this date is reached, the content will be visible in the review task list",            
                show_hm=False,
            ),
        )
    ]

    def __init__(self, context):
        self.context = context

    def getOrder(self, schematas):
        """ """
        # Let revisit date to be the last
        # import pdb ; pdb.set_trace()
        
        # dates = schematas["dates"]
        # ['effectiveDate', 'expirationDate', 'creation_date', 'modification_date', 'revisitDate']
        
        schematas["dates"] = ['effectiveDate', 'revisitDate', 'expirationDate', 'creation_date', 'modification_date']
        
        return schematas

    def getFields(self):
        return self.fields
    
