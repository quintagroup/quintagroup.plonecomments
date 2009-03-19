from Products.CMFCore.utils import getToolByName
from StringIO import StringIO

def uninstall(self):
    out = StringIO()
    setup_tool = getToolByName(self, 'portal_setup')
    setup_tool.runAllImportStepsFromProfile('profile-quintagroup.plonecomments:uninstall')
    print >> out, "Imported uninstall profile."
    return out.getvalue()
