import transaction

from Products.Five import zcml, fiveconfigure

from Testing import ZopeTestCase as ztc
from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import onsetup

from quintagroup.plonecomments.tests.config import PRODUCT


@onsetup
def setup_product():
    """Set up additional products and ZCML required to test this product.

    The @onsetup decorator causes the execution of this body to be deferred
    until the setup of the Plone site testing layer.
    """

    # Load the ZCML configuration for this package and its dependencies

    fiveconfigure.debug_mode = True
    import quintagroup.plonecomments
    zcml.load_config('configure.zcml', quintagroup.plonecomments)
    zcml.load_config('overrides.zcml', quintagroup.plonecomments)
    fiveconfigure.debug_mode = False

    # We need to tell the testing framework that these products
    # should be available. This can't happen until after we have loaded
    # the ZCML.
    if not ptc.PLONE31:
        ztc.installPackage("plone.browserlayer")
    ztc.installPackage(PRODUCT)
    transaction.commit()


# The order here is important: We first call the deferred function and then
# let PloneTestCase install it during Plone site setup

setup_product()
if not ptc.PLONE31:
    ptc.setupPloneSite(products=["plone.browserlayer", PRODUCT])
else:
    ptc.setupPloneSite(products=[PRODUCT])


class TestCase(ptc.PloneTestCase):
    """Base class used for test cases
    """


class FunctionalTestCase(ptc.FunctionalTestCase):
    """Test case class used for functional (doc-)tests
    """


class TestErase(TestCase):
    """Test case class used for uninstalling tests
    """
