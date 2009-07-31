## Script (Python) "report_abuse"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind state=state
##bind subpath=traverse_subpath
##parameters=message,text_format='plain',username=None,password=None
##title=Reply to content

from Products.PythonScripts.standard import url_quote_plus
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone import MessageFactory
from Products.CMFPlone import PloneMessageFactory
from quintagroup.plonecomments.utils import manage_mails

_ = MessageFactory('quintagroup.plonecomments')

req = context.REQUEST
mtool = getToolByName(context, 'portal_membership')
dtool = getToolByName(context, 'portal_discussion')
pp = getToolByName(context,'portal_properties')

isForAnonymous = pp['qPloneComments'].getProperty('enable_anonymous_report_abuse', False)

if username or password:
    # The user username/password inputs on on the comment form were used,
    # which might happen when anonymous commenting is enabled. If they typed
    # something in to either of the inputs, we send them to 'logged_in'.
    # 'logged_in' will redirect them back to this script if authentication
    # succeeds with a query string which will post the message appropriately
    # and show them the result.  if 'logged_in' fails, the user will be
    # presented with the stock login failure page.  This all depends
    # heavily on cookiecrumbler, but I believe that is a Plone requirement.
    came_from = '%s?subject=%s&amp;body_text=%s' % (req['URL'], subject, body_text)
    came_from = url_quote_plus(came_from)
    portal_url = context.portal_url()

    return req.RESPONSE.redirect(
        '%s/logged_in?__ac_name=%s'
        '&amp;__ac_password=%s'
        '&amp;came_from=%s' % (portal_url,
                               url_quote_plus(username),
                               url_quote_plus(password),
                               came_from,
                               )
        )

comment_creator = req.get('Creator', None)
if isForAnonymous and comment_creator:
    # Get entered anonymous name
    comment_creator = comment_creator
else:
    member = mtool.getAuthenticatedMember()
    comment_creator = member.getUserName()

if mtool.isAnonymousUser():
    email = req.get('email', '')
else:
    email = mtool.getAuthenticatedMember().getProperty('email')

tb = dtool.getDiscussionFor(context)

# Send notification e-mail
manage_mails(context, context, 'report_abuse')

# return to the discussable object.
redirect_target = context.plone_utils.getDiscussionThread(tb)[0]
view = redirect_target.getTypeInfo().getActionInfo('object/view',
                                                   redirect_target)['url']

portal_status_message=_(u'Your abuse report has been sent.')
context.plone_utils.addPortalMessage(portal_status_message)
target = '%s' % view
return req.RESPONSE.redirect(target)

