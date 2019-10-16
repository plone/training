.. _voltohandson-default-font-label:

=======
Theming
=======

We can use Semantic UI variables and theme overrides to achieve our theme, use Volto's ``custom.overrides`` or use both mixed as we desire.
There is no right way of doing it, and we will be using the Semantic UI theme engine in both cases.

.. image:: _static/theming_engine.png
   :align: center
   :alt: Theming engine diagram

Basic font family
=================

We will use Semantic UI variables for customizing the font, as it's a valuable feature.
Create a file in the following path ``theme/globals/site.variables`` and restart to make Volto aware of it.
Edit the file and add this:

.. code-block:: less

    @fontName: 'Open Sans';

You can set any Google font available from these setting, and the online version will be used.
You can also set other variables concerning the font used like the sizes available, etc.
In case you want to use more than one font or a font that is self-hosted,
you should define it as usual in CSS and set the variable ``importGoogleFonts`` appropiately.

.. tip:: You can find the list with the global Semantic UI variables available in ``omelette/theme/themes/default/global/site.variables``.

custom.overrides
================

Create a file named ``theme/extras/custom.overrides`` which will contain all the CSS concerning our local theme.
This is a file containing LESS declarations. It's loaded faster than the theme ones, because it's outside the theme.
You should restart to make Volto aware of it.
