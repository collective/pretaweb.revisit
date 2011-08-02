"""

    Retrofit revisit dates to Archetypes schema.

"""


from archetypes.schemaextender.field import ExtensionField
from archetypes.schemaextender.interfaces import IOrderableSchemaExtender, IBrowserLayerAwareExtender

from DateTime import DateTime

from plone.registry.interfaces import IRegistry

from pretaweb.revisit import revisitMessageFactory as _
from pretaweb.revisit.interfaces import IAddOnInstalled, IRevisitSettings

from zope.component import adapts, getUtility
from zope.interface import implements

from Products.Archetypes import public as atapi
from Products.Archetypes.interfaces import IBaseContent



class ExtensionDateField(ExtensionField, atapi.DateTimeField):
    """ Retrofitted date field """


class RevisitDefault(object):

    def __init__ (self, context):
        self.context = context
        registry = getUtility(IRegistry)
        settings = registry.forInterface (IRevisitSettings)

        self.defaultRevisitDaysWait = settings.defaultRevisitDaysWait
        self.defaultApplyToContent = settings.defaultApplyToContent
        

    def __call__ (self):

        if self.defaultApplyToContent:
            tInfo = self.context.getTypeInfo()
            if tInfo.getId() in self.defaultApplyToContent:
                revisitDate = DateTime() + self.defaultRevisitDaysWait
                return revisitDate.Date()
        return None



class RevisitExtender(object):
    """ Include revisit date on all objects. 
    
    An example extended which will create a new field on Dates tab between effective date and expiration date.
    """
    
    # This extender will apply to all Archetypes based content 
    adapts(IBaseContent)
    
    # We use both orderable and browser layer aware sensitive properties
    implements(IOrderableSchemaExtender, IBrowserLayerAwareExtender)
    
    # Don't do schema extending unless our add-on product is installed on Plone site
    layer = IAddOnInstalled

    fields = [
        ExtensionDateField("revisitDate",
            schemata="dates",
            widget = atapi.CalendarWidget(
                label=_(u"Revisit Date"),
                description=_(u"When this date is reached, the content will be visible in the revisit task list"),            
                show_hm=False,
            ),
        )
    ]

    def __init__(self, context):
        self.context = context

    def getOrder(self, schematas):
        """ Manipulate the order in which fields appear.
        
        @param schematas: Dictonary of schemata name -> field lists
        
        @return: Dictionary of reordered field lists per schemata.
        """
        schematas["dates"] = ['effectiveDate', 'revisitDate', 'expirationDate', 'creation_date', 'modification_date']
        
        return schematas

    def getFields(self):
        """
        @return: List of new fields we contribute to content. 
        """
        return self.fields
    
