import urllib
try:
    import hashlib as md5
    md5.md5
except ImportError:
    import md5

from Acquisition import aq_inner
from AccessControl import getSecurityManager

from Products.CMFPlone.utils import getToolByName
from Products.CMFFormController.ControllerState import ControllerState
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from quintagroup.plonecomments.utils import manage_mails

from plone.app.layout.viewlets import comments
from plone.app.kss.plonekssview import PloneKSSView


class CommentsViewlet(comments.CommentsViewlet):
    """A custom version of the comments viewlet
    """
    render = ViewPageTemplateFile('comments.pt')

    def __init__(self, *args):
        super(CommentsViewlet, self).__init__(*args)
        if hasattr(self, 'login_url') and not hasattr(self, 'login_action'):
            # In plone 4.0 in plone.app.layout.viewlets.comments function
            # login_ action was renamed to login_url
            self.login_action = self.login_url

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
        """ Returns a boolean indicating whether the user has
            the 'Moderate Discussion' permission
        """
        return getSecurityManager().checkPermission('Moderate Discussion',
                                                    aq_inner(self.context))

    def getGravatar(self, reply):
        """ """
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

    def ajax_report_abuse_enabled(self):
        """ """
        portal_properties = getToolByName(self.context, 'portal_properties')
        prop_sheet = portal_properties['qPloneComments']
        value = prop_sheet.getProperty('enable_ajax_report_abuse', False)
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

    def portal_url(self):
        """ """
        return getToolByName(self.context, 'portal_url')


class CommentsKSS(PloneKSSView):
    """ Operations on the report abuse form using KSS.
    """

    def submit_abuse_report(self):
        """ Send an email with the abuse report message and
            hide abuse report form.
        """
        errors = {}
        context = aq_inner(self.context)
        request = context.REQUEST
        portal = getToolByName(self.context, 'portal_url').getPortalObject()
        if hasattr(context, 'captcha_validator'):
            dummy_controller_state = ControllerState(
                id='comments.pt',
                context=context,
                button='submit',
                status='success',
                errors={},
                next_action=None,)
            # get the form controller
            controller = portal.portal_form_controller
            # send the validate script to the form controller
            # with the dummy state object
            controller_state = controller.validate(dummy_controller_state,
                                                   request, ['captcha_validator', ])
            errors.update(controller_state.errors)

        message = request.get('message')
        if not message:
            errors.update({'message': 'Please provide a message'})

        mtool = getToolByName(self.context, "portal_membership")
        member = mtool.getAuthenticatedMember()
        comment_id = self.context.request.get('comment_id')
        ksscore = self.getCommandSet('core')
        if errors:
            html = self.macroContent('context/report_abuse_form/macros/form',
                                     errors=errors,
                                     show_form=True,
                                     member=member,
                                     **request.form)
            node = ksscore.getHtmlIdSelector('span-reply-form-holder-%s' %
                                             comment_id)
            ksscore.replaceInnerHTML(node, html)
            return self.render()

        # report_abuse(context, context, message, comment)
        manage_mails(context, self.context, 'report_abuse')

        html = self.macroContent('context/report_abuse_form/macros/form',
                                 member=member,
                                 **request.form)
        node = ksscore.getHtmlIdSelector('span-reply-form-holder-%s' %
                                         comment_id)
        html = '<br/><span style="color:red">' \
            'You have reported this comment for abuse.</span>'
        self.commands.addCommand('remove_abuse_report_form',
                                 node,
                                 comment_id=comment_id,
                                 html=html)

        node = ksscore.getHtmlIdSelector('div-captcha-%s' % comment_id)
        html = self.macroContent('context/report_abuse_form/macros/captcha',
                                 **request.form)
        ksscore.replaceInnerHTML(node, html)
        return self.render()
