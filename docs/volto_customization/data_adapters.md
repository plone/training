### Enhance Teaser block with additional data

Teaser block has an ability to let user mutate or intercept block settings data from their customization. The `dataAdapter` field gets registered in Teaser configuration in order to acheive this.

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

The signature of `dataAdapter` is like this:

```js
export const TeaserBlockDataAdapter = ({
  block,
  data,
  id,
  onChangeBlock,
  value,
}) => {
  let dataSaved = {
    ...data,
    [id]: value,
  };
  if (id === "href" && !isEmpty(value) && !data.title && !data.description) {
    dataSaved = {
      ...dataSaved,
      title: value[0].Title,
      description: value[0].Description,
      head_title: value[0].head_title,
    };
  }
  onChangeBlock(block, dataSaved);
};
```

The above dataAdapter intercepts the blocksData and modifies its properties namely `title,description,head_title`. Note that you can also add new fields here.

We can register our own dataAdapter in place of this by maintaining same definition.

```{note}
In order for dataAdapters to work make sure the code of your block allows and consumes it in its implmentation.
```

The above Adapter gets consumed in [Data](https://github.com/plone/volto/blob/9667cf735e5c3e848de852d615941d98193e0a5e/src/components/manage/Blocks/Teaser/Data.jsx#L47) component of teaser block.

Let's register a new `dataAdapter` our config:

```js
config.blocks.blocksConfig.teaser.dataAdapter = myDataOwnAdapter;
```

In your data-adapter.js:

```js
export const myDataOwnAdapter = ({ block, data, id, onChangeBlock, value }) => {
  let dataSaved = {
    ...data,
    [id]: value,
  };
  if (id === "title" && !isEmpty(value) && !data.title) {
    dataSaved = {
      ...dataSaved,
      title: value[0].toUpperCase() + string.slice(1),
    };
  }
  onChangeBlock(block, dataSaved);
};
```

We are upperCasing the first letter of title in our blocksData. Make sure to call `onChangeBlock` at the end.