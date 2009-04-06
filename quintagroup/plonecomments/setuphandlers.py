from Products.CMFCore.utils import getToolByName
from config import LOGGER

def install(context):

    # Ordinarily, GenericSetup handlers check for the existence of XML files.
    # Here, we are not parsing an XML file, but we use this text file as a
    # flag to check that we actually meant for this import step to be run.
    # The file is found in profiles/default.

    if context.readDataFile('quintagroup.plonecomments_install.txt') is None:
        return

    # Add additional setup code here

    portal = context.getSite()
    logger = context.getLogger(LOGGER)

    # Add 'DiscussionManagers' group
    gtool = getToolByName(portal, 'portal_groups')
    existing = gtool.listGroupIds()
    if not 'DiscussionManager' in existing:
        gtool.addGroup('DiscussionManager', roles=['DiscussionManager'])
        logger.info('Added DiscussionManager group to portal_groups with DiscussionManager role.')

    # Remove workflow-chain for Discussion Item
    wf_tool = getToolByName(portal, 'portal_workflow')
    wf_tool.setChainForPortalTypes(('Discussion Item',), [])
    logger.info('Removed workflow chain for Discussion Item type.')

def uninstall(context):

    # Ordinarily, GenericSetup handlers check for the existence of XML files.
    # Here, we are not parsing an XML file, but we use this text file as a
    # flag to check that we actually meant for this import step to be run.
    # The file is found in profiles/default.

    if context.readDataFile('quintagroup.plonecomments_uninstall.txt') is None:
        return

    # Add additional setup code here

    portal = context.getSite()
    logger = context.getLogger(LOGGER)

    portal_conf=getToolByName(context.getSite(),'portal_controlpanel')
    portal_conf.unregisterConfiglet('prefs_comments_setup_form')
    logger.info('Unregister configlet prefs_comments_setup_form. ')
