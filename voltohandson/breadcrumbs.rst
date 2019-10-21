.. _voltohandson-breadcrumbs-label:

===========
Breadcrumbs
===========

Hiding them from the App first level component
==============================================

We want to hide breadcrumbs from the homepage.

We can do it by using bare styling, since Volto injects CSS classes in the body that help us to style depending on the object, the content type and the path.
Volto does it very much like Plone does.

.. code-block:: less

    .siteroot .ui.secondary.segment.breadcrumbs,
    .section-edit .ui.secondary.segment.breadcrumbs {
      display: none;
    }

We will return to breadcrumbs later to style it, after we finish with the homepage.

However, to simplify the training for now, we will remove the breadcrumbs for all pages.

.. code-block:: less

    .ui.secondary.segment.breadcrumbs {
      display: none;
    }
