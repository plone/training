---
myst:
  html_meta:
    "description": "Adding Installing New Block"
    "property=og:description": "Adding Installing New Block"
    "property=og:title": "Adding Installing New Block"
    "keywords": "Plone, Volto, Training"
---


# Adding A New Block

In this training module, we will learn how to integrate the @plone-collective/volto-relateditems-block into the Volto-light-theme. This block allows you to easily create links to related content in your Plone site.

## Installing *@plone-collective/volto-relateditems-block*

To install the related items block, use the following command:

```bash
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
    "@kitconcept/volto-light-theme",
    "@plone-collective/volto-relateditems-block"
  ],
  ```

  That's it! Your project should now be using @plone-collective/volto-relateditems-block which shows the relateditems as link for this content.