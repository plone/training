---
myst:
  html_meta:
    "description": ""
    "property=og:description": ""
    "property=og:title": ""
    "keywords": ""
---

(volto-addon-label)=

# Using Volto add-ons

````{card} Frontend chapter

For Plone backend add-ons see chapter {ref}`add-ons-label`
````


(add-ons-volto-overview-label)=

## Awesome Volto Add-ons

Add-ons enrich a Volto app with specialized blocks, themes, integration of non-Volto Node packages, and more.
A selection of add-ons can be found on:

- [Awesome Volto](https://github.com/collective/awesome-volto/blob/main/README.md#addons)
- [npm #volto-addon](https://www.npmjs.com/search?q=keywords:volto-addon)
- [github #volto-addon](https://github.com/search?o=desc&q=%23volto-addon&s=&type=Repositories)

Some add-ons do require a backend add-on, some do not.
A backend add-on is needed for a content type or a `REST API endpoint`.

Two examples:

[`@eeacms/volto-matomo`](https://www.npmjs.com/package/@eeacms/volto-matomo) integrates Matomo with Volto sites.
No backend add-on is needed.
The add-on integrates the code snippet from `Matomo` into your pages to ping your web stats installation.

[`@rohberg/volto-slate-glossary`](https://github.com/rohberg/volto-slate-glossary) adds tooltips to selected pages according a given glossary.
As it depends on a permanent glossary, it communicates with the backend add-on [`collective.glossary`](https://pypi.org/project/collective.glossary/).
The Volto add-on provides, aside from the tooltips, a UI to edit the glossary.


## Install an add-on

Here is how you would install a Volto add-on in your app:

Add-ons that are already released on [npm](https://www.npmjs.com):

: Update `package.json`:
  ```{code-block} json
  :emphasize-lines: 5

  "dependencies": {
    "@plone/volto": "workspace:*",
    "@plone/registry": "workspace:*",
    "volto-ploneconf": "workspace:*",
    "@eeacms/volto-matomo": "^5.0.0"
  },
  ```

: Update `volto.config.js`:
  ```{code-block} js
  :emphasize-lines: 1

  const addons = ['@eeacms/volto-matomo', 'volto-ploneconf'];
  const theme = '';

  module.exports = {
    addons,
    theme,
  };
  ```

Add-ons that are **not yet released** on `npm` but available on `Github`:

: Update `package.json`:
  ```{code-block} json
  :emphasize-lines: 5

  "dependencies": {
    "@plone/volto": "workspace:*",
    "@plone/registry": "workspace:*",
    "volto-ploneconf": "workspace:*",
    "@foo/volto-bar-block": "github:foo/volto-bar-block#x.y.z"
  },
  ```

: Update `volto.config.js`:
  ```{code-block} js
  :emphasize-lines: 1

  const addons = ['@foo/volto-bar-block', 'volto-ploneconf'];
  const theme = '';

  module.exports = {
    addons,
    theme,
  };
  ```

Install the new add-on and restart Volto:

```shell
make install
make start
```


(add-ons-volto-backedupbyplone-label)=

## Complementing Volto with Plone add-ons

With some additional features of Volto add-ons in place, where do we need to work if there is more that add-ons do not already implement?
With the split of Plone in backend and frontend, the backend Plone is still the place to shape your data model.
For our training story 'Platform for a Plone Conference' we need to model the content type talk.
So in an earlier {doc}`dexterity` chapter we created a **new Plone Python add-on** `ploneconf.site` that adds the content type `talk`.
And in chapter {doc}`volto_talkview` we created the view for a talk in our custom Volto add-on `volto-ploneconf`.
