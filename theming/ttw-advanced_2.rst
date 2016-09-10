=============================================================
TTW advanced II: Creating a custom theme based on Barceloneta
=============================================================

Inheriting from Barceloneta
---------------------------

Copying Barceloneta is not recommended:

- it makes your theme heavier,
- upgrading is more difficult.

Instead of copying it, Barceloneta can inherited by a custom theme. Two elements must be inherited: the **rules**, and the **style**:

Create a new theme in the theming editor containing the following files:

- ``manifest.cfg``, declaring your theme:

.. code-block:: ini

    [theme]
    title = mytheme
    description =
    development-css = /++theme++mytheme/styles.less
    production-css = /++theme++mytheme/styles.css

- ``rules.xml``, including the Barceloneta rules:

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

- a copy of ``index.html`` from Barceloneta (this one cannot be imported or inherited, it must be local to your theme).

- ``styles.less``, importing Barceloneta styles:

.. code-block:: css

    /* Import Barceloneta styles */
    @import "++theme++barceloneta/less/barceloneta.plone.less";

    /* Customize whatever you want */
    @plone-sitenav-bg: pink;
    @plone-sitenav-link-hover-bg: darken(pink, 20%);
    .plone-nav > li > a {
      color: @plone-text-color;
    }

Then you have to compile ``styles.less`` to obtain your ``styles.css`` file using the "Build CSS" button.

Your theme is ready.

Exercise: create a new theme inheriting from Barceloneta
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Just follow the previous explanations.

Introduction to the Diazo rules
-------------------------------

Diazo uses rules to specify where the content elements (title, footer, main text, etc.) must be located in the targeted theme page.

- `<after>` inserts the content element after the theme element,
- `<before>` inserts the content element before the specified theme element,
- `<replace>` replaces the theme element with the content element,
- `<drop>` removes the content or the theme element.

You use `css:theme` to specify CSS selector corresponding to the targeted element in the theme, and `css:content` to specifiy the CSS selector corresponding to the content element to display.

Similarly, you can use `css:theme-children` and `css:content-children` to target the element's children.

.. note:: sometimes CSS selectors are not powerful enough, and you can use XPath selector (using `theme` and `content`).

To apply a rule conditionnally, you use `css:if-theme` and `css:if-content` (or `if-theme` and `if-content` with XPath).

You can also create conditions about the current path using `if-path`.

Conditionally enable Barceloneta
---------------------------------

The Plone `<body>` element has a lot of CSS classes that allow you to create accurate conditions for your Diazo rules.

Those classes allow to get many information on the context like:

- the current user role, and his permissions,
- the current content-type and its template,
- the site section and sub section,
- the current subsite (if any).

Here is an example::

    template-summary_view portaltype-collection site-Plone section-news subsection-aggregator icons-on thumbs-on frontend viewpermission-view userrole-manager userrole-authenticated userrole-owner plone-toolbar-left plone-toolbar-expanded plone-toolbar-left-expanded pat-plone patterns-loaded

Imagine you might want to use Barceloneta for the website administrators (so they can manage the content conviniently) and offer a completely different layout for visitors, you just need to create rules with ``css:if-content="body.userrole-anonymous"`` or ``css:if-content="body.:not(userrole-anonymous)"`` to enable the theme you want.

As you can see, if the visitor is anonymous, Diazo will use a specific HTML theme (named ``front.html``) and not the Barceloneta's ``index.html``.

Exercise: create a specific design for visitors only
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Go to http://www.csszengarden.com/, download a theme (do not use the download links, use your brwoser debugger to get the actual HTML markup and the CSS), and add it to your Diazo theme for anonymous visitors only.

..  admonition:: Solution
    :class: toggle

    - create a ``front`` folder in the theme,
    - put the 2 downloaded files in this folder,
    - in ``index.html``, fix the ``<link>`` element to load ``front/style.css``,
    - change ``rules.xml`` to:

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

.. note::

    When you create your Diazo rules, it is important to know how is structured the content Diazo is receiving from Plone. In order to see a non-diazoed page, just add ``?diazo.off=1`` at the end of its URL.
