================================================
Basic: Customizing logo and CSS of default theme
================================================

In this section you will:

* Use the Site control panel to add a custom logo
* Customize the look of a Plone site by adjusting Less Variables
* Add a custom toolbar logo

Topics covered:

* The "Site" control panel
* The "Resource Registries" Control Panel
* Resource Registries > Development Mode

Customize logo
--------------

1. Go to the Plone Control Panel: :menuselection:`toolbar --> admin --> Site Setup`
2. Go to the "Site" control panel.
3. You will see this form:

   .. image:: http://docs.plone.org/_images/change-logo-in-site-control-panel.png

4. You can now add / remove your custom logo

See the `official docs <plone:change-the-logo>`_.


Customize CSS/Less variables
----------------------------

1. Go back to the Control Panel.
2. Go to the :guilabel:`Resource Registries` control panel.
3. On the first tab: enable :guilabel:`Development Mode`.
4. In the "plone" bundle below, click on "develop CSS".

Your panel should now look like this:

.. image:: ../theming/_static/theming-dev_mode_on.png
   :align: center


Now we can play with some Less variables:

1. Go to the :guilabel:`Less Variables` tab.
2. Find the variable ``plone-left-toolbar-expanded`` and set it to 400px.

.. image:: ../theming/_static/theming-less_var_hack.png
   :align: center


3. Hit the :guilabel:`Save` button in the upper right and reload the page.
4. Click on the toolbar logo to expand the toolbar: voilá!

You can play around with some other variables, if you want.

..  Warning::

    "Development Mode" is really expensive for the browser.
    Depending on the browser and on the system, you might encounter extreme slowness while rendering the page.
    You could see an unthemed page for a while.
    Remember to switch it off as soon as you finished tweaking.
