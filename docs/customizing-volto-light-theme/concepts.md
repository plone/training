---
myst:
  html_meta:
    "description": "Foundation, Concepts & Project Setup"
    "property=og:description": "Foundation, Concepts & Project Setup"
    "property=og:title": "Foundation, Concepts & Project Setup"
    "keywords": "Plone, Volto, Training, Volto Light Theme"
---

# Foundation, Concepts & Project Setup

## The Project

Rather than theme an abstract site, this training builds one: **the Robotarium**, a neighborhood workshop that lends robots the way a library lends books. Members browse the fleet, check what is charged and available, and book a unit for the afternoon.

It is a small site with an ordinary shape—a fleet to list, a workshop to describe, and a way to visit—which is exactly what makes it useful here. Every VLT feature the training covers earns its place by solving something the Robotarium actually needs:

| The site needs | You will learn |
| --- | --- |
| A look that is its own, not the default | Design tokens, color system, block themes |
| A full-width opening on the landing page | Building a custom block with VLT's widgets |
| A fleet listing showing charge levels | Summary components and listing variations |
| A booking button on each robot | The Card primitive and its Actions slot |
| A sign-up form above the footer | Slots |

The project add-on is called `robotarium` throughout. If you would rather build something else, every step works the same with your own name substituted; only the copy changes.

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

These six properties are not declared as plain custom properties.
VLT registers them with the CSS [`@property`](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/At-rules/@property) at-rule, which declares their type and their default value in one place:

```scss
@property --primary-color {
  inherits: true;
  initial-value: #fff;
  syntax: '<color>';
}
```

Registering them buys three things that matter for a theme:

- The `initial-value` is the default, so the property always resolves to a valid color even when nothing has set it.
- The `<color>` syntax makes the value typed, so an invalid value is rejected instead of silently cascading.
- Typed properties can be interpolated, so transitions and `color-mix()` behave predictably.

You override them the same way as any other custom property, by assigning to them in `:root`.

### Semantic Color Properties

As an additional layer on top of the main color properties, we have set in place some semantic custom properties for the basic layout sections. As a default they use the values from the main color variables, but they can be detached if desired by setting new color values. However, leaving these color relationships as they are helps create a cohesive final design:

```scss
// Header
--header-background: var(--primary-color);
--header-foreground: var(--primary-foreground-color);

// Footer
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
--link-color: #0070a2;
```

Links are the one exception to the pattern above.
By default `<a>` elements inherit `--theme-foreground-color`, so they take the foreground color of whatever block theme they sit in, rather than a color of their own.
VLT ships `--link-foreground-color` as an opt-in: define it in your project to give links a distinct color everywhere.

```scss
:root {
  // Turn links into a different color than the theme foreground color
  --link-foreground-color: var(--link-color);
}
```

### Block Themes

VLT includes a block theme system that enables individual blocks to use distinct color palettes. These themes are configured in `config.blocks.themes` and applied through the StyleWrapper system at runtime.

**The four core block theme variables:**

- `--theme-color`: Primary background color—the most visible color in the block
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

Users select a block theme from the **Background color** control in the block sidebar's **Styling** tab.
VLT's `defaultStylingSchema` adds a `theme` field to the block's schema and renders it with the `color_picker` widget, which draws one button per configured theme using that theme's `--theme-color` as the button color.

```{note}
`color_picker` is a legacy name for what is really a swatch picker, and VLT registers the very same `ColorSwatch` component under both `color_picker` and `colorSwatch`.
VLT's own source says as much, with a rename planned for Volto 19.

Do not confuse it with two similarly named widgets:

- `colorPicker` is a different widget entirely—a full color input with a contrast checker—used for the site-wide colors that the backend behaviors expose.
- `themeColorSwatch` is registered by VLT but currently is not used by any schema VLT ships.
```

### Container Width System

VLT uses three types of container widths:

```scss
// Three-width layout system
--layout-container-width: 1440px; // for major elements like headers & large Blocks
--default-container-width: 940px; // balanced content presentation for most Blocks
--narrow-container-width: 620px; // optimal readability for text
```

Those three are the site-wide scale. Individual blocks never read them directly. Instead, each block carries a `--block-width` property that points at one of them, and the `blockWidth` widget is what chooses the target:

| Token stored | `--block-width` becomes | Resulting width |
| --- | --- | --- |
| `narrow` | `var(--narrow-container-width)` | 620px |
| `default` | `var(--default-container-width)` | 940px |
| `layout` | `var(--layout-container-width)` | 1440px |
| `full` | `100%` | edge to edge |

The indirection is what makes the scale worth having. A block's stylesheet only ever writes `max-width: var(--block-width)`, so it never needs to know which of the three it was handed, and changing `--default-container-width` in one place moves every block set to `default`. Only `full` steps outside the scale, which is why it resolves to a plain `100%` rather than to a container width.

The section on style fields below explains how the stored token becomes that value.

### Block Alignment

The `blockAlignment` widget works the same way, storing one of `left`, `center`, or `right` and resolving it to `--block-alignment`. The three tokens map to these values:

```scss
--align-left: start;
--align-center: center;
--align-right: end;
```

### Style Fields and the `:noprefix` Convention

Width and alignment are both **style fields**, and every style field follows the same two-step process: store a token, then resolve that token to a style object at render time.

What a block actually saves is short. A block set to narrow width and left alignment stores this in its `styles` object:

```json
{
  "blockWidth:noprefix": "narrow",
  "align:noprefix": "left"
}
```

Only the tokens are stored—no CSS, no custom property values. Resolution happens when the block renders:

1. For each key in `styles`, VLT looks up a `styleFieldDefinition` utility registered under **that exact key**.
2. The utility returns a list of style definitions. For `blockWidth:noprefix` that list is `config.blocks.widths`.
3. VLT finds the definition whose `name` matches the stored token and takes its `style` object. For `narrow`, that is `{ '--block-width': 'var(--narrow-container-width)' }`.
4. The StyleWrapper injects that object as an inline style on the block.

Storing tokens rather than values is what makes the system re-themeable. Change what `narrow` means in `config.blocks.widths` and every block already set to `narrow` follows, because the content only ever recorded the word.

Separately, the StyleWrapper turns each style field into a CSS class.
By default it prefixes the class with the field name, so a field named `align` with the value `center` produces `has--align--center`.

A field name ending in `:noprefix` opts out of that prefixing.
VLT uses this suffix for its own style fields, and registers the matching style definitions under the same literal name:

```typescript
config.registerUtility({
  name: 'align:noprefix',
  type: 'styleFieldDefinition',
  method: ({ data }) =>
    config.blocks.blocksConfig?.[data?.['@type'] ?? '']?.alignments ||
    config.blocks.alignments,
});
```

The suffix is part of the field name, not decoration.
A field named `align` and a field named `align:noprefix` are two different fields: only the second one matches the utility above, and only the second one gets its CSS custom properties injected.
The three style fields VLT defines this way are `align:noprefix`, `blockWidth:noprefix`, and `size:noprefix`.


### Generated Block Classes

Beyond the style fields, VLT registers a set of `styleClassNameExtenders` that inspect each block's position in the page and inject extra classes on it.
This is what lets the theme control vertical spacing between blocks from CSS alone, without a block needing to know anything about its neighbors.

The classes available on every block are:

| Class | Injected when |
| --- | --- |
| `next--is--${type}` | the following block is of that type |
| `previous--is--same--block-type` | the preceding block has the same type |
| `next--is--same--block-type` | the following block has the same type |
| `is--first--of--block-type` | the preceding block has a different type |
| `is--last--of--block-type` | the following block has a different type |
| `has--headline` | the block has a headline, or follows a heading block |
| `previous--has--same--backgroundColor` | the preceding block uses the same theme |
| `next--has--same--backgroundColor` | the following block uses the same theme |
| `previous--has--different--backgroundColor` | the preceding block uses a different theme |
| `next--has--different--backgroundColor` | the following block uses a different theme |
| `has--block-width--${width}` | always, from the `blockWidth:noprefix` field |
| `has--block-alignment--${alignment}` | always, from the `align:noprefix` field |
| `has--background-color--${theme}` | always, from the block's selected theme |

You will see these used throughout VLT's own stylesheets, and in the examples later in this training.
A typical use is collapsing the gap between two adjacent blocks that share a background, so the pair reads as one band of color:

```scss
.block.listing {
  &.next--has--same--backgroundColor.next--is--same--block-type {
    .listing-item:last-child {
      padding-bottom: 0;
      border-bottom: none;
    }
  }
}
```

Because the extenders are registered in configuration, a project can add its own to inject any class it needs.

## Create a New Project with Cookieplone

When creating your Plone project with **Cookieplone**, choose template **1, "Volto Project"**, then answer the prompts.

The defaults are fine for almost everything, but two answers matter for the rest of this training:

| Prompt | Default | Answer |
| --- | --- | --- |
| `[1/19] Project Title` | `Project Title` | `robotarium` |
| `[3/19] Project Slug` | `robotarium` | accept |
| `[8/19] Plone Version` | `6.2.1` | accept |
| `[9/19] Volto Version` | `19.4.0` | accept |
| `[10/19] Python Package Name` | `robotarium` | accept |
| `[11/19] Volto Addon Name` | `volto-robotarium` | **`robotarium`** |
| everything else | | accept |

```{important}
This is where the project gets its name.
The Project Title you type at `[1/19]` becomes the project slug, the output folder, and the Python package name, and it is what every path in this training refers to.

Pay particular attention to `[11/19] Volto Addon Name`: Cookieplone offers `volto-robotarium`, prefixed with `volto-`.
This training uses `robotarium`, so override that default.
If you accept the default instead, or build something other than a Robotarium, every path below of the form {file}`frontend/packages/robotarium/…` becomes {file}`frontend/packages/<your addon name>/…`.
```

You should end up with this shape:

```console
robotarium/
├── Makefile
├── backend/
│   ├── pyproject.toml
│   └── src/robotarium/
└── frontend/
    ├── mrs.developer.json
    ├── volto.config.js
    └── packages/robotarium/     <- your project add-on
```

For more detail, see the [Cookieplone guide](https://6.docs.plone.org/install/create-project-cookieplone.html).

## Installing Volto Light Theme

VLT is shipped as two add-ons that you must install together:

- the frontend Volto add-on `@kitconcept/volto-light-theme`, which is also a theme add-on,
- the backend Plone add-on `kitconcept.voltolighttheme`, which provides the site customization behaviors.

```{note}
This training targets the VLT 8 line, which is currently released as alpha (`8.0.0-alpha.x` on npm, `8.0.0a.x` on PyPI), and is the version documented in the [official VLT install guide](https://volto-light-theme.readthedocs.io/how-to-guides/install.html).
If you need a stable release instead, use the latest 7.x version of both packages and skip the "install the recommended add-ons as dependencies" step, since 7.x still ships them as `peerDependencies`.
```

### Step 1: Install VLT and Recommended Block Add-ons

VLT is installed like any other Volto add-on, as a dependency of your project add-on in {file}`frontend/packages/robotarium/package.json`:

```json
{
  "dependencies": {
    "@kitconcept/volto-light-theme": "^8.0.0-alpha.31"
  }
}
```

From the root of your project, you can let pnpm add it to the workspace package for you:

```bash
pnpm --filter robotarium add @kitconcept/volto-light-theme@alpha
```

Volto Light Theme supports all core blocks, and it also supports blocks coming from a set of recommended add-ons that provide the basic blocks for your website.
Including them is not required, and you can pick only the ones you want to use.

Since VLT 8.0.0, these recommended add-ons are no longer declared as `peerDependencies` of VLT, so you have to install them yourself as dependencies of your project add-on in {file}`frontend/packages/robotarium/package.json`:

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

Don't install anything yet.
The backend needs an edit too, and a single command at the end installs both—see {ref}`vlt-install-step-3`.

### Step 2: Configure VLT as the Theme Provider

VLT is not only a regular add-on, it is also a theme add-on, so it has to be declared as the theme of your project.
How you do that depends on your Volto version.

For Volto 18.29.1 or later, and 19.0.0-alpha.10 or later, declare it with the `theme` key of your project add-on {file}`frontend/packages/robotarium/package.json`, next to the `addons` key:

```json
{
  "addons": [
    ...,
    "@kitconcept/volto-light-theme"
  ],
  "theme": "@kitconcept/volto-light-theme"
}
```

Cookieplone already generates both keys for you, as `"addons": []` and `"theme": ""`, so this is an edit rather than something you add from scratch.

For older Volto versions, open the {file}`volto.config.js` file in your `frontend` folder and declare the theme there instead:

```javascript
const addons = ["robotarium"];
const theme = "@kitconcept/volto-light-theme";

module.exports = {
  addons,
  theme,
};
```

You'll need to restart your Plone frontend to see the changes.

That's it! Your project should now be using Volto Light Theme with its additional blocks and components.

(vlt-install-step-3)=

### Step 3: Add the Backend Package and Install Everything

Edit {file}`backend/pyproject.toml` and add `kitconcept.voltolighttheme` to the dependencies array:

```toml
dependencies = [
    "Products.CMFPlone==6.2.1",
    "plone.api",
    "plone.restapi",
    "plone.volto",
    "kitconcept.voltolighttheme==8.0.0a31",
]
```

Both manifests are now edited, so install the whole project in one step, from the project root:

```bash
make install
```

### Step 4: Start the Servers and Install the Backend Add-on

Start your development environment, from the project root, in two terminals:

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

The backend add-on ships five behaviors. None of them is enabled automatically, because each one adds fields to the Plone Site edit form and you should opt into the ones you want.

| Behavior | Shown in the Behaviors tab as | What it adds |
| --- | --- | --- |
| `voltolighttheme.header` | Header customizations for sites/subsites | Site logo, complementary logo, fat menu toggle, intranet header, header actions |
| `voltolighttheme.theme` | Theme colors customizations for sites/subsites | Five color fields for the navigation, fat menu, and footer—see below |
| `voltolighttheme.footer` | Footer customizations for sites/subsites | Footer links, footer logos and their size, colophon text |
| `kitconcept.footer` | kitconcept specific footer customizations | The additional footer arrangement used by kitconcept distributions |
| `kitconcept.sticky_menu` | Sticky menu | A menu fixed to the right side of the screen |

To activate them:

1. Go to http://localhost:3000/controlpanel/dexterity-types/Plone%20Site
2. In the "Behaviors" tab, tick the behaviors from the table above that you want
3. Click "Save"

The first three are the ones this training uses. Enable all five if you want to see everything the add-on offers.

These behaviors put the knobs on the content type they are applied to, so applying them to the Plone Site configures the whole site, and applying them to a subsite configures that branch instead.

#### What the theme behavior actually does

The behavior adds five empty, optional fields to the edit form, each rendered with the `colorPicker` widget:

| Field | Label in the form | Custom property it sets |
| --- | --- | --- |
| `header_foreground` | Navigation Text Color | `--header-foreground` |
| `accent_foreground_color` | Fat Menu / Breadcrumbs Text Color | `--accent-foreground-color` |
| `accent_color` | Fat Menu Background Color | `--accent-color` |
| `secondary_foreground_color` | Footer Font Color | `--secondary-foreground-color` |
| `secondary_color` | Footer Background Color | `--secondary-color` |

Note that there is no primary color pair here: `primary_color` exists in VLT's frontend color map but is deliberately commented out of the behavior's fieldset.

```{important}
Those declarations land in `:root` from a tag in the document head, at the same specificity as the design tokens you will define in the next chapter.
If you set `--accent-color` in your project's stylesheet **and** an editor fills in Fat Menu Background Color, the editor's value is the one that applies.
That is the intended division of labour—the behaviors exist so that editors can override the theme—but it does mean these five properties are not yours to fix from CSS once the behavior is active.
```

```{note}
Behaviors can be added in new releases, and this table reflects `kitconcept.voltolighttheme` 8.0.0a31.
The authoritative list is the behavior registration in the add-on itself, at {file}`backend/src/kitconcept/voltolighttheme/behaviors/configure.zcml` in the [VLT repository](https://github.com/kitconcept/volto-light-theme).
See the [site customization guide](https://volto-light-theme.readthedocs.io/conceptual-guides/site-customization.html) for what each field does.
```

Now your project should have the VLT Site configurations available.

## File Structure Setup

Let's set up the recommended file structure in your project add-on's `src` folder.
Cookieplone already gave you some of it—`index.ts` and `config/settings.ts` exist and have content, so you are filling in the gaps rather than starting from nothing:

```console
src/
├── components/
│   └── blocks/          # new
├── config/
│   ├── settings.ts      # exists, generated with your language settings
│   └── blocks.ts        # new
├── index.ts             # exists, generated with applyConfig()
└── theme/               # new
    ├── blocks/
    ├── _variables.scss
    └── _main.scss
```

From {file}`frontend/packages/robotarium/src`:

```bash
mkdir -p components/blocks config theme/blocks
touch config/blocks.ts theme/_variables.scss theme/_main.scss
```

```{warning}
Do not overwrite the generated {file}`index.ts` and {file}`config/settings.ts`.
The generated `settings.ts` holds your `isMultilingual`, `supportedLanguages`, and `defaultLanguage` values, and `index.ts` already wires it up.
Every later step in this training that shows one of these two files is showing an **edit**, not a replacement.
```

Remember that if you add new files to your project, it will be necessary to restart your Plone frontend.

### The Two Theme Insertion Points

Two of those filenames are load-bearing.
Volto scans every add-on for {file}`theme/_variables.scss` and {file}`theme/_main.scss`, and injects whichever it finds into the theme's stylesheet at two different points:

| File | Injected | Use it for |
| --- | --- | --- |
| {file}`theme/_variables.scss` | **before** VLT's own variables | the few SCSS variables VLT compiles with |
| {file}`theme/_main.scss` | **after** all of VLT's styles | everything else, including all your custom properties |

The order is what makes each one useful.
No other filename is special—`theme/blocks/` and anything else you add are ordinary partials that become part of the build only because {file}`_main.scss` imports them.

```{note}
Volto skips these two files for whichever add-on is registered as the `theme`.
They work for {file}`robotarium` precisely because VLT, not your project, is the theme add-on.
```

#### Prefer CSS custom properties

Almost all of your theming should be CSS custom properties written in {file}`_main.scss`, not SCSS variables.

VLT is built as a custom-property system: the color pairs, the semantic properties, the container widths, and the block themes are all custom properties, resolved in the browser. That is what makes them overridable per block, per section, and at runtime—a block theme works by re-declaring `--theme-color` on one block, which no build-time variable could do. Setting your design tokens as custom properties in `:root` is the normal path, and it is what the next chapter does:

```scss
// src/theme/_main.scss
:root {
  --primary-color: #10131a;
  --accent-color: #d8f24e;
  --link-color: #2f5fd8;
}
```

{file}`_variables.scss` is the narrow exception, for values VLT **computes with at build time**. VLT declares its SCSS variables with `!default`, so each one applies only when nothing has already set it. Since {file}`_variables.scss` is injected first, anything you assign there wins—and it is the *only* place they can be changed, because by the time {file}`_main.scss` is injected, VLT's stylesheets have already been compiled:

```scss
// src/theme/_variables.scss
$tablet-breakpoint: 900px;
$default-container-width: 1120px;
```

Two kinds of value belong there:

- **Breakpoints**, which cannot be custom properties at all, since media queries cannot read them.
- **The container widths**, which are subtler and worth understanding.

The rule of thumb: custom properties for anything meant to vary per block, per section, or at runtime—which is nearly everything, and all of the color system. SCSS variables only for the handful of values VLT compiles into media queries and mixins.

## Checkpoint

Restart both servers and confirm the install landed before moving on. Most trouble in later chapters traces back to one of these:

- The site at http://localhost:3000 renders in VLT's styling, not Volto's default Pastanaga theme. If it looks unchanged, VLT is registered as an add-on but not as the `theme`.
- Editing a page and selecting a block shows a **Background color** control in the sidebar's **Styling** tab. This confirms VLT's block configuration is applied.
- The add-ons control panel lists **Volto Light Theme** as installed, and the Plone Site content type shows the `voltolighttheme` behaviors as active.
- Adding an empty {file}`src/theme/_main.scss` with a single obvious rule, such as `body { border-top: 4px solid red; }`, actually shows that border. If it does not, your add-on is not being picked up as a theme add-on, and no amount of CSS in later chapters will apply.

## Further Reading

This training covers the parts of VLT you need to build a project. The theme's own documentation goes deeper on each topic:

- [Color system](https://volto-light-theme.readthedocs.io/conceptual-guides/color-system.html)
- [Layout](https://volto-light-theme.readthedocs.io/conceptual-guides/layout.html)
- [Vertical spacing](https://volto-light-theme.readthedocs.io/conceptual-guides/vertical-spacing.html)
- [Install guide](https://volto-light-theme.readthedocs.io/how-to-guides/install.html)
