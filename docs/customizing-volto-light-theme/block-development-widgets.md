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
  name: "myColorField",
  type: "styleFieldDefinition",
  method: (props) => colors,
});
```

```{note}
This is the recommended way to use this widget, since it decouples the styles from the CSS and keeps a single source of truth for the color definitions.
```

### ThemeColorSwatch Widget

Allows selection from configured themes stored in `config.blocks.themes`:

```javascript
{
  widget: 'themeColorSwatch',
  title: 'Color Theme',
  colors: config.blocks.themes,
}
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

Selects the block size from a default list of values, one of either `small`, `medium`, or `large`:

```javascript
{
  widget: 'size',
  title: 'Size',
  default: 'medium',
}
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
Add it after a color input field in your own widget to warn the editor in real time about insufficient contrast:

```jsx
import ContrastChecker from "./ContrastChecker";

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
    colorPair: "primary_foreground_color",
    default: "#ffffff",
  },
  primary_foreground_color: {
    colorPair: "primary_color",
    default: "#000000",
  },
};
```

### Buttons Component

Another helper rather than a widget, used to build widgets that show a list of buttons where a single value can be toggled.
The BlockAlignment and Size widgets are built on top of it.
You can pass it a configurable list of `actions`, along with the icon and the i18n message used for each one in `actionsInfoMap`, and filter out the default actions you don't want with `filterActions`.

```{note}
As of VLT 8.0.0-alpha.5 these components were moved to the Volto core package.
If you are on Volto 19.0.0-alpha.12 or later, use the ones from Volto core instead of the ones provided by VLT.
```

## Creating a Custom Hero Block

Let's build a hero block step by step, starting with a basic implementation and then enhancing it with VLT widgets.

### Step 1: Create Basic Block Schema

Create `src/components/blocks/myHero/schema.ts`:

```javascript
import { defineMessages } from "react-intl";

const messages = defineMessages({
  hero: {
    id: "Hero",
    defaultMessage: "Hero",
  },
  title: {
    id: "Title",
    defaultMessage: "Title",
  },
  subtitle: {
    id: "Subtitle",
    defaultMessage: "Subtitle",
  },
  backgroundImage: {
    id: "Background Image",
    defaultMessage: "Background Image",
  },
});

const heroBlockSchema = (props) => {
  const { intl } = props;

  return {
    title: intl.formatMessage(messages.hero),
    fieldsets: [
      {
        id: "default",
        title: "Default",
        fields: ["title", "subtitle"],
      },
      {
        id: "design",
        title: "Design",
        fields: ["backgroundImage"],
      },
    ],
    properties: {
      title: {
        title: intl.formatMessage(messages.title),
        type: "string",
      },
      subtitle: {
        title: intl.formatMessage(messages.subtitle),
        type: "string",
      },
      backgroundImage: {
        title: intl.formatMessage(messages.backgroundImage),
        widget: "object_browser",
        mode: "image",
        allowExternals: false,
      },
    },
    required: [],
  };
};

export { heroBlockSchema };
```

### Step 2: Create View Component

Create `src/components/blocks/myHero/View.tsx`:

```tsx
import React from "react";
import cx from "classnames";
import config from "@plone/volto/registry";
import { flattenToAppURL, isInternalURL } from "@plone/volto/helpers/Url/Url";
import type { BlockViewProps } from "@plone/types";

const HeroView = (props: BlockViewProps) => {
  const { className, style } = props;
  const { title, subtitle, backgroundImage, url } = props?.data || {};

  const hasImage = backgroundImage?.[0]?.["@id"];

  let renderedImage = null;
  if (hasImage) {
    const Image = config.getComponent("Image").component;
    const imageItem = backgroundImage[0];

    if (Image) {
      renderedImage = (
        <Image
          item={{
            "@id": imageItem["@id"],
            image_field: imageItem.image_field,
            image_scales: imageItem.image_scales,
          }}
          alt=""
          loading="lazy"
          responsive
        />
      );
    } else {
      renderedImage = (
        <img
          src={
            isInternalURL(url?.["@id"])
              ? `${flattenToAppURL(url["@id"])}/@@images/image`
              : url?.["@id"]
          }
          alt=""
          loading="lazy"
        />
      );
    }
  }

  return (
    <div
      className={cx("block hero", className, { "has-image": hasImage })}
      style={style}
    >
      {hasImage && <div className="hero-image-wrapper">{renderedImage}</div>}

      <div className="hero-content">
        <div className="hero-text">
          {title && <h1 className="hero-title">{title}</h1>}
          {subtitle && <p className="hero-subtitle">{subtitle}</p>}
        </div>
      </div>
    </div>
  );
};

export default HeroView;
```

### Step 3: Create Edit Component

Create `src/components/blocks/myHero/Edit.tsx`:

```tsx
import React from "react";
import { useIntl } from "react-intl";
import SidebarPortal from "@plone/volto/components/manage/Sidebar/SidebarPortal";
import { BlockDataForm } from "@plone/volto/components/manage/Form";
import { heroBlockSchema } from "./schema";
import HeroView from "./View";
import type { BlockEditProps } from "@plone/types";

const HeroEdit = (props: BlockEditProps) => {
  const { selected, onChangeBlock, block, data } = props;
  const intl = useIntl();

  return (
    <>
      <HeroView {...props} />
      <SidebarPortal selected={selected}>
        <BlockDataForm
          {...props}
          data={data}
          block={block}
          schema={heroBlockSchema({ props, intl })}
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

export default HeroEdit;
```

### Step 4: Register the Basic Block

Update `src/config/blocks.ts`:

```typescript
import type { ConfigType } from "@plone/registry";
import HeroView from "../components/blocks/myHero/View";
import HeroEdit from "../components/blocks/myHero/Edit";
import { heroBlockSchema } from "../components/blocks/myHero/schema";
import heroSVG from "@plone/volto/icons/hero.svg";

export default function install(config: ConfigType) {
  // ... block themes configuration ...

  // Register Hero Block
  config.blocks.blocksConfig.hero = {
    id: "hero",
    title: "Hero",
    icon: heroSVG,
    group: "common",
    view: HeroView,
    edit: HeroEdit,
    restricted: false,
    mostUsed: true,
    blockSchema: heroBlockSchema,
    sidebarTab: 1,
    category: "hero",
  };

  return config;
}
```

### Step 5: Add Basic Block Styles

Create `src/theme/blocks/_hero.scss`:

```scss
.block.hero {
  position: relative;
  display: flex;
  width: 100%;
  max-width: var(--block-width) !important;
  align-items: center;
  justify-content: center;
  background-color: var(--theme-color);
  color: var(--theme-foreground-color);
  margin-inline: auto;

  .hero-content {
    position: relative;
    z-index: 1;
    width: 100%;
  }

  .hero-text {
    display: flex;
    width: 100%;
    height: 100%;
    flex-direction: column;
    align-items: var(--align--block-alignment);
    gap: 1rem;
    text-align: var(--align--block-alignment);

    .hero-title {
      margin-bottom: $spacing-small;
      font-size: 5rem;
      line-height: 1.1;
    }

    .hero-subtitle {
      margin-bottom: $spacing-small;
      font-size: 2rem;
      line-height: 1.3;
      opacity: 0.9;
    }
  }

  &.has-image {
    color: #fff;

    .hero-image-wrapper {
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
        background: rgba(0, 0, 0, 0.4);
        content: "";
        inset: 0;
      }
    }

    .hero-content {
      position: relative;
      z-index: 1;
    }
  }
}
```

Import in `src/theme/_main.scss`:

```scss
@import "./blocks/hero";
@import "./site";
```

### Step 6: Enhance with VLT Widgets

Now let's add VLT's powerful widgets to control block width and alignment. Update the schema file to add the schema enhancer.

Update `src/components/blocks/myHero/schema.ts`:

```javascript
import { defineMessages } from "react-intl";

const messages = defineMessages({
  hero: {
    id: "Hero",
    defaultMessage: "Hero",
  },
  title: {
    id: "Title",
    defaultMessage: "Title",
  },
  subtitle: {
    id: "Subtitle",
    defaultMessage: "Subtitle",
  },
  backgroundImage: {
    id: "Background Image",
    defaultMessage: "Background Image",
  },
  blockWidth: {
    id: "Block Width",
    defaultMessage: "Block Width",
  },
  textAlignment: {
    id: "Text Alignment",
    defaultMessage: "Text Alignment",
  },
});

const heroBlockSchema = (props) => {
  const { intl } = props;

  return {
    title: intl.formatMessage(messages.hero),
    fieldsets: [
      {
        id: "default",
        title: "Default",
        fields: ["title", "subtitle"],
      },
      {
        id: "design",
        title: "Design",
        fields: ["backgroundImage"],
      },
    ],
    properties: {
      title: {
        title: intl.formatMessage(messages.title),
        type: "string",
      },
      subtitle: {
        title: intl.formatMessage(messages.subtitle),
        type: "string",
      },
      backgroundImage: {
        title: intl.formatMessage(messages.backgroundImage),
        widget: "object_browser",
        mode: "image",
        allowExternals: false,
      },
    },
    required: [],
  };
};

// Schema enhancer to add VLT widget styling fields
const heroSchemaEnhancer = ({ formData, schema, intl }) => {
  // Add custom fields to the styling schema at the beginning
  schema.properties.styles.schema.fieldsets[0].fields = [
    "blockWidth:noprefix",
    "align",
    ...schema.properties.styles.schema.fieldsets[0].fields,
  ];

  schema.properties.styles.schema.properties["blockWidth:noprefix"] = {
    widget: "blockWidth",
    title: intl.formatMessage(messages.blockWidth),
    default: "default",
  };

  schema.properties.styles.schema.properties.align = {
    widget: "blockAlignment",
    title: intl.formatMessage(messages.textAlignment),
    default: "center",
  };

  return schema;
};

export { heroBlockSchema, heroSchemaEnhancer };
```

### Step 7: Update Block Registration with Schema Enhancer

Update `src/config/blocks.ts` to include the schema enhancer:

```typescript
import type { ConfigType } from "@plone/registry";
import HeroView from "../components/blocks/myHero/View";
import HeroEdit from "../components/blocks/myHero/Edit";
import {
  heroBlockSchema,
  heroSchemaEnhancer,
} from "../components/blocks/myHero/schema";
import { composeSchema } from "@plone/volto/helpers/Extensions";
import { defaultStylingSchema } from "@kitconcept/volto-light-theme/components/Blocks/schema";
import heroSVG from "@plone/volto/icons/hero.svg";

export default function install(config: ConfigType) {
  // ... block themes configuration ...

  // Register Hero Block
  config.blocks.blocksConfig.hero = {
    id: "hero",
    title: "Hero",
    icon: heroSVG,
    group: "common",
    view: HeroView,
    edit: HeroEdit,
    restricted: false,
    mostUsed: true,
    blockSchema: heroBlockSchema,
    schemaEnhancer: composeSchema(defaultStylingSchema, heroSchemaEnhancer),
    sidebarTab: 1,
    category: "hero",
  };

  return config;
}
```

### Step 8: Update Styles to Use Widget Values

Update `src/theme/blocks/_hero.scss` to use the CSS custom properties set by the widgets:

```scss
.block.hero {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  background-size: cover;
  background-position: center;
  background-color: var(--theme-color);
  color: var(--theme-foreground-color);
  max-width: var(--block-width) !important;
  margin-left: auto;
  margin-right: auto;

  .hero-content {
    .hero-image-wrapper {
      img {
        aspect-ratio: var(--image-aspect-ratio, 16/9);
        opacity: 0.8;
      }
    }

    .hero-text {
      position: absolute;
      display: flex;
      flex-direction: column;
      align-items: var(--align--block-alignment);
      width: 100%;
      height: 100%;
      padding: 4rem;
      z-index: 2;

      .hero-title {
        font-size: 5rem;
        margin-bottom: $spacing-small;
        line-height: 1;
      }

      .hero-subtitle {
        font-size: 3rem;
        opacity: 0.95;
        line-height: 1;
      }
    }
  }
}
```

## Integrating Third-Party Blocks

Let's learn how to integrate the `@plone-collective/volto-relateditems-block` into VLT.

### Install the Block

To install the related items block, make sure you are in the `frontend/packages/volto-my-project` folder, and use the following command:

```bash
pnpm install @plone-collective/volto-relateditems-block@latest
```

Add it to your `package.json` addons (before VLT):

```json
"addons": [
  "@eeacms/volto-accordion-block",
  "@kitconcept/volto-button-block",
  "@kitconcept/volto-heading-block",
  "@kitconcept/volto-highlight-block",
  "@kitconcept/volto-introduction-block",
  "@kitconcept/volto-separator-block",
  "@kitconcept/volto-slider-block",
  "@plone-collective/volto-relateditems-block",
  "@kitconcept/volto-light-theme"
],
```

### Enhance the Block Schema

To add the theme feature to the Related Items block, update `src/config/blocks.ts` to register the `defaultStylingSchema` enhancer:

```typescript
export default function install(config: ConfigType) {
  // ... previous configuration ...

  config.blocks.blocksConfig.relatedItems = {
    ...config.blocks.blocksConfig.relatedItems,
    schemaEnhancer: defaultStylingSchema,
  };

  return config;
}
```

### Add Custom Styles

Create `src/theme/blocks/_relatedItems.scss`:

```scss
.block.relatedItems {
  .inner-container {
    background: var(--theme-high-contrast-color);
    padding: 3rem;
    width: var(--narrow-container-width);

    h2.headline {
      color: var(--theme-foreground-color);
    }

    ul {
      color: var(--theme-foreground-color);
      li a {
        color: var(--link-foreground-color);
      }
    }
  }
}
```

Import it in `_main.scss`:

```scss
@import "./blocks/hero";
@import "./blocks/relatedItems";
@import "./site";
```
