## Script (Python) "discussion_edit"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=subject,body_text
##title=Delete discussion item
##

from Products.PythonScripts.standard import url_quote_plus
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone import PloneMessageFactory as _
dtool = getToolByName(context, 'portal_discussion')
req = context.REQUEST

tb = dtool.getDiscussionFor(context)
id = context.getId()
reply = tb.getReply(id)

modif_date = reply.modification_date

# Set Title
reply.setTitle(subject)

# Update text
reply.edit(text_format=reply.Format(), text=body_text)

# TODO THIS NEEDS TO GO AWAY!
if hasattr(dtool.aq_explicit, 'cookReply'):
    dtool.cookReply(reply, text_format='plain')

# Set modification date to old value
reply.setModificationDate(modification_date=modif_date)

parent = tb.aq_parent

# return to the discussable object.
redirect_target = context.plone_utils.getDiscussionThread(tb)[0]
view = redirect_target.getTypeInfo().getActionInfo('object/view',
                                                   redirect_target)['url']
anchor = reply.getId()

from Products.CMFPlone.utils import transaction_note
transaction_note('Added comment to %s at %s' % (parent.title_or_id(),
                                                reply.absolute_url()))

context.plone_utils.addPortalMessage(_(u'Comment updated.'))
target = '%s#%s' % (view, anchor)
return req.RESPONSE.redirect(target)
