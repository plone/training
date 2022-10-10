---
myst:
  html_meta:
    "description": ""
    "property=og:description": ""
    "property=og:title": ""
    "keywords": ""
---

# Before Running the Import

Some development may need to be done in your new Plone site before running the first import.
This will mostly be the case if you are migrating custom content types.
The custom types will need to be in your new site prior to running the import.

The easiest way to import the custom types will be to set up the new type with the same type name and field names as the old site.
This way, even if you are migrating from {term}`Archetypes` to {term}`Dexterity`,
no custom code needs to be added to the import.

If you need to change the type name or field names, it's no big deal.
We'll cover how to handle that switch in the import.
The important thing is that you get the new custom content types built.

If you plan on migrating using only Plone's default content types,
then you only need to set up your new buildout with a migration package.
See <https://github.com/plone/simple-plone-buildout> if you need a place to get started with buildout.
