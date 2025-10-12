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

## Creating a Custom Hero Block

Let's build a hero block step by step, starting with a basic implementation and then enhancing it with VLT widgets.

### Step 1: Create Basic Block Schema

Create `src/components/blocks/myHero/schema.ts`:

```javascript
import { defineMessages } from 'react-intl';

const messages = defineMessages({
  hero: {
    id: 'Hero',
    defaultMessage: 'Hero',
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

const heroBlockSchema = (props) => {
  const { intl } = props;

  return {
    title: intl.formatMessage(messages.hero),
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

export { heroBlockSchema };
```

### Step 2: Create View Component

Create `src/components/blocks/myHero/View.tsx`:

```tsx
import React from 'react';
import cx from 'classnames';
import config from '@plone/volto/registry';
import { flattenToAppURL, isInternalURL } from '@plone/volto/helpers/Url/Url';
import type { BlockViewProps } from '@plone/types';

const HeroView = (props: BlockViewProps) => {
  const { className, style } = props;
  const { title, subtitle, backgroundImage, url } = props?.data || {};

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
      renderedImage = (
        <img
          src={
            isInternalURL(url?.['@id'])
              ? `${flattenToAppURL(url['@id'])}/@@images/image`
              : url?.['@id']
          }
          alt=""
          loading="lazy"
        />
      );
    }
  }

  return (
    <div
      className={cx('block hero', className, { 'has-image': hasImage })}
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
import React from 'react';
import { useIntl } from 'react-intl';
import SidebarPortal from '@plone/volto/components/manage/Sidebar/SidebarPortal';
import { BlockDataForm } from '@plone/volto/components/manage/Form';
import { heroBlockSchema } from './schema';
import HeroView from './View';
import type { BlockEditProps } from '@plone/types';

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
import type { ConfigType } from '@plone/registry';
import HeroView from '../components/blocks/myHero/View';
import HeroEdit from '../components/blocks/myHero/Edit';
import { heroBlockSchema } from '../components/blocks/myHero/schema';
import heroSVG from '@plone/volto/icons/hero.svg';

export default function install(config: ConfigType) {
  // ... block themes configuration ...

  // Register Hero Block
  config.blocks.blocksConfig.hero = {
    id: 'hero',
    title: 'Hero',
    icon: heroSVG,
    group: 'common',
    view: HeroView,
    edit: HeroEdit,
    restricted: false,
    mostUsed: true,
    blockSchema: heroBlockSchema,
    sidebarTab: 1,
    category: 'hero',
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
  width: var(--default-container-width);
  max-width: var(--block-width) !important;
  align-items: center;
  justify-content: center;
  background-color: var(--theme-color);
  color: var(--theme-foreground-color);
  margin-inline: auto;

  // default text view
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

  // has-image version
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
        content: '';
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
@import './blocks/hero';
@import './site';
```

### Step 6: Enhance with VLT Widgets

Now let's add VLT's powerful widgets to control block width and alignment. Update the schema file to add the schema enhancer.

Update `src/components/blocks/myHero/schema.ts`:

```javascript
import { defineMessages } from 'react-intl';

const messages = defineMessages({
  hero: {
    id: 'Hero',
    defaultMessage: 'Hero',
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

const heroBlockSchema = (props) => {
  const { intl } = props;

  return {
    title: intl.formatMessage(messages.hero),
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

// Schema enhancer to add VLT widget styling fields
const heroSchemaEnhancer = ({ formData, schema, intl }) => {
  // Add custom fields to the styling schema at the beginning
  schema.properties.styles.schema.fieldsets[0].fields = [
    'blockWidth:noprefix',
    'align',
    ...schema.properties.styles.schema.fieldsets[0].fields,
  ];

  schema.properties.styles.schema.properties['blockWidth:noprefix'] = {
    widget: 'blockWidth',
    title: intl.formatMessage(messages.blockWidth),
    default: 'default',
  };

  schema.properties.styles.schema.properties.align = {
    widget: 'blockAlignment',
    title: intl.formatMessage(messages.textAlignment),
    default: 'center',
  };

  return schema;
};

export { heroBlockSchema, heroSchemaEnhancer };
```

### Step 7: Update Block Registration with Schema Enhancer

Update `src/config/blocks.ts` to include the schema enhancer:

```typescript
import type { ConfigType } from '@plone/registry';
import HeroView from '../components/blocks/myHero/View';
import HeroEdit from '../components/blocks/myHero/Edit';
import {
  heroBlockSchema,
  heroSchemaEnhancer,
} from '../components/blocks/myHero/schema';
import { composeSchema } from '@plone/volto/helpers/Extensions';
import { defaultStylingSchema } from '@kitconcept/volto-light-theme/components/Blocks/schema';
import heroSVG from '@plone/volto/icons/hero.svg';

export default function install(config: ConfigType) {
  // ... block themes configuration ...

  // Register Hero Block
  config.blocks.blocksConfig.hero = {
    id: 'hero',
    title: 'Hero',
    icon: heroSVG,
    group: 'common',
    view: HeroView,
    edit: HeroEdit,
    restricted: false,
    mostUsed: true,
    blockSchema: heroBlockSchema,
    schemaEnhancer: composeSchema(defaultStylingSchema, heroSchemaEnhancer),
    sidebarTab: 1,
    category: 'hero',
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
@import './blocks/hero';
@import './blocks/relatedItems';
@import './site';
```

---
