========================================================
Basic: Customize The Logo And CSS From The Default Theme
========================================================

In this section you will:

* Use the Site control panel to add a custom logo
* Customize the look of a Plone site by adjusting Less Variables
* Add a custom toolbar logo

Topics covered:

* The "Site" control panel
* The "Resource Registries" Control Panel
* Resource Registries > Development Mode

Customize Logo
--------------

#. Go to the Plone Control Panel: :menuselection:`toolbar --> admin --> Site Setup`
#. Go to the "Site" control panel.
#. You will see this form:

   .. image:: https://docs.plone.org/_images/change-logo-in-site-control-panel.png

#. You can now add/edit/remove your custom logo.

For more information, take a look at the `official docs <https://docs.plone.org/adapt-and-extend/change-the-logo.html>`_.


Customize CSS/Less Variables
----------------------------

#. Go back to the Control Panel.
#. Go to the :guilabel:`Resource Registries` control panel.
#. On the first tab: enable :guilabel:`Development Mode`.
#. In the "plone" bundle below, click on "develop CSS".

Your panel should now look like this:

.. image:: ../theming/_static/theming-dev_mode_on.png
   :align: center


Now we can play with some Less variables:

#. Go to the :guilabel:`Less Variables` tab.
#. Find the variable ``plone-left-toolbar-expanded`` and set it to 400px.

   .. image:: ../theming/_static/theming-less_var_hack.png
      :align: center

#. Hit the :guilabel:`Save` button in the upper right and reload the page.
#. Click on the toolbar logo to expand the toolbar: voilá!

You can play around with some other variables, if you want.

..  Warning::

    "Development Mode" is really expensive for the browser.
    Depending on the browser and on the system, you might encounter extreme slowness while rendering the page.
    You could see an unthemed page for a while.
    Remember to switch it off as soon as you finished tweaking.
