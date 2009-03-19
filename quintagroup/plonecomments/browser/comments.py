import urllib, md5

from Acquisition import aq_inner
from AccessControl import getSecurityManager
from Products.CMFPlone.utils import getToolByName

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.layout.viewlets import comments

class CommentsViewlet(comments.CommentsViewlet):
    """A custom version of the comments viewlet
    """

    render = ViewPageTemplateFile('comments.pt')

    def is_moderation_enabled(self):
        """ Returns a boolean indicating whether the user has enabled moderation
            in the qPloneComments configlet
        """
        portal_properties = getToolByName(self.context, 'portal_properties')
        try:
            return portal_properties.qPloneComments.getProperty('enable_moderation', None)
        except AttributeError:
            return False

    def can_moderate(self):
        """ Returns a boolean indicating whether the user has the 'Moderate Discussion'
            permission
        """
        return getSecurityManager().checkPermission('Moderate Discussion', aq_inner(self.context))

    def getGravatar(self, reply):
        purl = getToolByName(self.context, 'portal_url')
        default = purl() + '/defaultUser.gif' 
        email = ''

        creator = reply.Creator()
        if creator and not creator=='Anonymous User':
            mtool = getToolByName(self.context, "portal_membership")
            member = mtool.getMemberById(creator)
            email = member and member.getProperty('email','') or ''
        else:
            email = reply.getProperty('email',d='')
        if not email:
            return default

        size = 40
        gravatar_url = "http://www.gravatar.com/avatar.php?"
        # construct the url
        gravatar_url += urllib.urlencode({'gravatar_id':md5.md5(email).hexdigest(), 
            'default':default, 'size':str(size)})

        return gravatar_url