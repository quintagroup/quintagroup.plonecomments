PRODUCT = 'quintagroup.plonecomments'
PRODUCT_SKIN_NAME = "quintagroup_plonecomments"
PROPERTY_SHEET = "qPloneComments"
CONFIGLET_ID = "prefs_comments_setup_form"

EMAIL_PID = "email_discussion_manager"
EMAIL_SUBJECT_PID = "email_subject_prefix"
REQUIRE_EMAIL_PID = "require_email"
APPROVE_NOTIFICATION_PID = "enable_approve_notification"
PUBLISHED_NOTIFICATION_PID = "enable_published_notification"
REJECTED_NOTIFICATION_PID = "enable_rejected_user_notification"
APPROVE_USER_NOTIFICATION_PID = "enable_approve_user_notification"
REPLY_USER_NOTIFICATION_PID = "enable_reply_user_notification"
MODERATION_PID = "enable_moderation"
ANONYMOUS_COMMENTING_PID = "enable_anonymous_commenting"

PERM_NAME = 'Moderate Discussion'
USERS = {# Common Members
         'admin':{'passw': 'secret_admin', 'roles': ['Manager']},
         'owner':{'passw': 'secret_owner', 'roles': ['Owner']},
         'member':{'passw': 'secret_member', 'roles': ['Member']},
         'reviewer':{'passw': 'secret_reviewer', 'roles': ['Reviewer']},
         # Members for discussion manager group
         'dm_admin':{'passw': 'secret_dm_admin', 'roles': ['Manager']},
         'dm_owner':{'passw': 'secret_dm_owner', 'roles': ['Owner']},
         'dm_member':{'passw': 'secret_dm_member', 'roles': ['Member']},
         'dm_reviewer':{'passw': 'secret_dm_reviewer', 'roles': ['Reviewer']},
        }
COMMON_USERS_IDS = [u for u in USERS.keys() if not u.startswith('dm_')]
COMMON_USERS_IDS.append('anonym')
DM_USERS_IDS = [u for u in USERS.keys() if u.startswith('dm_')]
