---
myst:
  html_meta:
    "description": "Block Development, Widgets & Integration"
    "property=og:description": "Block Development, Widgets & Integration"
    "property=og:title": "Block Development, Widgets & Integration"
    "keywords": "Plone, Volto, Training, Volto Light Theme"
---

# Block Development, Widgets & Integration

## Understanding VLT Widgets

VLT provides powerful widgets for block configuration that work with the StyleWrapper system.

### BlockWidth Widget

Controls the content width of blocks:

```javascript
{
  widget: 'blockWidth',
  title: 'Block Width',
  default: 'default',
}
```

### BlockAlignment Widget

Controls content alignment within blocks:

```javascript
{
  widget: 'blockAlignment',
  title: 'Alignment',
  default: 'center',
}
```

### ColorSwatch Widget

Lets editors pick from a curated palette instead of entering free-form values.
Each entry follows the `StyleDefinition` type from `@plone/types`, and you should always provide a `default` option so the field has a predictable fallback:

```javascript
{
  widget: 'colorSwatch',
  title: 'Background color',
  default: 'default',
  colors: [
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
  ],
}
```

The widget stores the chosen color's `name` token, and the StyleWrapper adds that token as a CSS class on the block, so you can target it in your stylesheets.
If you also want the CSS custom properties injected inline, register a `styleFieldDefinition` utility for the field name used in the schema:

```javascript
config.registerUtility({
  name: 'myColorField',
  type: 'styleFieldDefinition',
  method: (props) => colors,
});
```

```{note}
This is the recommended way to use this widget, since it decouples the styles from the CSS and keeps a single source of truth for the color definitions.
```

### ObjectList Widget

Allows introducing a list of ordered objects with drag and drop:

```javascript
{
  widget: 'object_list',
  title: 'Items',
  schemaName: 'mySchemaName',
}
```

### ColorPicker Widget

A real color picker, with an RGB visual color chooser and a `hex` color field:

```javascript
{
  widget: 'colorPicker',
  title: 'Custom color',
}
```

### color_picker Widget

A Semantic UI-free drop-in replacement that overrides Volto's `color_picker` widget.
Given an array of color definitions, it displays the colors that editors can choose:

```javascript
{
  widget: 'color_picker',
  title: 'Color',
  colors: [
    { name: 'default', label: 'Default' },
    { name: 'grey', label: 'Grey' },
  ],
}
```

### Size Widget

Selects the block size from a default list of three values.
The stored values are the tokens `s`, `m`, and `l`. The names Small, Medium, and Large are only their labels, so a `default` must be one of the tokens:

```javascript
{
  widget: 'size',
  title: 'Size',
  default: 'm',
}
```

VLT maps each token to the `--media-size` custom property through `config.blocks.sizes`, resolved by the `size:noprefix` style field:

```typescript
config.blocks.sizes = [
  { style: { '--media-size': 'var(--size-small)' }, name: 's', label: 'Small' },
  { style: { '--media-size': 'var(--size-medium)' }, name: 'm', label: 'Medium' },
  { style: { '--media-size': 'var(--size-large)' }, name: 'l', label: 'Large' },
];
```

Like the BlockAlignment widget, it is based on the Buttons component under the hood, so its actions and the styles they apply are configurable.

### SoftText and SoftTextarea Widgets

`softTextWidget` and `softTextareaWidget` behave like the `text` and `textarea` widgets, but they display a real-time character count while typing.
When the count exceeds the limit set in `softMaxLength`, a notification appears, but the editor is still allowed to save the content.

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

### ColorContrastChecker Component

Not a widget itself, but a component that calculates the contrast ratio between two colors following the WCAG accessibility guidelines.
It is provided by VLT, at `@kitconcept/volto-light-theme/components/Widgets/ColorContrastChecker`.
Add it after a color input field in your own widget to warn the editor in real time about insufficient contrast:

```jsx
import ContrastChecker from '@kitconcept/volto-light-theme/components/Widgets/ColorContrastChecker';

const MyColorWidget = (props) => {
  return (
    <>
      <FormFieldWrapper {...props} />
      <ContrastChecker {...props} />
    </>
  );
};

export default MyColorWidget;
```

It accepts hex color codes, and compares the value of the field against its paired color.
The pairings and their defaults are defined in `config.settings.colorMap`:

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
};
```

### Buttons Component

Another helper rather than a widget, used to build widgets that show a list of buttons where a single value can be toggled.
The BlockAlignment and Size widgets are built on top of it.
You can pass it a configurable list of `actions`, along with the icon and the i18n message used for each one in `actionsInfoMap`, and filter out the default actions you don't want with `filterActions`.

```{note}
As of VLT 8.0.0-alpha.5, four of these components live in Volto core rather than in VLT: `ButtonsWidget`, `BlockAlignment`, `BlockWidth`, and `Size`.
If you are on Volto 19.0.0-alpha.12 or later, import them from `@plone/volto/components/manage/Widgets/` instead of from VLT.

`ColorContrastChecker` was not part of that move and is still provided by VLT.
```

(cover-block-label)=

## Creating a Custom Cover Block

Let's build a cover block step by step, starting with a basic implementation and then enhancing it with VLT widgets.

### Step 1: Create Basic Block Schema

Create `src/components/blocks/Cover/schema.ts`:

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

Before writing any markup, note what the block view is **not** responsible for.
Volto already wraps every block, and under Block Model v3 it wraps it twice:

```html
<div class="block cover">              <!-- rendered for you -->
  <div class="block-inner-container">  <!-- rendered for you under BM3 -->
    ...your markup starts here...
```

The outer `.block` carries the block's identity and its theme; the inner container carries the width and the alignment.
This split is what lets a block have a background that behaves independently of its content width, and it is described in full in {ref}`the two-container system <bm3-two-container-label>`.

A block view that renders its own `.block` wrapper therefore produces a duplicate.
The way to stay correct under both block models is `BlockWrapper` from `@kitconcept/volto-bm3-compat`, which renders the wrappers under Block Model v2 and steps aside under v3, where Volto renders them itself.

Create `src/components/blocks/Cover/View.tsx`:

```tsx
import config from '@plone/volto/registry';
import { flattenToAppURL, isInternalURL } from '@plone/volto/helpers/Url/Url';
import { BlockWrapper } from '@kitconcept/volto-bm3-compat';
import type { BlockViewProps } from '@plone/types';
import type { ReactNode } from 'react';

// Under block model 2, BlockWrapper renders `.block.cover` and then this
// ExtraWrapper. Under block model 3 it renders neither, because Volto already
// emits both. Either way the result is
// `.block.cover > .block-inner-container > ...`.
const InnerContainer = (props: { children: ReactNode }) => (
  <div className="block-inner-container">{props.children}</div>
);

const CoverView = (props: BlockViewProps) => {
  const { title, subtitle, backgroundImage } = props?.data || {};

  const hasImage = backgroundImage?.[0]?.['@id'];

  let renderedImage = null;
  if (hasImage) {
    const Image = config.getComponent('Image').component;
    const imageItem = backgroundImage[0];

    if (Image) {
      renderedImage = (
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
      );
    } else {
      const src = imageItem['@id'];
      renderedImage = (
        <img
          src={
            isInternalURL(src) ? `${flattenToAppURL(src)}/@@images/image` : src
          }
          alt=""
          loading="lazy"
        />
      );
    }
  }

  return (
    <BlockWrapper {...props} ExtraWrapper={InnerContainer}>
      {hasImage && <div className="cover-image-wrapper">{renderedImage}</div>}

      <div className="cover-text">
        {title && <h2 className="cover-title">{title}</h2>}
        {subtitle && <p className="cover-subtitle">{subtitle}</p>}
      </div>
    </BlockWrapper>
  );
};

export default CoverView;
```

### Step 3: Create Edit Component

Create `src/components/blocks/Cover/Edit.tsx`:

```tsx
import React from 'react';
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
          schema={coverBlockSchema({ props, intl })}
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

### Step 4: Register the Basic Block

Edit `src/config/blocks.ts`. Do not replace the file: it already holds the block themes from the previous chapter.
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

The icon is a separate matter. Icon assets are not tied to block names, and {file}`hero.svg` is the one that depicts this layout, so it we will use it in this example.
```

### Step 5: Add Basic Block Styles

The block has no styling fields yet, so this step sets up **structure only**.
Everything that depends on a widget—the width, the alignment, the theme color—arrives in Step 8, once the fields that produce those properties exist.

Create `src/theme/blocks/_cover.scss`:

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

Two decisions worth calling out.

**The width goes on `.block-inner-container`, not on `.block`.**
That is the two-container split: the outer element is the block's full extent, the inner one is where content is constrained. Putting `max-width` on the outer element instead fights VLT, which already constrains inner containers, and it makes a full-width block impossible.

**`min-height` is load-bearing.**
The image sits in an absolutely positioned wrapper and contributes no height, so without it a cover with an image collapses to nothing—at which point the alignment control in Step 8 will appear to do nothing, because there is no space to align within.

Import it in `src/theme/_main.scss`:

```scss
@import './blocks/button';
@import './blocks/cover';
@import './blocks/grid';
@import './blocks/slider';
@import './blocks/teaser';
```

### Step 6: Enhance with VLT Widgets

Now let's add VLT's widgets for block width and alignment, by adding a schema enhancer alongside the block schema.

```{important}
The enhancer below **extends** the styling fieldset; it does not create one.
`schema.properties.styles` only exists once VLT's `defaultStylingSchema` has run, so this enhancer is meaningful only when composed after it—which is what Step 7 does:

    schemaEnhancer: composeSchema(defaultStylingSchema, coverSchemaEnhancer)

Registered on its own, it throws, because `schema.properties.styles` is `undefined`.
This is also why the block gets its **Background color** control for free: that field comes from `defaultStylingSchema`, not from anything you write here.
```

Replace the whole of `src/components/blocks/Cover/schema.ts` with the following. It repeats the schema from Step 1, adds two messages, and exports the new enhancer:

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

// Schema enhancer to add VLT widget styling fields.
// Only meaningful when composed *after* VLT's `defaultStylingSchema`, which is
// what creates `schema.properties.styles`.
const coverSchemaEnhancer = ({ formData, schema, intl }) => {
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

Two details in that enhancer decide whether it works at all.

**The field names must end in `:noprefix`.**
As covered in the previous chapter, `align:noprefix` and `align` are different field names.
VLT registers its style definitions under the literal names `align:noprefix` and `blockWidth:noprefix`, so a field called `align` matches nothing: the `--block-alignment` property is never injected, and the styles in Step 8 that read it silently do nothing.
The failure is quiet—the buttons still appear in the sidebar, they just have no effect.

Match the names VLT registers, and you inherit its behavior. What the suffix suppresses is the generated `has--align--center` class, and the more your styling is driven by custom properties—as the Cover block's is—the less those classes matter.

**Pass `actions` from `config.blocks`.**
Both widgets fall back to a built-in list when `actions` is omitted, and those built-in defaults are close to VLT's but not identical—Volto's `full` width resolves to `unset` where VLT's resolves to `100%`.
Deriving the actions from `config.blocks.alignments` and `config.blocks.widths` keeps the block in step with the theme, and with any width or alignment your project adds.

### Step 7: Update Block Registration with Schema Enhancer

Back in `src/config/blocks.ts`, add the two new imports and the `schemaEnhancer` key to the registration you wrote in Step 4:

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

```{tip}
The same technique adds VLT's theming to a block **you did not write**—one from a third-party add-on, or a core Volto block. The only difference is that such a block may already have a `schemaEnhancer` of its own, which you must preserve:

    config.blocks.blocksConfig.<blockId> = {
      ...config.blocks.blocksConfig.<blockId>,
      schemaEnhancer: composeSchema(
        config.blocks.blocksConfig.<blockId>.schemaEnhancer,
        defaultStylingSchema,
      ),
    };

```

### Step 8: Update Styles to Use Widget Values

The structure from Step 5 stays as it is. This step connects it to the three custom properties that now exist, because the schema enhancers from Steps 6 and 7 are in place: `--block-width`, `--block-alignment`, and `--theme-color`.

Make these four changes in `src/theme/blocks/_cover.scss`:

```scss
// 1. Lift VLT's layout-width cap. See the explanation below.
#page-document .blocks-group-wrapper > .block.cover {
  max-width: 100%;
}

.block.cover {
  // 2. The theme's foreground color, set by the Background color control.
  color: var(--theme-foreground-color);

  .block-inner-container {
    position: relative;
    display: flex;
    overflow: hidden;
    min-height: 60vh;

    // 3. Driven by the Block Width control, with the site default as a
    //    fallback so the block stays sane if the field is ever removed.
    max-width: var(--block-width, var(--default-container-width));
    align-items: center;
    padding: 4rem 2rem;
    margin-inline: auto;

    // The theme's background. `background`, never `background-color` — see the
    // warning below.
    background: var(--theme-color);
  }

  .cover-text {
    position: relative;
    z-index: 1;
    display: flex;
    width: 100%;
    flex-direction: column;

    // 4. Driven by the Text Alignment control.
    align-items: var(--block-alignment, start);
    gap: 1rem;
    text-align: var(--block-alignment, start);

    // ... the rest is unchanged from Step 5 ...
  }
}
```

Because the width and the background both sit on `.block-inner-container`, the Block Width control now resizes the whole visual unit—color, image, and text together—rather than only the text.

## Checkpoint

Restart the frontend, then add a Cover block to the Robotarium landing page. Give it the title **Book a robot. Build something.**, a subtitle such as *Twelve units, one afternoon at a time*, and a workshop photo as the background image. Confirm that:

- The block appears in the block chooser, listed as **Cover**.
- The **Styling** tab of the sidebar shows **Alignment** and **Block Width** controls.
- Changing the alignment moves the title and subtitle, and changing the width resizes the block. If the controls appear but nothing moves, check that the field names end in `:noprefix`.
- Setting the width to **Full Width** takes the block edge to edge, background image included.

```{seealso}
A block can also offer more than one rendering of the same data, as the Listing block does with its variations.
That is covered in the next chapter, where the Robotarium gets a **Robot Fleet** listing variation with its own card layout and per-item actions.
```

## Further Reading

- [Widgets reference](https://volto-light-theme.readthedocs.io/reference/widgets.html)
- [Develop add-ons for VLT](https://volto-light-theme.readthedocs.io/how-to-guides/develop-add-ons.html)
- [Image aspect ratio](https://volto-light-theme.readthedocs.io/reference/image-aspect-ratio.html)
