
from plone.app.registry.browser.controlpanel import RegistryEditForm, ControlPanelFormWrapper

from pretaweb.revisit import revisitMessageFactory as _
from pretaweb.revisit.interfaces import IRevisitSettings

from zope.publisher.browser import BrowserView

try:
    # only in z3c.form 2.0
    from z3c.form.browser.textlines import TextLinesFieldWidget
    from z3c.form.browser.text import TextFieldWidget
except ImportError:
    from plone.z3cform.textlines import TextLinesFieldWidget
    from plone.z3cform.text import TextFieldWidget


from utils import expired_revisit_content_data

class RevisitSettingsEditForm (RegistryEditForm):
    schema = IRevisitSettings
    label = _(u"Revisit Settings")
    description = _(u"Settings for revisit default date settings")

 
    def updateFields(self):
        super(RevisitSettingsEditForm, self).updateFields()
        self.fields['defaultRevisitDaysWait'].widgetFactory = TextFieldWidget
        self.fields['defaultApplyToContent'].widgetFactory = TextLinesFieldWidget
        
    
    def updateWidgets(self):
        super(RevisitSettingsEditForm, self).updateWidgets()
        self.widgets['defaultApplyToContent'].rows = 4
        self.widgets['defaultApplyToContent'].style = u'width: 30%;'
        self.widgets['defaultRevisitDaysWait'].size = 5


class RevisitSettingsControlPanel(ControlPanelFormWrapper):
    form = RevisitSettingsEditForm


class FullRevisitListView (BrowserView):

    def revisit_items (self):
        offset_days = int(self.request.get("offset_days", "7"))
        return expired_revisit_content_data (
                self.context,
                self.request,
                offset_days  )
                


