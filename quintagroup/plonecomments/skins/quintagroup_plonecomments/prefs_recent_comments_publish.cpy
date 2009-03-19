## Script (Python) "prefs_recent_comments_publish"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=
##
from Products.CMFCore.utils import getToolByName
from quintagroup.plonecomments.utils import publishDiscussion, manage_mails, setStatusMsg
from Products.CMFPlone import MessageFactory
_ = MessageFactory('quintagroup.plonecomments')

request = context.REQUEST

comment_ids = request.get('ids', [])
portal_catalog = getToolByName(context, "portal_catalog")

for comment_id in comment_ids:
    comment = portal_catalog(id=comment_id,portal_type='Discussion Item')[0].getObject()
    publishDiscussion(comment)
    manage_mails(comment, container, action='publishing')

msg = comment_ids and _(u'Comment(s) published.') or _(u'Please select items to be processed.')
setStatusMsg(state, context, msg)

return state
