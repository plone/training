.. _voltohandson-blocks-label:

==============
Blocks anatomy
==============

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
