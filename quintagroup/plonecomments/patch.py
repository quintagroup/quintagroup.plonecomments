from DateTime import DateTime
try:
    from App.class_init import InitializeClass
    InitializeClass
except ImportError:
    from Globals import InitializeClass
from AccessControl import Unauthorized
from AccessControl import getSecurityManager
from Products.CMFCore.utils import getToolByName
from Products.CMFDefault.DiscussionItem import DiscussionItem
from Products.CMFDefault.DiscussionItem import DiscussionItemContainer
from quintagroup.plonecomments.utils import getProp


def createReply(self, title, text, Creator=None, email=''):
    """Create a reply in the proper place.
    """
    container = self._container

    id = int(DateTime().timeTime())
    while container.get(str(id), None) is not None:
        id += 1
    id = str(id)

    item = DiscussionItem(id, title=title, description=title)

    if Creator:
        if getattr(item, 'addCreator', None) is not None:
            item.addCreator(Creator)
        else:
            item.creator = Creator

    container[id] = item
    item = item.__of__(self)

    item.setFormat('structured-text')
    item._edit(text)

    pm = getToolByName(self, 'portal_membership')
    if pm.isAnonymousUser():
        item.manage_addProperty(id='email', value=email, type='string')

    item.review_state = 'private'

    # Control of performing moderation
    if getProp(self, 'enable_moderation', marker=False):
        md_roles = self.acl_users.rolesOfPermission('Moderate Discussion')
        roles = [role['name']
                 for role in md_roles
                 if role['selected'] == 'SELECTED']
        roles.append('DiscussionManager')
        item.manage_permission('Delete objects', roles, acquire=1)
        item.manage_permission('View', roles, acquire=0)
    else:
        item.review_state = 'published'

    item.setReplyTo(self._getDiscussable())
    item.indexObject()

    return id


def getReplies(self):
    """Return a sequence of the DiscussionResponse objects which are
       associated with this Discussable.
    """
    objects = []
    validate = getSecurityManager().validate

    result_ids = self._getReplyResults()
    for id in result_ids:
        comment = self._container.get(id).__of__(self)
        try:
            if validate(self, self, id, comment):
                objects.append(comment)
        except Unauthorized:
            pass
    return objects


perms = DiscussionItemContainer.__ac_permissions__
new_perms = []
for perm in perms:
    perm_name = perm[0]
    funcs = perm[1]
    if 'deleteReply' in funcs:
        new_perms.append((perm_name, [f for f in funcs if f != 'deleteReply']))
        new_perms.append(('Moderate Discussion', ('deleteReply',)))
    else:
        new_perms.append(perm)

DiscussionItemContainer.__ac_permissions__ = new_perms
InitializeClass(DiscussionItemContainer)

DiscussionItemContainer.createReply = createReply
DiscussionItemContainer.getReplies = getReplies
