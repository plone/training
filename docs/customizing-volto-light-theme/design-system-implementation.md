---
myst:
  html_meta:
    "description": "Design system implementation & theming"
    "property=og:description": "Design system implementation & theming"
    "property=og:title": "Design system implementation & theming"
    "keywords": "Plone, Volto, Training, Theme, Footer"
---

# Design System Implementation & Theming

The Robotarium has a look: workshop teal, a technical typeface, and surfaces that read like painted metal. This chapter turns that into a working theme.

Nothing here is specific to robots. The steps are the ones you follow for any design handed to you—pull the decisions out of it, express them as tokens, and let VLT's components pick them up.

## Extracting Design Tokens

When working with a given design, systematically extract design decisions. Identify:

### Color Extraction Checklist

1. **Primary Colors**
   - Background color
   - Text color on primary

2. **Secondary Colors**
   - Background color
   - Text color on secondary

3. **Accent Colors**
   - Highlight color
   - Text color on accent

4. **Semantic Colors**
   - Link colors

### Typography Extraction

Look for:
- Font families
- Line heights
- Font weights


## Implementing Your Design System

VLT has migrated to use standardized color definitions. These use CSS properties that are injected at runtime in the right places, so your CSS can adapt to use them generically. The resulting CSS is simpler, and there's no need to define class names for each color definition.

### Step 1: Add Font Files

If you're using custom fonts, add the font files to your theme directory.
The Robotarium uses [Chakra Petch](https://fonts.google.com/specimen/Chakra+Petch); from {file}`frontend/packages/robotarium/src/theme`:

```bash
mkdir -p fonts/Chakra_Petch
```

at the end, it should look like:

```
src/theme/fonts/Chakra_Petch/
  ├── ChakraPetch-Regular.ttf
  └── ChakraPetch-Bold.ttf
```

This ensures the font files are bundled with your theme and can be referenced in your SCSS files.

### Step 2: Override SCSS Variables

Some of VLT's design decisions are SCSS variables rather than CSS custom properties. Those belong in {file}`src/theme/_variables.scss`:

```scss
// src/theme/_variables.scss
$default-container-width: 1120px;
$spacing-large: 80px;
```

VLT declares its variables with `!default`, so whatever you assign here wins.
It also derives the matching CSS custom properties from them, which means setting `$default-container-width` here updates `--default-container-width` too. You do not need to set both.

### Step 3: Define Your Design Tokens

In {file}`src/theme/_main.scss`, declare the fonts and the CSS custom properties that carry your design:

```scss
@font-face {
  font-family: 'Chakra Petch';
  src: url('./fonts/Chakra_Petch/ChakraPetch-Regular.ttf') format('truetype');
  font-weight: 400;
  font-style: normal;
  font-display: swap;
}

@font-face {
  font-family: 'Chakra Petch';
  src: url('./fonts/Chakra_Petch/ChakraPetch-Bold.ttf') format('truetype');
  font-weight: 700;
  font-style: normal;
  font-display: swap;
}

:root {
  // Extract these from your design
  --accent-color: #3b5759;
  --accent-foreground-color: #fff;
  --secondary-color: #afcac8;

  // Typography. VLT reads the font through
  // `$page-font: var(--custom-main-font, $page-font-template)`.
  --custom-main-font: 'Chakra Petch', sans-serif;

  // Give links a color of their own instead of the theme foreground color
  --link-foreground-color: #157a7a;

  // Breadcrumbs
  --breadcrumbs-background: var(--background, #fff);
  --breadcrumbs-foreground: var(--secondary-foreground-color, #3b5759);

  // Gradients for header and footer
  --header-background: linear-gradient(
    -3deg,
    var(--background, #fff) 0%,
    color-mix(in oklab, var(--secondary-color) 1%, var(--background, #fff)) 20%,
    color-mix(in oklab, var(--secondary-color) 3%, var(--background, #fff)) 35%,
    color-mix(in oklab, var(--secondary-color) 10%, var(--background, #fff)) 50%,
    color-mix(in oklab, var(--secondary-color) 30%, var(--background, #fff)) 65%,
    color-mix(in oklab, var(--secondary-color) 65%, var(--background, #fff)) 80%,
    color-mix(in oklab, var(--secondary-color) 90%, var(--background, #fff)) 92%,
    var(--secondary-color) 100%
  );

  --footer-background: radial-gradient(
    ellipse 100% 100% at 50% 100%,
    var(--secondary-color) 0%,
    var(--secondary-color) 20%,
    color-mix(in oklab, var(--secondary-color) 85%, var(--background, #fff)) 30%,
    color-mix(in oklab, var(--secondary-color) 65%, var(--background, #fff)) 40%,
    color-mix(in oklab, var(--secondary-color) 45%, var(--background, #fff)) 50%,
    color-mix(in oklab, var(--secondary-color) 30%, var(--background, #fff)) 60%,
    color-mix(in oklab, var(--secondary-color) 18%, var(--background, #fff)) 70%,
    color-mix(in oklab, var(--secondary-color) 10%, var(--background, #fff)) 80%,
    color-mix(in oklab, var(--secondary-color) 4%, var(--background, #fff)) 90%,
    var(--background, #fff) 100%
  );

  --fatmenu-foreground: #fff;
}
```

Notice that the header and footer gradients are assigned to the same `--header-background` and `--footer-background` properties you saw in the previous chapter.
Because VLT reads those properties rather than hard-coded colors, a gradient works everywhere a flat color would, with no component changes.

Setting a font is a good example of the "prefer custom properties" rule from the previous chapter: you do not shadow VLT's typography stylesheets, you set the one property they already read.

Site-wide rules that are not tokens go in the same file, outside `:root`:

```scss
.breadcrumbs {
  border-bottom: 1px solid var(--secondary-color);
}

// Let the first block sit flush with the header
#page-document,
#page-edit,
#page-add {
  .blocks-group-wrapper:first-child {
    padding-top: 0;
  }
}

// Match the theme swatch in the sidebar to the custom "charging bay" theme
#sidebar {
  .color-swatch-widget .color-swatch-option-handler.charging-bay {
    background: linear-gradient(135deg, var(--secondary-color) 0%, #fff 100%);
  }
}
```

```{warning}
Declare custom properties inside `:root`, but keep normal rules outside it.
Nesting a selector such as `#page-document` inside `:root` compiles to `:root #page-document`, which adds specificity you will have to fight later.
```

### Step 4: Add Block-Specific Styles

Keep per-block styles in their own partials under {file}`src/theme/blocks/`, one file per block.
This keeps them easy to find and stops {file}`_main.scss` from turning too complex.


```scss
// src/theme/blocks/_button.scss
body .block.__button {
  > .button.container,
  > .block-inner-container {
    a,
    button {
      padding: 1rem;
      transition:
        background 0.2s ease,
        color 0.2s ease;

      &:hover,
      &:active,
      &:focus {
        background: var(--accent-color);
        color: var(--accent-foreground-color);
      }
    }
  }
}
```

```scss
// src/theme/blocks/_slider.scss
.block.slider .teaser-item .teaser-item-title {
  background: rgb(255 255 255 / 10%);
  backdrop-filter: blur(20px) saturate(110%);
  box-shadow:
    0 8px 32px 0 rgb(31 135 125 / 10%),
    inset 0 0 0 1px rgb(255 255 255 / 10%);
  color: var(--theme-foreground-color);
}
```

```scss
// src/theme/blocks/_grid.scss
.block.gridBlock .four .slate:not(.inner) {
  padding: 2.5rem;
  padding-top: 4rem;
  backdrop-filter: blur(20px) saturate(110%);
  box-shadow:
    0 8px 32px 0 rgb(31 135 125 / 10%),
    inset 0 0 0 1px rgb(255 255 255 / 10%);
}
```

```scss
// src/theme/blocks/_teaser.scss
.block.teaser .card .card-inner .card-summary {
  padding: $spacing-large;
}
```

The teaser rule uses `$spacing-large`, one of VLT's SCSS variables.
Those are in scope for your stylesheets because {file}`_main.scss` is compiled after VLT's variables and mixins, so you can reuse the theme's spacing scale, breakpoints, and typography mixins instead of inventing new values.

(charging-bay-label)=

### Step 5: Configure Block Themes

Block themes are the palettes an editor can choose between on any block. The Robotarium gets two: the plain default, and **Charging Bay**, a soft teal wash for sections that should feel like the lit alcove where the robots dock.

In `src/config/blocks.ts`, define them:

```typescript
import type { ConfigType } from '@plone/registry';

export default function install(config: ConfigType) {
  // Block palettes
  config.blocks.themes = [
    {
      style: {
        '--theme-color': 'white',
        '--theme-high-contrast-color': '#bbd1d0',
        '--theme-foreground-color': 'black',
        '--theme-low-contrast-foreground-color': '#555555',
      },
      name: 'default',
      label: 'Default',
    },
    {
      style: {
        '--theme-color': `linear-gradient(180deg, oklab(1 0 0 / 0.9) 0%, transparent 15%, transparent 85%, oklab(1 0 0 / 0.9) 100%),
                radial-gradient(ellipse 850px 700px at 12% 15%, oklab(1 0 0 / 0.4) 0%, transparent 70%),
                radial-gradient(ellipse 900px 650px at 85% 85%, oklab(1 0 0 / 0.4) 0%, transparent 70%),
                radial-gradient(ellipse 850px 750px at 70% 35%, oklab(0.805 -0.030 -0.003 / 0.5) 0%, oklab(0.835 -0.025 -0.002 / 0.2) 50%, transparent 85%),
                radial-gradient(ellipse 920px 800px at 25% 65%, oklab(0.780 -0.032 -0.004 / 0.45) 0%, oklab(0.825 -0.027 -0.003 / 0.2) 50%, transparent 87%),
                radial-gradient(ellipse 1100px 900px at 50% 50%, oklab(0.805 -0.030 -0.003 / 0.25) 0%, oklab(0.850 -0.025 -0.002 / 0.1) 60%, transparent 90%),
                linear-gradient(182deg, oklab(1 0 0) 0%, oklab(0.988 -0.006 0) 10%, oklab(0.958 -0.016 -0.001) 22%, oklab(0.910 -0.025 -0.003) 35%, oklab(0.860 -0.030 -0.003) 45%, oklab(0.820 -0.032 -0.004) 52%, oklab(0.860 -0.030 -0.003) 59%, oklab(0.910 -0.025 -0.003) 69%, oklab(0.958 -0.016 -0.001) 82%, oklab(0.988 -0.006 0) 92%, oklab(1 0 0) 100%)`,
        '--theme-high-contrast-color': 'oklab(1 0 0 / 0.1)',
        '--theme-foreground-color': 'black',
        '--theme-low-contrast-foreground-color': '#555555',
      },
      name: 'charging-bay',
      label: 'Charging Bay',
    },
  ];

  // Re-point the Grid block at the new palettes. See below.
  config.blocks.blocksConfig.gridBlock.themes = config.blocks.themes;

  return config;
}
```

```{note}
The Grid block is the only block in VLT—or in any of the recommended add-ons—that keeps its own copy of the palettes, so this is the only place the extra line is needed.
```

### Step 6: Keep the Layout Settings in Sync

Widening the container in SCSS is only half the change.
VLT also reads the container width from configuration, in {file}`src/config/settings.ts`.
Add the `layout` block to the file Cookieplone generated—do not replace it, or you will drop your language settings:

```typescript
import type { ConfigType } from '@plone/registry';

export default function install(config: ConfigType) {
  // Language settings (generated — keep these)
  config.settings.isMultilingual = false;
  config.settings.supportedLanguages = ['en'];
  config.settings.defaultLanguage = 'en';

  // Added in this step
  config.settings.layout = {
    ...config.settings.layout,
    defaultContainerWidth: 1120,
  };

  return config;
}
```

This value is not used for layout—the CSS custom property does that. It is used to compute the `sizes` attribute of responsive images in teasers and listings, which tells the browser how wide an image will actually be so it can pick the right scale to download.

If the two disagree, nothing breaks visibly, but the browser makes its choice from the wrong number and downloads scales that are too small, so images look soft.
Whenever you change `$default-container-width`, change `defaultContainerWidth` to match.

```{note}
`config.settings.layout` also carries `tabletBreakpoint`, used in the same calculation.
Keep it in sync with `$tablet-breakpoint` for the same reason.
```

### Step 7: Main Index Configuration

The generated {file}`src/index.ts` already calls `installSettings`. Add the two lines that wire up your block configuration:

```typescript
import type { ConfigType } from '@plone/registry';
import installSettings from './config/settings';
import installBlocks from './config/blocks';

function applyConfig(config: ConfigType) {
  installSettings(config);
  installBlocks(config);
  return config;
}

export default applyConfig;
```

### Step 8: Import Your Stylesheets

{file}`_main.scss` is the entry point Volto injects after all of VLT's styles. Import your partials there, in the order you want them applied:

```scss
// src/theme/_main.scss
// ... your @font-face rules, :root tokens, and site-wide rules above ...

@import './blocks/button';
@import './blocks/grid';
@import './blocks/slider';
@import './blocks/teaser';
```

{file}`_variables.scss` needs no import. Volto picks it up on its own and injects it ahead of VLT's variables.

## Checkpoint

Restart the frontend and confirm the following before moving on:

- The site renders in your custom font, and the header and footer show their gradients.
- Links use `--link-foreground-color` rather than the surrounding text color.
- Opening a page in edit mode and selecting a block shows **Default** and **Charging Bay** in the block's color theme selector.

## Further Reading

- [Color system](https://volto-light-theme.readthedocs.io/conceptual-guides/color-system.html)
- [Colors reference](https://volto-light-theme.readthedocs.io/reference/colors.html)
- [Layout](https://volto-light-theme.readthedocs.io/conceptual-guides/layout.html)
