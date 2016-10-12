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
----------------------------------------------------------

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



- the current user role, and its permissions,
- the current content-type and its template,
- the site section and sub section,
- the current subsite (if any).


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


Conditionally enable Barceloneta
---------------------------------

Imagine you might want to use Barceloneta for the website administrators (so they can manage the content conveniently) and offer a completely different layout for visitors, you just need to create rules with ``css:if-content="body.userrole-anonymous"`` or ``css:if-content="body.:not(userrole-anonymous)"`` to enable the theme you want.

As you can see, if the visitor is anonymous, Diazo will use a specific HTML theme (named :file:`front.html`) and not the Barceloneta's :file:`index.html`.

Exercise 4 - Create a specific design for visitors only
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

1. To get started `download a copy of the clean-blog theme as a zip file <https://github.com/BlackrockDigital/startbootstrap-clean-blog/archive/master.zip>`_.
Then upload it to the theme controlpanel.

    .. note:: Clean Blog is a free Bootstrap theme, 
          the latest version is available on github `<https://github.com/BlackrockDigital/startbootstrap-clean-blog>`_

2. Add a :file:`styles.less` file and import the Barceloneta styles 

3. Add a :file:`manifest.cfg` file, configure the production-css`` to use ``styles.css``

    .. hint:: You'll need to include the proper theme path, in this case it will most likely be ``++theme++startbootstrap-clean-blog-master``
              You can identify the theme path by reading your browser's address bar when your theme is open in the 
              theming tool.

4. Adjust the :file:`rules.xml` file to include Barceloneta rules 

    .. hint:: Use ``<xi:include href="++theme++barceloneta/rules.xml" />``

..  admonition:: Solution
    :class: toggle

    - create a :file:`front` folder in the theme,
    - put the 2 downloaded files in this folder,
    - in :file:`index.html`, fix the ``<link>`` element to load :file:`front/style.css`,
    - change :file:`rules.xml` to:

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
                <theme href="front/index.html" />
                <replace css:theme-children=".intro header h2" css:content-children=".documentFirstHeading" />
                <replace css:theme-children=".summary" css:content-children=".documentDescription" />
                <replace css:theme-children=".preamble" css:content-children="#content-core" />
              </rules>
            </rules>

