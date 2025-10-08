---
myst:
  html_meta:
    "description": "How to customize content-type Views and other Components"
    "property=og:description": "How to customize content-type Views and other Components"
    "property=og:title": "Customize Content-type Views and other Components"
    "keywords": "Volto, Customize, Shadowing"
---

# Customize Content-type Views and other Components

You can customize all components of Volto using a technique called component shadowing.

Basically you copy the component (i.e. the file) to a folder `customizations` keeping the same folder-structure and the overridden file will replace the original.

```{tip}
Those familiar with Plone's JBOT (just a bunch of templates) customizing add-on will recognize this pattern since it works the same way, except that here you have to create exactly the same folder structure hierarchy of the original component instead of using the dotted notation used in JBOT overrides.
```

To avoid duplication we simply follow the chapter {ref}`volto-overrides-label` of the Mastering Plone Training.

In that chapter you learn how to override the logo, the footer, the news-item view and the default listing-block.

The only difference is whenever we add new files instead of adding them to the project we add the to our add-on.

For example when we customize the News Item View instead of adding the override as:

`src/customizations/components/theme/View/NewsItemView.jsx`

we add it as

`packages/volto-teaser-tutorial/src/customizations/components/theme/View/NewsItemView.jsx`.

Both paths work fine though, we just want to go all-in with the add-on approach.

```{seealso}
- {ref}`voltohandson-header-component-label` (Volto Hands-On Training)
- {doc}`plone6docs:volto/development/customizing-components` (Plone Frontend Documentation)
- {doc}`plone6docs:volto/development/customizing-views` (Plone Frontend Documentation)
```
