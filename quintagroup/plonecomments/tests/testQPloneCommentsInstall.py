#
# Test product's installation
#

from base import getToolByName, TestCase
from config import *


class TestInstallation(TestCase):

    def afterSetUp(self):
        self.loginAsPortalOwner()
        self.qi = self.portal.portal_quickinstaller

    def test_package_install(self):
        self.failUnless(self.qi.isProductInstalled(PRODUCT),
            '%s is not installed.' % PRODUCT)

    def test_configlet_install(self):
        configTool = getToolByName(self.portal, 'portal_controlpanel', None)
        self.failUnless(CONFIGLET_ID in [a.getId() for a in configTool.listActions()],
            'Configlet %s is not registered.' % CONFIGLET_ID)

    def test_skins_install(self):
        skinstool=getToolByName(self.portal, 'portal_skins')
        self.failUnless(PRODUCT_SKIN_NAME in skinstool.objectIds(),
                'There is no %s folder in portal_skins.' % PRODUCT_SKIN_NAME)
        for skin in skinstool.getSkinSelections():
	    path = skinstool.getSkinPath(skin)
            layers = map(str.strip, path.split(','))
            self.failUnless(PRODUCT_SKIN_NAME in layers,
 	        '%s layer is not registered for %s.' % (PRODUCT_SKIN_NAME, skin))

    def test_layer_install(self):
        from plone.browserlayer.utils import registered_layers
        from quintagroup.plonecomments.interfaces import IPloneCommentsLayer
        self.failUnless(IPloneCommentsLayer in registered_layers(),
            '%s layer is not registered.' % IPloneCommentsLayer.getName())

    def test_propertysheet_install(self):
        portal_properties = getToolByName(self.portal, 'portal_properties', None)
        self.failUnless(PROPERTY_SHEET in portal_properties.objectIds(),
            '%s properies not found in portal_properties.' % PROPERTY_SHEET)
        property_ids = portal_properties[PROPERTY_SHEET].propertyIds()
        self.failUnless(EMAIL_PID in property_ids,
            '%s propery not found in %s property.' % (EMAIL_PID, PROPERTY_SHEET))
        self.failUnless(EMAIL_SUBJECT_PID in property_ids,
            '%s propery not found in %s property.' % (EMAIL_SUBJECT_PID, PROPERTY_SHEET))
        self.failUnless(REQUIRE_EMAIL_PID in property_ids,
            '%s propery not found in %s property.' % (REQUIRE_EMAIL_PID, PROPERTY_SHEET))
        self.failUnless(APPROVE_NOTIFICATION_PID in property_ids,
            '%s propery not found in %s property.' % (APPROVE_NOTIFICATION_PID, PROPERTY_SHEET))
        self.failUnless(PUBLISHED_NOTIFICATION_PID in property_ids,
            '%s propery not found in %s property.' % (PUBLISHED_NOTIFICATION_PID, PROPERTY_SHEET))
        self.failUnless(REJECTED_NOTIFICATION_PID in property_ids,
            '%s propery not found in %s property.' % (REJECTED_NOTIFICATION_PID, PROPERTY_SHEET))
        self.failUnless(APPROVE_USER_NOTIFICATION_PID in property_ids,
            '%s propery not found in %s property.' % (APPROVE_USER_NOTIFICATION_PID, PROPERTY_SHEET))
        self.failUnless(REPLY_USER_NOTIFICATION_PID in property_ids,
            '%s propery not found in %s property.' % (REPLY_USER_NOTIFICATION_PID, PROPERTY_SHEET))
        self.failUnless(MODERATION_PID in property_ids,
            '%s propery not found in %s property.' % (MODERATION_PID, PROPERTY_SHEET))
        self.failUnless(ANONYMOUS_COMMENTING_PID in property_ids,
            '%s propery not found in %s property.' % (ANONYMOUS_COMMENTING_PID, PROPERTY_SHEET))

    def test_permission_added(self):
        roles = [item['name'] for item in self.portal.rolesOfPermission(PERM_NAME)]
        self.failIf( roles == [], '%s not installed.' % PERM_NAME)


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestInstallation))
    return suite
