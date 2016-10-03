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

    * It allows managing of the layout, not the design (like Diazo).
    * It can manage the layout of any page, it does not provide a specific layout-enabled content (like collective.cover).

.. only:: not presentation

    * Compare to Diazo:

        Diazo allows to theme our Plone site, by providing CSS, images, and HTML templates. And it will apply to the entire page (footer, main content, portlets, etc.).

        Mosaic uses the grid provided by our design to dynamically build specific content layouts.

    * Compare to collective.cover:

        collective.cover provides a specific content-type (a "Cover page") where we can manage the layout in order to build our homepage.

        Mosaic does not provide any content-type, it allows to edit any existing content layout.

Installation
------------

We will use a `Plone pre-configured Heroku instance <https://github.com/collective/training-sandbox>`_.

Once deployed, create a Plone site, and go to Plone control panel / Add-ons http://localhost:8080/Plone/prefs_install_products_form, and install Mosaic.

.. only:: not presentation

    Modify ``buildout.cfg`` to add Rapido as a dependency::

        eggs =
            ...
            plone.app.mosaic

        versions =
            ...
            plone.tiles = 1.5.2
            plone.app.tiles = 2.2.1
            plone.app.standardtiles = 1.0
            plone.app.blocks = 3.1.0
            plone.app.drafts = 1.0

    Run your buildout::

        $ bin/buildout -N

    Then go to Plone control panel / Add-ons http://localhost:8080/Plone/prefs_install_products_form, and install Mosaic.

Principle
---------

The basic component of a Mosaic based layout is called a tile.
A layout is a combination of several tiles.

A tile is a dynamic portion of a web page, it can be a text element, an image, a field, etc.

Mosaic provides an editor able to easily position tiles across our theme's grid.

The Mosaic editor
-----------------

To enable the Mosaic editor on a content item change its default display as follows: go to "Display" menu and select "Mosaic layout".

Now, when we click on "Edit", the default Plone edit form is replaced with the Mosaic editor.

This editor allows to change our content fields content (just like the regular Plone form), but the fields are rendered into the view layout and they are edited in-place.

.. TODO:: ADD SCREENSHOT HERE

The top bar offers different buttons:

- "Save", to save our field entries.
- "Cancel", to cancel our changes.
- "Properties", to access the content properties: it displays the regular Plone form tabs, but the fields currently involved in the layout are hidden.
- "Layout", to manage the content layout.

Change the content layout
-------------------------

If we click on "Layout" / "Change", we can choose the layout we want for our content.
The choices are restricted to the layout applicable to the current content-type.

For instance for a Page, Mosaic proposes (by default) two layouts: Basic and Document.

.. TODO:: ADD SCREENSHOT HERE

Customize a content layout
--------------------------

If we click on "Layout" / "Customize", the Mosaic editor switches to the layout mode, where we can still change our field values, but also change the layout:

- by hovering the page content, existing tiles are highlighted and we can drag & drop them in different places,
- by clicking in a tile, we can edit its content,
- by clicking outside the curently edited tile, we disable the edit mode.

In layout mode, the top bar contains two extra buttons:

- "Format", which provides different simple formatting options for tiles (text padding, floating) or for rows (change background color),
- "Insert", which allows to add new tiles to our layout.

The tiles
---------

Mosaic proposes the following tiles:

- Structure tiles:

    - heading,
    - subheading,
    - text,
    - table,
    - bulleted list,
    - numbered list,
    - table of contents,
    - navigation: this tiles displays a navigation menu, its settings can be changed in a modal window (click on the "i" button on the bottom-right corner to display the modal),

- Media:

    - image,
    - embed: it allows to display any remote embeddable content (like a YouTube video for instance),
    - attachment,

- Fields: all the existing fields of the current content,

- Applications: for now, there is only Discussion, which shows the discussion form (discussion needs to be enable in the site setup),

- Properties:

    - document byline,
    - related contents,
    - keywords,

- Advanced:

    - content listing: it is a collection-like tile, it allows to list all contents matching given criterias (criterias can be changed in the modal window),
    - existing content: it allows to display another content in a tile
    - if Rapido is installed, there is also a Rapido tile, which allows to display any Rapido block.

Exercise 1: Customize the home page layout
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Create an attractive layout for the home page.

..  admonition:: Solution
    :class: toggle

    - go to Display menu and select "Mosaic layout",
    - click Edit,
    - click on Layout / Customize,
    - change the layout,
    - click Save.

Create a reusable layout
------------------------

When the layout has been customized, the "Layout" menu offers a "Save" action.

This action allows to save the current layout as a reusable layout. 

If "Global" is checked, the layout will be usable by any user (else it is restricted to the current user).

The layout is associated to the current content type, by default it will not be usable for other content types.

Once saved, our layout will be listed with the other available layouts when we click on "Layout" / "Change".

Exercise 2: create a layout for talks
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Create an attractive layout for a talk, save it and reuse it for another talk.

..  admonition:: Solution
    :class: toggle

    - customize a talk layout (see Exercise 1),
    - click on Layout / Save,
    - enter its title: "Talk", and select "Global",
    - click Save,
    - navigate to another talk,
    - go to Display menu and select "Mosaic layout",
    - click Edit,
    - click on Layout / Change,
    - choose "Talk".

Manage custom layouts
---------------------
 
Custom layouts can be managed from the Plone control panel:

- click on user menu / Site settings,
- click on Mosaic Layout Editor (in the last section, named "Add-on configuration"),

In the third tab of this control panel, named "Show/hide content layouts", we can see the exitsing layouts, their associated content types, and we can deactivate (or re-activate) them by clicking on "Hide" (or "Show").

In the first tab, named "Content layouts", there is a source editor.

By editing ``manifest.cfg``, we can assign a layout to another content type by changing the ``for =`` line. If we remove this line, the layout is available for any content type.

We can also delete the layout section from ``manifest.cfg``, and the layout will be deleted (if we do so, it is recommended to delete its associated HTML file too).

Deleting a custom layout can also be managed in another way:

Note: the second tab, named "Site layouts", is not usable for now.


Edit the layout HTML structure
------------------------------
In the Mosaic Layout Editor's first tab ("Content layouts"), ``manifest.cfg`` is not the only editable file.

There is also some HTML files. Each of them corresponds to a layout and they represent what we have built by drag&dropping tiles in our layouts.

Using the code editor, we can change this HTML structure manually instead of using the WYSIWIG editor.

Layouts are implemented in regular HTML using nested `<div>` elements and specific CSS classes. Those classes are provided by the Mosaic grid which works as any CSS grid:

- structure:
    - mosaic-grid-row
    - mosaic-grid-cell
- sizes:
    - mosaic-width-full
    - mosaic-width-half
    - mosaic-width-quarter
    - mosaic-width-three-quarters
    - mosaic-width-third
    - mosaic-width-two-thirds
- positions:
    - mosaic-position-leftmost
    - mosaic-position-third
    - mosaic-position-two-thirds
    - mosaic-position-quarter
    - mosaic-position-half
    - mosaic-position-three-quarters

Import layouts
--------------

We might want to work on a layout on our development server, and then be able to deploy it on our production server.

We can achieve that using the Mosaic editor control panel, which allows to copy the layout HTML structure and its declaration in `manifest.cfg`.
