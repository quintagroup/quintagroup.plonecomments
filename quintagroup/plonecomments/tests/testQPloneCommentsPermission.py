#
# Test 'Moderate Discussion' permission
#

from Products.CMFDefault.DiscussionItem import DiscussionItemContainer

from base import *

class TestPermission(TestCase):

    def afterSetUp(self):
        self.loginAsPortalOwner()
        self.portal.portal_quickinstaller.installProduct(PRODUCT)

    def test_install_moderate_discussion_permission(self):
        roles = [item['name'] for item in self.portal.rolesOfPermission(PERM_NAME) if item['selected'] == 'SELECTED']
        self.assert_( roles != [], '%s not installed'%PERM_NAME)

    def test_deleteReply_permission(self):
        #dic = DiscussionItemContainer()
        #dic.createReply('Title', 'Text')
        pass

    def test_manager_moderation(self):
        pass


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestPermission))
    return suite
