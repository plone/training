---
myst:
  html_meta:
    "description": "Design system implementation & theming"
    "property=og:description": "Design system implementation & theming"
    "property=og:title": "Design system implementation & theming"
    "keywords": "Plone, Volto, Training, Theme, Footer"
---

# Design System Implementation & Theming

The Robotarium has a look: workshop teal, a technical font, and surfaces that read like painted metal. This chapter turns that into a working theme.

Nothing here is specific to robots. The steps are the ones you follow for any design handed to you—pull the decisions out of it, express them as tokens, and let VLT's components pick them up.

## Extracting Design Tokens

Before writing any code, list the decisions that the design makes:

- **Color pairs**: the primary, secondary, and accent background colors, and the text color used on each.
- **Link color**, if links should stand out from the surrounding text.
- **Typography**: the font families, and any line heights or font weights that differ from VLT's.
- **Block palettes**: the backgrounds that editors should be able to choose for a section of a page.

For the Robotarium, that list comes down to a dark teal accent with white text, a pale teal secondary color, a teal link color, the Chakra Petch font, and one extra block palette.

## Implementing Your Design System

### Step 1: Add Font Files

If you're using custom fonts, add the font files to your theme directory.
The Robotarium uses [Chakra Petch](https://fonts.google.com/specimen/Chakra+Petch).
From {file}`frontend/packages/volto-robotarium/src/theme`, create a folder for it:

```shell
mkdir -p fonts/Chakra_Petch
```

Download the font family from Google Fonts, and copy its regular and bold files into that folder:

```console
src/theme/fonts/Chakra_Petch/
├── ChakraPetch-Regular.ttf
└── ChakraPetch-Bold.ttf
```

Keeping the files inside your theme bundles them with it, so your stylesheets can refer to them with relative paths.

### Step 2: Override SCSS Variables

Set the build-time values in {file}`src/theme/_variables.scss`, as described in {ref}`light-theme-custom-properties-label`:

```scss
// src/theme/_variables.scss
$default-container-width: 1120px;
$spacing-large: 80px;
```

The Robotarium widens the default container from 940px to 1120px, and increases VLT's large spacing step from 60px to 80px.
Setting `$default-container-width` also updates `--default-container-width`, so you do not need to set both.

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

  // Breadcrumbs: a white bar, with text in the footer text color
  --breadcrumbs-background: var(--background);
  --breadcrumbs-foreground: var(--secondary-foreground-color);

  // Gradients for header and footer.
  // `--background` is VLT's base color, white by default.
  --header-background: linear-gradient(
    -3deg,
    var(--background) 0%,
    color-mix(in oklab, var(--secondary-color) 1%, var(--background)) 20%,
    color-mix(in oklab, var(--secondary-color) 3%, var(--background)) 35%,
    color-mix(in oklab, var(--secondary-color) 10%, var(--background)) 50%,
    color-mix(in oklab, var(--secondary-color) 30%, var(--background)) 65%,
    color-mix(in oklab, var(--secondary-color) 65%, var(--background)) 80%,
    color-mix(in oklab, var(--secondary-color) 90%, var(--background)) 92%,
    var(--secondary-color) 100%
  );

  --footer-background: radial-gradient(
    ellipse 100% 100% at 50% 100%,
    var(--secondary-color) 0%,
    var(--secondary-color) 20%,
    color-mix(in oklab, var(--secondary-color) 85%, var(--background)) 30%,
    color-mix(in oklab, var(--secondary-color) 65%, var(--background)) 40%,
    color-mix(in oklab, var(--secondary-color) 45%, var(--background)) 50%,
    color-mix(in oklab, var(--secondary-color) 30%, var(--background)) 60%,
    color-mix(in oklab, var(--secondary-color) 18%, var(--background)) 70%,
    color-mix(in oklab, var(--secondary-color) 10%, var(--background)) 80%,
    color-mix(in oklab, var(--secondary-color) 4%, var(--background)) 90%,
    var(--background) 100%
  );
}
```

The breadcrumbs tokens replace VLT's defaults, which use the accent colors.
The Robotarium's accent text color is white, for the teal fat menu, and it would disappear on the white breadcrumbs bar, so the breadcrumbs take the text color of the footer instead.
As a result, the Footer Font Color field of the theme behavior also changes the color of the breadcrumbs.

The header and footer gradients are assigned to the same `--header-background` and `--footer-background` properties you saw in the previous chapter.
VLT paints the header and the footer with `background`, not `background-color`, so a gradient works there as well as a flat color, with no component changes.

Setting a font is a good example of the {ref}`prefer custom properties <light-theme-custom-properties-label>` rule from the previous chapter: you do not shadow VLT's typography stylesheets, you set the one property they already read.

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
```

```{warning}
Declare custom properties inside `:root`, but keep normal rules outside it.
Nesting a selector such as `#page-document` inside `:root` compiles to `:root #page-document`, which adds specificity you will have to fight later.
```

### Step 4: Add Block-Specific Styles

Keep per-block styles in their own partials under {file}`src/theme/blocks/`, one file per block.
This keeps them easy to find, and stops {file}`_main.scss` from growing too large.
The Robotarium adds four of them.

The button partial replaces the colors of buttons on hover and focus with the accent colors:

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

VLT colors buttons inside themed blocks with rules that start with `body`.
Starting your rule with `body` as well gives it the same specificity, and it wins because your stylesheet loads after VLT's.

The hover colors also matter for the gradient palette that you add in Step 5.
VLT's own hover state uses `--theme-color` as the text color.
A gradient is not a valid text color, so in a section with a gradient palette, the button text would inherit the dark foreground color and disappear against the dark hover background.
The accent colors avoid that.

The slider and grid partials give text a frosted-glass panel, on the slide titles and in four-column grids:

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

The teaser partial adds space around the text of Teaser blocks:

```scss
// src/theme/blocks/_teaser.scss
.block.teaser .card .card-inner .card-summary {
  padding: $spacing-large;
}
```

The teaser rule uses `$spacing-large`, one of VLT's SCSS variables, which you set to 80px in Step 2.
VLT's variables and mixins are in scope for your stylesheets because {file}`_main.scss` is compiled after them, so you can reuse the theme's spacing scale, breakpoints, and typography mixins instead of inventing new values.

(charging-bay-label)=

### Step 5: Configure Block Themes

Block themes are the palettes an editor can choose between on any block. The Robotarium gets two: the plain default, and **Charging Bay**, a soft teal wash for sections that should feel like the lit alcove where the robots dock.

In {file}`src/config/blocks.ts`, define them:

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
VLT copies the default palettes to the Grid block when its own configuration runs, which is before yours.
The Grid block is the only block in VLT, or in any of the recommended add-ons, that keeps its own copy of the palettes, so this is the only place where the extra line is needed.
```

(light-theme-gradient-themes-label)=

```{warning}
`--theme-color` is usually a flat color, but Charging Bay sets it to a gradient.
A gradient only works where a stylesheet reads the property with `background`, as VLT does for block backgrounds.
Where a stylesheet reads it with `background-color` or `color`, the browser ignores the declaration:

- The Charging Bay swatch in the block settings would look empty, which the rule below fixes.
- The Button block would lose its hover text color, which the button partial from Step 4 fixes.

In your own styles, read `--theme-color` with `background`, never with `background-color`.
```

VLT styles the swatches in the **Background color** control with `background-color: var(--theme-color)`.
Add this rule to {file}`src/theme/_main.scss`, next to the other site-wide rules, to give the Charging Bay swatch a gradient of its own:

```scss
// Match the theme swatch in the sidebar to the custom "charging bay" theme
#sidebar {
  .color-swatch-widget .color-swatch-option-handler.charging-bay {
    background: linear-gradient(135deg, var(--secondary-color) 0%, #fff 100%);
  }
}
```

### Step 6: Keep the Layout Settings in Sync

Widening the container in SCSS is only half the change.
VLT also reads the container width from configuration, in {file}`src/config/settings.ts`.
Add the `layout` block to the file that Cookieplone generated.
Do not replace the file, or you will drop your language settings:

```typescript
import type { ConfigType } from '@plone/registry';

export default function install(config: ConfigType) {
  // ... the language settings generated by Cookieplone ...

  // Added in this step
  config.settings.layout = {
    ...config.settings.layout,
    defaultContainerWidth: 1120,
  };

  return config;
}
```

This value is not used for layout—the CSS custom property does that.
It is used to compute the `sizes` attribute of responsive images in teasers and listings, which tells the browser how wide an image will actually be, so that it can pick the right scale to download.

If the two values disagree, nothing breaks visibly, but the browser picks image scales for the wrong width.
When the configured width is too small, images look soft; when it is too large, pages download bigger images than they need.
Whenever you change `$default-container-width`, change `defaultContainerWidth` to match.

```{note}
`config.settings.layout` also carries `tabletBreakpoint`, 768 by default, which is used in the same calculation.
It matches VLT's `$largest-mobile-screen` SCSS variable, so if you change VLT's breakpoints, update it as well.
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

{file}`_main.scss` is the entry point that Volto injects after all of VLT's styles.
Import your partials there, in the order you want them applied:

```scss
// src/theme/_main.scss
// ... your @font-face rules, :root tokens, and site-wide rules above ...

@import './blocks/button';
@import './blocks/grid';
@import './blocks/slider';
@import './blocks/teaser';
```

{file}`_variables.scss` needs no import, because Volto injects it on its own.

## Checkpoint

Restart the frontend and confirm the following before moving on:

- The site renders in Chakra Petch, and the header and footer show their gradients.
- Links in body text are teal, rather than the color of the surrounding text.
- Opening a page in edit mode and selecting a Text block shows **Default** and **Charging Bay** in the **Background color** control, and the Charging Bay swatch shows a gradient.
- Choosing **Charging Bay** for a block gives it the teal wash.

## Further Reading

- [Color system](https://volto-light-theme.readthedocs.io/conceptual-guides/color-system.html)
- [Colors reference](https://volto-light-theme.readthedocs.io/reference/colors.html)
- [Layout](https://volto-light-theme.readthedocs.io/conceptual-guides/layout.html)
