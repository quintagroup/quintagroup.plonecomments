============
Introduction
============

Copyright (c) "Quintagroup": http://quintagroup.com, 2004-2009

Plone Comments (quintagroup.plonecomments) is a Plone product developed 
to improve the site managers and editors expirience with standard 
commenting mechanism in Plone.

.. contents::


Features
============

- Notify admin about comment posted

- Notify commentator about his comment aproval

- Notify author of parent comment about new follow up added

- Moderation of comments, approval of comments

- Anonymous commenting

- Added Name field to comment form, it is required for anonymous comments

- Article author can be notified about new comment after the approval by reviewer

- List of recent comments for more comfortable moderation

- Configlet that allow:

  o Turning on/off Moderation

  o Turning on/off Manager notification

  o Turning on/off Editor notification

  o Turning on/off Anonymous Commenting

  o Configure admin e-mail for notifications

  o Configure notification subject

- qPloneCaptcha integrated (needs the qPloneCaptcha to be installed)


Notes
============

Comments moderation is implemented with involvement of two stage workflow.
Comments are created in "private" state and visible only to DiscussionManager
group of users.

To differentiate between logged-in (registered) commentors and Anonymous
commentors that pretend to be one person or other one, we use Boldness of
name. The Comment author is in bold when posted by logged in member. The
names provided when posting Anonymously are in plain text.

Notification subject control allows to enter custom prefix to disctinct
notifications comming from different sites.


Usage
============

One of possible UseCases:

  Moderation is enabled and authors notification is turned on.

    - New comment posted in private state.

    - Notification is sent to the emails entered in Plone Comments configlet.

    - Moderator User with DiscussionManager role see the comment.

    - The comment can be deleted or published on modaration stage.

    - When comment is published notification is sent to Article Editor.


Links
============

- Download releases from Sourceforge.net "Plone Comments project area":http://sf.net/projects/quintagroup

- Get latest development version from "SVN":http://svn.quintagroup.com/products/quintagroup.plonecomments/trunk


Requirements
============

- Plone 3.x

- plone.browserlayer is required for Plone 3.0.x


License
============

Please find license in *LICENSE.GPL*.


Author
============

The product is developed and maintained by http://quintagroup.com team.

  Authors:

    - Volodymyr Cherepanyak

    - Andriy Mylenkyy

    - Mykola Kharechko

    - Vitaliy Stepanov

  Contributors:

    - Gerry Kirk: product translations improvement and proofreading

    - Dorneles Tremea: code cleanup and generic setup porting
