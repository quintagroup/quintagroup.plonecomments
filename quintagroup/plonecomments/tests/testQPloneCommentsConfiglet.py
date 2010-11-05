#
# Test configuration form working
#

from Products.CMFCore.permissions import ReplyToItem
from AccessControl.SecurityManagement import noSecurityManager
from base import getToolByName, FunctionalTestCase
from config import USERS, PROPERTY_SHEET, DM_USERS_IDS, COMMON_USERS_IDS

def addUsers(self):
    self.loginAsPortalOwner()
    # Add all users
    self.membership = getToolByName(self.portal, 'portal_membership', None)
    for user_id in USERS.keys():
        self.membership.addMember(user_id, USERS[user_id]['passw'] , USERS[user_id]['roles'], [])

    # Add users to Discussion Manager group
    portal_groups = getToolByName(self.portal, 'portal_groups')
    dm_group = portal_groups.getGroupById('DiscussionManager')
    dm_users = [dm_group.addMember(u) for u in DM_USERS_IDS]


class TestConfiglet(FunctionalTestCase):

    def afterSetUp(self):
        self.loginAsPortalOwner()

        # VERY IMPORTANT to guarantee product skin's content visibility
        self._refreshSkinData()

        '''Preparation for functional testing'''
        # Allow discussion for Document
        portal_types = getToolByName(self.portal, 'portal_types', None)
        doc_fti = portal_types.getTypeInfo('Document')
        doc_fti._updateProperty('allow_discussion', 1)

        # Make sure Documents are visible by default
        # XXX only do this for plone 3
        self.portal.portal_workflow.setChainForPortalTypes(('Document',), 'plone_workflow')

        portal_properties = getToolByName(self.portal, 'portal_properties', None)
        self.prefs = portal_properties[PROPERTY_SHEET]
        self.request = self.app.REQUEST

        # Add Manager user - 'dm' and add him to Discussion Manager group
        self.portal.portal_membership.addMember('dm', 'secret' , ['Manager'], [])
        portal_groups = getToolByName(self.portal, 'portal_groups')
        dm_group = portal_groups.getGroupById('DiscussionManager')
        dm_group.addMember('dm')
        #self.logout()
        self.login('dm')
        # For prepare mail sending - enter an e-mail adress
        self.prefs._updateProperty('email_discussion_manager', 'discussion.manager@test.com')
        member = self.portal.portal_membership.getAuthenticatedMember()
        member.setMemberProperties({'email':'creator@test.com'})
        #self.fail(member.getMemberId()+' :: '+member.getUserName()+' \
        #    :: '+str(member.getRoles())+' :: '+member.getProperty('email'))

        # Add testing document to portal
        my_doc = self.portal.invokeFactory('Document', id='my_doc')
        self.my_doc = self.portal['my_doc']
        self.my_doc.edit(text_format='plain', text='hello world')

    def testAnonymousCommenting(self):
        getPortalReplyPerm = self.portal.rolesOfPermission
        def getReplyRoles():
            return [r['name'] for r in getPortalReplyPerm(ReplyToItem) if r['selected']=='SELECTED']
        # Simulate switching ON Anonymous Commenting
        self.request.form['enable_anonymous_commenting'] = 'True'
        self.portal.prefs_comments_setup()
        actual_reply_permission = getReplyRoles()
        self.failUnless('Anonymous' in actual_reply_permission, \
            "'Reply to Item' permission set for %s. 'Anonymous' "
            "role NOT added" %  actual_reply_permission)
        # Simulate switching OFF Anonymous Commenting
        if self.request.form.has_key('enable_anonymous_commenting'):
           del self.request.form['enable_anonymous_commenting']
        self.portal.prefs_comments_setup()
        actual_reply_permission = getReplyRoles()
        self.failIf('Anonymous' in actual_reply_permission, \
            "'Reply to Item' permission set for %s. 'Anonymous' role "
            "NOT erased" %  actual_reply_permission)

    def testSwitchONModeration(self):
        addUsers(self)
        self.discussion = self.portal.portal_discussion
        self.request.form['enable_anonymous_commenting'] = 'True'
        self.request.form['enable_moderation'] = 'True'
        self.portal.prefs_comments_setup()
        # Create talkback for document and Add comment to my_doc
        self.discussion.getDiscussionFor(self.my_doc)
        self.my_doc.discussion_reply('Reply 1','text of reply')
        # Check moderating discussion
        # MUST ALLOW for: members of 'DiscussionMnagers' group
        # MUST REFUSE for: NOT members of 'DiscussionMnagers' group
        getReplies = self.discussion.getDiscussionFor(self.my_doc).getReplies
        for u in DM_USERS_IDS:
            self.logout()
            self.login(u)
            self.failUnless(getReplies(),
                "None discussion item added or discussion forbiden for %s user" % u)
        for u in COMMON_USERS_IDS:
            self.logout()
            if not u=='anonym':
                self.login(u)
            noSecurityManager()
            self.failIf(getReplies(), "Viewing discussion item allow for Anonymous user")

    def testSwitchOFFModeration(self):
        addUsers(self)
        self.discussion = self.portal.portal_discussion
        self.request.form['enable_anonymous_commenting'] = 'True'
        self.portal.prefs_comments_setup()
        # Create talkback for document and Add comment to my_doc
        self.discussion.getDiscussionFor(self.my_doc)
        self.request.form['Creator'] = self.portal.portal_membership.getAuthenticatedMember().getUserName()
        self.request.form['subject'] = "Reply 1"
        self.request.form['body_text'] = "text of reply"
        self.my_doc.discussion_reply('Reply 1','text of reply')
        # Check moderating discussion
        # MUST ALLOW for: user with any role or Anonym
        all_users_ids = DM_USERS_IDS + COMMON_USERS_IDS
        for u in all_users_ids:
            self.logout()
            if not u=='anonym':
                self.login(u)
            replies = self.discussion.getDiscussionFor(self.my_doc).getReplies()
            self.failUnless(replies,
                "No discussion item added or discussion forbidden for %s user" % u)

    def testApproveNotification(self):
        # Check ON Notification Anonymous Commenting
        self.request.form['enable_approve_notification'] = 'True'
        self.portal.prefs_comments_setup()
        self.failUnless(self.prefs.getProperty('enable_approve_notification')==1,
            "Approve Notification not terned ON")

        # Check OFF Notification Anonymous Commenting
        if self.request.form.has_key('enable_approve_notification'):
           del self.request.form['enable_approve_notification']
        self.portal.prefs_comments_setup()
        self.failUnless(self.prefs.getProperty('enable_approve_notification')==0,
            "Approve Notification not terned OFF")

    def testPublishedNotification(self):
        # Check ON Notification Anonymous Commenting
        self.request.form['enable_published_notification'] = 'True'
        self.portal.prefs_comments_setup()
        self.failUnless(self.prefs.getProperty('enable_published_notification')==1,
            "Published Notification not terned ON")

        # Check OFF Notification Anonymous Commenting
        if self.request.form.has_key('enable_published_notification'):
           del self.request.form['enable_published_notification']
        self.portal.prefs_comments_setup()
        self.failUnless(self.prefs.getProperty('enable_published_notification')==0,
            "Published Notification not terned OFF")


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestConfiglet))
    return suite
