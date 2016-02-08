.. _plone5-label:

What's New in Plone 5
=====================

If you are already used to Plone 5 you could skip this section.


.. _plone5-theme-label:

Default Theme
-------------

The new default theme is called `Barceloneta <https://github.com/plone/plonetheme.barceloneta/>`_

It is a Diazo theme, meaning it uses plone.app.theming to insert the output of Plone into static html/css.

It uses html5, so it uses ``<header>``, ``<nav>``, ``<aside>``, ``<section>``, ``<article>`` and ``<footer>`` for semantic html.

The theme is mostly built with `LESS <http://lesscss.org/>`_ (lots of it!) and uses the same grid system as `bootstrap <http://getbootstrap.com/css/#grid>`_. This means you can use css classes like ``col-xs-12 col-sm-9`` to control the width of elements for different screen-sizes. It is you prefer a different grid-system (like `foundation <http://foundation.zurb.com/docs/components/grid.html>`_) over bootstrap you can adapt the theme to use that.

The `index.html <https://github.com/plone/plonetheme.barceloneta/blob/master/plonetheme/barceloneta/theme/index.html>`_ and `rules.xml <https://github.com/plone/plonetheme.barceloneta/blob/master/plonetheme/barceloneta/theme/rules.xml>`_ are actually not that complicated. Have a look at them.

The following example from the ``rules.xml`` makes sure that the banner saying *"Welcome! Plone 5 rocks!"* is only visible on the frontpage:

.. code-block:: xml

   <!-- include view @@hero on homepage only -->
   <after css:theme="#mainnavigation-wrapper"
          css:content=".principal"
          href="/@@hero"
          css:if-content="body.template-document_view.section-front-page" />

The browser-view ``@@hero`` (you can find it by searching all zcml-files for ``name="hero"``) is only included when the body-tag of the current page has the css-classes ``template-document_view`` and ``section-front-page``.


.. _plone5-ui-widgets-label:

New UI and widgets
------------------

The green edit bar is replaced by a toolbar that is located on the left or top and can be expanded. The design of the toolbar is pretty isolated from the theme and it should not break if you use a different theme.

The widgets where you input data are also completely rewritten.

* We now use the newest TinyMCE
* The tags (keywords) widget and the widgets where you input usenames now use `select2 <http://select2.github.io>`_ autocomplete to give a better user experience
* The related-items widget is a complete rewrite


.. _plone5-foldercontents-label:

Folder Contents
---------------

The view to display the content of a folder is new and offers many new features:

* configurable table columns
* changing properties of multiple items at once
* querying (useful for folders with a lot of content)
* persistent selection of items


.. _plone5-content-types-label:

Content Types
-------------

All default types are based on Dexterity. This means you can use behaviors to change their features and edit them through the web. Existing old content can be migrated to these types.


.. _plone5-resource-registry-label:

Resource Registry
-----------------

The resource registry allows you to configure and edit the static resources (js, css) of Plone. It replaces the old javascript and css registries. And it can be used to customize the theme by changing the variables used by LESS or overriding LESS files.


.. _plone5-chameleon-label:

Chameleon template engine
-------------------------

`Chameleon <https://chameleon.readthedocs.org/en/latest/>`_ is the new rendering engine of Plone 5. It offers many improvements:

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

For debugging check out the variable ``econtext``, it holds all the current elements.

You can also add real python blocks inside templates.

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

There is also a useful new portlet type ``Actions`` used for displaying the site_actions.


.. _plone5-skins-label:

Remove portal_skins
-------------------

Many of the old skin templates were replaced by real browser views.

