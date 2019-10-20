.. _voltohandson-introtoblocks-label:

======
Blocks
======

We will use Volto blocks (tiles) to compose the homepage.
We are in the process of replacing the term ``tile`` and use ``block`` everywhere, so bear with us during the migration process.
In some places the terms are not yet updated, especially code in both Volto and plone.restapi.

Brief introduction to Volto blocks
==================================

Volto features the Pastanaga Editor Engine, allowing you to compose a page visually using blocks.
The editor allows you to add, modify, reorder and delete blocks.
Blocks provide the user the ability to display content in an arbitrary way, although blocks can also define behavior and can have specific features.
Blocks are composed of two basic (and required) components: the Block edit and view components.

By default, Volto ships with the most basic set of Blocks, including Title, Text, Image, Video, and Maps.

.. note:: Volto Blocks are not enabled by default in Plone content types.
          However, the ``kitconcept.voltodemo`` package enables Blocks for the ``Document`` content type,
          so you will be able to use Blocks when you create or edit a page.

How to manually enable Blocks on a content type
===============================================

There is a behavior called ``Tiles`` made available by ``plone.restapi``.

1. Go to ``ControlPanel`` -> ``Dexterity Content Types``, select the content type.
2. Go to ``Behaviors``
3. Select the ``Tiles`` behavior
4. Save

Test the ``Tiles`` behavior for the content type you've just added it to, by creating a new object of that type from the Volto frontend (i.e. not from "classic" Plone).

Blocks anatomy
==============

Every Block is composed of an edit (``Edit.jsx``) component and a view (``View.jsx``) component.

Create your first block in the project by adding these two components in a new directory in ``src/components/Blocks/MainSlider``.
This is the ``Edit.jsx``:

.. code-block:: jsx

    import React from 'react';

    const Edit = props => {
      return <div>I'm the MainSlider edit component!</div>;
    };

    export default Edit;

and the ``View.jsx``.

.. code-block:: jsx

    import React from 'react';

    const View = props => {
      return <div>I'm the MainSlider view component!</div>;
    };

    export default View;

Block view component props
--------------------------

The view component of a block receives these props (properties) from the Blocks Engine:

  - id - the unique ID for the current block
  - properties - the current content
  - data - the data of the block (stored in the block itself)

You can use them to render the view component.

.. _voltohandson-introtoblocks-editprops-label:

Block edit component props
--------------------------

The edit component of a block receives these props from the Blocks Engine:

  - type - the type of the block
  - id - the unique ID for the current block
  - data - the data of the block (stored in the block itself)
  - selected - (Bool) true if the block is currently selected
  - index - the block index order in the list of blocks
  - pathname - the current URL pathname
  - onAddTile - handler for adding a block in the block list
  - onMutateTile - handler for mutating a block type into another
  - onChangeTile - handler for changing the data of that block
  - onSelectTile - handler for selecting the block
  - onDeleteTile - handler for deleting the block
  - onFocusPreviousTile - handler for focusing the previous block in the block list
  - onFocusNextTile - handler for focusing the next block in the block list
  - handleKeyDown - handler for managing press keys while the block is selected
  - onMoveTile - handler for moving blocks

You can use all these props to render your edit block and model its behavior.

Blocks settings
---------------

We need to configure the project to make it aware of a new block by adding it to the object configuration:
We add these lines to the ``config.js`` in the root of our project.

.. code-block:: js

    import MainSliderViewBlock from '@package/components/Blocks/MainSlider/View';
    import MainSliderEditBlock from '@package/components/Blocks/MainSlider/Edit';
    import sliderSVG from '@plone/volto/icons/slider.svg';

    ...

    const customTiles = {
      mainslider: {
        id: 'mainslider',
        title: 'Main Slider',
        icon: sliderSVG,
        group: 'common',
        view: MainSliderViewBlock,
        edit: MainSliderEditBlock,
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

We add this also, to fulfill all our i18n requirements:

.. code-block:: js

    import { defineMessages } from 'react-intl';

    ...

    defineMessages({
      mainslider: {
        id: 'Main Slider',
        defaultMessage: 'Main Slider',
      },
    });

Our new block should be ready to use in the editor.
