---
myst:
  html_meta:
    "description": "Design system implementation & theming"
    "property=og:description": "Design system implementation & theming"
    "property=og:title": "Design system implementation & theming"
    "keywords": "Plone, Volto, Training, Theme, Footer"
---

# 2. Design System Implementation & Theming

## 2.1 Extracting Design Tokens

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


## 2.2 Implementing Your Design System

VLT has migrated to use standardized color definitions. These use CSS properties that are injected at runtime in the right places, so your CSS can adapt to use them generically. The resulting CSS is simpler, and there's no need to define class names for each color definition.

### Step 1: Create _site.scss

In `src/theme/_site.scss`, define your color variables and custom properties:

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

### Step 2: Configure Block Themes

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
        '--theme-color': `/* White edge bleed for continuity */
                linear-gradient(180deg,
                    rgba(255, 255, 255, 0.9) 0%,
                    rgba(255, 255, 255, 0.6) 8%,
                    rgba(255, 255, 255, 0.3) 12%,
                    transparent 18%,
                    transparent 82%,
                    rgba(255, 255, 255, 0.3) 88%,
                    rgba(255, 255, 255, 0.6) 92%,
                    rgba(255, 255, 255, 0.9) 100%),

                /* Top white highlights - asymmetric cluster */
                radial-gradient(ellipse 900px 650px at 12% 8%,
                    rgba(255, 255, 255, 0.38) 0%,
                    rgba(243, 251, 251, 0.26) 28%,
                    rgba(228, 244, 244, 0.14) 52%,
                    transparent 72%),

                radial-gradient(ellipse 750px 850px at 6% 22%,
                    rgba(255, 255, 255, 0.34) 0%,
                    rgba(238, 249, 249, 0.2) 32%,
                    rgba(220, 240, 240, 0.1) 58%,
                    transparent 78%),

                radial-gradient(ellipse 820px 580px at 88% 12%,
                    rgba(255, 255, 255, 0.42) 0%,
                    rgba(246, 252, 252, 0.28) 30%,
                    rgba(232, 246, 246, 0.15) 54%,
                    transparent 74%),

                /* Bottom white highlights - dispersed asymmetrically */
                radial-gradient(ellipse 980px 620px at 82% 88%,
                    rgba(255, 255, 255, 0.4) 0%,
                    rgba(244, 251, 251, 0.27) 26%,
                    rgba(230, 245, 245, 0.13) 50%,
                    transparent 73%),

                radial-gradient(ellipse 680px 780px at 18% 90%,
                    rgba(255, 255, 255, 0.35) 0%,
                    rgba(240, 250, 250, 0.22) 34%,
                    rgba(225, 242, 242, 0.11) 60%,
                    transparent 80%),

                radial-gradient(ellipse 720px 520px at 68% 94%,
                    rgba(255, 255, 255, 0.3) 0%,
                    rgba(235, 247, 247, 0.17) 38%,
                    transparent 68%),

                /* Color hotspot 1 - upper right quadrant */
                radial-gradient(ellipse 850px 750px at 70% 35%,
                    rgba(175, 202, 200, 0.5) 0%,
                    rgba(180, 206, 204, 0.38) 25%,
                    rgba(190, 212, 210, 0.24) 45%,
                    rgba(200, 220, 218, 0.12) 65%,
                    transparent 85%),

                /* Color hotspot 2 - lower left quadrant */
                radial-gradient(ellipse 920px 800px at 25% 65%,
                    rgba(165, 195, 193, 0.45) 0%,
                    rgba(175, 202, 200, 0.34) 28%,
                    rgba(185, 210, 208, 0.22) 50%,
                    rgba(195, 215, 213, 0.11) 70%,
                    transparent 87%),

                /* Color hotspot 3 - center right */
                radial-gradient(circle 700px at 78% 52%,
                    rgba(170, 198, 196, 0.42) 0%,
                    rgba(180, 205, 203, 0.3) 30%,
                    rgba(192, 214, 212, 0.18) 55%,
                    rgba(205, 222, 220, 0.09) 75%,
                    transparent 90%),

                /* Organic flow connecting hotspots */
                radial-gradient(ellipse 1100px 900px at 45% 48%,
                    rgba(175, 202, 200, 0.28) 0%,
                    rgba(185, 210, 208, 0.18) 35%,
                    rgba(195, 216, 214, 0.1) 60%,
                    rgba(205, 222, 220, 0.05) 78%,
                    transparent 90%),

                /* Additional scattered color pockets */
                radial-gradient(circle 550px at 15% 40%,
                    rgba(172, 198, 196, 0.32) 0%,
                    rgba(182, 207, 205, 0.2) 38%,
                    rgba(195, 216, 214, 0.1) 68%,
                    transparent 85%),

                radial-gradient(ellipse 680px 580px at 88% 68%,
                    rgba(178, 203, 201, 0.35) 0%,
                    rgba(188, 210, 208, 0.22) 35%,
                    rgba(200, 218, 216, 0.11) 65%,
                    transparent 82%),

                radial-gradient(ellipse 620px 720px at 52% 28%,
                    rgba(168, 196, 194, 0.3) 0%,
                    rgba(180, 205, 203, 0.18) 40%,
                    rgba(195, 215, 213, 0.08) 70%,
                    transparent 88%),

                radial-gradient(circle 480px at 35% 78%,
                    rgba(175, 200, 198, 0.28) 0%,
                    rgba(188, 210, 208, 0.15) 42%,
                    transparent 75%),

                /* Asymmetrical accent flows */
                conic-gradient(from 125deg at 28% 44%,
                    transparent 0deg,
                    rgba(178, 203, 201, 0.18) 48deg,
                    rgba(185, 210, 208, 0.14) 95deg,
                    transparent 145deg,
                    rgba(172, 198, 196, 0.12) 235deg,
                    transparent 285deg),

                /* Base gradient foundation - subtle */
                linear-gradient(182deg,
                    #ffffff 0%,
                    #f9fcfc 10%,
                    #ebf4f3 22%,
                    #d8e6e5 35%,
                    #c5d8d6 45%,
                    #b8cece 52%,
                    #c5d8d6 59%,
                    #d8e6e5 69%,
                    #ebf4f3 82%,
                    #f9fcfc 92%,
                    #ffffff 100%)`,
        '--theme-high-contrast-color': 'rgba(255, 255, 255, 0.1)',
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

### Step 3: Configure Settings

In `src/config/settings.ts`:

```typescript
import type { ConfigType } from '@plone/registry';
import installBlocks from './blocks';

export default function install(config: ConfigType) {
  // Language settings
  config.settings.isMultilingual = false;
  config.settings.supportedLanguages = ['en'];
  config.settings.defaultLanguage = 'en';

  installBlocks(config);

  return config;
}
```

### Step 4: Main Index Configuration

In `src/index.ts`:

```typescript
import type { ConfigType } from '@plone/registry';
import installSettings from './config/settings';

function applyConfig(config: ConfigType) {
  installSettings(config);
  return config;
}

export default applyConfig;
```

### Step 5: Import SCSS Files

In `src/theme/_main.scss`:

```scss
@import './site';
```

## 2.3 Customizing Block Styles

Let's add custom styles for specific blocks. In your `_site.scss`, add block-specific styles:

```scss
:root {
  // ... previous variables ...

  #page-document {
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
          --theme-color: white;
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
          .slate {
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
```

---