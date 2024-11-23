---
myst:
  html_meta:
    "description": "Extend the Volto Light Theme"
    "property=og:description": "Extend the Volto Light Theme"
    "property=og:title": "Extend the Volto Light Theme"
    "keywords": "Plone, Volto, Training, Extend, Volto Light Theme"
---

# Extend VLT

In this section we'll extend the VLT to create a "dark" aesthetic for our project. The same patterns can be applied for other visual identity cases.

## File structure

Let us start by setting up the recommended file structure. In your project add-on's {file}`src` folder, create a subfolder named {file}`theme`.
Inside {file}`theme` create two empty files named {file}`_main.scss` and {file}`_variables.scss`. Refer to the following file system diagram:

```console
src/
├── components
├── index.js
└── theme
    ├── _main.scss
    └── _variables.scss
```

Remember that if you add new files to your ptoject, it will be necessary to restart your Plone frontend.

### `_variables.scss`

{file}`_variables.scss` is where you can override the base theme SCSS variables.

```scss
:root {
    --primary-color: black;
    --primary-foreground-color: lemonchiffon;

    --secondary-color: darkslategrey;
    --secondary-foreground-color: lemonchiffon;

    --accent-color: darkslategrey;
    --accent-foreground-color: lemonchiffon;

    --link-color: lightblue;
}
```

### `_main.scss`

{file}`_main.scss` is where you should put any custom styles. You can also include other SCSS or CSS files, as follows:

```scss
@import 'variables';
```

## Block themes

Now we need to change the available themes for the blocks by adding the following definition inside the `applyConfig` function in our project's {file}`index.js`:

```js
config.blocks.themes = [
  {
    style: {
      '--theme-color': 'black',
      '--theme-high-contrast-color': 'darkslategrey',
      '--theme-foreground-color': 'lemonchiffon',
      '--theme-low-contrast-foreground-color': 'lightgrey',
    },
    name: 'default',
    label: 'Default',
  },
  {
    style: {
      '--theme-color': 'darkslategrey',
      '--theme-high-contrast-color': 'black',
      '--theme-foreground-color': 'lemonchiffon',
      '--theme-low-contrast-foreground-color': 'lightgrey',
    },
    name: 'green',
    label: 'Green',
  },
];
```

## Extend add-on styles

The theme provides the ability to extend or modify existing components. Let's create one more file named {file}`relatedItems.scss` to add specific styles for the add-on, as follows:

```console
src/
├── components
├── index.js
└── theme
    ├── blocks
        └── _relatedItems.scss
    ├── _main.scss
    └── _variables.scss
```

In the new {file}`_relatedItems.scss`, let's fix the text color, and add background color to the `.inner-container` element with the variables `--primary-foreground-color` and `--theme-high-contrast-color`. Lastly, let's use `--link-foreground-color` for the related items links:

```scss
.block.relatedItems {
  .inner-container {
    background: var(--theme-high-contrast-color);
    padding: 3rem;

    h2.headline {
        color: var(--primary-foreground-color);
    }

    ul.items-list {
      color: var(--primary-foreground-color);
      li a {
        color: var(--link-foreground-color);
      }
    }
  }
}
```

And now we need to add {file}`_relatedItems.scss` in {file}`_main_.scss`:

```scss
@import 'blocks/relatedItems';
@import 'variables';
```

## Enhancing a block schema

To be able to use the Block Width widget with our Related Items block, we need to add it to the block schema.
To do this we'll use a `schemaEnhancer`. A schema enhancer is a function that receives an object with `formData` (the block `data`), the `schema` (the original schema that we want to tweak), and the injected `intl` (to aid with internationalization).

Usually we would want to keep the schema enhancers in individual files per block, after which they can be imported to the {file}`index.js`. For this example we'll leave everything in the same file:

```js
import { defineMessages } from 'react-intl';
import { composeSchema } from '@plone/volto/helpers/Extensions';
import { defaultStylingSchema } from '@kitconcept/volto-light-theme/components/Blocks/schema';
import { addStyling } from '@plone/volto/helpers/Extensions/withBlockSchemaEnhancer';

const messages = defineMessages({
  BlockWidth: {
    id: 'Block Width',
    defaultMessage: 'Block Width',
  },
});

const applyConfig = (config) => {
  config.settings = {
    ...config.settings,
    isMultilingual: false,
    supportedLanguages: ['en'],
    defaultLanguage: 'en',
  };

  config.blocks.themes = [
    {
      style: {
        '--theme-color': 'black',
        '--theme-high-contrast-color': 'darkslategrey',
        '--theme-foreground-color': 'lemonchiffon',
        '--theme-low-contrast-foreground-color': 'lightgrey',
      },
      name: 'default',
      label: 'Default',
    },
    {
      style: {
        '--theme-color': 'darkslategrey',
        '--theme-high-contrast-color': 'black',
        '--theme-foreground-color': 'lemonchiffon',
        '--theme-low-contrast-foreground-color': 'lightgrey',
      },
      name: 'green',
      label: 'Green',
    },
  ];

  const relatedItemsEnhancer = ({ formData, schema, intl }) => {
    addStyling({ schema, intl });

    schema.properties.styles.schema.fieldsets[0].fields = [
      'blockWidth:noprefix',
      ...schema.properties.styles.schema.fieldsets[0].fields,
    ];
    schema.properties.styles.schema.properties['blockWidth:noprefix'] = {
      widget: 'blockWidth',
      title: intl.formatMessage(messages.BlockWidth),
      default: 'default',
      filterActions: ['narrow', 'default'],
    };
    return schema;
  };

  config.blocks.blocksConfig.relatedItems = {
    ...config.blocks.blocksConfig.relatedItems,
    schemaEnhancer: composeSchema(defaultStylingSchema, relatedItemsEnhancer),
  };

  return config;
};

export default applyConfig;
```

Finally, let's wire the width classes for our block in the file {file}`_relatedItems.scss`:

```scss
.block.relatedItems {
    margin-right: auto;
    margin-left: auto;

  .inner-container {
    background: var(--theme-high-contrast-color);
    padding: 3rem;

    h2.headline {
        color: var(--primary-foreground-color);
    }

    ul {
      color: var(--primary-foreground-color);
      li a {
        color: var(--link-foreground-color);
      }
    }
  }

  &.has--block-width--narrow {
    max-width: var(--narrow-container-width) !important;
  }

  &.has--block-width--default {
    max-width: var(--default-container-width) !important;
  }
}

.block-editor-relatedItems {
  &.has--block-width--narrow .block .block .block {
    max-width: var(--narrow-container-width) !important;
  }

  &.has--block-width--default .block .block .block {
    max-width: var(--default-container-width) !important;
  }
}
```


## Set themes for one block

To demonstrate this feature, we'll add a custom list of themes just for the Related Items block, which will include one more theme called `Blue`. Add the property `themes` to the `relatedItems` block in the `blocksConfig` object:

```js
import { defineMessages } from 'react-intl';
import { composeSchema } from '@plone/volto/helpers/Extensions';
import { defaultStylingSchema } from '@kitconcept/volto-light-theme/components/Blocks/schema';
import { addStyling } from '@plone/volto/helpers/Extensions/withBlockSchemaEnhancer';

const messages = defineMessages({
  BlockWidth: {
    id: 'Block Width',
    defaultMessage: 'Block Width',
  },
});

const applyConfig = (config) => {
  config.settings = {
    ...config.settings,
    isMultilingual: false,
    supportedLanguages: ['en'],
    defaultLanguage: 'en',
  };

  config.blocks.themes = [
    {
      style: {
        '--theme-color': 'black',
        '--theme-high-contrast-color': 'darkslategrey',
        '--theme-foreground-color': 'lemonchiffon',
        '--theme-low-contrast-foreground-color': 'lightgrey',
      },
      name: 'default',
      label: 'Default',
    },
    {
      style: {
        '--theme-color': 'darkslategrey',
        '--theme-high-contrast-color': 'black',
        '--theme-foreground-color': 'lemonchiffon',
        '--theme-low-contrast-foreground-color': 'lightgrey',
      },
      name: 'green',
      label: 'Green',
    },
  ];

  const relatedItemsEnhancer = ({ formData, schema, intl }) => {
    addStyling({ schema, intl });

    schema.properties.styles.schema.fieldsets[0].fields = [
      'blockWidth:noprefix',
      ...schema.properties.styles.schema.fieldsets[0].fields,
    ];
    schema.properties.styles.schema.properties['blockWidth:noprefix'] = {
      widget: 'blockWidth',
      title: intl.formatMessage(messages.BlockWidth),
      default: 'default',
      filterActions: ['narrow', 'default'],
    };
    return schema;
  };

  config.blocks.blocksConfig.relatedItems = {
    ...config.blocks.blocksConfig.relatedItems,
    schemaEnhancer: composeSchema(defaultStylingSchema, relatedItemsEnhancer),
    themes: [
      ...config.blocks.themes,
      {
        style: {
          '--theme-color': 'midnightblue',
          '--theme-high-contrast-color': 'black',
          '--theme-foreground-color': 'lemonchiffon',
          '--theme-low-contrast-foreground-color': 'lightgrey',
        },
        name: 'blue',
        label: 'Blue',
      },
    ],
  };

  return config;
};

export default applyConfig;
```

## Conclusion

Understanding how to extend VLT will help you take advantage of the system and quickly create consistent and flexible designs.
