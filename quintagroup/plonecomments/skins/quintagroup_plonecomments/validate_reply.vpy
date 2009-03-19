## Controller Script Python "validate_reply"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind state=state  
##bind subpath=traverse_subpath
##parameters=
##title=validates discussion_reply
from Products.CMFPlone import MessageFactory
_ = MessageFactory('quintagroup.plonecomments')

if hasattr(context, 'review_state') and not context.review_state=="published":
    msg = _(u'Reply not allowed because the response is to a comment waiting to be\
 approved. Please wait for the comment to be approved before replying.')

    state.set(status='failure', portal_status_message=msg)
    return state.set(status='failure')

return state