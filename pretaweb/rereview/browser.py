
from plone.app.registry.browser import controlpanel
try:
    # only in z3c.form 2.0
    from z3c.form.browser.textlines import TextLinesFieldWidget
    from z3c.form.browser.text import TextFieldWidget
except ImportError:
    from plone.z3cform.textlines import TextLinesFieldWidget
    from plone.z3cform.text import TextFieldWidget

from interfaces import IRereviewSettings

class RereviewSettingsEditForm (controlpanel.RegistryEditForm):
    schema = IRereviewSettings
    label = u"Rereview Settings"
    description = u"Settings for rereview default date settings"

 
    def updateFields(self):
        super(RereviewSettingsEditForm, self).updateFields()
        self.fields['defaultRereviewDaysWait'].widgetFactory = TextFieldWidget
        self.fields['defaultApplyToContent'].widgetFactory = TextLinesFieldWidget
        
    
    def updateWidgets(self):
        super(RereviewSettingsEditForm, self).updateWidgets()
        self.widgets['defaultApplyToContent'].rows = 4
        self.widgets['defaultApplyToContent'].style = u'width: 30%;'
        self.widgets['defaultRereviewDaysWait'].size = 5


class RereviewSettingsControlPanel(controlpanel.ControlPanelFormWrapper):
    form = RereviewSettingsEditForm


