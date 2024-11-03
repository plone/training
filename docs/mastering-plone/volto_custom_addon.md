---
myst:
  html_meta:
    "description": "Write your own Volto add-on"
    "property=og:description": "Write your own Volto add-on"
    "property=og:title": "Extending Volto with a custom add-on package"
    "keywords": "Plone, Volto, add-on, development"
---

(volto-custom-addon-label)=

# Extending Volto with a custom add-on package

````{card} Frontend chapter

See {ref}`voting-story-backend-package-label` for extending Plone with backend add-ons.
````

As soon as you have repeating needs in Volto projects, you will want to move the code to an add-on that can be applied to multiple projects. One of several ways to start with a new add-on is the [cookieplone](https://github.com/plone/cookieplone) Cookiecutter template.


(volto-custom-addon-preparation-label)=

If you haven't prepared 'cookieplone' already, see https://github.com/plone/cookieplone?tab=readme-ov-file#installation- for installation.


'cookieplone' creates an add-on that comes with a Volto app.
So you can start a Volto app right after creation of the add-on and proceed with developing your add-on.

```shell
pipx run cookieplone
```

Go to the app folder and run the embedding app with:

```shell
make start
```

You now have a Volto app running which includes the new add-on.

Open `packages/your-add-on` and start coding.


(volto-custom-addon-final-label)=

```{note} Step to the next chapter and come back here for a release.
We will create a new block type in the next chapter {doc}`volto_custom_addon2`.
We will do this in an add-on to apply the feature to multiple projects.
```

````{note}
Coming back here with the new block type, you can now release the new add-on to npm. 

```{code-block} console
make release
````

(volto-custom-addon-include-label)=

## Enrich an existing project with your new released add-on

You already released your add-on. Go on with {file}`package.json` and {file}`volto.config.js` and include your new add-on.

: Update `package.json`:
  ```{code-block} json
  :emphasize-lines: 5

  "dependencies": {
    "@plone/volto": "workspace:*",
    "@plone/registry": "workspace:*",
    "volto-ploneconf": "workspace:*",
    "@greenthumb/volto-qa-block": "^1.0.0"
  },
  ```

: Update `volto.config.js`:
  ```{code-block} js
  :emphasize-lines: 1

  const addons = ['@greenthumb/volto-qa-block', 'volto-ploneconf'];
  const theme = '';

  module.exports = {
    addons,
    theme,
  };
  ```

Modify versions as necessary.

Install new add-on and restart Volto:

```shell
make install
make start
```


## Create a new project with your new released add-on

This is the same procedure as creating an add-on.

```shell
pipx run cookieplone
```

Follow the steps from previous section {ref}`volto-custom-addon-include-label`.
