import unittest

#from zope.testing import doctestunit
#from zope.component import testing
#from Testing import ZopeTestCase as ztc
#from base import TestCase


def test_suite():
    return unittest.TestSuite([

        # Unit tests
        #doctestunit.DocFileSuite(
        #    'README.txt', package='quintagroup.plonecomments',
        #    setUp=testing.setUp, tearDown=testing.tearDown),

        #doctestunit.DocTestSuite(
        #    module='quintagroup.plonecomments.mymodule',
        #    setUp=testing.setUp, tearDown=testing.tearDown),


        # Integration tests that use PloneTestCase
        #ztc.ZopeDocFileSuite(
        #    'README.txt', package='quintagroup.plonecomments',
        #    test_class=TestCase),

        #ztc.FunctionalDocFileSuite(
        #    'browser.txt', package='quintagroup.plonecomments',
        #    test_class=TestCase),

    ])

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
