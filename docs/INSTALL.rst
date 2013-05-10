Installation
============

If you are using zc.buildout and the plone.recipe.zope2instance
recipe to manage your project, you can do this:

* Add ``quintagroup.plonecomments`` to the list of eggs to install, e.g.::

    [buildout]
    ...
    eggs =
        ...
        quintagroup.plonecomments
       
* Tell the plone.recipe.zope2instance recipe to install a ZCML slug::

    [instance]
    recipe = plone.recipe.zope2instance
    ...
    zcml =
        quintagroup.plonecomments
        quintagroup.plonecomments-overrides
      
* Re-run buildout, e.g. with::

    $ ./bin/buildout

* Restart the Zope server, for example, with the following command in the terminal::

    $ ./bin/instance restart

* Install quintagroup.plonecomments via ZMI portal_setup. Select ``quintagroup.plonecomments``
  from the list of available profiles and press *Import all steps*.


  **Atention**: If you are using a Plone version **before** 3.1 you need to install
  "plone.browserlayer":http://pypi.python.org/pypi/plone.browserlayer (which also
  requires a "GenericSetup":http://pypi.python.org/pypi/Products.GenericSetup version
  greater than 1.4) in your Plone site. It shows up as **Local browser layer support**
  in the Plone Add-on Products Control Panel.


Uninstallation
==============

* To uninstall quintagroup.plonecomments - select ``quintagroup.plonecomments uninstall``
  profile from the list of available profiles and press *Import all steps*.
