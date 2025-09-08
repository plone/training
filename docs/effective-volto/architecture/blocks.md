---
myst:
  html_meta:
    "description": "Volto Blocks"
    "property=og:description": "Volto Blocks"
    "property=og:title": "Volto Blocks"
    "keywords": "Volto, Plone, Volto blocks, Pastanaga"
---

# Volto Blocks

Volto features the Pastanaga Editor Engine, allowing you to visually compose
a page using blocks. The editor allows you to add, modify, reorder and delete
blocks given your requirements. Blocks provide the user the ability to display
content in an specific way, although they can also define behavior and have
specific features.

Volto's blocks are one of its most attractive propositions and represent the
culmination of Plone's community efforts for a full composite page solution.
They are loved by both the editors and developers for their ease of use, and
this is demonstrated by the big numbers of open source blocks already
available.

Their secret is that they're almost self-contained mini-applications, supported
by Volto's infrastructure, so they can be anything and they can easily
integrate the huge number of React libraries. Sliders, carousels, fully
editable charts, layout solutions like tabs, accordions, rows and columns, they
can all be powered by Volto's blocks.

Volto ships with several built-in blocks (richtext editor, listing, image,
table of contents, html, etc) and can easily be extended with new blocks,
completly replace the existing blocks or enhance the blocks with new
features.

## Volto Blocks engine

Any Dexterity content type can be made compatible with Volto blocks engine by
enabling the `Blocks` behavior. From the Content Types Control Panel it's also
possible to define a default [blocks layout](../addons/blockslayout.md) for
a particular content type.

A Volto block is defined in the Volto Configuration Registry, the
`config.blocks.blocksConfig` branch:

```js
  html: {
    id: 'html',
    title: 'HTML',
    icon: codeSVG,
    group: 'common',
    view: ViewHTMLBlock,
    edit: EditHTMLBlock,
    schema: BlockSettingsSchema,
    restricted: false,
    mostUsed: false,
    sidebarTab: 0,
    security: {
      addPermission: [],
      view: [],
    },
  },
```


A Volto block is two React component: the `Edit` and the `View` component.
These components receive the `data` as input property and the `onChangeBlock`
callback to upstream the modified data. They can be any valid React components,
but typically they integrate with several Volto pieces:

- The `SidebarPortal`, which allows edit components to place things inside the
  Sidebar
- The `BlockDataForm` which provides variations-aware [schema-based forms](../addons/blockdataform)
  for JSON data, so it can be placed in the sidebar
- [Variations](../addons/block-extensions) and [Styling
  extensions](../addons/block-styling), which open schema-powered blocks to
  "third-party" extensions.

The block manifests its data a simple JavaScript Object:

```json
{
  "@type": "heroBlock"
  // anything else we want
}
```

Passed down from the main Edit Form are the block `id` and several callbacks,
the main one being `onChangeBlock`. So, when writing the most basic block edit
component, all we need to do is something like:

```js
onChangeBlock(
  blockId,
  {
    '@type': 'heroBlock',
    title: "My hero block",
    text: "something here"
    // ... something else
  }
)
```

Almost all Volto blocks use the Sidebar to place additional settings and
controls for the data they provide. To simplify this task, we define this block
data form using a **block schema**, which is derived from the way plone.restapi
publishes edit schemas for backend content types.

Note: these schemas are pure "frontend" schemas, they are not defined in the
Plone backend, but only in Volto frontend code.

Once we have the schema, in the Edit component of that block, we can use it to
generate the Sidebar controls:

```
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
```

Being able to have the block edit controls expressed as data (the schemas)
allows us to programatically manipulate the data (the schema and the generated
controls), so we open the door to the **schemaEnhancer** mechanism.

By mutating the Volto Configuration Registry settings for a block and
adding/overwriting the `schemaEnhancer`, you can configure a function that can
tweak the schema. This functionality is provided by the `BlockDataForm`
component, see the [BlockDataForm](../addons/blockdataform) page.
