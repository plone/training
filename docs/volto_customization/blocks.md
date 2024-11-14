---
myst:
  html_meta:
    "description": "How to extend volto blocks"
    "property=og:description": "How to extend volto blocks"
    "property=og:title": "Extend volto blocks"
    "keywords": "Volto, Training, Extend block"
---

# Extend Volto blocks

There are various ways of extending Volto blocks.
Component shadowing (see last chapter) is a very basic to customize components in Volto.
But it comes with its own problems like keeping the shadowed component up to date with latest fixes and features of newer Volto versions.
Instead of shadowing components we can:

- Change the block-config
- Extend blocks by adding new block-variations
- Write add schemaEnhancer to modify blocks schema

Let us first change the View of the teaser block which we already have in Volto core by changing the block-configuration.
In our add-on `volto-teaser-tutorial` we will step by step extend each component that we have in Volto core.

The most simple customization is the View of the Teaser. The Volto core teaser block configration (in `/frontend/core/packages/volto/src/config/Blocks.jsx`) looks like:

```js
  teaser: {
    id: 'teaser',
    title: 'Teaser',
    icon: imagesSVG,
    group: 'common',
    view: TeaserViewBlock,
    edit: TeaserEditBlock,
    restricted: false,
    mostUsed: true,
    sidebarTab: 1,
    blockSchema: TeaserSchema,
    dataAdapter: TeaserBlockDataAdapter,
    variations: [
      {
        id: 'default',
        isDefault: true,
        title: 'Default',
        template: TeaserBlockDefaultBody,
      },
    ],
  },
```

Every block in Volto has Edit and View components.
You can customize these individually by either shadowing or directly in the confuguration (`index.js` of your add-on) like this:

```js
import MyTeaserView from "volto-teaser-tutorial/components/Blocks/Teaser/View";

const applyConfig = (config) => {
  config.blocks.blocksConfig.teaser.view = MyTeaserView;
  return config;
};

export default applyConfig;
```

Of course we need to add our custom `MyTeaserView` component in our add-on.
From the root of the project that is `packages/volto-teaser-tutorial/src/components/Blocks/Teaser/View.jsx`:

```jsx
import TeaserBody from "@plone/volto/components/manage/Blocks/Teaser/Body";
import { withBlockExtensions } from "@plone/volto/helpers";

const TeaserView = (props) => {
  return <TeaserBody {...props} extraProps={{ foo: "bar" }} />;
};

export default withBlockExtensions(TeaserView);
```

Here, the View component renders a TeaserBody which will be a result of an active variation, we will come to that in later chapters.
