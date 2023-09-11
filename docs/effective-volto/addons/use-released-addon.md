---
myst:
  html_meta:
    "description": "Configure a released Volto Add-on in your project"
    "property=og:description": "Configure a released Volto Add-on in your project"
    "property=og:title": "Configure a released Volto Add-on in your project"
    "keywords": "Volto, Plone, Volto add-on"
---

# Add a third-party released Volto Add-on in your project

1. Add the JS package as a dependency to your project:

```
yarn add <name_of_addon>
```

2. Update the `package.json` to add the package name as a Volto addon:

```json
"addons": [
    "@kitconcept/volto-blocks-grid"
],

```

If, instead, you want to add a Volto addon as a dependency to one of your
development addons, you should run:

```
yarn workspace <myaddon> add <otheraddon>
```

And then you can edit the `package.json` of your development addon and add the
other Volto addon to the `addons` list (create it if it's not already there).
