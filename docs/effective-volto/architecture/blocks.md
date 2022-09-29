# Volto Blocks

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
