import smtplib
from Products.CMFPlone import MessageFactory
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone import PloneMessageFactory as _
from config import warning

# Get apropriate property from (propery_sheeet) configlet
def getProp(self, prop_name, marker=None):
    result = marker
    pp = getToolByName(self, 'portal_properties')
    config_ps = getattr(pp, 'qPloneComments', None)
    if config_ps:
        result =  getattr(config_ps, prop_name, marker)
    return result

def publishDiscussion(self):
    roles = ['Anonymous']
    self.review_state = "published"
    self.manage_permission('View', roles, acquire=1)
    self._p_changed = 1
    self.reindexObject()

def setAnonymCommenting(context, allow=False):
    portal = getToolByName(context, 'portal_url').getPortalObject()
    if allow:
        portal.manage_permission('Reply to item', ['Anonymous','Manager','Member'], 1)
    else:
        portal.manage_permission('Reply to item', ['Manager','Member'], 1)

def manage_mails(reply, context, action):
    def sendMails(props, actions, key):
        for p in props:
            if p in actions[key]:
                send_email(reply, context, p)

    prop_sheet = context.portal_properties['qPloneComments']
    props = filter(lambda x: prop_sheet.getProperty(x), prop_sheet.propertyIds())

    actions = { 'onPublish': ('enable_approve_user_notification',
                              'enable_reply_user_notification',
                              'enable_published_notification'),
                'onDelete' :  ('enable_rejected_user_notification',),
                'onApprove': ('enable_approve_notification',),
                'onAnonymousReportAbuse': ('enable_anonymous_report_abuse',),
                'onAuthenticatedReportAbuse': ('enable_authenticated_report_abuse')}

    if action == 'publishing':
        sendMails(props, actions, 'onPublish')

    elif action == 'deleting':
        sendMails(props, actions, 'onDelete')

    elif action == 'aproving':
        sendMails(props, actions, 'onApprove')

    elif action == 'report_abuse':
        pm = getToolByName(context, 'portal_membership')
        if pm.isAnonymousUser():
            sendMails(props, actions, 'onAnonymousReportAbuse')
        else:
            sendMails(props, actions, 'onAuthenticatedReportAbuse')

def getMsg(context, template, args):
    return getattr(context, template)(**args)

def allowEmail(context, reply, state, creator):
    condition = getattr(context, 'emailCommentNotification', True)
    if callable(condition):
        condition = condition(reply=reply, state=state, creator=creator)
    return condition

def send_email(reply, context, state):
    def getEmail(obj, context):
        email = obj.getProperty('email', None)
        if email is None:
            creators = hasattr(obj, 'listCreators') and obj.listCreators() or [obj.Creator(),]
            userid = creators and creators[0] or ""
            creator = getToolByName(context, 'portal_membership').getMemberById(userid)
            if creator and allowEmail(context, reply, state, creator):
                return creator.getProperty('email', '')
        else:
            return email
        return ''

    def getParent(reply):
        if reply.meta_type == 'Discussion Item':
            reply = reply.inReplyTo()
            return getParent(reply)
        return reply

    def getDIParent(reply):
        r = reply.inReplyTo()
        return r.meta_type == 'Discussion Item' and r or None

    def getParentOwnerEmail(reply, context):
        creator_id = getParent(reply).getOwnerTuple()[1]
        creator = getToolByName(context, 'portal_membership').getMemberById(creator_id)
        if creator and allowEmail(context, reply, state, creator):
            return creator.getProperty('email', '')
        return ''

    args = {}
    if reply:
        user_email = getEmail(reply, context)
        reply_parent = getParent(reply)

    organization_name = getProp(context, 'email_subject_prefix', '')
    creator_name = reply.getOwnerTuple()[1]
    admin_email = context.portal_url.getPortalObject().getProperty('email_from_address')

    subject = ''
    if state == 'enable_approve_user_notification':
        subject = 'Your comment on %s is now published' % getParent(context).Title()
        if user_email:
            template = 'notify_comment_template'
            args={'mto': user_email,
                  'mfrom': admin_email,
                  'obj': reply_parent,
                  'organization_name': organization_name,
                  'name': creator_name}
        else:
            args = {}

    elif state == 'enable_rejected_user_notification':
        subject = 'Your comment on %s was not approved' % getParent(context).Title()
        if user_email:
            template = 'rejected_comment_template'
            args={'mto': user_email,
                  'mfrom': admin_email,
                  'obj': reply_parent,
                  'organization_name': organization_name,
                  'name': creator_name}
        else:
            args = {}

    elif state == 'enable_reply_user_notification':
        template = 'reply_notify_template'
        subject = 'Someone replied to your comment on %s' % getParent(context).Title()
        di_parrent = getDIParent(reply)
        if di_parrent:
            user_email = getEmail(di_parrent, context)
            if user_email:
                args={'mto': user_email,
                      'mfrom': admin_email,
                      'obj': reply_parent,
                      'organization_name': organization_name,
                      'name': di_parrent.getOwnerTuple()[1]}
            else:
                args = {}
        else:
            args = {}

    elif state == 'enable_published_notification':
        template = 'published_comment_template'
        user_email = getParentOwnerEmail(reply, context)
        if user_email:
            args={'mto':user_email,
                  'mfrom':admin_email,
                  'obj':reply_parent,
                  'organization_name':organization_name}
            subject = '[%s] New comment added' % organization_name
        else:
            args = {}

    elif state == 'enable_approve_notification':
        template = 'approve_comment_template'
        user_email = getProp(context, "email_discussion_manager", None)
        if user_email:
            args={'mto':user_email,
                  'mfrom':admin_email,
                  'obj':reply_parent,
                  'organization_name':organization_name}
            subject = '[%s] New comment awaits moderation' % organization_name
        else:
            args = {}

    elif state in ('enable_authenticated_report_abuse', 'enable_anonymous_report_abuse'):
        template = 'report_abuse_template'
        user_email = getProp(context, "email_discussion_manager", None)
        if user_email:
            message = context.REQUEST.get('message')
            comment_id = context.REQUEST.get('comment_id')
            pd = context.portal_discussion
            dl = pd.getDiscussionFor(context)
            comment = dl._container.get(comment_id)
            args = {'mto': user_email,
                    'mfrom': admin_email,
                    'obj': reply_parent,
                    'message':message,
                    'organization_name': organization_name,
                    'name': creator_name,
                    'comment_id':comment_id,
                    'comment_desc':comment.description,
                    'comment_text':comment.text
                    }
            subject = '[%s] A comment on "%s" has been reported for abuse.' \
                            % (organization_name, getParent(context).Title())
        else:
            args = {}

    if args:
        msg = getMsg(context, template, args)
        p_utils = context.plone_utils
        site_props = context.portal_properties.site_properties
        host = p_utils.getMailHost()
        try:
            host.secureSend(msg, user_email, admin_email,
                            subject = subject,
                            subtype = 'plain',
                            debug = False,
                            charset = site_props.getProperty('default_charset', 'utf-8'),
                            From = admin_email)
        except smtplib.SMTPRecipientsRefused:
            log.error(_('SMTPRecipientsRefused: Could not send the email'
            'notification. Have you configured an email server for Plone?'))

def setStatusMsg(state, context, msg):
    context.plone_utils.addPortalMessage(msg)
