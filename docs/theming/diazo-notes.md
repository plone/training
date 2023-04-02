---
myst:
  html_meta:
    "description": "Diazo notes"
    "property=og:description": "Diazo notes"
    "property=og:title": "Diazo notes"
    "keywords": "Diazo, Plone, training"
---

# Diazo notes

## create addon and theme

- plonecli create addon
- plonecli add theme

## create content

- add Folders with Pages, except for Products > Folder + Collection

## integrate static theme

- download and extract theme
- inspect CSS and JS in index.html
- yarn install
- npm run build
- merge CSS in a SCSS file and register it in manifest
- show static theme in Plone

## add tinymce templates for some content sections

## add content types

- plonecli add content_type >> Product
- enable name from title behavior and basic behavior
- define CT schema: Text, Photo
- Add some products
- List Product in Collection
- plonecli add view >> ProductsView for ICollection and add it in FTI
- show title, description, text and photo in wanted markup


