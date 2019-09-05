.. _plone5-label:

What's New in Plone 5, 5.1 and Plone 5.2
========================================

Plone 5.0 was released in September 2015. Plone 5 was a mayor release, that changed the content type framework, the user interface and the default design.

Plone 5.1 was released in Oktober 2017 and holds a couple of smaller improvements.

Plone 5.2 was released in March 2019. Plone 5.2 is the first version that supports Python 3. It also has some improvements like a new drop-down navigation and built-in url-management.

If you are already familiar with Plone 5.0, 5.1 and 5.2 you can skip this section.


.. _plone5-theme-label:

Default Theme
-------------

The default theme of Plone 5.x is called `Barceloneta <https://github.com/plone/plonetheme.barceloneta/>`_

It is a Diazo theme, meaning it uses :py:mod:`plone.app.theming` to insert the output of Plone into static html/css.

It uses html5, so it uses ``<header>``, ``<nav>``, ``<aside>``, ``<section>``, ``<article>`` and ``<footer>`` for semantic html.

The theme is mostly built with `LESS <http://lesscss.org/>`_ (lots of it!)
and uses the same grid system as `Bootstrap <https://getbootstrap.com/css/#grid>`_.
This means you can use CSS classes like ``col-xs-12 col-sm-9`` to control the width of elements for different screen sizes.
If you prefer a different grid system (like `Foundation <https://foundation.zurb.com/sites/docs/grid.html>`_) over Bootstrap you can adapt the theme to use that.

The `index.html <https://github.com/plone/plonetheme.barceloneta/blob/master/plonetheme/barceloneta/theme/index.html>`_ and `rules.xml <https://github.com/plone/plonetheme.barceloneta/blob/master/plonetheme/barceloneta/theme/rules.xml>`_ are the main elements to make this happen.

.. _plone5-ui-widgets-label:

New UI and widgets
------------------

While Plone 4 had a green edit-bar above the content Plone 5 has a toolbar that is located on the left or top and can be expanded. The design of the toolbar is pretty isolated from the theme and it should not break if you use a different theme.

The widgets where you input data are also completely rewritten.

* Plone now uses the newest TinyMCE
* The tags (keywords) widget and the widgets where you input usernames use `select2 <http://select2.github.io>`_ autocomplete to give a better user experience
* The related-items widget is a complete rewrite


.. _plone5-foldercontents-label:

Folder Contents
---------------

The view to display the content of a folder is new and offers many new features compared to Plone 4:

* configurable table columns
* changing properties of multiple items at once
* querying (useful for folders with a lot of content)
* persistent selection of items


.. _plone5-content-types-label:

Content Types
-------------

While Plone 4 used Archetypes all default types are based on Dexterity in Plone 5. This means you can use behaviors to change their features and edit them through the web. Existing old content can be migrated to these types.


.. _plone5-resource-registry-label:

Resource Registry
-----------------

The resource registry allows you to configure and edit the static resources (js, css) of Plone. It replaces the old javascript and css registries. And it can be used to customize the theme by changing the variables used by LESS or overriding LESS files.


.. _plone5-chameleon-label:

Chameleon template engine
-------------------------

`Chameleon <https://chameleon.readthedocs.io/en/latest/>`_ is the new rendering engine of Plone 5. It offers many improvements:

Old syntax:

.. code-block:: html

    <h1 tal:attributes="title view/title"
        tal:content="view/page_name">
    </h1>

New (additional) syntax:

.. code-block:: html

    <h1 title="${view/title}">
        ${view/page_name}
    </h1>

Template debugging:

You can now put a full-grown ``pdb`` in a template.

.. code-block:: html

    <?python import pdb; pdb.set_trace() ?>

For debugging check out the variable :py:obj:`econtext`, it holds all the current elements.

You can also add real Python blocks inside templates.

.. code-block:: html

    <?python

    from plone import api

    catalog = api.portal.get_tool('portal_catalog')
    results = []
    for brain in catalog(portal_type='Folder'):
        results.append(brain.getURL())

    ?>

    <ul>
        <li tal:repeat="result results">
          ${result}
        </li>
    </ul>

Don't overdo it!


.. _plone5-control-panel-label:

Control panel
-------------

* You can finally upload a logo in ``@@site-controlpanel``.
* All control panels were moved to z3c.form
* Many small improvements


.. _plone5-dateformatting-label:

Date formatting on the client side
----------------------------------

Using the js library moment.js the formatting of dates was moved to the client.

.. code-block:: html

    <ul class="pat-moment"
        data-pat-moment="selector:li;format:calendar;">
        <li>${python:context.created().ISO()}</li>
        <li>2015-10-22T12:10:00-05:00</li>
    </ul>

returns

    * Today at 3:24 PM
    * 10/22/2015


.. _plone5-multilingual-label:

plone.app.multilingual
----------------------

`plone.app.multilingual <https://github.com/plone/plone.app.multilingual>`_ is the new default add-on for sites in more than one language.


.. _plone5-portletmanager-label:

New portlet manager
-------------------

``plone.footerportlets`` is a new place to put portlets. The footer (holding the footer, site_actions, colophon) is now built from portlets. This means you can edit the footer TTW.

There is also a useful new portlet type :guilabel:`Actions` used for displaying the site_actions.


.. _plone5-skins-label:

Remove portal_skins
-------------------

Many of the old skin templates were replaced by real browser views.


Plone 5.1
---------

Plone 5.1 comes with many incremental improvements. None of these changes the way you develop for Plone. Here are three noteworthy changes:

* The operations for indexing, reindexing and unindexing are queued, optimized and only processed at the end of the transaction. This change can have big performance benefits.

* Actions now have a user-interface in the Plone control panel. You no longer need to use the ZMI to manage them by hand.

* "Retina" Image scales: Plone now has scales for high pixel density images.

For a complete list of changes see https://docs.plone.org/manage/upgrading/version_specific_migration/upgrade_to_51.html#changes-between-plone-5-0-and-5-1


Plone 5.2
---------

Plone 5.2 supports Python 2.7, 3.6 and 3.7. It is based on Zope 4.0 and runs WSGI. These three changes resulted in mayor changes under the hood but have only limited effect on end-users. Plone 5.2 also comes with a ton if bugfixes and a couple of nice improvement. Here are some noteworthy changes:

* New navigation with dropdown. Site-Administrators can use the navigation control panel ``/@@navigation-controlpanel`` to configure the dropdown-navigation.

* Merge Products.RedirectionTool into core. Site-Administrators can use the :guilabel:`URL Management` control panel (`/@@redirection-controlpanel`) to manage and add alternative URLs including bulk upload of alternative urls. As an Editor, you can see the :guilabel:`URL Management` link in the :guilabel:`actions` menu of a content item, and add or remove alternative URLs for this specific content item.

* Plone 5.2 ships with plone.restapi

* New Login. The ols skin-templates and skin-scipts were replace by browser-views that are much easier to customize.

For the complete list of changes see https://github.com/plone/documentation/blob/5.2/manage/upgrading/version_specific_migration/upgrade_to_52.rst
