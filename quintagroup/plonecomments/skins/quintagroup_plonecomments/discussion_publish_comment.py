## Script (Python) "discussion_publish_comment"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=obj=None
##title=
##
from Products.CMFPlone.utils import transaction_note
from Products.CMFCore.utils import getToolByName
from quintagroup.plonecomments.utils import publishDiscussion, manage_mails
from Products.CMFPlone import MessageFactory
_ = MessageFactory('quintagroup.plonecomments')

if obj is None:
    obj = context

parent = obj.inReplyTo()
if parent is not None:
    dtool = getToolByName(context, 'portal_discussion')
    talkback = dtool.getDiscussionFor(parent)
else:
    talkback = parent = obj.aq_parent

reply = talkback.getReply(obj.getId())
publishDiscussion(reply)
manage_mails(reply, context, action='publishing')

putils = getToolByName(context, 'plone_utils')
redirect_target = putils.getDiscussionThread(talkback)[0]
view = redirect_target.getTypeInfo().getActionInfo('object/view')['url']
rt = redirect_target.absolute_url()

if rt and rt[-1] == '/':
    rt = rt[:-1]

if view and view[0] == '/':
    view = view[1:]

if view and view[-1] == '/':
    view = view[:-1]

anchor = reply.getId()

transaction_note('Published discussion item')

context.plone_utils.addPortalMessage(_(u'Comment published.'))
target = '%s#%s' % (rt, anchor)

return context.REQUEST.RESPONSE.redirect(target)
