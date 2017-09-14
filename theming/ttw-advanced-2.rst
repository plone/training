=============================================================
TTW Theming II: Creating a custom theme based on Barceloneta
=============================================================

In this section you will:

* Create a new theme by inheriting from the :term:`Barceloneta` theme.
* Use the :file:`manifest.cfg` to register a production CSS file.
* Use an ``XInclude`` to incorporate rules from the :term:`Barceloneta` theme.
* Use ``?diazo.off=1`` to view unthemed versions.
* Use conditional rules to have a different backend theme from the anonymous visitors theme.

Topics covered:

* Inheriting from Barceloneta theme.
* Diazo rule directives and attributes.
* Viewing the unthemed version of a Plone item.
* Creating a visitor-only theme.


Inheriting from Barceloneta
---------------------------
.. sidebar:: Key Ideas

    When inheriting from the Barceloneta theme keep the following in mind:

    * The theme provides styles and assets used by Plone's backend tools.
    * Inheritance involves including the Barceloneta :file:`rules.xml` (``++theme++barceloneta/rules.xml``) and styles.
    * The prefix/unique path to the Barceloneta theme is ``++theme++barceloneta``.
    * It is necessary to include a copy of Barceloneta's :file:`index.html` in the root of your custom theme.
    * The three key files involved are :file:`manifest.cfg`, :file:`rules.xml` and a Less file defined in the manifest which we will call :file:`styles.less`.
    * Use "Build CSS" to generate a CSS file from your custom Less file.

Copying Barceloneta makes your theme heavier and will likely make upgrading more difficult.

The Barceloneta theme provides many assets used by Plone's utilities that you do not need to duplicate.
Additionally new releases of the theme may introduce optimizations or bug fixes.
By referencing the Barceloneta rules and styles, instead of copying them, you automatically benefit from any updates to the Barceloneta theme while also keeping your custom theme relatively small.

Exercise 1 - Create a new theme that inherits from Barceloneta
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

In this exercise we will create a new theme that inherits the Barceloneta rules and styles.

#. Go to the :guilabel:`Theming` control panel.
#. Click the :guilabel:`New theme` button to create a new theme:

   .. image:: ../theming/_static/theming-new-theme.png

#. Give the theme a name, e.g. "Custom", and click the checkbox to immediately enable the theme:

   .. image:: ../theming/_static/theming-new-theme2.png

#. Click on :guilabel:`Create` and you get redirected to your new theme's inspector.

#. In the theming editor, ensure that your new theme contains the files :file:`manifest.cfg`, :file:`rules.xml`, :file:`index.html` (from Barceloneta) and :file:`styles.less`.

#. Edit the file :file:`manifest.cfg` which contains the configuration for your theme:

   .. code-block:: ini

      [theme]
      title = Custom
      description = A custom theme
      development-css = ++theme++custom/styles.less
      production-css = ++theme++custom/styles.css

#. Edit the file :file:`rules.xml` which includes the link to the Barceloneta rules:

   .. code-block:: xml

      <?xml version="1.0" encoding="UTF-8"?>
      <rules
          xmlns="http://namespaces.plone.org/diazo"
          xmlns:css="http://namespaces.plone.org/diazo/css"
          xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
          xmlns:xi="http://www.w3.org/2001/XInclude">

        <!-- Import Barceloneta rules -->
        <xi:include href="++theme++barceloneta/rules.xml" />

        <rules css:if-content="#visual-portal-wrapper">
          <!-- Placeholder for your own additional rules -->
        </rules>

      </rules>

#. Create a copy of the file :file:`index.html` from Barceloneta (this one cannot be imported or inherited, it must be local to your theme).

#. Edit the file :file:`styles.less` which includes imports from the Barceloneta styles:

   .. code-block:: css

      /* Import Barceloneta styles */
      @import "++theme++barceloneta/less/barceloneta.plone.less";

      /* Customize whatever you want */
      @plone-sitenav-bg: pink;
      @plone-sitenav-link-hover-bg: darken(pink, 20%);
      .plone-nav > li > a {
        color: @plone-text-color;
      }

#. Generate the :file:`styles.css` CSS file using :file:`styles.less`.
   Click the buttons :guilabel:`Save` and :guilabel:`Build CSS` to create the file.

#. Your theme is ready.


Diazo rule directives and attributes
------------------------------------

The Diazo rules file is an XML document containing rules to specify where the content elements
(title, footer, main text, etc.) will be located in the targeted theme page.
The rules are created using *rule directives* which have *attributes*; attribute values
are either CSS expressions or XPath expressions.

CSS selector based attributes
+++++++++++++++++++++++++++++
It is generally recommended that you use CSS3 selectors to target elements in your content or theme.
The CSS3 selectors used by Diazo directives are listed below:

``css:theme``
    Used to select target elements from the theme using CSS3 selectors.
``css:content``
    Used to specify the element that should be taken from the content.
``css:theme-children``
    Used to select the children of matching elements.
``css:content-children``
    Used to identify the children of an element that will be used.


XPath selector based attributes
+++++++++++++++++++++++++++++++

Depending on complexity of the required selector it is sometimes necessary or more convenient
to use XPath selectors instead of CSS selectors. XPath selectors use the unprefixed
attributes ``theme`` and ``content``. The common XPath selector attributes include:

``theme``
    Used to select target elements from the theme using XPath selectors.
``content``
    Used to specify the element that should be taken from the content using XPath selectors.
``theme-children``
    Used to select the children of matching elements using XPath selectors.
``content-children``
    Used to identify the children of an element that will be used using XPath selectors.

You can also create conditions about the current path using ``if-path``.


.. note:: For a more comprehensive overview of all the Diazo rule directives
   and related attributes see: http://docs.diazo.org/en/latest/basic.html#rule-directives

Viewing the unthemed Plone site
-------------------------------

When you create your Diazo rules, it is important to know how the content Diazo is receiving from Plone is structured.
In order to see a "non-diazoed" version page, just add ``?diazo.off=1`` at the end of its URL.

Exercise 2 - Viewing the unthemed site
++++++++++++++++++++++++++++++++++++++

1. Use ``diazo.off=1`` to view the unthemed version of your site.

2. Using your browser's inspector, find out the location/name of some of Plone's elements.
   Then try to answer the following:

   What do you think is the difference between "content-core" and "content"?
   There are several viewlets, how many do you count?
   Can you identify any portlets, what do you think they are for?

    .. admonition:: Solution
       :class: toggle

       The "content-core" does not include the "title" and "description" while
       the "content" combines the "title", "description" and "content-core".

       Out of the box there are six viewlets (``viewlet-above-content``, ``viewlet-above-content-title``
       ``viewlet-below-content-title``, ``viewlet-above-content-body``, ``viewlet-below-content-body``,
       ``viewlet-below-content``).

       There are a few *footer* portlets which construct the footer of the site.


Exercise 3 - the ``<drop>`` directives
++++++++++++++++++++++++++++++++++++++

1. Add a rule that drops the "search section" checkbox from the search box.
   See the diagram below:

   .. image:: ../theming/_static/theming-dropping-thesearchsection.png


Conditional attributes
^^^^^^^^^^^^^^^^^^^^^^
The following attributes can be used to conditionally activate a directive.

``css:if-content``
    Defines a CSS3 expression: if there is an element in the *content* that matches the expression then activate the directive.
``css:if-theme``
    Defines a CSS3 expression: if there is an element in the *theme* that matches the expression then activate the directive.
``if-content``
    Defines an XPath expression: if there is an element in the *content* that matches the expression then activate the directive.
``if-theme``
    Defines an XPath expression: if there is an element in the *theme* that matches the expression then activate the directive.
``if-path``
    Conditionally activate the current directive based on the current path.

.. note:: In a previous chapter we discussed the Plone ``<body>`` element and how to take advantage of the custom CSS classes associated with it.
    We were introduced to the attribute ``css:if-content``.
    Remember that we are able to determine a lot of context related information from the classes,
    such as::

    - the current user role, and its permissions,
    - the current content-type and its template,
    - the site section and sub section,
    - the current subsite (if any).

    Here is an example

    .. code-block:: xml

        <body class="template-summary_view
                     portaltype-collection
                     site-Plone
                     section-news
                     subsection-aggregator
                     icons-on
                     thumbs-on
                     frontend
                     viewpermission-view
                     userrole-manager
                     userrole-authenticated
                     userrole-owner
                     plone-toolbar-left
                     plone-toolbar-expanded
                     plone-toolbar-left-expanded
                     pat-plone
                     patterns-loaded">


Converting an existing HTML template into an theme
---------------------------------------------------
In the Plone "universe" it is not uncommon to convert an existing HTML template into a
Diazo theme. Just ensure that when you zip up the source theme that there is a single folder
in the root of the zip file. We will explore this in more detail in the next exercise.

Exercise 4 - Convert a HTML template into a Diazo theme
+++++++++++++++++++++++++++++++++++++++++++++++++++++++

In this exercise we will walk through the process of converting an existing free HTML theme
into a Diazo-based Plone theme.

.. image:: ../theming/_static/theming-startbootstrap-newage-theme.png

We've selected the free `New Age Bootstrap theme <https://github.com/BlackrockDigital/startbootstrap-new-age>`_.
The theme is already packaged in a manner that will work with the theming tool.

.. note:: When being distributed, Plone themes are packaged as zip files. A theme should be structured such that
          there is only one top level directory in the root of the zip file. By convention the directory
          should contain your :file:`index.html` and supporting files, the supporting
          files (CSS, javascript and other files) may be in subdirectories.

1. To get started `download a copy of the New Age theme as a zip file <https://codeload.github.com/BlackrockDigital/startbootstrap-new-age/zip/master>`_.
   Then upload it to the theme controlpanel.

    .. hint::
       :class: toggle

       This is a generic theme, it does not provide the Plone/Diazo specific :file:`rules.xml` or
       :file:`manifest.cfg` file. When you upload the zip file the theming tool generates a :file:`rules.xml`.
       In the next steps you will add additional files including a :file:`manifest.cfg` (perhaps in the future
       the manifest.cfg will also be generated for you).

       .. image:: ../theming/_static/theming-uploadzipfile.png

       Select the downloaded zip file.

       .. image:: ../theming/_static/theming-uploadzipfile2.png

2. Add a :file:`styles.less` file and import the Barceloneta styles.

3. Add a :file:`manifest.cfg` file, set ``production-css`` equal to ``styles.css``

    .. note:: Clean Blog is a free Bootstrap theme,
          the latest version is available on github `<https://github.com/BlackrockDigital/startbootstrap-clean-blog>`_

    .. hint::
       :class: toggle

       You can identify the theme path by reading your browser's address
       bar when your theme is open in the theming tool.
       You'll need to include the proper theme path in your :file:`manifest.cfg`,
       in this case it will most likely be something like ``++theme++startbootstrap-new-age-gh-pages``

       [theme]
       title = New Age
       prefix = ++theme++startbootstrap-new-age-gh-pages/
       production-css = ++theme++startbootstrap-new-age-gh-pages/styles.css


4. Add rules to include the Barceloneta backend utilities
   ::

       <?xml version="1.0" encoding="UTF-8"?>
    <rules
        xmlns="http://namespaces.plone.org/diazo"
        xmlns:css="http://namespaces.plone.org/diazo/css"
        xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
        xmlns:xi="http://www.w3.org/2001/XInclude">

      <!-- Include the backend theme -->
      <xi:include href="++theme++barceloneta/backend.xml" />


5. Add rules to include content, add site structure, drop unneeded elements, customize the menu.

   .. warning::

     Look out for inline styles in this theme
     (i.e. the use of the ``style`` attribute on a tag). This is especially problematic with
     background images set with relative paths. The two issues that result are:

       * the relative path does not translate properly in the context of the
         theme;
       * it can be tricky to dynamically replace background images provided by
         inline styles.

Creating a visitor-only theme - conditionally enabling Barceloneta
------------------------------------------------------------------

Sometimes it is more convenient for your website administrators to use Barceloneta, Plone's default theme.
Other visitors would see a completely different layout provided by your custom theme.
To achieve this you will need to associate your visitor theme rules with
an expression like ``css:if-content="body.userrole-anonymous"``.
For rules that will affect logged-in users you can use the expression
``css:if-content="body.:not(userrole-anonymous)"``.

Once you've combined the expressions above with the right Diazo rules you will be able
to present an anonymous visitor with a specific HTML theme while presenting the
Barceloneta theme to logged-in users.

.. warning::

   The Barceloneta :file:`++theme++barceloneta/rules.xml` expects the
   Barceloneta :file:`index.html` to reside locally in your current theme.
   To avoid conflict and to accomodate the inherited Barceloneta, ensure that
   your theme file has a different name such as :file:`front.html`.


Exercise 5 - Convert the theme to be a visitor-only theme
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++

In this exercise we will alter our theme from the previous exercise to make it
into a visitor-only theme.

1. Update the :file:`rules.xml` file to include Barceloneta rules.

    .. hint::
       :class: toggle

       Use ``<xi:include href="++theme++barceloneta/rules.xml" />``

2. Add conditional rules to :file:`rules.xml` so that the new theme is only shown to anonymous users,
   rename the theme's :file:`index.html` to :file:`front.html` and add a copy of the Barceloneta :file:`index.html`.

    .. hint::
       :class: toggle

       Copy the contents of the Barceloneta :file:`index.html` file
       then add it to the theme as the new :file:`index.html` file.

       Change :file:`rules.xml` to look similar to this:

        .. code-block:: xml

            <?xml version="1.0" encoding="UTF-8"?>
            <rules
                xmlns="http://namespaces.plone.org/diazo"
                xmlns:css="http://namespaces.plone.org/diazo/css"
                xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                xmlns:xi="http://www.w3.org/2001/XInclude">

              <notheme css:if-not-content="#visual-portal-wrapper" />

              <rules css:if-content="body:not(.userrole-anonymous)">
                <!-- Import Barceloneta rules -->
                <xi:include href="++theme++barceloneta/rules.xml" />
              </rules>

              <rules css:if-content="body.userrole-anonymous">
                <theme href="front.html" />
                <replace css:theme-children=".intro header h2" css:content-children=".documentFirstHeading" />
                <replace css:theme-children=".summary" css:content-children=".documentDescription" />
                <replace css:theme-children=".preamble" css:content-children="#content-core" />
              </rules>
            </rules>
