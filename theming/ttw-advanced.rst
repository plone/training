=============================================
TTW Theming I: Introduction to Diazo Theming
=============================================

In this section you will:

* Use the "Theming" control panel to make a copy of Plone's default theme (:term:`Barceloneta`)
* Customize a theme using :term:`Diazo` rules
* Customize a theme by editing and compiling :term:`Less` files

Topics covered:

* :term:`Diazo` and plone.app.theming
* The Default Plone Theme (:term:`Barceloneta`)
* The "Theming Tool"
* Building CSS in the "Theming Tool"
* CSS classes of the ``<body>`` element
* Conditionally activating :term:`Diazo` rules


Installation
------------

We will use a `Plone pre-configured Heroku instance <https://github.com/collective/training-sandbox>`_.

Once deployed, create a Plone site.


Two approaches to theming
-------------------------

There are two main approaches to creating a custom theme:

#. Copying the default Barceloneta theme
#. Inheriting from the default Barceloneta theme.

In this section we'll look at the first approach, part II will explore the second approach.


What is Diazo?
--------------

:program:`Diazo` is a theming engine used by Plone to make theming a site easier.
At its core, a Diazo theme consists of an HTML page and :file:`rules.xml` file containing directives.

.. note::

   You can find extended information about Diazo and its integration package :py:mod:`plone.app.theming` in the official docs: `Diazo docs <http://docs.diazo.org/en/latest/>`_ and `plone.app.theming docs <https://docs.plone.org/external/plone.app.theming/docs/index.html#what-is-a-diazo-theme>`_.


Principles
----------

For this part of the training you just need to know the basic principles of a Diazo theme:

* Plone renders the content of the page.
* Diazo rules inject the content into any static theme.


Copy barceloneta theme
----------------------

To create our playground we will copy the existing Barceloneta theme.

#. Go to the :guilabel:`Theming` control panel.
#. You will see a list of the available themes.
   In a bare new Plone site, you will see something like this:

   .. image:: ../theming/_static/theming-bare_plone_themes_list.png
      :align: center

#. Look for the *Barceloneta Theme* and click the :guilabel:`Copy` button next to it.
#. Insert "My theme" as the name and click the checkbox to immediately enable the theme:

   .. image:: ../theming/_static/theming-copy_theme_form.png
      :align: center

#. Click on :guilabel:`Create` and you get redirected to your new theme's inspector:

   .. image:: ../theming/_static/theming-just_copied_theme_inspector.png
      :align: center


Anatomy of a Diazo theme
------------------------

The most important files:

* :file:`manifest.cfg`: contains metadata about the theme (`manifest reference <https://docs.plone.org/external/plone.app.theming/docs/index.html#the-manifest-file>`_);
* :file:`rules.xml`: contains the theme rules (`rules reference <https://docs.plone.org/external/plone.app.theming/docs/index.html#rules-syntax>`_);
* :file:`index.html`: the static HTML of the theme.

Exercise 1 - Inspecting the :file:`manifest.cfg`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To better understand how your theme is arranged start by reading the :file:`manifest.cfg` file.

In the theming tool, open the :file:`manifest.cfg` spend a minute or two looking through it, then see if you can answer the questions below.

#. Where are the main rules located for your theme?
#. What property in the :file:`manifest.cfg` file defines the source CSS/Less file used by the theme?
#. What do you think is the purpose of the ``prefix`` property?

.. admonition:: Solution
   :class: toggle

   #. The main rules are defined by the ``rules`` property (you could point this anywhere, however the accepted convention is to use a file named :file:`rules.xml`.
   #. The ``development-css`` property points at the main Less file, when compiled to CSS it is placed in the location defined by the ``production-css`` property.
   #. The ``prefix`` property defines the default location to look for non prefixed files, for example if your prefix is set to ``/++theme++mytheme`` then a file like index.html will be expected at ``/++theme++mytheme/index.html``


``<body>`` CSS classes
----------------------

As you browse a Plone site, Plone adds rich information about your current context.
This information is represented as special classes in the ``<body>`` element.
Information represented by the ``<body>`` classes includes:

* the current user role, and permissions,
* the current content-type and its template,
* the site section and sub section,
* the current subsite (if any),
* whether this is a frontend view,
* whether icons are enabled.

``<body>`` classes for an anonymous visitor
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Below you can see an example of the body classes for a page named "front-page", located in the root of a typical Plone site called "acme":

.. code-block:: html

    <body class="template-document_view
                 portaltype-document
                 site-acme
                 section-front-page
                 icons-on
                 thumbs-on
                 frontend
                 viewpermission-view
                 userrole-anonymous">

``<body>`` classes for a manager
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

And here is what the classes for the same page look like when viewed by a manager who has logged in:

.. code-block:: html

    <body class="template-document_view
                 portaltype-document
                 site-acme
                 section-front-page
                 icons-on
                 thumbs-on
                 frontend
                 viewpermission-view
                 userrole-member
                 userrole-manager
                 userrole-authenticated
                 plone-toolbar-left
                 plone-toolbar-expanded
                 plone-toolbar-left-expanded">

Notice the addition of ``userrole-manager``.

Exercise 2 - Discussion about the ``<body>`` classes
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Look back at the ``<body>`` classes for a manager. Can you answer the following questions?

#. What other roles does the manager have?
#. Can you see other differences?
#. What do you think the ``plone-toolbar-expanded`` class does?

.. admonition:: Solution
   :class: toggle

   #. The manager also has the role "member" and "authenticated"
   #. There are ``plone-toolbar`` classes added to the ``<body>`` element, these control the display of the toolbar
   #. The ``plone-toolbar-expanded`` class is used to control styles used by the expanded version of the toolbar.


Custom rules
------------
Let's open the default rules file :file:`rules.xml`.
You will see all the rules that are used in the Barceloneta theme right now.
For the time being let's concentrate on how to hack these rules.

Conditionally showing content
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. image:: ../theming/_static/theming-viewlet-above-content-in-plone-site.png
   :align: center

Suppose that we want to make the "above content" block (the one that contains breadcrumbs) conditional, and show it only for authenticated users.

In the :file:`rules.xml` find this line:

.. code-block:: xml

   <replace css:content="#viewlet-above-content" css:theme="#above-content" />

This rule states that the element that comes from the content (Plone) with the id ``#viewlet-above-content`` must replace the element with the id ``#above-content`` in the static theme.

We want to hide it for anonymous users  (hint: we'll use the ``<body>`` classses we discussed above).

The class we are looking for is ``userrole-authenticated``.
Add another attribute to the rule so that we produce this code:

.. code-block:: xml

    <replace
        css:if-content="body.userrole-authenticated"
        css:content="#viewlet-above-content"
        css:theme="#above-content" />

The attribute ``css:if-content`` allows us to put a condition on the rule based on a CSS selector that acts on the content.
In this way the rule will be applied only if the body element has the class ``.userrole-authenticated``.

We will learn more about Diazo rules in :doc:`./ttw-advanced-2`.


Customize CSS
-------------

#. In the theme editor open the file :file:`less/barceloneta.plone.less`.
   This file is the main Less file as specified in the :file:`manifest.cfg`.
#. Add your own customization at the bottom of the file, like:

   .. code-block:: css

      body {
          background-color: red;
          font-size: 18px;
      }

   .. Note::

      Normally you would place this in a separate file to keep the main one clean but for this example it is enough.

#. Click the buttons :guilabel:`Save` and :guilabel:`Build CSS`.

   .. image:: ../theming/_static/theming-editor_compile_css.png
      :align: center

#. Go back to the Plone site and reload the page: voilá!

.. Warning::

   At the moment you need to "Build CSS" from the main file, the one declared in the manifest (in this case :file:`less/barceloneta.plone.less`).
   So, whatever Less file you edit, go back to the main one to compile.
   This behavior will be improved in the future, but for now just remember this simple rule.
