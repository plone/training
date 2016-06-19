Mosaic
======

In this part you will:

* create a home page layout,
* create a specific talk detail layout,

Topics covered:

* Create custom layouts
* Manage layouts
* Use the layout editor

What is Mosaic?
---------------

* A Plone add-on,
* it allows to manage layouts from the Plone interface.

Few comparisons
---------------

.. only:: presentation

    * It allows to manage the layout, not the design (like Diazo).
    * It can manage the layout of any page, it does not provide a specific layout-enabled content (like collective.cover).

.. only:: not presentation

    * Compare to Diazo:

        Diazo allows to theme our Plone site, by providing CSS, images, and HTML templates. And it will apply to the entire page (footer, main content, portlets, etc.).

        Mosaic uses the grid provided by our design to dynamically build specific content layouts.

    * Compare to collective.cover:

        collective.cover provides a specific content-type (a "Cover page") where we can manage the layout in order to build our homepage.

        Mosaic does not provide any content-type, it allows to edit any existing content layout.
