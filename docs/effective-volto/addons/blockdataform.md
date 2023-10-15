---
myst:
  html_meta:
    "description": "Create a block using `BlockDataForm`"
    "property=og:description": "Create a block using `BlockDataForm`"
    "property=og:title": "Create a block using `BlockDataForm`"
    "keywords": "Volto, Plone, BlockDataForm, Volto block extensions"
---

# Create a block using `BlockDataForm`

The `BlockDataForm` component renders a form fully integrated with Volto's blocks extensions
mechanisms: variations and block styles. To use it, instantiate the schema and
pass it down to the component. A full Volto block edit component could be like:

```jsx
export const myBlockSchema = ({data, intl}) => {
  // notice that we are pass the data, so the schema is "dynamic", we can
  // compose it based on the data.

  return {
    title: "My block",
    fieldsets: [
      {
        id: 'default',
        title: 'Default',
        fields: ['myfield']
      }
    ],
    properties: {
      myfield: {
        title: "My field",
        widget: "number",
      }
    }
    required: [],
  };
}

export const MyBlockEdit = (props) => {
  const {
    block,
    onChangeBlock,
    data,
    selected,
    intl,
  } = props;

  let schema = Schema({ data, intl });

  return (
    <>
      <MyBlockViewComponent
        {...props}
        path={getBaseUrl(props.pathname)}
        mode="edit"
      />
      <SidebarPortal selected={selected}>
        <BlockDataForm
          schema={schema}
          onChangeField={(id, value) => {
            onChangeBlock(block, {
              ...data,
              [id]: value,
            });
          }}
          formData={data}
          onChangeBlock={onChangeBlock}
          block={block}
          blocksConfig={blocksConfig}
        />
      </SidebarPortal>
    </>
  );
};
```

If there's any registered variations for this block, they will be displayed as
a Select control for the active variation, in the sidebar.


```js
  myblock: {
    id: 'myblock',
    title: 'My Block',
    icon: heroSVG,
    group: 'common',
    view: MyBlockView,
    edit: MyBlockEdit,
    restricted: false,
    mostUsed: false,
    blockHasOwnFocusManagement: true,
    sidebarTab: 1,
    blockSchema: myBlockSchema,
    variations: [
      {
        id: 'leftSideView',
        isDefault: true,
        view: MyLeftSideView,
      },
      {
        id: 'rightSideView',
        isDefault: true,
        view: MyRighSideView,
      }
    ]
  },

```

Note: you can assign the schema to `blockSchema` in the block configuration. It
is used to extract the block default values.

Volto also has a "generic block edit component", the `EditDefaultBlock` which
you get by simply not setting the `edit` field of the block configuration
registration. This component uses the `blockSchema` field, so you are required
to set that.

## Using a blockSchema and the dataAdapter pattern

You can declare the schema that the block is using internally in the `blockSchema` property in the block configuration.

Sometimes is also useful to adapt the incoming data to other data format, structure or type.
You can use the dataAdapter pattern in `BlockDataForm` as this:

Given a block with the config:

```js
  config.blocks.blocksConfig.myBlock = {
    // ...
    schemaEnhancer: myBlockSchemaEnhancer,
    blockSchema: myBlockSchema,
    dataAdapter: myBlockDataAdapter,
    // ...
  };
```

```jsx
  const schema = blocksConfig.myBlock.blockSchema({ intl });
  const dataAdapter = blocksConfig.myBlock.dataAdapter;

    <BlockDataForm
      schema={schema}
      title={schema.title}
      onChangeField={(id, value) => {
        dataAdapter({
          block,
          data,
          id,
          onChangeBlock,
          value,
        });
      }}
      onChangeBlock={onChangeBlock}
      formData={data}
      block={block}
      blocksConfig={blocksConfig}
    />
```

and define `dataAdapter` as this:

```js
import { isEmpty } from 'lodash';

export const myBlockDataAdapter = ({
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

  // The adaptation that I need to inject to the block value(s)
  if (id === 'href' && !isEmpty(value) && !data.title && !data.description) {
    dataSaved = {
      ...dataSaved,
      title: value[0].Title,
      description: value[0].Description,
      head_title: value[0].head_title,
    };
  }

  // Then we save it to the current block data
  onChangeBlock(block, dataSaved);
};
```
