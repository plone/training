---
myst:
  html_meta:
    "description": "Adding Installing New Block"
    "property=og:description": "Adding Installing New Block"
    "property=og:title": "Adding Installing New Block"
    "keywords": "Plone, Volto, Training"
---


# Adding a New Block

In this training module, we'll learn how to integrate the @plone-collective/volto-relateditems-block into VLT. This block allows you to easily create links to related content in your Plone site.

## Installing *@plone-collective/volto-relateditems-block*

To install the related items block, make sure you are in the `frontend/packages/volto-my-project` folder, and use the following command:

```shell
pnpm install @plone-collective/volto-relateditems-block
```

After installation, ensure that the addon is included in the addons key of your project's package.json:

```json
  "addons": [
    "@eeacms/volto-accordion-block",
    "@kitconcept/volto-button-block",
    "@kitconcept/volto-heading-block",
    "@kitconcept/volto-highlight-block",
    "@kitconcept/volto-introduction-block",
    "@kitconcept/volto-separator-block",
    "@kitconcept/volto-slider-block",
    "@plone-collective/volto-relateditems-block",
    "@kitconcept/volto-light-theme"
  ],
```

  That's it! Your project should now be using @plone-collective/volto-relateditems-block, which shows related items for the content as a list of links.