## Script (Python) "deleteDiscussion"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=obj=None
##title=Delete discussion item
##

from quintagroup.plonecomments.utils import manage_mails
from Products.CMFPlone import PloneMessageFactory

if obj is None:
    obj = context

parent = obj.inReplyTo()
if parent is not None:
    talkback = context.portal_discussion.getDiscussionFor(parent)
else:
    talkback = parent = obj.aq_parent

# remove the discussion item
talkback.deleteReply(obj.getId())
manage_mails(obj, context, 'deleting')

# redirect to the object that is being discussed
redirect_target = context.plone_utils.getDiscussionThread(talkback)[0]
view = redirect_target.getTypeInfo().immediate_view

context.plone_utils.addPortalMessage(PloneMessageFactory(u'Reply deleted.'))

context.REQUEST['RESPONSE'].redirect(redirect_target.absolute_url() +
                                     '/%s' % view)
