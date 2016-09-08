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

Conditionnally enable Barceloneta
---------------------------------

Use the Plone `<body>` classes to disable Barceloneta and create a completely different theme in given cases.

Use backend.xml
---------------

Explain how to use `backend.xml`.

