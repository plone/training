.. _voltohandson-introtoblocks-label:

======
Blocks
======

We will use Volto blocks (a.k.a. tiles) to compose the homepage.

Brief intro to Volto blocks
===========================

Volto features the Pastanaga Editor Engine, allowing you to compose visually a page using blocks.
The editor allows you to add, modify, reorder and delete blocks given your requirements.
Blocks provide the user the ability to display content in an specific way, although they can also define behavior and have specific features.
Blocks are composed of two basic (and required) components: the Block edit and view components.

By default, Volto ships with the most basic set of Blocks: Title, Text, Image, Video, Maps, etc...

.. note:: Volto Blocks are not enabled by default in Plone content types.
          If you are using the ``kitconcept.voltodemo`` package it sets it up for you for the ``Document`` content type.
          So if you create a page, by default it is enabled.

How to enable manually Blocks on a content type
===============================================

There is a behavior ``Tiles`` that ``plone.restapi`` makes available.

1. Go to ``ControlPanel`` -> ``Dexterity Content Types``, select the content type.
2. Go to ``Behaviors``
3. Select the ``Tiles`` behavior
4. Save

Test that the content type you've just enable the tiles behavior is working, by creating a new object of that type from Volto.

Blocks anatomy
==============

Every Block is composed of an edit (``Edit.jsx``) and a view (``View.jsx``) components.

Create your first tile in the project by adding these two components in a new directory in ``src/components/Tiles/MainTile``.
This is the ``Edit.jsx``:

.. code-block:: jsx

    import React from 'react';

    const Edit = props => {
      return <div>I'm the tile edit component!</div>;
    };

    export default Edit;

and the ``View.jsx``.

.. code-block:: jsx

    import React from 'react';

    const View = props => {
      return <div>I'm the tile view component!</div>;
    };

    export default View;


Blocks settings
---------------

We need to configure the project to make it aware of new tiles by adding it to the tiles object configuration:
So we add this lines to the ``config.js`` in the root of our project.

.. code-block:: js

    import MainSliderView from '@package/components/Tiles/MainSlider/View';
    import MainSliderEdit from '@package/components/Tiles/MainSlider/Edit';
    import sliderSVG from '@plone/volto/icons/slider.svg';

    ...

    const customTiles = {
      mainslider: {
        id: 'mainslider',
        title: 'Main Slider',
        icon: sliderSVG,
        group: 'common',
        view: MainSliderView,
        edit: MainSliderEdit,
        restricted: false,
        mostUsed: true,
        security: {
          addPermission: [],
          view: [],
        },
      },
    };

    export const tiles = {
      ...defaultTiles,
      tilesConfig: { ...defaultTiles.tilesConfig, ...customTiles },
    };

We add this also, for fulfill all our i18n requirements:

.. code-block:: js

    import { defineMessages } from 'react-intl';

    ...

    defineMessages({
      mainslider: {
        id: 'Main Slider',
        defaultMessage: 'Main Slider',
      },
    });

Our new tile should be ready to use in the editor.
