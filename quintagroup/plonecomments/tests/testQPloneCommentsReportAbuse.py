from quintagroup.plonecomments.tests.testQPloneCommentsCommenting import \
    TestCommBase


class TestReportAbuse(TestCommBase):

    def afterSetUp(self):
        TestCommBase.afterSetUp(self)
        self.testAnonymousReportAbuse()
        self.testAuthenticatedReportAbuse()

    def testAnonymousReportAbuse(self):
        self.login('dm_admin')
        doc_obj = getattr(self.portal, "doc_anonym")
        discussion = self.discussion.getDiscussionFor(doc_obj)
        comment = discussion._container.values()[0]
        self.logout()
        # Add abuse report on document.
        doc_obj.REQUEST.set('comment_id', comment.id)
        try:
            doc_obj.report_abuse("Anonymous Report Abuse")
        except:
            raise "Anonymous user CAN'T report abuse in turned ON *Anonymous"\
                  " report abuse mode*."

    def testAuthenticatedReportAbuse(self):
        not_anonym_users = [u for u in self.all_users_id if not u == 'anonym']
        failed_users = []
        for u in not_anonym_users:
            self.login('dm_admin')
            doc_id = "doc_%s" % u
            doc_obj = getattr(self.portal, doc_id)
            discussion = self.discussion.getDiscussionFor(doc_obj)
            comment = discussion._container.values()[0]
            doc_obj.REQUEST.set('comment_id', comment.id)
            self.login(u)
            try:
                doc_obj.report_abuse("Anonymous Report Abuse")
            except:
                failed_users.append(u)

        self.assert_(not failed_users,
                     "%s - user(s) can not report abuse" % failed_users)


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestReportAbuse))
    return suite
