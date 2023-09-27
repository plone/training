---
myst:
  html_meta:
    "description": "Define what the page you are creating should look like in the end of the training"
    "property=og:description": "Define what the page you are creating should look like in the end of the training"
    "property=og:title": "Project requirements"
    "keywords": "Plone, Volto, Training, Requirements"
---

(voltohandson-customcss-label)=

# Project requirements

Our hands-on exercise is to recreate the 2023 version of [plone.org](https://plone.org) or rather a set of parts of the site that are suited to show off different ways you can customize Volto. These include
- Theme (Footer, Header, Breadcrumbs)
- Highlight-Slide
- News Listing
- Release Announcement

The screenshot below shows the frontpage of `plone.org` (as of 2023 just before Plone conf) with the areas, we will recreate marked in red.

```{image} _static/ploneorg-frontpage.png
:align: center
:alt: plone.com theme
```

## Tasks

These are the tasks we will go through:

- Set up CSS basics
- Customize the header and the footer
- Create a static Slider that shows current Highlights from the Plone community
- Edit your projects config
- Create a new Block that shows an configurable logo
- Create new listing block template to show event items in a grid like view with buttons on the side
- Create a new View for a new content type "Plone Release"
- Add translatable strings to your project
- Add a new Addon to the project and customize it

## Training ressources and assets

There are a few files, mostly images, that you will need to recreate for the `plone.org` page.
They are currently available from this [location in github](https://github.com/plone/training/tree/main/docs/voltohandson/ressources).
