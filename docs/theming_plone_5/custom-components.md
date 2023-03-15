---
myst:
  html_meta:
    "description": ""
    "property=og:description": ""
    "property=og:title": ""
    "keywords": ""
---

# Creating Custom Components

Plone is a powerful system and it provides many interesting features and function.
To dive into this, we recommend to go through the `Mastering Plone 5: Development` of the training.

For theming the most relevant part are the following components, which render some parts of Plone, you may want to customize or build new once.

## Views

In Plone a view usually consists of multiple components, a Python class based on BrowserView and a template which renders the markup.
Is is possible to have a template which is only a view.

It is also possible to have a view which has no template, but renders the output by it self, as JSON for example.

For more details about views and there possibilities see the view sections of the `Mastering Plone 5: Development` chapters.

## Viewlets

Viewlets are small pieces which are rendered inside a view.
They are registered for an ordered ViewletManager, which renders all Viewlets in the given order.
You can change the order even TTW (Through-The-Web) or via configuration.

A Viewlet consists of a Viewlet Python class and a template.

Plone has default Viewlets and ViewletManagers like ContentAbove and BelowContent which you can use to register small pieces of functionality.

For an overview of existing Viewlets and ViewletManagers look at the `/@@manage-viewlets` view.

For more details about Viewlets/ViewletManagers and their possibilities, see {doc}`/mastering-plone/viewlets_1`.

## Portlets

Portlets are a very flexible way of providing context related information in the right, left or footer area.

For details on how to use, configure and create Portlets,
look into the Plone docs [Plone docs Portlet sections](https://5.docs.plone.org/develop/plone/functionality/portlets.html).
