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
      '--theme-color': '#fff',
      '--theme-high-contrast-color': '#ecebeb',
      '--theme-foreground-color': '#000',
      '--theme-low-contrast-foreground-color': '#555555',
    },
    name: 'default',
    label: 'Default',
  },
  {
    style: {
      '--theme-color': '#ecebeb',
      '--theme-high-contrast-color': '#fff',
      '--theme-foreground-color': '#000',
      '--theme-low-contrast-foreground-color': '#555555',
    },
    name: 'grey',
    label: 'Grey',
  },
];
```

Users select block themes through the `themeColorSwatch` widget in the block sidebar. This widget renders colored buttons using each theme's `--theme-color` value, allowing visual theme selection.

### Container Width System

VLT uses three types of container widths:

```scss
// Three-width layout system
--layout-container-width: 1440px;  // for major elements like headers & large Blocks
--default-container-width: 940px;  // balanced content presentation for most Blocks
--narrow-container-width: 620px;   // optimal readability for text
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

### Step 1: Install VLT and Recommended Block Add-ons

Navigate to the `frontend/packages/my-vlt-project` folder and install VLT:

```bash
pnpm install @kitconcept/volto-light-theme@latest
```

Volto Light Theme comes with several pre-configured add-ons that provide basic blocks for your website. If you'd like to include them, you can add them in the `addons` section in your {file}`package.json`, but this is not required.

Here is the list of recommended addons to install, including VLT, which should be the last element:

```json
"addons": [
  "@eeacms/volto-accordion-block",
  "@kitconcept/volto-button-block",
  "@kitconcept/volto-heading-block",
  "@kitconcept/volto-highlight-block",
  "@kitconcept/volto-introduction-block",
  "@kitconcept/volto-separator-block",
  "@kitconcept/volto-slider-block",
  "@kitconcept/volto-light-theme"
],
```

While in your project package folder, add VLT and the block addons to the `addons` list in your `package.json`:

```json
{
  "name": "my-vlt-project",
  "addons": [
    "@eeacms/volto-accordion-block",
    "@kitconcept/volto-button-block",
    "@kitconcept/volto-heading-block",
    "@kitconcept/volto-highlight-block",
    "@kitconcept/volto-introduction-block",
    "@kitconcept/volto-separator-block",
    "@kitconcept/volto-slider-block",
    "@kitconcept/volto-light-theme"
  ]
}
```

**Important:** VLT must be the last addon in the list to ensure proper style cascade. Your project addon will still be the last applied if defined in `volto.config.js`.

### Step 2: Configure VLT as the Theme Provider

Open the `volto.config.js` file in your `frontend` folder and modify it as shown below:

```javascript
const addons = ['my-vlt-project'];
const theme = '@kitconcept/volto-light-theme';

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

```
dependencies = [
    "Products.CMFPlone==6.1.3",
    "plone.api",
    "plone.restapi",
    "plone.volto",
    "kitconcept.voltolighttheme==7.3.1",
]
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

Create the files:

```bash
cd src
mkdir -p components/blocks config theme/blocks
touch config/settings.ts config/blocks.ts
touch index.ts
touch theme/_main.scss theme/_site.scss
```

Remember that if you add new files to your project, it will be necessary to restart your Plone frontend.


---