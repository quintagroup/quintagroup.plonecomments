Introduction
============

Plone Comments (quintagroup.plonecomments) is a Plone product developed 
to improve the site managers and editors experience with standard 
commenting mechanism in Plone.

Features
--------

Plone Comments allows to:

* Notify admin about comment posted
* Notify commentator about his comment aproval
* Notify author of parent comment about new follow up added
* Moderation of comments, approval of comments
* Anonymous commenting
* Added Name field to comment form, it is required for anonymous comments
* Article author can be notified about new comment after the approval by reviewer
* List of recent comments for more comfortable moderation

Plone Comments Configlet allows:

* Turning on/off Moderation
* Turning on/off Manager notification
* Turning on/off Editor notification
* Turning on/off Anonymous Commenting
* Configure admin e-mail for notifications
* Configure notification subject

Plone Comments can be integrated with Plone Captchas (requires quintagroup.plonecaptchas to be installed)

Notes
-----

Comments moderation is implemented with involvement of two stage workflow.
Comments are created in "private" state and visible only to DiscussionManager
group of users.

To differentiate between logged-in (registered) commentors and Anonymous
commentors that pretend to be one person or other one, we use Boldness of
name. The Comment author is in bold when posted by logged in member. The
names provided when posting Anonymously are in plain text.

Notification subject control allows to enter custom prefix to distinct
notifications coming from different sites.

Usage
-----

One of possible UseCases:

Moderation is enabled and authors notification is turned on.

- New comment posted in private state.
- Notification is sent to the emails entered in Plone Comments configlet.
- Moderator User with DiscussionManager role see the comment.
- The comment can be deleted or published on modaration stage.
- When comment is published notification is sent to Article Editor.


Links
-----

* Get latest development version from "SVN": http://svn.quintagroup.com/products/quintagroup.plonecomments/trunk

* Watch Plone Comments Screencast http://quintagroup.com/cms/screencasts/plone-comments to learn how to install and set up Plone Comments on your buildout-based Plone instance for Plone 3.2 or above. You will also find one of the possible use cases of using Plone Comments Plone add-on included.

* Watch Plone Comments Use Cases Screencast http://quintagroup.com/cms/screencasts/plone-comments/use-cases to learn about integration of Plone Comments with Plone Captchas, see 2 examples of possible use cases: anonymous and registered users commenting. 

Requirements
------------

* Plone 3.x
* plone.browserlayer is required for Plone 3.0.x

License
-------

Please find license in *LICENSE.GPL*.

Authors
-------

The product is developed and maintained by http://quintagroup.com team.

* Volodymyr Cherepanyak
* Andriy Mylenkyy
* Mykola Kharechko
* Vitaliy Stepanov
* Roman Kozlovskyi

Contributors
------------
 
* Gerry Kirk: product translations improvement and proofreading
* Dorneles Tremea: code cleanup and generic setup porting
* Andreas Stocker: German translation
* Héctor Velarde: Spanish translation
* Benjamin Klups: French translation
* Kees Hink: Dutch translation
* Erico Andrei: Portuguese translation
* Olha Pelishok: Ukraininan translation

