#
# Test product's uninstallation
#

import unittest
import transaction
from AccessControl.SecurityManagement import newSecurityManager, \
    noSecurityManager
from Products.PloneTestCase.layer import PloneSiteLayer

from base import getToolByName, TestCase, ztc
from config import *

class TestErase(TestCase):
    # we use here nested layer for not to make an impact on
    # the rest test cases, this test case check uninstall procedure
    # thus it has to uninstall package which will be required to
    # be installed for other test cases
    class layer(PloneSiteLayer):
        @classmethod
        def setUp(cls):
            app = ztc.app()
            portal = app.plone
            
            # elevate permissions
            user = portal.getWrappedOwner()
            newSecurityManager(None, user)

            tool = getToolByName(portal, 'portal_quickinstaller')
            if tool.isProductInstalled(PRODUCT):
                tool.uninstallProducts([PRODUCT,])
            
            # drop elevated perms
            noSecurityManager()
            
            transaction.commit()
            ztc.close(app)

class TestUninstallation(TestErase):

    def afterSetUp(self):
        self.loginAsPortalOwner()
        self.qi = self.portal.portal_quickinstaller

    def test_package_uninstall(self):
        self.failIf(self.qi.isProductInstalled(PRODUCT),
            '%s is not uninstalled.' % PRODUCT)

    def test_skins_uninstall(self):
        skinstool=getToolByName(self.portal, 'portal_skins')
        self.failIf(PRODUCT_SKIN_NAME in skinstool.objectIds(),
            'There is still %s folder in portal_skins.' % PRODUCT_SKIN_NAME)
        for skin in skinstool.getSkinSelections():
            path = skinstool.getSkinPath(skin)
            layers = map(str.strip, path.split(','))
            self.failIf(PRODUCT_SKIN_NAME in layers,
                '%s layer is still in %s.' % (PRODUCT_SKIN_NAME, skin))

    def test_layer_uninstall(self):
        from plone.browserlayer.utils import registered_layers
        from quintagroup.plonecomments.interfaces import IPloneCommentsLayer
        self.failIf(IPloneCommentsLayer in registered_layers(),
            '%s layer found after uninstallation.' % IPloneCommentsLayer.getName())

    def test_configlet_uninstall(self):
        configTool = getToolByName(self.portal, 'portal_controlpanel', None)
        self.failIf(CONFIGLET_ID in [a.getId() for a in configTool.listActions()],
            'Configlet %s found after uninstallation.' % CONFIGLET_ID)

    def test_propertysheet_uninstall(self):
        portal_properties = getToolByName(self.portal, 'portal_properties')
        self.failUnless(PROPERTY_SHEET in portal_properties.objectIds(),
            '%s property_sheet not found in portal_properties after uninstallation.' % PROPERTY_SHEET)

def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestUninstallation))
    return suite
