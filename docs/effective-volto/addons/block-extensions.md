---
myst:
  html_meta:
    "description": "Block Extensions"
    "property=og:description": "Block Extensions"
    "property=og:title": "Block Extensions"
    "keywords": "Volto, Plone, Pastanaga, Volto blocks extensions"
---

# Block Extensions

A common pattern in blocks is the "variations" UI pattern - a slightly different
versions of a block that can be toggled on demand by the editors. Choosing the
listing template (gallery, summary listing, etc.) for the `Listing` block is
one example of the typical use case for this feature.

A block defines variations in its block configuration. These variations can
be used to enhance or complement the default behavior of a block without having
to shadow its stock components. These enhancements can be at the settings level
(add or remove block settings) via schema enhancers or, if the code of your
block allows it, even use alternative renderers (e.g., in view mode) showing the
enhanced fields or modifying the block behavior or look and feel.

```
export default (config) => {
  config.blocks.blocksConfig.teaserBlock.variations = [
    {
      id: 'default',
      title: 'Default',
      isDefault: true,
      template: SimpleTeaserView
    },
    {
      id: 'card',
      label: 'Card',
      template: CardTeaserView,
      schemaEnhancer: ({schema, formData, intl}) => {
        schema.properties.cardSize = '...'; // fill in your implementation
        return schema;
      }
    }
  ];
}
```

The capabilities of a block can't be constrained only to the "variations". What
if, for example, one such variation is so advanced that it needs its own
"variations"? So the `variations` are simply a more concrete example of a Volto
block extension.

Volto provides several helpers to manage the extensions:

- `resolveBlockExtensions`, a function that resolves `extensions` (all available
  extensions for that block` and `resolvedExtensions` (the current active
  extensions of that block)
- `withBlockExtensions`, a React HOC uses the `resolveBlockExtensions` to
  inject `extensions` and `resolvedExtensions` as block props
- `withBlockSchemaEnhancer` which bootstraps the variation mechanism (by
  providing a select control to toggle the active variation) and use any
  defined `schemaEnhancer` for the block
- `withVariationSchemaEnhancer`, a React HOC which uses the defined
  `schemaEnhancer` from the active block variation
  to mutate the schema.
- `withStylingSchemaEnhancer`, a similar HOC which enhances the schema with
  information from the `stylesSchema`. These 2 helpers are directly wrapped
  over the `InlineForm` to create the `BlockDataForm` component.
