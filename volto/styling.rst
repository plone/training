.. _styling-label:

=======
Styling
=======

Semantic UI
===========

For styling our website in Volto we use Semantic UI. Semantic UI uses LESS as
the underlaying technology. By default Volto uses the pastanaga theme but any
theme can be used. A theme has the following folder structure:

- assets
- collections
- elements
- globals
- modules
- views

The assets folder contains all the images and fonts. The other folders contain
LESS files. Those less files are separate for each ui component. For example we
have separate files for buttons. Each ui component has 2 files a :file:`.variables`
file and an :file:`.overrides` file. The :file:`.variables` file contains all the
predefined variables which you can override in your theme. If you want to do
more specific customizations you can use the :file:`.overrides` file to write your
own LESS.

In the globals folder we have the :file:`site.variables` and :file:`site.overrides`
files which contain the side wide styling. If we want to customize something
we can create the same file (including the matching folder structure) in our
theme folder.

Changing Base Font
==================

We start by creating the file :file:`theme/globals/site.variables`. In this file
we can override any value. We don't need to copy the whole file we can just add
variables we would like to change. When we want to change the base font we add
the following:

::

    @fontName : 'Comic Sans MS';

Changing The Breadcrumbs
========================

Change the breadcrumbs so that the divider is pink:

..  admonition:: Solution
    :class: toggle

    :file:`theme/collections/breadcrumb.variables`:

    ::

        @dividerColor: @pink;

Using Overrides
===============

For features which are not supported in Semantic UI through the variables we
can use the overrides files. Update the breadcrumbs so that the links are
underlined.


..  admonition:: Solution
    :class: toggle

    :file:`theme/collections/breadcrumb.overrides`:

    ::

        .ui.breadcrumb a {
          text-decoration: underline;
        }
