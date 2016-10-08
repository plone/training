=============================================
TTW advanced I: introduction to Diazo Theming
=============================================

In this section you will:

* Use the "Theming" control panel to make a copy of Plone's default theme (barceloneta)
* Customize a theme using Diazo rules
* Customize a theme by editing and compiling Less files

Topics covered:

* "Barceloneta" - The Default Plone Theme
* Diazo and plone.app.theming
* The "Theming tool"
* Building CSS in the "Theming tool"
* Plone Body Tag Base CSS Classes
* if-content

What is Diazo?
--------------

``Diazo`` is a theming engine used by Plone to make theming a site easier.
At its core, a Diazo theme consists of an HTML page and rules.xml file containing directives.

.. note::

    You can find extended information about Diazo and its integration package ``plone.app.theming`` in the official docs: `Diazo docs <http://docs.diazo.org/en/latest/>`_ and `plone.app.theming docs <http://docs.plone.org/external/plone.app.theming/docs/index.html#what-is-a-diazo-theme>`_.

Principles
----------

For this part of the training you just need to know the basic principles of a Diazo theme:

* Plone renders the content of the page;
* Diazo rules inject the content into any static theme;

Copy barceloneta theme
----------------------

To create our playground we will copy the existing Barceloneta theme.

1. go to the "Theming" control panel
2. you will see the available themes. In a bare new Plone site, you will see something like this:

.. image:: _static/theming-bare_plone_themes_list.png
   :align: center

3. click on the "copy" button and get to the copy form
4. insert "My theme" as the name and activate it by default

.. image:: _static/theming-copy_theme_form.png
   :align: center

5. click on create and you get redirected to your new theme's inspector:

.. image:: _static/theming-just_copied_theme_inspector.png
   :align: center


Anatomy of a Diazo theme
------------------------

The most important files:

* :file:`manifest.cfg`: contains metadata about the theme (`manifest reference <http://docs.plone.org/external/plone.app.theming/docs/index.html#the-manifest-file>`_);
* :file:`rules.xml`: contains the theme rules (`rules reference <http://docs.plone.org/external/plone.app.theming/docs/index.html#rules-syntax>`_);
* :file:`index.html`: the static HTML of the theme.


Custom rules
------------
Let's open :file:`rules.xml`. You will see all the rules that are used in Barceloneta theme right now. For the time being let's concentrate on how to hack these rules.

Conditionally showing content
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Suppose that we want to make the "above content" block (the one that contains breadcrumbs) conditional, and show it only for authenticated users.

Find this line:

.. code-block:: xml

    <replace css:content="#viewlet-above-content" css:theme="#above-content" />

This rule states that the element that comes from the content (Plone) with the id `#viewlet-above-content` must replace the element with the id `#above-content` in the static theme.

We want to hide it for anynoymous users so we can take advantage of the base CSS classes that Plone exposes on the body.

A short note about base CSS classes on the body tag
```````````````````````````````````````````````````
As you browse a Plone site, Plone adds rich information about each item that you view. This information is represented as special classes in the body tag.

Below you can see an example of a page named "front-page", located in the root of a typical plone site::

    <body class="template-document_view portaltype-document site-acme section-front-page icons-on thumbs-on frontend viewpermission-view userrole-anonymous">

And here is what the body tag looks like on the same "front-page" for a manager that has logged in::

    <body class="template-document_view portaltype-document site-acme section-front-page icons-on thumbs-on frontend viewpermission-view userrole-member userrole-manager userrole-authenticated plone-toolbar-left plone-toolbar-expanded plone-toolbar-left-expanded">

Can you see differences?


The class we are looking for is `userrole-authenticated`. Add another property to the rule so that we produce this code:

.. code-block:: xml

    <replace
        css:if-content="body.userrole-authenticated"
        css:content="#viewlet-above-content"
        css:theme="#above-content" />

The attribute `css:if-content` allows us to put a condition on the rules based on a CSS selector that acts on the content. In this way the rule will be applied only if the body element has the class `.userrole-authenticated`.

We will learn more about Diazo rules in :doc:`./ttw-advanced_2`.


Customize CSS
-------------

1. from theme editor open the file `less/barceloneta.plone.less`, that is the main LESS file as specified in the manifest;
2. add your own customization at the bottom, like:

.. code-block:: css

    body{ background-color: red; font-size: 18px ;};

*Note: normally you would place this in a separate file to keep the main one clean but for this example it is enough.*

3. push the buttons "Save" and "Build CSS"

.. image:: _static/theming-editor_compile_css.png
   :align: center

4. go back to the plone site and reload the page: voilá!


..  Warning::

    At the moment you need to "Build CSS" from the main file, the one declared in the manifest (in this case `less/barceloneta.plone.less`). So, whatever LESS file you edit, go back to the main one to compile. This behavior will be improved but for now, just remember this simple rule ;)
