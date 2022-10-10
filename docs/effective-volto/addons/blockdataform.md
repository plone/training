---
myst:
  html_meta:
    "description": "Create a block using `BlockDataForm`"
    "property=og:description": "Create a block using `BlockDataForm`"
    "property=og:title": "Create a block using `BlockDataForm`"
    "keywords": "Volto, Plone, BlockDataForm, Volto block extensions"
---

# Create a block using `BlockDataForm`

The BlockDataForm renders an form fully integrated with a block's extension
mechanisms: variations and block styles. To use it, instantiate the schema and
pass it down to the component. A full Volto block edit component could be like:

```
export const MyBlockSchema = ({data, intl}) => {
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
        />
      </SidebarPortal>
    </>
  );
};
```

Note: in the future, this step may even be completely avoided, when Volto will
have a generic Edit component that uses this recipe for all the blocks.

If there's any registered variations for this block, they will be displayed as
a Select control for the active variation, in the sidebar.


```
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
    blockSchema: MyBlockSchema,
    security: {
      addPermission: [],
      view: [],
    },
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
is used only to extract the block default values. This integration will be
improved, in the future.
