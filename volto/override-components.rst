.. _override_components-label:

===================
Override Components
===================

Override The Logo
=================

When we want to override a specific file we can create an alias pointing to
our own theme. So for example if we want to replace the logo, which is located
in Volto at :file:`components/theme/Logo/Logo.svg`, we will add an logo to
our theme and create an alias. It is best practice to match the folder structure
of Volto in the :file:`customizations` folder. After we put our new logo at
:file:`customizations/theme/Logo/Logo.svg` we will create an entry
in the :file:`package.json` to override the logo:

::

    "customizations": {
    },

Change The Not Found Page
=========================


Change The Title
================
