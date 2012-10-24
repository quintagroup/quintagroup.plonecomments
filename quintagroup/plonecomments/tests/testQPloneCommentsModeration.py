#
# Test moderation behavior
#

import re
from Products.CMFCore.utils import getToolByName
from quintagroup.plonecomments.tests.common import addMembers, add2Group
from quintagroup.plonecomments.tests.base import FunctionalTestCase
from quintagroup.plonecomments.tests.config import USERS, DM_USERS_IDS, \
    COMMON_USERS_IDS


class TestModeration(FunctionalTestCase):

    def afterSetUp(self):
        self.loginAsPortalOwner()

        # Add all users
        addMembers(self.portal, USERS)

        # Add users to Discussion Manager group
        add2Group(self.portal, 'DiscussionManager', DM_USERS_IDS)

        # Allow discussion for Document
        portal_types = getToolByName(self.portal, 'portal_types')
        doc_fti = portal_types.getTypeInfo('Document')
        doc_fti._updateProperty('allow_discussion', 1)

        # Make sure Documents are visible by default
        self.portal.portal_workflow.setChainForPortalTypes(('Document',),
                                                           'plone_workflow')

        # Add testing documents to portal. Add one document for avery user.
        # For testing behaviors, where made some changes to document state
        # it's more usefull.
        self.discussion = getToolByName(self.portal, 'portal_discussion', None)
        all_users_id = DM_USERS_IDS + COMMON_USERS_IDS
        for user_id in all_users_id:
            doc_id = 'doc_%s' % user_id
            self.portal.invokeFactory('Document', id=doc_id)
            doc_obj = getattr(self.portal, doc_id)
            doc_obj.edit(text_format='plain',
                         text='hello world from %s' % doc_id)
            # Create talkback for document and Add comment to doc_obj
            self.discussion.getDiscussionFor(doc_obj)
            doc_obj.discussion_reply('A Reply for %s' % doc_id,
                                     'text of reply for %s' % doc_id)

    ## TEST VIEWING

    def testViewRepliesNotPublishedDMUsers(self):
        # All members of DiscussionManager group MUST VIEW comments
        doc = getattr(self.portal, 'doc_%s' % DM_USERS_IDS[0])
        for u in DM_USERS_IDS:
            self.login(u)
            replies = self.discussion.getDiscussionFor(doc).getReplies()
            self.failUnless(replies,
                            "Viewing discussion item forbiden for %s - "
                            "member of DiscussionManager group" % u)

    def testViewRepliesNotPublishedNotDMUsers(self):
        # All common users SHOULD NOT VIEW NOT PUBLISHED comments
        doc = getattr(self.portal, 'doc_%s' % DM_USERS_IDS[0])
        roles = [r['name']
                 for r in self.portal.rolesOfPermission('Moderate Discussion')
                 if r['selected'] == 'SELECTED']
        authorized_users = [user
                            for user in COMMON_USERS_IDS
                            if user != 'anonym']
        users_without_md_perm = [u
                                 for u in authorized_users
                                 if filter(lambda x: x not in roles, USERS[u]['roles'])]
        for u in users_without_md_perm:
            self.logout()
            if not u == 'anonym':
                self.login(u)
            replies = self.discussion.getDiscussionFor(doc).getReplies()
            self.failIf(replies,
                        "Viewing of NOT published discussion item allow %s - "
                        "user without 'Moderate Discussion' permission" % u)

    def testViewRepliesPublishedAllUsers(self):
        # All users MUST VIEW PUBLISHED comments
        # Get any document and publish it's comment
        doc = getattr(self.portal, 'doc_%s' % 'dm_admin')
        self.login('dm_admin')
        di = self.discussion.getDiscussionFor(doc).getReplies()[0]
        di.discussion_publish_comment()

        all_users_id = USERS.keys() + ['anonym']
        for u in all_users_id:
            self.logout()
            if not u == 'anonym':
                self.login(u)
            replies = self.discussion.getDiscussionFor(doc).getReplies()
            self.failUnless(replies,
                            "Viewing PUBLISHED discussion item forbiden for %s user" % u)

    ## TEST PUBLISHING

    def testViewPublishButtonNonDMUsers(self):
        # Publish button MUST BE ABSENT in document view form
        # Pattern for publish button presence checking
        pattern = re.compile('.*<input.+?value="Publish"', re.S | re.M)
        roles = [r['name']
                 for r in self.portal.rolesOfPermission('Moderate Discussion')
                 if r['selected'] == 'SELECTED']
        authorized_users = [user
                            for user in COMMON_USERS_IDS
                            if user != 'anonym']
        users_without_md_perm = [u
                                 for u in authorized_users
                                 if filter(lambda x: x not in roles, USERS[u]['roles'])]
        for u in users_without_md_perm:
            self.logout()
            auth = "%s:" % u
            if not u == 'anonym':
                self.login(u)
                auth = '%s:%s' % (u, USERS[u]['passw'])
            doc_id = "doc_%s" % u
            html = str(self.publish(self.portal.id + '/%s' % doc_id, auth))
            m = pattern.match(html)
            self.failIf(m, "Publish button present for %s - user without "
                           "Moderate Discussion permission" % u)

    """
    def testViewPublishButtonDMUsers(self):
        # Publish button MUST PRESENT in document view form
        # Pattern for publish button presence checking
        pattern = re.compile('.*<input.+?value="Publish"',re.S|re.M)
        # pattern = re.compile('.*<input\\s*class="standalone"\\s*type='
                               '"submit"\\s*value="Publish"\\s*/>', re.S|re.M)
        for u in DM_USERS_IDS:
            self.login(u)
            auth = '%s:%s' % (u,USERS[u]['passw'])
            doc_id = "doc_%s" % u
            html = str(self.publish(self.portal.id+'/%s' % doc_id, auth))
            m = pattern.match(html)
            self.failUnless(m, "Publish button NOT PRESENT for %s - member "
                               "of DiscussionManager group" % u)
    """

    def testPublishing(self):
        # Check whether perform real publishing
        # Pattern for publish button presence checking
        pattern = re.compile('.*<input.+?value="Publish"', re.S | re.M)
        for u in DM_USERS_IDS:
            doc_id = "doc_%s" % u
            doc_obj = getattr(self.portal, doc_id)
            getReplies = self.discussion.getDiscussionFor(doc_obj).getReplies
            # Check whether anonymous get no reply
            self.logout()
            self.failIf(getReplies(),
                        "View not published reply ALLOW for Anonymous")
            # Login with actual (tested) user with DiscussionManager role and
            # publish discussion
            self.login(u)
            self.failUnless(getReplies(), "%s - member of DiscussionManager "
                            "group NOT VIEW not published reply" % u)
            getReplies()[0].discussion_publish_comment()
            # Check if Publish button still present in document view page
            auth = "%s:" % u
            if not u == 'anonym':
                auth = '%s:%s' % (u, USERS[u]['passw'])
            html = str(self.publish(self.portal.id + '/%s' % doc_id, auth))
            m = pattern.match(html)
            self.failIf(m, "Publish button present for %s - DiscussionManager "
                           "role user after publishing" % u)
            # Check whether Anonym view published reply
            self.logout()
            self.failUnless(getReplies(),
                            "%s - member of DiscussionManager group NOT PUBLISH reply" % u)

    ## TEST DELETING

    """
    def testViewDeleteButtonNonDMUsers(self):
        # Check Delete reply button presense ONLY for PUBLISHED reply.
        # Because of NOT PUBLUISHED replies is not visible at all for common
        # users.
        # Delete reply button in document view form MUST BE ABSENT for all
        # EXCEPT manager.
        # Publish replies
        self.logout()
        self.login('dm_admin')
        for u in COMMON_USERS_IDS:
            doc_id = "doc_%s" % u
            doc_obj = getattr(self.portal, doc_id)
            reply = self.discussion.getDiscussionFor(doc_obj).getReplies()[0]
            reply.discussion_publish_comment()
        # Prepare pattern for delete reply button presence checking
        pattern = re.compile('.*<input\\s*class="destructive"\\s*type="submit"'
                             '\\s*value="Remove"\\s*/>', re.S|re.M)
        for u in COMMON_USERS_IDS:
            self.logout()
            auth = "%s:" % u
            if not u=='anonym':
                self.login(u)
                auth = '%s:%s' % (u,USERS[u]['passw'])
            doc_id = "doc_%s" % u
            html = str(self.publish(self.portal.id+'/%s' % doc_id, auth))
            m = pattern.match(html)
            if not u=='anonym' and 'Manager' in USERS[u]['roles']:
                self.failUnless(m, "%s - user with Manager role NOT VIEW "
                    "Delete reply button for published reply on document "
                    "view form" % u)
            else:
                self.failIf(m, "%s - user without Manager role CAN VIEW "
                    "Delete reply button for published reply on document "
                    "view form" % u)
    """

    def testDeleting(self):
        # Manager with DiscussionManager role CAN delete ANY REPLY.
        # Manager without DiscussionManager role [common manager] CAN delete
        # ONLY PUBLISHED REPLY.
        # Get Managers
        managers = [u for u in USERS.keys() if 'Manager' in USERS[u]['roles']]
        dm_man = [u for u in managers if u.startswith('dm_')][0]
        common_man = [u for u in managers if not u.startswith('dm_')][0]
        # Publish document for common manager
        self.login(dm_man)
        doc_obj = getattr(self.portal, "doc_%s" % common_man)
        reply = self.discussion.getDiscussionFor(doc_obj).getReplies()[0]
        reply.discussion_publish_comment()
        # Check for really deleting
        for u in managers:
            self.login(u)
            doc_id = "doc_%s" % u
            doc_obj = getattr(self.portal, doc_id)
            getReplies = self.discussion.getDiscussionFor(doc_obj).getReplies
            self.failUnless(getReplies(), "%s - user with Manager role not "
                                          "view discussion reply" % u)
            getReplies()[0].deleteDiscussion()
            self.failIf(getReplies(), "%s - user with Manager role not really "
                                      "delete discussion" % u)


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestModeration))
    return suite
