---
myst:
  html_meta:
    "description": "Block Development, Widgets & Integration"
    "property=og:description": "Block Development, Widgets & Integration"
    "property=og:title": "Block Development, Widgets & Integration"
    "keywords": "Plone, Volto, Training, Volto Light Theme"
---

# Block Development, Widgets & Integration

## Widgets for Block Styling

A block's styling options are ordinary schema fields, rendered by a handful of widgets.
Some of these widgets come with Volto, and some with VLT.
This section introduces the ones you will meet in this chapter and in VLT's own blocks.
The [VLT widgets reference](https://volto-light-theme.readthedocs.io/reference/widgets.html) covers them in more detail.

| Widget | Provided by | Stores | Used for |
| --- | --- | --- | --- |
| `blockWidth` | Volto | a width token, such as `default` | the width of a block, resolved through `config.blocks.widths` |
| `blockAlignment` | Volto | an alignment token, such as `center` | the alignment of a block's content, resolved through `config.blocks.alignments` |
| `size` | Volto | a size token: `s`, `m`, or `l` | the size of media, resolved through `config.blocks.sizes` |
| `colorSwatch`, also registered as `color_picker` | VLT | the name of a palette entry | block themes and other curated palettes |
| `colorPicker` | VLT | a hex color | a free choice of color, as in the theme behavior |
| `object_list` | VLT, replacing Volto's widget of the same name | a list of objects | repeating items, such as header actions and footer links |
| `softTextWidget` and `softTextareaWidget` | VLT | text | text with a recommended maximum length |

### Width, Alignment, and Size

`blockWidth` and `blockAlignment` let editors pick one of a few buttons:

```javascript
{
  widget: 'blockWidth',
  title: 'Block Width',
  default: 'default',
  actions: config.blocks.widths.map((width) => width.name),
}
```

```javascript
{
  widget: 'blockAlignment',
  title: 'Alignment',
  default: 'center',
  actions: config.blocks.alignments.map((alignment) => alignment.name),
}
```

Always pass the token names as `actions`, as shown above.
Without `actions`, both widgets use a default list whose entries carry their own style objects, and the widget then stores the style object instead of the token.
{ref}`Step 6 of the Cover block <light-theme-cover-actions-label>` explains the consequences.

VLT resolves the tokens only for fields named `blockWidth:noprefix` and `align:noprefix`, as {ref}`the previous chapter <light-theme-style-fields-label>` explains.

`size` selects a size from a default list of three:

```javascript
{
  widget: 'size',
  title: 'Size',
  default: 'm',
}
```

The stored values are the tokens `s`, `m`, and `l`.
The names Small, Medium, and Large are only their labels, so `default` must be one of the tokens.
The default entries of `size` carry no styles, so it stores the tokens even without `actions`.
When the field is named `size:noprefix`, VLT maps each token to the `--media-size` custom property through `config.blocks.sizes`:

```typescript
config.blocks.sizes = [
  { style: { '--media-size': 'var(--size-small)' }, name: 's', label: 'Small' },
  { style: { '--media-size': 'var(--size-medium)' }, name: 'm', label: 'Medium' },
  { style: { '--media-size': 'var(--size-large)' }, name: 'l', label: 'Large' },
];
```

All three widgets are built on Volto's `buttons` widget, which you can also use for your own single-choice fields.
It accepts a list of `actions`, an `actionsInfoMap` with the icon and the label of each action, and `filterActions` to show only some of the actions.

### Palettes: `colorSwatch`

`colorSwatch` lets editors pick from a curated palette instead of entering free-form values.
Each entry follows the `StyleDefinition` type from `@plone/types`.
Always provide a `default` entry, so that the field has a predictable fallback.

The following schema enhancer adds such a field to the `styles` object of a block.
Like the Cover block's enhancer later in this chapter, it only works when it runs after VLT's `defaultStylingSchema`:

```javascript
const colors = [
  {
    name: 'default',
    label: 'Default',
    style: {
      '--theme-color': '#fff',
      '--theme-foreground-color': '#000',
    },
  },
  {
    name: 'grey',
    label: 'Grey',
    style: {
      '--theme-color': '#ecebeb',
      '--theme-foreground-color': '#000',
    },
  },
];

const myColorSchemaEnhancer = ({ schema }) => {
  schema.properties.styles.schema.fieldsets[0].fields.push('myColorField');
  schema.properties.styles.schema.properties.myColorField = {
    widget: 'colorSwatch',
    title: 'My color',
    default: 'default',
    colors,
  };
  return schema;
};
```

The widget stores the `name` of the chosen entry, and the StyleWrapper turns it into a class on the block, such as `has--myColorField--grey`, which you can target in your stylesheets.
To also inject the entry's custom properties as inline styles, register a `styleFieldDefinition` utility under the field name:

```javascript
config.registerUtility({
  name: 'myColorField',
  type: 'styleFieldDefinition',
  method: () => colors,
});
```

VLT only looks up these utilities for the fields inside a block's `styles` object, which is why the example adds the field there.

```{note}
This is the recommended way to use this widget, because the same `colors` list feeds both the widget and the styles, which keeps a single source of truth for the palette.
```

VLT registers the same component as `color_picker`.
That is the widget `defaultStylingSchema` uses for the **Background color** field, with the palettes passed in a `themes` prop instead of `colors`.
VLT also registers `themeColorSwatch`, a variant that always shows the palettes in `config.blocks.themes`.

### Free Colors: `colorPicker`

`colorPicker` is a color picker with a visual chooser and a hex input.
The theme behavior uses it for its five color fields.

For fields listed in `config.settings.colorMap`, `colorPicker` also renders `ColorContrastChecker`.
This component warns the editor when the contrast between the field and its paired color is below 4.5:1, following the WCAG guidelines.
The pairs and their default values are defined like this:

```javascript
config.settings.colorMap = {
  primary_color: {
    colorPair: 'primary_foreground_color',
    default: '#ffffff',
  },
  primary_foreground_color: {
    colorPair: 'primary_color',
    default: '#000000',
  },
  // ... and the same for the secondary and accent pairs
};
```

You can reuse the checker in your own color widget.
Render it after the field, and only for fields listed in `colorMap`, as VLT's `colorPicker` does, because it throws an error for any other field.
It compares hex colors with the paired field of the content being edited, so it is meant for content fields such as the theme behavior's, not for block settings.

```jsx
import FormFieldWrapper from '@plone/volto/components/manage/Widgets/FormFieldWrapper';
import config from '@plone/volto/registry';
import ColorContrastChecker from '@kitconcept/volto-light-theme/components/Widgets/ColorContrastChecker';

const MyColorWidget = (props) => {
  const { id, value, onChange } = props;

  return (
    <>
      <FormFieldWrapper {...props}>
        <input
          id={`field-${id}`}
          type="color"
          value={value || '#ffffff'}
          onChange={(event) => onChange(id, event.target.value)}
        />
      </FormFieldWrapper>
      {config.settings.colorMap[id] && <ColorContrastChecker {...props} />}
    </>
  );
};

export default MyColorWidget;
```

### Lists: `object_list`

VLT replaces Volto's `object_list` widget with one that supports reordering by drag and drop.
It stores a list of objects, each with a generated `@id`.
The shape of each object comes from a `schema` prop, or from `schemaName`, the name of a schema registered as a utility.
The schema can be a schema object, or a function that returns one:

```javascript
config.registerUtility({
  name: 'mySchemaName',
  type: 'schema',
  method: mySchema,
});
```

```javascript
{
  widget: 'object_list',
  title: 'Items',
  schemaName: 'mySchemaName',
}
```

VLT's header actions, footer links, and footer logos fields work this way, with the schemas `headerActions`, `footerLinks`, and `footerLogos`.

### Text With a Soft Limit

`softTextWidget` and `softTextareaWidget` behave like the `text` and `textarea` widgets, but they display a character count while the editor types.
When the count exceeds the limit set in `softMaxLength`, a warning appears, but the editor can still save the content.

These widgets are configured from the backend, with `directives.widget` and its `frontendOptions`:

```python
directives.widget(
    "seo_title",
    frontendOptions={
        "widget": "softTextWidget",
        "widgetProps": {"softMaxLength": "55"},
    },
)
seo_title = schema.TextLine(
    title="SEO Title",
    description="Override the meta title. Use maximum 55 characters.",
    required=False,
)
```

(cover-block-label)=

## Creating a Custom Cover Block

This section builds a cover block step by step, starting with a basic implementation and then adding VLT's styling fields to it.

### Step 1: Create Basic Block Schema

Create {file}`src/components/blocks/Cover/schema.ts`:

```typescript
import { defineMessages } from 'react-intl';

const messages = defineMessages({
  cover: {
    id: 'Cover',
    defaultMessage: 'Cover',
  },
  title: {
    id: 'Title',
    defaultMessage: 'Title',
  },
  subtitle: {
    id: 'Subtitle',
    defaultMessage: 'Subtitle',
  },
  backgroundImage: {
    id: 'Background Image',
    defaultMessage: 'Background Image',
  },
});

const coverBlockSchema = (props) => {
  const { intl } = props;

  return {
    title: intl.formatMessage(messages.cover),
    fieldsets: [
      {
        id: 'default',
        title: 'Default',
        fields: ['title', 'subtitle'],
      },
      {
        id: 'design',
        title: 'Design',
        fields: ['backgroundImage'],
      },
    ],
    properties: {
      title: {
        title: intl.formatMessage(messages.title),
        type: 'string',
      },
      subtitle: {
        title: intl.formatMessage(messages.subtitle),
        type: 'string',
      },
      backgroundImage: {
        title: intl.formatMessage(messages.backgroundImage),
        widget: 'object_browser',
        mode: 'image',
        allowExternals: false,
      },
    },
    required: [],
  };
};

export { coverBlockSchema };
```

### Step 2: Create View Component

Before writing any markup, note which wrappers the view is responsible for.
VLT supports two block models, and they wrap a block differently:

- Under **Block Model v2**, the default, the block view renders its own outer element, `div.block.cover`. The renderer passes it the block's classes and inline styles.
- Under **Block Model v3**, VLT's renderer adds two wrappers itself, and renders the view inside them:

```html
<div class="block cover">              <!-- added by VLT under v3 -->
  <div class="block-inner-container">  <!-- added by VLT under v3 -->
    ...your markup starts here...
```

The outer element carries the block's identity and its theme; the inner container carries the width and the alignment.
This split is what lets a block have a background that behaves independently of its content width, and it is described in full in {ref}`the two-container system <bm3-two-container-label>`.

A view that always renders its own `div.block` would be wrapped twice under v3.
`BlockWrapper` from `@kitconcept/volto-bm3-compat` avoids that.
It renders the outer element, and an optional inner element that you pass as `ExtraWrapper`, only when the block uses v2.
With it, the view produces the same structure under both models.

Create {file}`src/components/blocks/Cover/View.tsx`:

```tsx
import config from '@plone/volto/registry';
import { BlockWrapper } from '@kitconcept/volto-bm3-compat';
import type { BlockViewProps } from '@plone/types';
import type { ReactNode } from 'react';

// Under Block Model v2, BlockWrapper renders `.block.cover` and then this
// inner container. Under v3 it renders neither, because VLT's renderer adds
// both. Either way the result is `.block.cover > .block-inner-container > ...`.
const InnerContainer = (props: { children: ReactNode }) => (
  <div className="block-inner-container">{props.children}</div>
);

const CoverView = (props: BlockViewProps) => {
  const { title, subtitle, backgroundImage } = props?.data || {};
  const imageItem = backgroundImage?.[0];
  const Image = config.getComponent('Image').component;

  return (
    <BlockWrapper {...props} ExtraWrapper={InnerContainer}>
      {imageItem?.['@id'] && (
        <div className="cover-image-wrapper">
          <Image
            item={{
              '@id': imageItem['@id'],
              image_field: imageItem.image_field,
              image_scales: imageItem.image_scales,
            }}
            alt=""
            loading="lazy"
            responsive
          />
        </div>
      )}

      <div className="cover-text">
        {title && <h2 className="cover-title">{title}</h2>}
        {subtitle && <p className="cover-subtitle">{subtitle}</p>}
      </div>
    </BlockWrapper>
  );
};

export default CoverView;
```

The view renders the image with Volto's `Image` component, which picks a suitable image scale for the space available.

### Step 3: Create Edit Component

Create {file}`src/components/blocks/Cover/Edit.tsx`:

```tsx
import { useIntl } from 'react-intl';
import SidebarPortal from '@plone/volto/components/manage/Sidebar/SidebarPortal';
import { BlockDataForm } from '@plone/volto/components/manage/Form';
import { coverBlockSchema } from './schema';
import CoverView from './View';
import type { BlockEditProps } from '@plone/types';

const CoverEdit = (props: BlockEditProps) => {
  const { selected, onChangeBlock, block, data } = props;
  const intl = useIntl();

  return (
    <>
      <CoverView {...props} />
      <SidebarPortal selected={selected}>
        <BlockDataForm
          {...props}
          data={data}
          block={block}
          schema={coverBlockSchema({ intl })}
          onChangeBlock={onChangeBlock}
          formData={data}
          onChangeField={(id: string, value: any) => {
            onChangeBlock(block, {
              ...data,
              [id]: value,
            });
          }}
        />
      </SidebarPortal>
    </>
  );
};

export default CoverEdit;
```

`BlockDataForm` applies the block's `schemaEnhancer` from its configuration to the schema you pass, which is what makes the styling fields from Step 6 appear in the sidebar.

### Step 4: Register the Basic Block

Edit {file}`src/config/blocks.ts`. Do not replace the file: it already holds the block themes from the previous chapter.
Add the imports at the top of the file, and the registration inside the existing `install` function:

```typescript
import type { ConfigType } from '@plone/registry';
import CoverView from '../components/blocks/Cover/View';
import CoverEdit from '../components/blocks/Cover/Edit';
import { coverBlockSchema } from '../components/blocks/Cover/schema';
import coverSVG from '@plone/volto/icons/hero.svg';

export default function install(config: ConfigType) {
  // ... block themes configuration ...

  // Register Cover Block
  config.blocks.blocksConfig.cover = {
    id: 'cover',
    title: 'Cover',
    icon: coverSVG,
    group: 'common',
    view: CoverView,
    edit: CoverEdit,
    restricted: false,
    mostUsed: true,
    blockSchema: coverBlockSchema,
    sidebarTab: 1,
  };

  return config;
}
```

```{note}
Give project blocks their own key, and follow the convention every other block in the registry uses: a lowercase single word such as `teaser`, `banner`, or `slider`, reserving camelCase for genuinely multi-word names like `gridBlock`.

The icon is a separate matter. Icon assets are not tied to block names, and {file}`hero.svg` is the one that depicts this layout, so this example uses it.
```

### Step 5: Add Basic Block Styles

The block has no styling fields yet, so this step sets up **structure only**.
Everything that depends on a widget—the width, the alignment, the theme color—arrives in Step 8, once the fields that produce those properties exist.

Create {file}`src/theme/blocks/_cover.scss`:

```scss
.block.cover {
  .block-inner-container {
    position: relative;
    display: flex;
    overflow: hidden;
    min-height: 60vh;
    max-width: var(--default-container-width);
    align-items: center;
    padding: 4rem 2rem;
    margin-inline: auto;
  }

  .cover-text {
    // Above the background image.
    position: relative;
    z-index: 1;
    display: flex;
    width: 100%;
    flex-direction: column;
    gap: 1rem;

    .cover-title {
      margin-bottom: $spacing-small;
      font-size: 5rem;
      line-height: 1.1;
    }

    .cover-subtitle {
      margin-bottom: $spacing-small;
      font-size: 2rem;
      line-height: 1.3;
      opacity: 0.9;
    }
  }

  &:has(.cover-image-wrapper) {
    color: #fff;
  }

  .cover-image-wrapper {
    position: absolute;
    z-index: 0;
    inset: 0;

    img {
      width: 100%;
      height: 100%;
      object-fit: cover;
      opacity: 0.7;
    }

    &::after {
      position: absolute;
      background: rgb(0 0 0 / 40%);
      content: '';
      inset: 0;
    }
  }
}
```

Two decisions are worth calling out.

**The width goes on `.block-inner-container`, not on `.block`.**
That is the two-container split: the outer element is the block's full extent, the inner one is where content is constrained. Putting `max-width` on the outer element instead fights VLT, which already constrains inner containers, and it makes a full-width block impossible.

**`min-height` is load-bearing.**
The image sits in an absolutely positioned wrapper and contributes no height.
Without `min-height`, the cover is only as tall as its text, and the image is cropped to that strip.

Import the partial in {file}`src/theme/_main.scss`, next to the other block partials:

```scss
@import './blocks/cover';
```

(light-theme-cover-actions-label)=

### Step 6: Add Width and Alignment Fields

Now add width and alignment fields to the block, with a schema enhancer next to the block schema. VLT resolves both fields, as described in {ref}`the previous chapter <light-theme-style-fields-label>`.

:::{important}
The enhancer below **extends** the styling fieldset; it does not create one.
`schema.properties.styles` only exists once VLT's `defaultStylingSchema` has run, so this enhancer only works when it is composed after it, which is what Step 7 does:

```typescript
schemaEnhancer: composeSchema(defaultStylingSchema, coverSchemaEnhancer),
```

Registered on its own, it throws an error, because `schema.properties.styles` is `undefined`.
This is also why the block gets its **Background color** control for free: that field comes from `defaultStylingSchema`, not from anything you write here.
:::

Make three changes to {file}`src/components/blocks/Cover/schema.ts`.

First, import the registry at the top of the file:

```typescript
import config from '@plone/volto/registry';
```

Second, add two messages to the `messages` object:

```typescript
  blockWidth: {
    id: 'Block Width',
    defaultMessage: 'Block Width',
  },
  textAlignment: {
    id: 'Text Alignment',
    defaultMessage: 'Text Alignment',
  },
```

Third, add the enhancer after `coverBlockSchema`, and export it as well, by replacing the `export` line at the end of the file:

```typescript
// Schema enhancer that adds the width and alignment styling fields.
// Only meaningful when composed *after* VLT's `defaultStylingSchema`, which is
// what creates `schema.properties.styles`.
const coverSchemaEnhancer = ({ schema, intl }) => {
  // Add custom fields to the styling schema at the beginning
  schema.properties.styles.schema.fieldsets[0].fields = [
    'align:noprefix',
    'blockWidth:noprefix',
    ...schema.properties.styles.schema.fieldsets[0].fields,
  ];

  schema.properties.styles.schema.properties['align:noprefix'] = {
    widget: 'blockAlignment',
    title: intl.formatMessage(messages.textAlignment),
    default: 'center',
    actions: config.blocks.alignments.map((alignment) => alignment.name),
  };

  schema.properties.styles.schema.properties['blockWidth:noprefix'] = {
    widget: 'blockWidth',
    title: intl.formatMessage(messages.blockWidth),
    default: 'default',
    actions: config.blocks.widths.map((width) => width.name),
  };

  return schema;
};

export { coverBlockSchema, coverSchemaEnhancer };
```

::::{dropdown} The complete schema.ts after this step
```typescript
import { defineMessages } from 'react-intl';
import config from '@plone/volto/registry';

const messages = defineMessages({
  cover: {
    id: 'Cover',
    defaultMessage: 'Cover',
  },
  title: {
    id: 'Title',
    defaultMessage: 'Title',
  },
  subtitle: {
    id: 'Subtitle',
    defaultMessage: 'Subtitle',
  },
  backgroundImage: {
    id: 'Background Image',
    defaultMessage: 'Background Image',
  },
  blockWidth: {
    id: 'Block Width',
    defaultMessage: 'Block Width',
  },
  textAlignment: {
    id: 'Text Alignment',
    defaultMessage: 'Text Alignment',
  },
});

const coverBlockSchema = (props) => {
  const { intl } = props;

  return {
    title: intl.formatMessage(messages.cover),
    fieldsets: [
      {
        id: 'default',
        title: 'Default',
        fields: ['title', 'subtitle'],
      },
      {
        id: 'design',
        title: 'Design',
        fields: ['backgroundImage'],
      },
    ],
    properties: {
      title: {
        title: intl.formatMessage(messages.title),
        type: 'string',
      },
      subtitle: {
        title: intl.formatMessage(messages.subtitle),
        type: 'string',
      },
      backgroundImage: {
        title: intl.formatMessage(messages.backgroundImage),
        widget: 'object_browser',
        mode: 'image',
        allowExternals: false,
      },
    },
    required: [],
  };
};

// Schema enhancer that adds the width and alignment styling fields.
// Only meaningful when composed *after* VLT's `defaultStylingSchema`, which is
// what creates `schema.properties.styles`.
const coverSchemaEnhancer = ({ schema, intl }) => {
  // Add custom fields to the styling schema at the beginning
  schema.properties.styles.schema.fieldsets[0].fields = [
    'align:noprefix',
    'blockWidth:noprefix',
    ...schema.properties.styles.schema.fieldsets[0].fields,
  ];

  schema.properties.styles.schema.properties['align:noprefix'] = {
    widget: 'blockAlignment',
    title: intl.formatMessage(messages.textAlignment),
    default: 'center',
    actions: config.blocks.alignments.map((alignment) => alignment.name),
  };

  schema.properties.styles.schema.properties['blockWidth:noprefix'] = {
    widget: 'blockWidth',
    title: intl.formatMessage(messages.blockWidth),
    default: 'default',
    actions: config.blocks.widths.map((width) => width.name),
  };

  return schema;
};

export { coverBlockSchema, coverSchemaEnhancer };
```
::::

Two details in that enhancer decide whether it works at all.

**The field names must end in `:noprefix`.**
As covered in {ref}`the previous chapter <light-theme-style-fields-label>`, `align:noprefix` and `align` are different field names.
VLT registers its style definitions under the literal names `align:noprefix` and `blockWidth:noprefix`, so a field called `align` matches none of them.
The `--block-alignment` property is then never injected, and the styles in Step 8 that read it have no effect.
The mistake is easy to miss: the buttons still appear in the sidebar, but the text does not move.

**Pass the token names as `actions`.**
Without `actions`, the widgets fall back to Volto's default list, and each default entry carries its own style object, such as `{ '--block-width': 'unset' }` for Full.
When the chosen entry has a style object, the widget stores that object instead of the token.
The block would then save a style object rather than `"full"`, skip VLT's definitions in `config.blocks.widths`, and get the class `has--block-width--[object Object]`.
Mapping `config.blocks.alignments` and `config.blocks.widths` to their names makes the widgets store tokens, and keeps the block in step with the theme, including any width or alignment your project adds.

### Step 7: Update Block Registration with Schema Enhancer

Back in {file}`src/config/blocks.ts`, add the two new imports and the `schemaEnhancer` key to the registration you wrote in Step 4:

```typescript
import type { ConfigType } from '@plone/registry';
import CoverView from '../components/blocks/Cover/View';
import CoverEdit from '../components/blocks/Cover/Edit';
import {
  coverBlockSchema,
  coverSchemaEnhancer,
} from '../components/blocks/Cover/schema';
import { composeSchema } from '@plone/volto/helpers/Extensions';
import { defaultStylingSchema } from '@kitconcept/volto-light-theme/components/Blocks/schema';
import coverSVG from '@plone/volto/icons/hero.svg';

export default function install(config: ConfigType) {
  // ... block themes configuration ...

  // Register Cover Block
  config.blocks.blocksConfig.cover = {
    id: 'cover',
    title: 'Cover',
    icon: coverSVG,
    group: 'common',
    view: CoverView,
    edit: CoverEdit,
    restricted: false,
    mostUsed: true,
    blockSchema: coverBlockSchema,
    schemaEnhancer: composeSchema(defaultStylingSchema, coverSchemaEnhancer),
    sidebarTab: 1,
  };

  return config;
}
```

`composeSchema` runs its arguments in order, so `defaultStylingSchema` creates the styling fieldset and `coverSchemaEnhancer` then extends it. Reverse them and the second enhancer runs against a schema that has no `styles` property yet.

(light-theme-third-party-styling-label)=

:::{tip}
The same technique adds VLT's theming to a block **you did not write**—one from a third-party add-on, or a core Volto block.
The only difference is that such a block may already have a `schemaEnhancer` of its own, which you must preserve.
`composeSchema` skips an enhancer that is `undefined`, so this works whether or not the block has one:

```typescript
config.blocks.blocksConfig.<blockId> = {
  ...config.blocks.blocksConfig.<blockId>,
  schemaEnhancer: composeSchema(
    config.blocks.blocksConfig.<blockId>.schemaEnhancer,
    defaultStylingSchema,
  ),
};
```
:::

### Step 8: Update Styles to Use Widget Values

The schema enhancers from Steps 6 and 7 now provide the custom properties that the styles can read: `--block-width` and `--block-alignment` from the new fields, and the theme properties, such as `--theme-color`, from the **Background color** control.

Replace the whole of {file}`src/theme/blocks/_cover.scss` with the following version.
Compared with Step 5, it adds the five numbered changes:

```scss
// 1. Lift VLT's layout-width cap for this block. See the explanation below.
#page-document .blocks-group-wrapper > .block.cover {
  max-width: 100%;
}

.block.cover {
  // 2. The text color of the selected theme.
  color: var(--theme-foreground-color);

  .block-inner-container {
    position: relative;
    display: flex;
    overflow: hidden;
    min-height: 60vh;

    // 3. The width chosen in Block Width, with the site default as a
    //    fallback, so the block stays sane if the field is ever removed.
    max-width: var(--block-width, var(--default-container-width));
    align-items: center;
    padding: 4rem 2rem;
    margin-inline: auto;

    // 4. The background of the selected theme. Use `background`, not
    //    `background-color`, so that gradient themes work as well.
    background: var(--theme-color);
  }

  .cover-text {
    // Above the background image.
    position: relative;
    z-index: 1;
    display: flex;
    width: 100%;
    flex-direction: column;

    // 5. The alignment chosen in Text Alignment.
    align-items: var(--block-alignment, start);
    gap: 1rem;
    text-align: var(--block-alignment, start);

    .cover-title {
      margin-bottom: $spacing-small;
      font-size: 5rem;
      line-height: 1.1;
    }

    .cover-subtitle {
      margin-bottom: $spacing-small;
      font-size: 2rem;
      line-height: 1.3;
      opacity: 0.9;
    }
  }

  &:has(.cover-image-wrapper) {
    color: #fff;
  }

  .cover-image-wrapper {
    position: absolute;
    z-index: 0;
    inset: 0;

    img {
      width: 100%;
      height: 100%;
      object-fit: cover;
      opacity: 0.7;
    }

    &::after {
      position: absolute;
      background: rgb(0 0 0 / 40%);
      content: '';
      inset: 0;
    }
  }
}
```

The first rule is needed because VLT limits every block inside a block group to the layout width, with the selector `#page-document .blocks-group-wrapper > *`.
Lifting that limit for the Cover lets a Full Width cover reach the edges of the page, and the inner container's `max-width` then decides the actual width.

The image and the text both sit inside `.block-inner-container`, so the Block Width control resizes them together.
The theme color behind the Cover still spans the whole width of the page, because VLT groups consecutive blocks that share a theme and paints the theme on the group.
Change 4 repeats the theme background inside the Cover, where it shows through the partly transparent image.
For why gradient themes need `background`, see {ref}`the warning about gradient palettes <light-theme-gradient-themes-label>`.

## Checkpoint

Restart the frontend, then add a Cover block to the Robotarium landing page. Give it the title **Book a robot. Build something.**, a subtitle such as *Twelve units, one afternoon at a time*, and a workshop photo as the background image. Confirm that:

- The block appears in the block chooser, listed as **Cover**.
- The **Styling** section of the block settings shows the **Text Alignment**, **Block Width**, and **Background color** controls.
- Changing the alignment moves the title and subtitle, and changing the width resizes the image and the text. If the controls appear but nothing moves, check that the field names end in `:noprefix`.
- On the published page, setting the width to **Full Width** takes the image from edge to edge.

```{seealso}
A block can also offer more than one rendering of the same data, as the Listing block does with its variations.
That is covered in the next chapter, where the Robotarium gets a **Robot Fleet** listing variation with its own card layout and per-item actions.
```

## Further Reading

- [Widgets reference](https://volto-light-theme.readthedocs.io/reference/widgets.html)
- [Develop add-ons for VLT](https://volto-light-theme.readthedocs.io/how-to-guides/develop-add-ons.html)
