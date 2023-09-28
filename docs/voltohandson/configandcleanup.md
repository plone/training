---
myst:
  html_meta:
    'description': 'Learn how to edit the main config file of your project'
    'property=og:description': 'Learn how to edit the main config file of your project'
    'property=og:title': 'Edit config and site cleanup'
    'keywords': 'Plone, Volto, Training, config, Title Block'
---

# Edit config and site cleanup

## site cleanup

Before we want to add our first Volto Block we want to get rid of most of all the blocks from the Volto default frontpage. You can delete those blocks in edit mode by using the trashcan symbol. You will notice that you will be able to delete all blocks except the title block. That is because it is set as "required" in the Volto default configuration. To change this you will have to amend this.

```{hint}
Make sure you save your page after deleting all Blocks and before editing the `config`
```

## Making the Title block deletable

The config will be located inside the `config.js` folder in your policy addons `src` directory. Inside you will find the following code:

```js
const applyConfig = (config) => {

  return config;
};

export default applyConfig;

```

To enable removing the title block you only need to add the following line to override the original `requiredBlocks` array inside the `applyConfig` function:

```js
const applyConfig = (config) => {
  config.blocks.requiredBlocks = [];

  return config;
};

export default applyConfig;
```

```{hint}
You can find all default configurations in your `ommelette/src/config/`.
```
