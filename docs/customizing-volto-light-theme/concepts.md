---
myst:
  html_meta:
    "description": "Foundation, Concepts & Project Setup"
    "property=og:description": "Foundation, Concepts & Project Setup"
    "property=og:title": "Foundation, Concepts & Project Setup"
    "keywords": "Plone, Volto, Training, Volto Light Theme"
---

# Foundation, Concepts & Project Setup

## Volto Light Theme Core Concepts

Volto Light Theme (VLT) is a customizable theme built for the Volto frontend of the Plone CMS. It provides a foundation that aims to solve many common design challenges, while remaining flexible enough for customization. It's particularly valuable because it is based on real-world experience, while simultaneously embodying the Volto vision for the future. This module will help you understand the core concepts in VLT and create a mental map of its parts.

### Base Styling

VLT is designed with simplicity and a minimal aesthetic in mind. The three core principles are:

- **Consistency**: Predictable design patterns across all components
- **Accessibility**: WCAG compliant with contrast checkers and semantic HTML
- **Intuitiveness**: Clear visual hierarchy and user-friendly interfaces

### Customizable Variables

VLT offers a set of CSS custom properties (variables) that allow developers to customize various design elements:

- **Colors**: Using paired foreground/background color system
- **Spatial relationships**: Container widths and spacing scales
- **Layouts**: Three-width container system

These variables can be easily overridden in your project to match the desired visual identity.

### Color System

The color system is designed so that colors work in couples: a "background color" and a "foreground color". The "foreground color" is often called "text color" in other systems, but since we want to use this value for more than text—like icons or borders—this works better as a generic term. Colors that do not specify "foreground" in the name are meant to be background colors.

The main color properties for a project using VLT are:

```scss
--primary-color: #fff;
--primary-foreground-color: #000;

--secondary-color: #ecebeb;
--secondary-foreground-color: #000;

--accent-color: #ecebeb;
--accent-foreground-color: #000;
```

### Semantic Color Properties

As an additional layer on top of the main color properties, we have set in place some semantic custom properties for the basic layout sections. As a default they use the values from the main color variables, but they can be detached if desired by setting new color values. However, leaving these color relationships as they are helps create a cohesive final design:

```scss
// Header
--header-background: var(--primary-color);
--header-foreground: var(--primary-foreground-color);

//Footer
--footer-background: var(--secondary-color);
--footer-foreground: var(--secondary-foreground-color);

// Fat Menu
--fatmenu-background: var(--accent-color);
--fatmenu-foreground: var(--accent-foreground-color);

// Breadcrumbs
--breadcrumbs-background: var(--accent-color);
--breadcrumbs-foreground: var(--accent-foreground-color);

// Search bar
--search-background: var(--accent-color);
--search-foreground: var(--accent-foreground-color);

// Link color
--link-foreground-color: var(--link-color);
```

### Block Themes

VLT includes a block theme system that enables individual blocks to use distinct color palettes. These themes are configured in `config.blocks.themes` and applied through the StyleWrapper system at runtime.

**The four core block theme variables:**

- `--theme-color`: Primary background color — the most visible color in the block
- `--theme-high-contrast-color`: Secondary background color for nested elements (e.g., cards within a block) to create visual separation from the main background
- `--theme-foreground-color`: Default text and icon color
- `--theme-low-contrast-foreground-color`: Subdued text color for secondary content like placeholders or helper text

While the system can be extended with non-color CSS properties, the default four variables establish the color foundation for each theme.

**Example configuration:**

```typescript
config.blocks.themes = [
  {
    style: {
      "--theme-color": "#fff",
      "--theme-high-contrast-color": "#ecebeb",
      "--theme-foreground-color": "#000",
      "--theme-low-contrast-foreground-color": "#555555",
    },
    name: "default",
    label: "Default",
  },
  {
    style: {
      "--theme-color": "#ecebeb",
      "--theme-high-contrast-color": "#fff",
      "--theme-foreground-color": "#000",
      "--theme-low-contrast-foreground-color": "#555555",
    },
    name: "grey",
    label: "Grey",
  },
];
```

Users select block themes through the `themeColorSwatch` widget in the block sidebar. This widget renders colored buttons using each theme's `--theme-color` value, allowing visual theme selection.

### Container Width System

VLT uses three types of container widths:

```scss
// Three-width layout system
--layout-container-width: 1440px; // for major elements like headers & large Blocks
--default-container-width: 940px; // balanced content presentation for most Blocks
--narrow-container-width: 620px; // optimal readability for text
```

The VLT `BlockWidthWidget` stores the value of the custom property `--block-width` so that it can be used by the StyleWrapper when injecting styles into the markup.

### Block Alignment

The `BlockAlignmentWidget` takes advantage of the StyleWrapper by setting the `--block-alignment` property. The three default options are:

```scss
--align-left: start;
--align-center: center;
--align-right: end;
```

## Create a New Project with Cookieplone

We recommend creating your Plone project with **Cookieplone**. Our comprehensive documentation provides step-by-step guidance to help you get started. For detailed installation instructions, visit our [Cookieplone guide](https://6.docs.plone.org/install/create-project-cookieplone.html).

## Installing Volto Light Theme

VLT is shipped as two add-ons that you must install together:

- the frontend Volto add-on `@kitconcept/volto-light-theme`, which is also a theme add-on,
- the backend Plone add-on `kitconcept.voltolighttheme`, which provides the site customization behaviors.

```{note}
This training targets the VLT 8 line, which is currently released as alpha (`8.0.0-alpha.x` on npm, `8.0.0a.x` on PyPI), and is the version documented in the [official VLT install guide](https://volto-light-theme.readthedocs.io/how-to-guides/install.html).
If you need a stable release instead, use the latest 7.x version of both packages and skip the "install the recommended add-ons as dependencies" step, since 7.x still ships them as `peerDependencies`.
```

### Step 1: Install VLT and Recommended Block Add-ons

VLT is installed like any other Volto add-on, as a dependency of your project add-on in {file}`frontend/packages/my-vlt-project/package.json`:

```json
{
  "dependencies": {
    "@kitconcept/volto-light-theme": "^8.0.0-alpha.31"
  }
}
```

From the root of your project, you can let pnpm add it to the workspace package for you:

```bash
pnpm --filter my-vlt-project add @kitconcept/volto-light-theme@alpha
```

Volto Light Theme supports all core blocks, and it also supports blocks coming from a set of recommended add-ons that provide the basic blocks for your website.
Including them is not required, and you can pick only the ones you want to use.

Since VLT 8.0.0, these recommended add-ons are no longer declared as `peerDependencies` of VLT, so you have to install them yourself as dependencies of your project add-on in {file}`frontend/packages/my-vlt-project/package.json`:

```json
{
  "dependencies": {
    "@eeacms/volto-accordion-block": "^12.0.0",
    "@kitconcept/volto-banner-block": "^1.2.0",
    "@kitconcept/volto-bm3-compat": "^1.0.0-alpha.1",
    "@kitconcept/volto-button-block": "5.0.0-alpha.2",
    "@kitconcept/volto-calendar-block": "^1.0.0-alpha.9",
    "@kitconcept/volto-carousel-block": "^3.0.0-alpha.1",
    "@kitconcept/volto-dsgvo-banner": "^4.0.0-alpha.2",
    "@kitconcept/volto-heading-block": "^2.5.0",
    "@kitconcept/volto-highlight-block": "^5.0.0-alpha.2",
    "@kitconcept/volto-introduction-block": "^1.4.1",
    "@kitconcept/volto-logos-block": "^4.0.0-alpha.1",
    "@kitconcept/volto-separator-block": "^5.0.0-alpha.0",
    "@kitconcept/volto-slider-block": "^7.0.0-alpha.1",
    "@plonegovbr/volto-social-media": "^3.0.0-alpha.0",
    "@kitconcept/volto-light-theme": "^8.0.0-alpha.31"
  }
}
```

```{note}
The versions above are the known good versions at the time of writing.
The source of truth, up-to-date list lives in the [recommended add-ons reference](https://volto-light-theme.readthedocs.io/reference/recommended-addons.html) of the VLT documentation.
```

Installing a package is not enough: it also has to be declared as a Volto add-on in the `addons` key of the same {file}`package.json`, with VLT as the last element of the list:

```json
{
  "addons": [
    "@eeacms/volto-accordion-block",
    "@kitconcept/volto-banner-block",
    "@kitconcept/volto-bm3-compat",
    "@kitconcept/volto-button-block",
    "@kitconcept/volto-carousel-block",
    "@kitconcept/volto-dsgvo-banner",
    "@kitconcept/volto-heading-block",
    "@kitconcept/volto-highlight-block",
    "@kitconcept/volto-introduction-block",
    "@kitconcept/volto-logos-block",
    "@kitconcept/volto-separator-block",
    "@kitconcept/volto-slider-block",
    "@plonegovbr/volto-social-media",
    "@kitconcept/volto-light-theme"
  ]
}
```

-**Important:** VLT must be the last addon in the list to ensure proper style cascade. Your project addon will still be the last applied if defined in `volto.config.js`.

Run `pnpm install` from the project root after editing {file}`package.json` by hand, so that the workspace picks up the new dependencies.

### Step 2: Configure VLT as the Theme Provider

VLT is not only a regular add-on, it is also a theme add-on, so it has to be declared as the theme of your project.
How you do that depends on your Volto version.

For Volto 18.29.1 or later, and 19.0.0-alpha.10 or later, declare it with the `theme` key of your project add-on {file}`frontend/packages/my-vlt-project/package.json`, next to the `addons` key:

```json
{
  "addons": [
    ...,
    "@kitconcept/volto-light-theme"
  ],
  "theme": "@kitconcept/volto-light-theme"
}
```

For older Volto versions, open the {file}`volto.config.js` file in your `frontend` folder and declare the theme there:

```javascript
const addons = ["my-vlt-project"];
const theme = "@kitconcept/volto-light-theme";

module.exports = {
  addons,
  theme,
};
```

You'll need to restart your Plone frontend to see the changes.

That's it! Your project should now be using Volto Light Theme with its additional blocks and components.

### Step 3: Install Backend Package

In your backend folder, install the Python package for site customization behaviors.

Edit `backend/pyproject.toml` and add to the dependencies array:

```toml
dependencies = [
    "Products.CMFPlone==6.2.1",
    "plone.api",
    "plone.restapi",
    "plone.volto",
    "kitconcept.voltolighttheme==8.0.0a31",
]
```

Then install the dependency from your backend folder:

```bash
make install
```

### Step 4: Install the Backend Add-on

Start your development environment:

```bash
# Terminal 1 - Backend
make backend-start

# Terminal 2 - Frontend
make frontend-start
```

Once the frontend is running:

1. Go to http://localhost:3000/controlpanel/addons
2. Find "Volto Light Theme" in the list
3. Click "Install"

### Step 5: Activate Behaviors for Plone Site

To enable site customization through the UI:

1. Go to http://localhost:3000/controlpanel/dexterity-types/Plone%20Site
2. In the "Behaviors" tab, activate the desired behaviors
3. Click "Save"

These behaviors let you customize the header, footer, and theme of your Plone site with knobs on the content type they are applied to, either the Plone site or a subsite.
See the [site customization guide](https://volto-light-theme.readthedocs.io/conceptual-guides/site-customization.html) for the details of each behavior.

Now your project should have the VLT Site configurations available.

## File Structure Setup

Let's set up the recommended file structure. In your project add-on's `src` folder, create the following structure:

```console
src/
├── components/
│   └── blocks/
├── config/
│   ├── settings.ts
│   └── blocks.ts
├── index.ts
└── theme/
    ├── blocks/
    ├── _main.scss
    └── _site.scss
```

Create the files in `frontend/paackages/my-vlt-project` :

```bash
cd src
mkdir -p components/blocks config theme/blocks
touch config/settings.ts config/blocks.ts
touch index.ts
touch theme/_main.scss theme/_site.scss
```

Remember that if you add new files to your project, it will be necessary to restart your Plone frontend.
