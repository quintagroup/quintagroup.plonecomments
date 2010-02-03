#########################################################
##      Helper methods for testing Mail sending        ##
#########################################################

ALL_PROPS = ['enable_approve_user_notification', 'enable_reply_user_notification',
             'enable_rejected_user_notification','enable_moderation',
             'require_email', 'enable_anonymous_commenting',
             'enable_published_notification', 'enable_approve_notification']

def setProperties(prop_sheet, *props):
    for p in ALL_PROPS:
        prop_sheet._updateProperty(p, p in props)

def testMailExistance(sel):
    mailhost = sel.portal.MailHost
    if mailhost.messages: 
        return True
    return False
