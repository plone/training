---
myst:
  html_meta:
    "description": ""
    "property=og:description": ""
    "property=og:title": ""
    "keywords": ""
---

# Mosaic

In this section we will:

- create a *home page* layout,
- create a *specific talk detail* layout.

Topics covered:

- Create custom layouts.
- Manage layouts.
- Use the layout editor.

## What is Mosaic?

- A Plone add-on,
- which allows managing layouts from the Plone interface.

## Some Comparisons

```{only} presentation
- It allows to manage the *layout*, not the *design* (unlike Diazo).
- It can manage the layout of *any* page, it does not provide a specific layout-enabled content type (like {py:mod}`collective.cover`).
```

```{only} not presentation
- Compared to Diazo:

  Diazo enables theming our Plone site by providing CSS, images,
  and HTML templates.
  It will apply to the entire page (footer, main content, portlets, etc.).

  Mosaic uses the grid provided by our design to dynamically build specific
  content layouts.

- Compared to {py:mod}`collective.cover`:

  {py:mod}`collective.cover` provides a specific content-type
  (a "Cover page") where we can manage the layout in order to build our home page.

  Mosaic does not provide any content-type, it allows to edit any existing content layout.
```

## Installation

````{sidebar} On An Existing Plone Buildout
If you already have your own Plone installation you can
install Mosaic by customizing it as follows:

Modify {file}`buildout.cfg` to add Mosaic as a dependency

```ini
eggs =
    ...
    plone.app.mosaic

versions =
    ...
    plone.tiles = 1.8.0
    plone.subrequest = 1.7.0
    plone.app.tiles = 3.0.0
    plone.app.standardtiles = 2.0.0rc1
    plone.app.blocks = 4.0.0rc1
    plone.app.drafts = 1.1.1
    plone.app.mosaic = 2.0.0rc1
```

Run your buildout

```shell
bin/buildout -N
```

Then go to {menuselection}`Site Setup --> Add-ons` and Mosaic {guilabel}`Install`.
````

We will use a [Plone pre-configured Heroku instance](https://github.com/collective/training-sandbox).

Once deployed, create a Plone site, then go to the {menuselection}`Site Setup --> Add-ons` and Mosaic {guilabel}`Install`.

## Principle

The basic component of a Mosaic based layout is called a tile.
A layout is a combination of several tiles.

A tile is a dynamic portion of a web page, it can be a text element, an image, a field, etc.

Mosaic provides an editor able to position tiles across our theme's grid.

## The Mosaic Editor

To enable the Mosaic editor on a content item change its default display as follows:
go to {menuselection}`Display --> Mosaic layout`.

You have now enabled the Mosaic editor as a replacement for the default edit form.

Click on {guilabel}`Edit`. If this is the first time editing the current item, you will be prompted to select a layout.

```{image} _static/mosaic-select-layout.png
```

Choose a layout.

This editor allows to change our content fields content (like the regular Plone form),
but the fields are rendered into the view layout and they are edited in-place.

```{image} _static/mosaic-editor.png
```

The top bar offers different buttons:

- {guilabel}`Save`, to save our field entries.
- {guilabel}`Cancel`, to cancel our changes.
- {guilabel}`Properties`, to access the content properties: it displays the regular Plone form tabs, but the fields currently involved in the layout are hidden.
- {guilabel}`Layout`, to manage the content layout.

### Exercise 1 - Change The Layout Of The Front Page

Go to the front page of the website and update the layout
as follows:

1. Activate {menuselection}`Display --> Mosaic layout`.
2. {guilabel}`Edit` and select the "*Document*" layout.
3. Then select {menuselection}`Layout --> Customize`.
4. Add a *Document Byline* to the bottom of the layout {menuselection}`Insert > Document Byline`.
5. Click {guilabel}`Save`.

In the context of the Mosaic Editor, do you know the difference between {guilabel}`Save` and {menuselection}`Layout --> Save`?

## Change The Content Layout

If we click on {menuselection}`Layout --> Change`, we can choose the layout we want for our content.
The choices are restricted to the layout applicable to the current content-type.

For instance for a *Page*, Mosaic proposes (by default) two layouts: *Basic* and *Document*.

```{image} _static/mosaic-select-layout.png
```

## Customize A Content Layout

If we click on {menuselection}`Layout --> Customize`, the Mosaic editor switches to the layout mode,
where we can still change our field values, but also change the layout:

- by hovering the page content, existing tiles are highlighted and we can drag & drop them in different places,
- by clicking in a tile, we can edit its content,
- by clicking outside the currently edited tile, we disable the edit mode.

In layout mode, the top bar contains two extra buttons:

- {guilabel}`Format`, which provides different simple formatting options for tiles (text padding, floating) or for rows (change background color),
- {guilabel}`Insert`, which allows to add new tiles to our layout.

## The Tiles

Mosaic provides the following tiles:

- Structure tiles:

  > - heading,
  > - subheading,
  > - text,
  > - table,
  > - bulleted list,
  > - numbered list,
  > - table of contents,
  > - navigation: this tile displays a navigation menu. Its settings can be changed in a modal window (click on the {guilabel}`i` button on the bottom-right corner to display the modal),

- Media:

  > - image,
  > - embed: it allows to display any remote embeddable content (like a YouTube video for instance),
  > - attachment,

- Fields: all the existing fields of the current content,

- Applications: for now, there is only Discussion, which shows the discussion form (discussion needs to be enable in the site setup),

- Properties:

  > - document byline,
  > - related contents,
  > - keywords,

- Advanced:

  > - content listing: this is a collection-like tile. It allows to list all contents matching given criteria (which be edited in the modal window),
  > - existing content: it allows to display any content item in a tile.
  > - if Rapido is installed, there is also a Rapido tile, which allows to display any Rapido block.

### Exercise 2: Customize The Home Page Layout

Create an attractive layout for the home page.

```{dropdown} Solution
:animate: fade-in-slide-down
:icon: question

- Go to the {guilabel}`Display` menu and select {guilabel}`Mosaic layout`,
- Click {guilabel}`Edit`,
- Click on {menuselection}`Layout --> Customize`,
- Change the layout,
- Click {guilabel}`Save`.
```

## Create A Reusable Layout

When the layout has been customized, the {guilabel}`Layout` menu offers a {guilabel}`Save` action.

This action allows to save the current layout as a reusable layout.

If {guilabel}`Global` is checked, the layout will be usable by any user (else it is restricted to the current user).

The layout is associated with the current content type. By default it will not be usable for other content types.

Once saved, our layout will be listed with the other available layouts when we click on {menuselection}`Layout --> Change`.

### Exercise 3: Create A Layout For Talks

```{note}
This exercise assumes that you have created a content type called "Talk".
You can quickly create one by the following the steps in the `Dexterity: Creating TTW content types <dexterity1-create-ttw-label-ttw>` documentation.
```

Create an attractive layout for a talk, save it and reuse it for another talk.

```{dropdown} Solution
:animate: fade-in-slide-down
:icon: question

- customize a talk layout (see Exercise 2),
- click on :menuselection:{menuselection}`Layout --> Save`,
- enter its title: "Talk", and select "Global",
- click {guilabel}`Save`,
- navigate to another talk,
- go to {guilabel}`Display` menu and select "Mosaic layout",
- click {guilabel}`Edit`,
- click on {menuselection}`Layout --> Change`,
- choose "Talk".
```

## Manage Custom Layouts

Custom layouts can be managed from the Plone control panel:

- click on {menuselection}`user menu --> Site settings`,
- click on {guilabel}`Mosaic Layout Editor` (in the last section, namely {guilabel}`Add-on configuration`),

In the third tab of this control panel, named {guilabel}`Show/hide content layouts`, we can see the existing layouts, their associated content types, and we can deactivate (or re-activate) them by clicking on {guilabel}`Hide` (or {guilabel}`Show`).

In the first tab, named {guilabel}`Content layouts`, there is a source editor.

By editing {file}`manifest.cfg`, we can assign a layout to another content type by changing the `for =` line. If we remove this line, the layout is available for any content type.

We can also delete the layout section from {file}`manifest.cfg`, and the layout will be deleted (if we do so, it is recommended to delete its associated HTML file too).

Deleting a custom layout can also be managed in another way:

% missing?

Note: the second tab, named {guilabel}`Site layouts`, is not usable for now.

## Edit The Layout HTML Structure

In the Mosaic Layout Editor's first tab ({guilabel}`Content layouts`), {file}`manifest.cfg` is not the only editable file.

There are also some HTML files. Each of them corresponds to a layout and they represent what we have built by drag & dropping tiles in our layouts.

Using the code editor, we can change this HTML structure manually instead of using the WYSIWIG editor.

Layouts are implemented in regular HTML using nested `<div>` elements and specific CSS classes.
Those classes are provided by the Mosaic grid which works like any CSS grid:

- structure:
  : - `mosaic-grid-row`
    - `mosaic-grid-cell`
- sizes:
  : - `mosaic-width-full`
    - `mosaic-width-half`
    - `mosaic-width-quarter`
    - `mosaic-width-three-quarters`
    - `mosaic-width-third`
    - `mosaic-width-two-thirds`
- positions:
  : - `mosaic-position-leftmost`
    - `mosaic-position-third`
    - `mosaic-position-two-thirds`
    - `mosaic-position-quarter`
    - `mosaic-position-half`
    - `mosaic-position-three-quarters`

## Import Layouts

We might want to work on a layout on our development server, and then be able to deploy it on our production server.

We can achieve that using the Mosaic editor control panel, which allows to copy the layout HTML structure and its declaration in {file}`manifest.cfg`.
