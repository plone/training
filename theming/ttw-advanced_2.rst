=============================================================
TTW Theming II: Creating a custom theme based on Barceloneta
=============================================================

In this section you will:

* Create a theme by inheriting from the Barceloneta theme
* Using the :file:`manifest.cfg`, register a production CSS file
* Use an XInclude to incorporate rules from the Barceloneta theme
* Use ``?diazo.off=1`` to temporarily disable theme
* Use conditional rules to present visitors with a custom theme

Topics covered:

* Inheriting from Barceloneta
* Diazo rule directives and attributes
* Viewing the unthemed version of a Plone site
* Creating a visitor only theme

Inheriting from Barceloneta
---------------------------

Copying Barceloneta is not recommended:

- it makes your theme heavier,
- upgrading is more difficult.

Instead of copying it, Barceloneta can be inherited by a custom theme. Two elements must be inherited: the **rules**, and the **style**:

Create a new theme in the theming editor containing the following files:

- :file:`manifest.cfg`, declaring your theme:

.. code-block:: ini

    [theme]
    title = mytheme
    description =
    development-css = ++theme++custom/styles.less
    production-css = ++theme++custom/styles.css

- :file:`rules.xml`, including the Barceloneta rules:

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

- a copy of :file:`index.html` from Barceloneta (this one cannot be imported or inherited, it must be local to your theme).

- :file:`styles.less`, importing Barceloneta styles:

.. code-block:: css

    /* Import Barceloneta styles */
    @import "++theme++barceloneta/less/barceloneta.plone.less";

    /* Customize whatever you want */
    @plone-sitenav-bg: pink;
    @plone-sitenav-link-hover-bg: darken(pink, 20%);
    .plone-nav > li > a {
      color: @plone-text-color;
    }

Then you have to compile :file:`styles.less` to obtain your :file:`styles.css` file using the "Build CSS" button.

Your theme is ready.

Exercise 1 - create a new theme inheriting from Barceloneta
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Follow the example above and create a new theme that inherits from Barceloneta.

Diazo rule directives and attributes
------------------------------------

The Diazo rules file is an XML document containing rules to specify where the content elements (title, footer, main text, etc.) will be located in the targeted theme page.
The rules are created with ``rule directives`` which contain ``attributes``. 

CSS selector based attributes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
It is generally recommneded that you use CSS3 selectors to target elements in your content or theme.
The CSS3 selectors used by Diazo directives are listed below:

`css:theme`
    Used to select target elements from the theme using CSS3 selectors
`css:content`
    Used to specify the element that should be taken from the content
`css:theme-children`
    Used to select the the children of matching elements.
`css:content-children`
    Used to identify the children of an element that will be used.


Xpath selector based attributes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Sometimes the content or the theme does not have enough CSS markup to work reliably with CSS selectors.
In such cases you may be able to use XPath selectors these use the unprefixed
attributes ``theme`` and ``content``.

`theme`
    Used to select target elements from the theme using Xpath selectors
`content`
    Used to specify the element that should be taken from the content using Xpath selectors
`theme-children`
    Used to select the the children of matching elements using Xpath selectors.
`content-children`
    Used to identify the children of an element that will be used using Xpath selectors.

.. sidebar:: sometimes there are elements in your theme or content which are not easily targeted by CSS selectors
          in such cases you may need to use XPath selectors 
          the equivalent Xpath attributes to ``css:theme``,``css:content``,``css:if-theme`` and ``css:if-content``
          are ``theme``,``content``,``if-theme`` and ``if-content``).

You can also create conditions about the current path using ``if-path``.


.. note: For a more comprehensive overview of all the Diazo rule directives see: http://docs.diazo.org/en/latest/basic.html#rule-directives

Viewing the unthemed Plone site
-------------------------------

When you create your Diazo rules, it is important to know how the content Diazo is receiving from Plone is structured. 
In order to see a "non-diazoed" page, just add ``?diazo.off=1`` at the end of its URL.

Exercise 2 - Viewing the unthemed site
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

1. Use ``diazo.off=1`` to view the unthemed version of your site

2. Using your browser's inspector find out the location/name of some of the unthemed elements




Exercise 3 - the <drop> directives
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

1. Add a rule that drops the "search section" checkbox from the search box.
See the diagram below:

  .. image:: ../theming/_static/theming-dropping-thesearchsection.png


Conditional attributes
^^^^^^^^^^^^^^^^^^^^^^
The following attributes can be used to conditionally activate a directive.

`css:if-content`
    defines a CSS3 expression, if there is an element in the content that matches the expression then activate the directive
`css:if-theme`
    defines a CSS3 expression, if there is an element in the theme that matches the expression then activate the directive
`if-content`
    defines an Xpath expression, if there is an element in the content that matches the expression then activate the directive
`if-theme`
    defines an Xpath expression, if there is an element in the theme that matches the expression then activate the directive
`if-path`
    Conditionally activate the current directive based on the current path.

.. note:: In a previous chapter we discussed the Plone `<body>` element and how to take advantage of the custom CSS classes associated with it.
    We were introduced to the attribute ``css:if-content``
    Remember that we are able to determine a lot of context related information from the classes
    such as::

        - the current user role, and his permissions,
        - the current content-type and its template,
        - the site section and sub section,
        - the current subsite (if any).

    Here is an example

    .. code-block:: xml

        <body template-summary_view portaltype-collection site-Plone section-news subsection-aggregator icons-on thumbs-on frontend viewpermission-view userrole-manager userrole-authenticated userrole-owner plone-toolbar-left plone-toolbar-expanded plone-toolbar-left-expanded pat-plone patterns-loaded>


Converting an existing HTML template into an theme
--------------------------------------------------

Exercise 4 - Convert a HTML template into a Diazo theme
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


In this exercise we will work through the process of converting an existing free HTML theme
into a Diazo based Plone theme. 

.. note:: A theme is packaged as a zip file. Your theme should be structured such that 
          there is only one top level directory in the root of the zip file. The directory
          should contain your index.html and supporting files, it is okay if the supporting
          files (css, javascript and other files) are in subdirectories.

          We've selected the free `Clean Blog Bootstrap theme <https://github.com/BlackrockDigital/startbootstrap-clean-blog>`_. 
          The theme is already packaged in a manner that will work with the theming tool.

1. To get started `download a copy of the Clean Blog theme
   as a zip file <https://github.com/BlackrockDigital/startbootstrap-clean-blog/archive/gh-pages.zip>`_.
   Then upload it to the theme controlpanel.

    .. hint:: 
       :class: toggle

       This is a generic theme, it does not provide the Plone/Diazo specific :file:`rules.xml` or 
       :file:`manifest.cfg` file. When you upload the zip file the theming tool generates a :file:`rules.xml`.
       In the next steps you will add additional files including a :file:`manifest.cfg`.
             
       .. image:: ../theming/_static/theming-uploadzipfile.png
    
       Select the downloaded zip file.
    
       .. image:: ../theming/_static/theming-uploadzipfile2.png
    
2. Add a :file:`styles.less` file and import the Barceloneta styles 

3. Add a :file:`manifest.cfg` file, configure the ``production-css`` equal to ``styles.css``

    .. hint:: 
       :class: toggle
    
       You can identify the theme path by reading your browser's address 
       bar when your theme is open in the theming tool.
       You'll need to include the proper theme path in your :file:`manifest.cfg`,
       in this case it will most likely be something like ``++theme++startbootstrap-clean-blog-gh-pages``
             



Creating a visitor only theme - conditionally enabling Barceloneta
------------------------------------------------------------------

Sometimes you want to use Barceloneta for the website administrators (so they can manage the content conveniently)
and offer a completely different layout for visitors,
to do so associate your visitor theme rules with ``css:if-content="body.userrole-anonymous"``.
For rules that will affect logged in users use the expression
``css:if-content="body.:not(userrole-anonymous)"``.

Using the expressions above with the right Diazo rule it should be possible 
for an anonymous visitor to be presented with a specific HTML theme while presenting the 
Barceloneta theme to logged in users.

Exercise 5 - Convert the theme to be a visitors only theme
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In this exercise we will alter our theme from the previous exercise to make it
into a visitor only theme.

1. Update the :file:`rules.xml` file to include Barceloneta rules 

    .. hint:: 
       :class: toggle
       
       Use ``<xi:include href="++theme++barceloneta/rules.xml" />``

2. Add conditional rules to the :file:`rules.xml` so that new theme is only for anonymous users
   rename :file:`index.html` to :file:`front.html` and add a copy of the Barceloneta :file:`index.html`

    .. hint:: 
       :class: toggle

       copy the contents of the Barceloneta index.html file
       then in the new theme create a file called :file:`index.html` 
       
       change :file:`rules.xml` to:

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

