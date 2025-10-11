---
myst:
  html_meta:
    "description": "Design system implementation & theming"
    "property=og:description": "Design system implementation & theming"
    "property=og:title": "Design system implementation & theming"
    "keywords": "Plone, Volto, Training, Theme, Footer"
---

# Design System Implementation & Theming

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

If you're using custom fonts, add the font files to your theme directory. Create a `fonts` folder in your theme directory and place your font files there:

```
src/theme/fonts/Chakra_Petch/
  ├── ChakraPetch-Regular.ttf
  ├── ChakraPetch-Bold.ttf
  └── ... (other font weights/styles)
```

This ensures the font files are bundled with your theme and can be referenced in your SCSS files.

### Step 2: Create _site.scss

In `src/theme/_site.scss`, define your color variables, custom properties and block-specific styles:

```scss
@font-face {
  font-family: 'Chakra Petch';
  src: url('./fonts/Chakra_Petch/ChakraPetch-Regular.ttf') format('truetype');
}

:root {
  // Extract these from your design
  --accent-color: #3b5759;
  --accent-foreground-color: #fff;
  --secondary-color: #afcac8;

  // Typography
  --text-base: 1.15rem;
  --custom-main-font: 'Chakra Petch', sans-serif;
  --line-height-factor: 1.5;

  // Gradients for header/footer
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

  // Container widths (customized)
  --default-container-width: 1440px;
  --layout-container-width: 90%;

  // Link color
  --link-foreground-color: #157a7a;

  // Breadcrumbs
  --breadcrumbs-background: var(--background, #fff);
  --breadcrumbs-foreground: var(--secondary-foreground-color, #3b5759);

  .breadcrumbs {
    border-bottom: 1px solid #afcac8;
  }

  // Block-specific styles
  #page-document,
  #page-edit,
  #page-add {
    .blocks-group-wrapper:first-child {
      padding-top: 0;

    }
    .block {

      &.__button {
        .button {
          button {
            padding: 1rem;
          }
        }
      }

      &.__button {
        .ui.button:hover {
          --theme-color: #fff;
        }
      }

      &.slider {
        .teaser-item-title {
          background: rgba(255, 255, 255, 0.1);
          color: var(--theme-foreground-color) !important;
          backdrop-filter: blur(20px) saturate(110%);
          -webkit-backdrop-filter: blur(20px) saturate(180%);
          box-shadow:
            0 8px 32px 0 rgba(31, 135, 125, 0.1),
            inset 0 0 0 1px rgba(255, 255, 255, 0.1);
        }
      }

      &.gridBlock {
        .four {
          .slate:not(.inner) {
            padding: 2.5rem;
            padding-top: 4rem !important;
            backdrop-filter: blur(20px) saturate(110%);
            -webkit-backdrop-filter: blur(20px) saturate(180%);
            box-shadow:
              0 8px 32px 0 rgba(31, 135, 125, 0.1),
              inset 0 0 0 1px rgba(255, 255, 255, 0.1);
          }
        }
      }

      &.teaser {
        .card {
          .card-inner {
            .card-summary {
              padding: $spacing-large;
            }
          }
        }
      }
    }


  }
}

#sidebar {
 .color-swatch-widget {
      .buttons button.teal {
        background: linear-gradient(135deg, var(--secondary-color) 0%, #fff 100%);
      }
    }
}
```

### Step 3: Configure Block Themes

In `src/config/blocks.ts`, define block themes:

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
      name: 'teal',
      label: 'Teal',
    },
  ];

  return config;
}
```

### Step 4: Main Index Configuration

In `src/index.ts`:

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

### Step 5: Import SCSS Files

In `src/theme/_main.scss`:

```scss
@import './site';
```

---