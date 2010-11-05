#
# Test adding comments possibility on switching on/off moderation
#

from zExceptions import Unauthorized
from base import getToolByName, FunctionalTestCase
from config import USERS, PROPERTY_SHEET, DM_USERS_IDS, COMMON_USERS_IDS


class TestCommBase(FunctionalTestCase):

    def afterSetUp(self):
        self.loginAsPortalOwner()
        self.request = self.app.REQUEST

	# VERY IMPORTANT to guarantee product skin's content visibility
        self._refreshSkinData()

        # Add all users
        self.membership = getToolByName(self.portal, 'portal_membership', None)
        for user_id in USERS.keys():
            self.membership.addMember(user_id, USERS[user_id]['passw'],
	        USERS[user_id]['roles'], [])

        # Add users to Discussion Manager group
        portal_groups = getToolByName(self.portal, 'portal_groups')
        dm_group = portal_groups.getGroupById('DiscussionManager')
        dm_users = [dm_group.addMember(u) for u in DM_USERS_IDS]

        # Allow discussion for Document
        portal_types = getToolByName(self.portal, 'portal_types', None)
        doc_fti = portal_types.getTypeInfo('Document')
        doc_fti._updateProperty('allow_discussion', 1)

        # Make sure Documents are visible by default
        # XXX only do this for plone 3
        self.portal.portal_workflow.setChainForPortalTypes(('Document',), 'plone_workflow')

        # Add testing documents to portal. Add one document for avery user.
        # For testing behaviors, where made some changes to document state it's more usefull.
        self.discussion = getToolByName(self.portal, 'portal_discussion', None)
        self.all_users_id = DM_USERS_IDS + COMMON_USERS_IDS
        for user_id in self.all_users_id:
            doc_id = 'doc_%s' % user_id
            self.portal.invokeFactory('Document', id=doc_id)
            doc_obj = getattr(self.portal, doc_id)
            doc_obj.edit(text_format='plain', text='hello world from %s' % doc_id)
            # Create talkback for document and Add comment to doc_obj
            self.discussion.getDiscussionFor(doc_obj)
            doc_obj.discussion_reply('A Reply for %s' % doc_id,'text of reply for %s' % doc_id)


class TestMixinAnonymOn:

    def afterSetUp(self):
        pass

    def testAddCommentToDocAnonymUsers(self):

        # ADDING COMMENTS MUST ALLOWED for anonymous users
        self.login('dm_admin')
        doc_obj = getattr(self.portal, "doc_anonym")
        replies_before = len(self.discussion.getDiscussionFor(doc_obj).getReplies())

        # Create talkback for document and Add comment
        self.logout()
        doc_obj.discussion_reply("Anonym reply", "text of 'anonym' reply")
        self.login('dm_admin')
        replies_after = len(self.discussion.getDiscussionFor(doc_obj).getReplies())
        self.failUnless(replies_after-replies_before,
	    "Anonymous user CAN'T really add comment in terned ON *Anonymous commenting mode*.")

    def testAddCommentToDocNotAnonymUsers(self):

        # All users CAN ADD COMMENTS
        not_anonym_users = [u for u in self.all_users_id if not u=='anonym']
        failed_users = []
        for u in not_anonym_users:
            self.login('dm_admin')
            doc_id = "doc_%s" % u
            doc_obj = getattr(self.portal, doc_id)
            replies_before = self.discussion.getDiscussionFor(doc_obj).getReplies()
            self.login(u)

            # Create talkback for document and Add comment
            doc_obj.discussion_reply("%s's reply" % u, "text of '%s' reply" % u)

            # Check is comment added
            self.login('dm_admin')
            replies_after = self.discussion.getDiscussionFor(doc_obj).getReplies()
            disparity = len(replies_after) - len(replies_before)
            if not disparity:
                failed_users.append(u)
        self.failIf(failed_users, "%s - user(s) can not really add comment." % failed_users)


class TestMixinAnonymOff:

    def afterSetUp(self):
        all_users_id = DM_USERS_IDS + COMMON_USERS_IDS
        self.not_like_anonym = ['admin', 'member', 'dm_admin', 'dm_member']
        self.like_anonym = [u for u in all_users_id if u not in self.not_like_anonym]


    def testAddCommentToDocLikeAnonymUsers(self):

        # ADDING COMMENTS MUST REFUSED for anonymous users
        failed_users = []
        for u in self.like_anonym:
            self.login('dm_admin')
            doc_obj = getattr(self.portal, "doc_%s" % u)
            replies_before = self.discussion.getDiscussionFor(doc_obj).getReplies()

            # Create talkback for document and Add comment
            self.logout()
            if not u=='anonym':
                self.login(u)
            self.assertRaises(Unauthorized, doc_obj.discussion_reply,
	        "%s's reply" % u, "text of '%s' reply" % u)
            self.login('dm_admin')
            replies_after = self.discussion.getDiscussionFor(doc_obj).getReplies()
            disparity = len(replies_after) - len(replies_before)
            if disparity:
                failed_users.append(u)
        self.failIf(failed_users,
	    "%s user(s) CAN really add comment in terned OFF "
	    "*Anonymous commenting mode*." % failed_users)


    def testAddCommentToDocNotLikeAnonymUsers(self):

        # All users CAN ADD COMMENTS
        failed_users = []
        for u in self.not_like_anonym:
            self.login('dm_admin')
            doc_id = "doc_%s" % u
            doc_obj = getattr(self.portal, doc_id)
            replies_before = self.discussion.getDiscussionFor(doc_obj).getReplies()
            self.login(u)

            # Create talkback for document and Add comment
            doc_obj.discussion_reply("%s's reply" % u, "text of '%s' reply" % u)

            # Check is comment added
            self.login('dm_admin')
            replies_after = self.discussion.getDiscussionFor(doc_obj).getReplies()
            disparity = len(replies_after) - len(replies_before)
            if not disparity:
                failed_users.append(u)
        self.failIf(failed_users,
	    "%s - user(s) can not really add commentin terned OFF "
	    "*Anonymous commenting mode*." % failed_users)


class TestMixinModerationOn:

    def afterSetUp(self):

        # Get Moderation state
        pp = getToolByName(self.portal, 'portal_properties')
        config_ps = getattr(pp, PROPERTY_SHEET, None)
        EnableAnonymComm = getattr(config_ps, "enable_anonymous_commenting")

        # Group users depending on Anonymous commenting enabling/disabling
        if EnableAnonymComm:
            self.allowable_dm_users = DM_USERS_IDS
            self.allowable_common_users = COMMON_USERS_IDS
            self.illegal_dm_users = []
            self.illegal_common_users = []
        else:
            self.allowable_dm_users = ['dm_admin', 'dm_member']
            self.allowable_common_users = ['admin', 'member']
            self.illegal_dm_users = [u for u in DM_USERS_IDS if not u in self.allowable_dm_users]
            self.illegal_common_users = [u for u in COMMON_USERS_IDS if not u in self.allowable_common_users]

    
    def testAddCommentToNotPublishedReplyDMUsers(self):

        # DiscussionManager's group's members with Manager or Member roles CAN ADD COMMENTS
        # to reply IN ANY STATE (published/not published)
        failed_users = []
        for u in self.allowable_dm_users:
            self.login(u)
            doc_obj = getattr(self.portal, "doc_%s" % u)
            # Get reply to this document
            reply = self.discussion.getDiscussionFor(doc_obj).getReplies()[0]
            # Create talkback for reply and Add comment
            self.discussion.getDiscussionFor(reply)
            reply.discussion_reply("%s's reply" % u, "text of '%s' reply" % u)
            replies_to_reply = self.discussion.getDiscussionFor(reply).getReplies()
            if not replies_to_reply:
                failed_users.append(u)
        self.failIf(failed_users,
	    "%s - member(s) of DiscussionManager group CAN'T really ADD comment" % failed_users)

        # This is actual only in terned OFF *Anonymous commenting mode*
        failed_users = []
        for u in self.illegal_dm_users:
            self.login(u)
            doc_obj = getattr(self.portal, "doc_%s" % u)
            # Get reply to this document
            reply = self.discussion.getDiscussionFor(doc_obj).getReplies()[0]
            # Create talkback for reply and Add comment
            self.discussion.getDiscussionFor(reply)
            self.assertRaises(Unauthorized, reply.discussion_reply, "%s's reply" % u, "text of '%s' reply" % u)
            replies_to_reply = self.discussion.getDiscussionFor(reply).getReplies()
            if replies_to_reply:
                failed_users.append(u)
        self.failIf(failed_users,
	    "%s user(s) CAN really add comment in terned OFF "
	    "*Anonymous commenting mode*." % failed_users)

    """
    def testAddCommentToNotPublishedReplyNotDMUsers(self):
        # Users without DiscussionManager role CAN'T ACCESS an so ADD COMMENTS
        # TO NOT PUBLISHED reply.
        manager = 'dm_admin'
        for u in self.allowable_common_users:
            self.login(manager)
            doc_obj = getattr(self.portal, "doc_%s" % u)
            reply = self.discussion.getDiscussionFor(doc_obj).getReplies()[0]
            reply_to_reply = self.discussion.getDiscussionFor(reply).getReplies()
            reply_to_reply_before = len(reply_to_reply)
            self.logout()
            if not u=='anonym':
                self.login(u)
            # On adding reply to not published reply MUST generte Unauthorized exception
            self.assertRaises(Unauthorized, reply.discussion_reply, "Reply %s" % u, "text of %s reply" % u)
    """

    def testAddCommentToPublishedReplyALLUsers(self):

        # All users CAN ADD COMMENTS to published reply
        manager = 'dm_admin'
        allowable_users = self.allowable_dm_users + self.allowable_common_users
        illegal_users = self.illegal_dm_users + self.illegal_common_users
        all_users = allowable_users + illegal_users

        # 1. Publish comments
        self.login(manager)
        for u in all_users:
            doc_obj = getattr(self.portal, "doc_%s" % u)
            reply = self.discussion.getDiscussionFor(doc_obj).getReplies()[0]
            reply.discussion_publish_comment()

        # 2.Check adding reply to reply for allowable users
        failed_users = []
        for u in allowable_users:
            self.logout()
            if not u=='anonym':
                self.login(u)

            # Create talkback for document and Add comment
            self.discussion.getDiscussionFor(reply)
            reply.discussion_reply("Reply %s" % u, "text of %s reply" % u)

            # Check is comment added
            self.login(manager)
            reply_to_reply = self.discussion.getDiscussionFor(reply).getReplies()
            if not reply_to_reply:
                failed_users.append(u)
        self.failIf(failed_users,
	    "%s - user(s) can not really add comment to PUBLISHED reply." % failed_users)

        # 3.Check adding reply to reply for illegal users
        for u in illegal_users:
            self.logout()
            if not u=='anonym':
                self.login(u)

            # On adding reply to not published reply MUST generte Unauthorized exception
            self.discussion.getDiscussionFor(reply)
            self.assertRaises(Unauthorized, reply.discussion_reply,
	        "Reply %s" % u, "text of %s reply" % u)


class TestMixinModerationOff:

    def afterSetUp(self):

        # Get Moderation state
        pp = getToolByName(self.portal, 'portal_properties')
        config_ps = getattr(pp, PROPERTY_SHEET, None)
        EnableAnonymComm = getattr(config_ps, "enable_anonymous_commenting")

        # Group users depending on Anonymous commenting enabling/disabling
        if EnableAnonymComm:
            self.allowable_users = DM_USERS_IDS + COMMON_USERS_IDS
            self.illegal_users = []
        else:
            self.allowable_users = ['dm_admin', 'dm_member', 'admin', 'member']
            self.illegal_users = [u for u in self.all_users_id if not u in self.allowable_users]

        # Add testing document to portal in Moderation OFF mode.
        self.discussion = getToolByName(self.portal, 'portal_discussion', None)
        self.doc_moder_off_id = 'doc_moderation_off'
        self.portal.invokeFactory('Document', id=self.doc_moder_off_id)
        doc_obj = getattr(self.portal, self.doc_moder_off_id)
        doc_obj.edit(text_format='plain', text='hello world from in moderation off mode')

        # Create talkback for document and Add comment to 'doc_moderatio_off'
        self.discussion.getDiscussionFor(doc_obj)
        doc_obj.discussion_reply("A Reply to '%s'" % self.doc_moder_off_id,
	    "text of reply to '%s'" % self.doc_moder_off_id)


    def testAddCommentToReplyAllowableUsers(self):

        # Users CAN ADD COMMENTS
        failed_users = []
        for u in self.allowable_users:
            self.logout()
            if not u=='anonym':
                self.login(u)
            doc_obj = getattr(self.portal, self.doc_moder_off_id)

            # Get reply to this document
            reply_to_doc = self.discussion.getDiscussionFor(doc_obj).getReplies()[0]

            # Create talkback for reply and Add comment
            replies_before = self.discussion.getDiscussionFor(reply_to_doc).getReplies()
            if not replies_before:
                self.discussion.getDiscussionFor(reply_to_doc)
            reply_to_doc.discussion_reply("%s's reply" % u, "text of '%s' reply" % u)
            replies_after = self.discussion.getDiscussionFor(reply_to_doc).getReplies()
            disparity = len(replies_after) - len(replies_before)
            if not disparity:
                failed_users.append(u)
        self.failIf(failed_users ,
	    "%s - member(s) CAN'T really ADD comment in terned off"
	    " comments Moderation mode." % failed_users)


    def testAddCommentToReplyIllegalUsers(self):

        # This users CAN'T ADD COMMENTS
        # This is actual only in terned OFF *Anonymous commenting mode*
        for u in self.illegal_users:
            self.logout()
            if not u=='anonym':
                self.login(u)
            doc_obj = getattr(self.portal, self.doc_moder_off_id)

            # Get reply to this document
            reply_to_doc = self.discussion.getDiscussionFor(doc_obj).getReplies()[0]

            # Create talkback for reply and Add comment
            self.discussion.getDiscussionFor(reply_to_doc)
            self.assertRaises(Unauthorized, reply_to_doc.discussion_reply,
	    "%s's reply" % u, "text of '%s' reply" % u)


class TestModerationAnonymComm(TestCommBase, TestMixinAnonymOn, TestMixinModerationOn):

    def afterSetUp(self):
        TestCommBase.afterSetUp(self)

        # Preparation for functional testing
        # Tern On Moderation and tern on Anonymous commenting
        self.request.form['enable_anonymous_commenting'] = 'True'
        self.request.form['enable_moderation'] = 'True'
        self.portal.prefs_comments_setup()

        # Initialize base classes
        TestMixinAnonymOn.afterSetUp(self)
        TestMixinModerationOn.afterSetUp(self)


class TestModerationOFFAnonymComm(TestCommBase, TestMixinAnonymOff, TestMixinModerationOn):

    def afterSetUp(self):
        TestCommBase.afterSetUp(self)

        # Preparation for functional testing
        # Tern On Moderation and tern off Anonymous commenting
        self.request.form['enable_moderation'] = 'True'
        self.portal.prefs_comments_setup()

        # Initialize base classes
        TestMixinAnonymOff.afterSetUp(self)
        TestMixinModerationOn.afterSetUp(self)


class TestAnonymCommOFFModeration(TestCommBase, TestMixinAnonymOn, TestMixinModerationOff):

    def afterSetUp(self):
        TestCommBase.afterSetUp(self)

        # Preparation for functional testing
        # Tern On Anonymous commenting and tern off  Moderation
        self.request.form['enable_anonymous_commenting'] = 'True'
        self.portal.prefs_comments_setup()

        # Initialize base classes
        TestMixinAnonymOn.afterSetUp(self)
        TestMixinModerationOff.afterSetUp(self)


class TestOFFModerationOFFAnonymComm(TestCommBase, TestMixinAnonymOff, TestMixinModerationOff):

    def afterSetUp(self):
        TestCommBase.afterSetUp(self)

        # Preparation for functional testing
        # Tern Off Moderation and tern off Anonymous commenting
        self.portal.prefs_comments_setup()

        # Initialize base classes
        TestMixinAnonymOff.afterSetUp(self)
        TestMixinModerationOff.afterSetUp(self)


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestModerationAnonymComm))
    suite.addTest(makeSuite(TestModerationOFFAnonymComm))
    suite.addTest(makeSuite(TestAnonymCommOFFModeration))
    suite.addTest(makeSuite(TestOFFModerationOFFAnonymComm))

    return suite
