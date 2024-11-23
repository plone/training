---
myst:
  html_meta:
    "description": "Adding New Block"
    "property=og:description": "Adding New Block"
    "property=og:title": "Adding New Block"
    "keywords": "Plone, Volto, Training, Volto Light Theme, Integrate, block"
---

# Integrate a new block

In this training module, we'll learn how to integrate the `@plone-collective/volto-relateditems-block` into VLT. This block allows you to create links to related content in your Plone site.

## Install `@plone-collective/volto-relateditems-block`

To install the related items block, make sure you are in the {file}`frontend/packages/volto-my-project` folder, and use the following command:

```{note}
For now we'll be using an `alpha` release, so we need to specify the correct version.
```

```shell
pnpm install @plone-collective/volto-relateditems-block@1.0.0-alpha.1
```

After installation, ensure that the add-on is included in the `addons` key of your project's {file}`package.json`:

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

You'll need to restart your Plone frontend to see the changes.

That's it! Your project should now be using `@plone-collective/volto-relateditems-block`, which shows related items for the content as a list of links.
