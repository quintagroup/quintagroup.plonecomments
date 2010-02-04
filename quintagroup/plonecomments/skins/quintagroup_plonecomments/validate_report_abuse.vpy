## Controller Script Python "validate_talkback"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind state=state
##bind subpath=traverse_subpath
##parameters=message='', email='', require_email=False, comment_id=None
##title=validates a discussion entry
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone import MessageFactory
from Products.CMFPlone import PloneMessageFactory
_ = MessageFactory('quintagroup.plonecomments')

try:
    content = context.parentsInThread()[0]
except AttributeError:
    content = context

pm = getToolByName(context, 'portal_membership')
pp = getToolByName(context, 'portal_properties')
if pm.isAnonymousUser():
    if not pp.qPloneComments.getProperty('enable_anonymous_report_abuse'):
        raise Exception, "Abuse Report not allowed."
else:
    if not pp.qPloneComments.getProperty('enable_authenticated_report_abuse'):
        raise Exception, "Abuse Report not allowed."

if not message:
    state.setError('message', PloneMessageFactory(u'Please submit a message.'), 'message_required')

if require_email:
    if not email:
        state.setError('email', _(u'Please submit an email address.'), 'email_required')
    elif not context.portal_registration.isValidEmail(email):
        state.setError('email', _(u'Please submit a valid e-mail address.'), 'email_required')

if hasattr(context, 'captcha_validator'):
    context.captcha_validator()

isForAnonymous = pp['qPloneComments'].getProperty('enable_anonymous_commenting', None)
if isForAnonymous:
    pm = getToolByName(context, 'portal_membership')
    isAnonym = pm.isAnonymousUser()
    if isAnonym:
        req = context.REQUEST
        if not (req.form.has_key('creator') and not req.form['creator'] == ""):
            state.setError('creator', _(u'Please enter your name.'), 'name_required')

        try:
            captcha_view = context.restrictedTraverse('@@captcha')
            if not captcha_view.verify(captcha):
                state.setError('captcha', _(u'You must correctly enter the word.'), 'captcha')
        except:
            # no collective.captcha installed
            pass

if state.getErrors():
    context.plone_utils.addPortalMessage(_(u'Please correct the indicated errors.'))
    return state.set(status='failure')
else:
    return state
