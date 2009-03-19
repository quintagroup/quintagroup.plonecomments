## Controller Script Python "validate_setup"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind state=state  
##bind subpath=traverse_subpath
##parameters=
##title=validates qpc setup
##
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone import MessageFactory
from Products.CMFPlone import PloneMessageFactory
_ = MessageFactory("quintagroup.plonecomments")

form = context.REQUEST.form
email_key = 'email_discussion_manager'

if email_key in form:
    email = form[email_key] 
    pu = getToolByName(context, 'plone_utils')
    if not pu.validateEmailAddresses(email):
        state.setError(email_key, _(u'Please submit a valid e-mail address.'))

if state.getErrors():
    return state.set(status='failure', portal_status_message=PloneMessageFactory(u'Please correct the indicated errors.'))
else:
    return state

