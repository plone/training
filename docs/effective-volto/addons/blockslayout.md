---
myst:
  html_meta:
    "description": "Blocks Layout"
    "property=og:description": "Blocks Layout"
    "property=og:title": "Blocks Layout"
    "keywords": "Volto, Plone, Pastanaga, Dexterity Blocks Layout"
---

# Blocks Layout

Any Dexterity content type can be made compatible with Volto blocks engine by
enabling the `Blocks` behavior. From the Content Types Control Panel it's also
possible to define a default "layout" for a particular content type. In the
Block Layout page you get a regular Volto Pastanaga Blocks Editor page, but the
blocks have an additional tab in the sidebar, the "block settings".

When using the content type to instantiate a new Plone content, the add form
will already have the blocks from transfered from the Blocks Layout page of
that content type.

The available controls in the Block Settings tab are controlled by the `schema` property in the block configuration:

```
  hero: {
    id: 'hero',
    title: 'Hero',
    icon: heroSVG,
    group: 'common',
    view: ViewHeroImageLeftBlock,
    edit: EditHeroImageLeftBlock,
    // notice the schema here
    schema: BlockSettingsSchema,
    blockSchema: HeroImageLeftBlockSchema,
    restricted: false,
    mostUsed: false,
    blockHasOwnFocusManagement: true,
    sidebarTab: 1,
    security: {
      addPermission: [],
      view: [],
    },
  },
```

The generic BlockSettingsSchema allow control over the behavior of the block
in the future edit pages: is the block required? is it read only? etc.
