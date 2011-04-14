from Products.CMFCore.utils import getToolByName
from StringIO import StringIO


def install(self):
    out = StringIO()
    setup_tool = getToolByName(self, 'portal_setup')
    profile = 'profile-quintagroup.plonecomments:default'
    setup_tool.runAllImportStepsFromProfile(profile)
    print >> out, "Imported install profile."
    return out.getvalue()


def uninstall(self):
    out = StringIO()
    setup_tool = getToolByName(self, 'portal_setup')
    profile = 'profile-quintagroup.plonecomments:uninstall'
    setup_tool.runAllImportStepsFromProfile(profile)
    print >> out, "Imported uninstall profile."
    return out.getvalue()
