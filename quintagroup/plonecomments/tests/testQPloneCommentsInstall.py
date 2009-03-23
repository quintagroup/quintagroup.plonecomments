#
# Test product's installation/uninstallation
#

from base import *

class TestInstallation(TestCase):

    def afterSetUp(self):
        self.loginAsPortalOwner()
        self.qi = self.portal.portal_quickinstaller
        self.qi.installProduct(PRODUCT)

    def test_configlet_install(self):
        configTool = getToolByName(self.portal, 'portal_controlpanel', None)
        self.assert_(CONFIGLET_ID in [a.getId() for a in configTool.listActions()], 'Configlet not found')

    def test_skins_install(self):
        skinstool=getToolByName(self.portal, 'portal_skins')
        for skin in skinstool.getSkinSelections():
            path = skinstool.getSkinPath(skin)
            path = map(str.strip, path.split(','))
            self.assert_(PRODUCT_SKIN_NAME in path, 'quintagroup.plonecomments layer not found in %s' % skin)

    def test_layer_install(self):
        from plone.browserlayer.utils import registered_layers
        from quintagroup.plonecomments.interfaces import IPloneCommentsLayer
        self.failUnless(IPloneCommentsLayer in registered_layers())

    def test_propertysheet_install(self):
        portal_properties = getToolByName(self.portal, 'portal_properties', None)

        self.assert_(PROPERTY_SHEET in portal_properties.objectIds(), 'qPloneComments properies not found in portal_properties')

        property_ids = portal_properties[PROPERTY_SHEET].propertyIds()
        self.assert_(EMAIL_PID in property_ids, '%s propery not found in %s property' % (EMAIL_PID, PROPERTY_SHEET))
        self.assert_(APPROVE_NOTIFICATION_PID in property_ids, '%s propery not found in %s property' % (APPROVE_NOTIFICATION_PID, PROPERTY_SHEET))
        self.assert_(PUBLISHED_NOTIFICATION_PID in property_ids, '%s propery not found in %s property' % (PUBLISHED_NOTIFICATION_PID, PROPERTY_SHEET))
        self.assert_(MODERATION_PID in property_ids, '%s propery not found in %s property' % (MODERATION_PID, PROPERTY_SHEET))
        self.assert_(ANONYMOUS_COMMENTING_PID in property_ids, '%s propery not found in %s property' % (ANONYMOUS_COMMENTING_PID, PROPERTY_SHEET))

    def test_skins_uninstall(self):
        self.qi.uninstallProducts([PRODUCT])
        self.assertNotEqual(self.qi.isProductInstalled(PRODUCT), True,'quintagroup.plonecomments is already installed')
        skinstool=getToolByName(self.portal, 'portal_skins')

        self.assert_(not PRODUCT_SKIN_NAME in skinstool.objectIds(), '%s directory view found in portal_skins after uninstallation' % PRODUCT_SKIN_NAME)
        for skin in skinstool.getSkinSelections():
            path = skinstool.getSkinPath(skin)
            path = map(str.strip, path.split(','))
            self.assert_(not PRODUCT_SKIN_NAME in path, '%s layer found in %s after uninstallation' % (PRODUCT_SKIN_NAME, skin))

    def test_layer_uninstall(self):
        self.qi.uninstallProducts([PRODUCT])
        self.assertNotEqual(self.qi.isProductInstalled(PRODUCT), True,'quintagroup.plonecomments is already installed')

        from plone.browserlayer.utils import registered_layers
        from quintagroup.plonecomments.interfaces import IPloneCommentsLayer
        self.failIf(IPloneCommentsLayer in registered_layers())

    def test_configlet_uninstall(self):
        self.qi.uninstallProducts([PRODUCT])
        self.assertNotEqual(self.qi.isProductInstalled(PRODUCT), True,'quintagroup.plonecomments is already installed')

        configTool = getToolByName(self.portal, 'portal_controlpanel', None)
        self.assert_(not CONFIGLET_ID in [a.getId() for a in configTool.listActions()], 'Configlet found after uninstallation')

    def test_propertysheet_uninstall(self):
        self.qi.uninstallProducts([PRODUCT])
        self.assertNotEqual(self.qi.isProductInstalled(PRODUCT), True,'quintagroup.plonecomments is already installed')

        portal_properties = getToolByName(self.portal, 'portal_properties')
        self.assert_(PROPERTY_SHEET in portal_properties.objectIds(), \
                     'qPloneComments property_sheet not found in portal_properties after uninstallation')

    def test_permission_added(self):
        roles = [item['name'] for item in self.portal.rolesOfPermission(PERM_NAME)]
        self.assert_( roles != [], '%s not installed'%PERM_NAME)


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestInstallation))
    return suite
