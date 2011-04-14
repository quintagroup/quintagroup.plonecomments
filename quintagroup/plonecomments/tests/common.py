#
# Common constants and methods
#
from Products.CMFCore.utils import getToolByName


def addMembers(portal, users_map):
    """ Add all members """
    membership = getToolByName(portal, 'portal_membership', None)
    for user_id in users_map.keys():
        membership.addMember(user_id, users_map[user_id]['passw'],
                             users_map[user_id]['roles'], [],
                             {'email': '%s@test.com' % user_id, })


def add2Group(portal, group, group_members):
    """ Add users to Discussion Manager group """
    pg = getToolByName(portal, 'portal_groups')
    group = pg.getGroupById(group)
    [group.addMember(u) for u in group_members]
