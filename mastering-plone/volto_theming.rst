.. _volto_theming-label:

================
Theming in Volto
================

.. sidebar:: Volto chapter

  .. figure:: _static/volto.svg
     :alt: Volto Logo

  This chapter is about the react frontend Volto.

  Solve the same tasks in classic frontend in chapter :doc:`theming`


.. sidebar:: Get the code! (:doc:`More info <code>`)

   Code for the beginning of this chapter::

       git checkout *TODO*

   Code for the end of this chapter::

        git checkout *TODO*


To develop our theme, we can use Semantic UI. There are two cases: Some attributes like the overall font that are covered by Semantic UI variables. The other case is styling of for example listing news that needs some custom CSS rules.

We start with the first case and change the font to another Google font, Lato.

The overall font is defined in omelette in ``theme/globals/site.variables``. So create an empty file ``site.variables`` in ``theme/globals/`` and set your font.

.. code-block:: css

  @fontName : 'Lato';

Semantic UI does not provide a less variable for increasing the letter-spacing. So we add a CSS rule for it. We use the ``site.overrides`` as this rule should apply site wide. Create an empty file ``site.overrides``in ``theme/globals``and set the letter-spacing.

.. code-block:: css

  #main {
      letter-spacing: .05em;
  }

We can use variables and theme overrides to achieve our theme, or we can use Volto’s custom.overrides, or we can mix elements of both as needed. There is no right or wrong way of doing it, and we will be using the Semantic UI theming engine in both cases.

So there are these two ``custom.overrides`` and ``custom.variables`` for everything else, that is not belonging to the site as a whole, not belonging to the header, navigation, breadcrumbs, etc.. It's a convention to put styling of your additional non default components in ``custom.overrides`` and ``custom.variables``.

In chapter :ref:`volto-component-label` we will create an addional component to show the sponsors. We address this component in ``theme/extras/custom.overrides``

.. code-block:: css

  .ui.segment.sponsors {
    background-color: rgb(177, 192, 219);
  }

Take into account to use theme variables as 

.. code-block:: css

  .ui.segment.sponsors {
    background-color: @lightGrey;
  }

Changing the favicon
----------------------

Find the favicon.ico in ``public/``and replace it with a custom favicon. 

.. note::

  As you already know, the Node app Volto needs to be restarted after adding new files.


