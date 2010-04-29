import urllib
try:
    import hashlib as md5
except ImportError:
    import md5

from Acquisition import aq_inner
from AccessControl import getSecurityManager
from Products.CMFPlone.utils import IndexIterator
from Products.CMFPlone.utils import getToolByName
from Products.CMFFormController.ControllerState import ControllerState
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from quintagroup.plonecomments.utils import manage_mails
from plone.app.layout.viewlets import comments


class CommentsViewlet(comments.CommentsViewlet):
    """A custom version of the comments viewlet
    """
    render = ViewPageTemplateFile('comments.pt')

    def is_moderation_enabled(self):
        """ Returns a boolean indicating whether the user has enabled
            moderation in the qPloneComments configlet
        """
        portal_properties = getToolByName(self.context, 'portal_properties')
        try:
            return portal_properties.qPloneComments.getProperty(
                'enable_moderation', None)
        except AttributeError:
            return False

    def can_moderate(self):
        """ Returns a boolean indicating whether the user has the
            'Moderate Discussion' permission
        """
        return getSecurityManager().checkPermission('Moderate Discussion',
                                                    aq_inner(self.context))

    def getGravatar(self, reply):
        purl = getToolByName(self.context, 'portal_url')
        mtool = getToolByName(self.context, 'portal_membership')
        portrait_url = purl() + '/defaultUser.gif'
        email = ''

        creator = reply.Creator()
        if creator and not creator == 'Anonymous User':
            mtool = getToolByName(self.context, "portal_membership")
            member = mtool.getMemberById(creator)
            email = member and member.getProperty('email', '') or ''
            mem_id = getattr(member, 'getId', lambda: 'Anonymous User')()
            portrait = mtool.getPersonalPortrait(mem_id)
            portrait_url = portrait.absolute_url()
        else:
            email = reply.getProperty('email', d='')

        if not email or not 'defaultUser.gif' in portrait_url:
            return portrait_url

        size = 40
        gravatar_url = "http://www.gravatar.com/avatar.php?"
        # construct the url
        gravatar_url += urllib.urlencode({
            'gravatar_id': md5.md5(email).hexdigest(),
            'default': portrait_url,
            'size': str(size)})
        return gravatar_url

    def authenticated_report_abuse_enabled(self):
        """ """
        portal_properties = getToolByName(self.context, 'portal_properties')
        prop_sheet = portal_properties['qPloneComments']
        value = prop_sheet.getProperty('enable_authenticated_report_abuse',
                                       False)
        return value

    def anonymous_report_abuse_enabled(self):
        """ """
        portal_properties = getToolByName(self.context, 'portal_properties')
        prop_sheet = portal_properties['qPloneComments']
        value = prop_sheet.getProperty('enable_anonymous_report_abuse', False)
        return value

    def visual_effects_level(self):
        """ """
        portal_properties = getToolByName(self.context, 'portal_properties')
        prop_sheet = portal_properties['qPloneComments']
        value = prop_sheet.getProperty('visual_effects', 0)
        return value

    def email_from_address(self):
        """ """
        portal_url = getToolByName(self.context, 'portal_url')
        portal = portal_url.getPortalObject()
        return portal.email_from_address

    def member(self):
        """ """
        pm = getToolByName(self.context, 'portal_membership')
        return pm.getAuthenticatedMember()

    def tabindex(self):
        """ Needed for BBB, tabindex has been deprecated.
        """
        return IndexIterator()

    def portal_url(self):
        """ """
        return getToolByName(self.context, 'portal_url')
