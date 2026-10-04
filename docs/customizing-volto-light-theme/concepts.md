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

Every VLT feature the training covers earns its place by solving something the Robotarium actually needs:

| The site needs | You will learn | Covered in |
| --- | --- | --- |
| A look that is its own, not the default | Design tokens, the color system, and block themes | {doc}`design-system-implementation` |
| A full-width opening on the landing page | Building a custom block with VLT's widgets | {doc}`block-development-widgets` |
| A fleet listing showing charge levels | Summary components and listing variations | {doc}`advanced-components-bm3` |
| A booking button on each robot | The Card primitive and its Actions slot | {doc}`advanced-components-bm3` |
| A newsletter sign-up at the top of the footer | Slots | {doc}`advanced-components-bm3` |

The project is called `robotarium`, and Cookieplone names its frontend add-on `volto-robotarium`.
If you would rather build something else, every step works the same with your own names substituted.

## Volto Light Theme Core Concepts

Volto Light Theme (VLT) is a customizable theme for the Volto frontend of Plone.
It provides a foundation that solves many common design challenges, while remaining flexible enough for customization.
It is based on real-world projects, and it follows the direction that Volto is taking.

Most of VLT's design decisions are CSS custom properties that your project can override: the color pairs, the container widths, and the palettes that editors apply to blocks.
This section introduces each of them, so that you have a mental map of VLT's parts before you start building.

### Color System

The color system is designed so that colors work in pairs: a background color and a foreground color.
Other systems often call the foreground color the text color, but VLT uses it for more than text, such as icons and borders, so it uses the more generic term.
Colors that do not have "foreground" in their name are background colors.

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

Registering them has three consequences that matter for a theme:

- The `initial-value` is the default, so the property always has a valid color, even when nothing sets it. For the same reason, a fallback such as `var(--accent-color, teal)` is never used.
- The `<color>` syntax makes the value typed, so an invalid value is rejected instead of silently cascading.
- The browser can animate a typed property, so a transition from one color to another is smooth instead of jumping.

VLT registers `--background` the same way, with white as its default, and uses it as the default value of `--primary-color`.

You override these properties the same way as any other custom property, by assigning to them in `:root`.

### Semantic Color Properties

On top of the main color properties, VLT declares semantic properties for the main layout sections.
By default they take their values from the main color properties.
You can set them to other colors, but keeping these relationships helps create a cohesive design:

```scss
// Header
--header-background: var(--primary-color);

// Footer
--footer-background: var(--secondary-color);
--footer-foreground: var(--secondary-foreground-color);

// Fat menu
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

VLT does not declare `--header-foreground` by default.
The navigation items fall back to `--primary-foreground-color`, and the {ref}`theme behavior <light-theme-behavior-colors-label>` sets `--header-foreground` when an editor picks a navigation text color.

Links are the one exception to the pattern above.
VLT declares `--link-color`, but does not use it by default.
Instead, links use `--link-foreground-color` when it is set, and otherwise the foreground color of the block theme they sit in, `--theme-foreground-color`.
To give links a distinct color everywhere, set `--link-foreground-color` in your project:

```scss
:root {
  // Turn links into a different color than the theme foreground color
  --link-foreground-color: var(--link-color);
}
```

### Block Themes

VLT includes a block theme system that lets individual blocks use their own color palette.
The themes are configured in `config.blocks.themes`, and applied through the StyleWrapper when a block renders.

**The four core block theme variables:**

- `--theme-color`: primary background color, the most visible color in the block
- `--theme-high-contrast-color`: secondary background color for nested elements, such as cards within a block, to separate them from the main background
- `--theme-foreground-color`: default text and icon color
- `--theme-low-contrast-foreground-color`: subdued text color for secondary content, such as placeholders or helper text

A theme can also set other CSS properties, but these four variables are the color foundation of each theme.

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

Editors select a block theme from the **Background color** control, in the **Styling** section of the block settings in the sidebar.
VLT's `defaultStylingSchema` adds a `theme` field to the block's schema and renders it with the `color_picker` widget, which draws one swatch per configured theme, colored with that theme's `--theme-color`.
The block stores the name of the selected theme in its `theme` field.

```{note}
`color_picker` is a legacy name for what is really a swatch picker.
VLT registers the same `ColorSwatch` component under both `color_picker` and `colorSwatch`, and a comment in VLT's source notes that the widget should be renamed.

Do not confuse it with two similarly named widgets:

- `colorPicker` is a different widget, a free color input with a contrast checker, used for the site-wide colors that the backend behaviors expose.
- `themeColorSwatch` is registered by VLT, but currently no schema that VLT ships uses it.
```

### Container Width System

VLT uses three container widths:

```scss
// Three-width layout system
--layout-container-width: 1440px; // for major elements like headers and large blocks
--default-container-width: 940px; // balanced content presentation for most blocks
--narrow-container-width: 620px; // optimal readability for text
```

VLT declares these three custom properties from SCSS variables of the same name, such as `$default-container-width`.
To change them, set the SCSS variables, as explained in {ref}`light-theme-custom-properties-label`.

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

(light-theme-style-fields-label)=

### Style Fields and the `:noprefix` Convention

Width and alignment are both **style fields**, and every style field follows the same two-step process: store a token, then resolve that token to a style object at render time.

What a block actually saves is short. A block set to narrow width and left alignment stores this in its `styles` object:

```json
{
  "blockWidth:noprefix": "narrow",
  "align:noprefix": "left"
}
```

Only the tokens are stored—no CSS, no custom property values.
This relies on the widget storing the token rather than a style object, which {ref}`the Cover block <light-theme-cover-actions-label>` in chapter 3 shows how to ensure.
Resolution happens when the block renders:

1. For each key in `styles`, VLT looks up a `styleFieldDefinition` utility registered under **that exact key**.
2. The utility returns a list of style definitions. For `blockWidth:noprefix` that list is `config.blocks.widths`.
3. VLT finds the definition whose `name` matches the stored token and takes its `style` object. For `narrow`, that is `{ '--block-width': 'var(--narrow-container-width)' }`.
4. The StyleWrapper injects that object as an inline style on the block.

Storing tokens rather than values is what makes the system re-themeable. Change what `narrow` means in `config.blocks.widths` and every block already set to `narrow` follows, because the content only ever recorded the word.

Separately, the StyleWrapper turns each style field into a CSS class.
By default it prefixes the class with the field name, so a field named `align` with the value `center` produces `has--align--center`.
A field name ending in `:noprefix` opts out of that prefixing, so `align:noprefix` with the value `center` produces the class `center`.

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

(light-theme-generated-classes-label)=

### Generated Block Classes

Beyond the style fields, VLT adds a set of functions to `config.settings.styleClassNameExtenders`.
They inspect each block's position in the page and inject extra classes on it.
This is what lets the theme control vertical spacing between blocks from CSS alone, without a block needing to know anything about its neighbors.

The classes available on every block are:

| Class | Injected when |
| --- | --- |
| `next--is--${type}` | there is a following block, and `${type}` is its type |
| `previous--is--same--block-type` | the preceding block has the same type |
| `next--is--same--block-type` | the following block has the same type |
| `is--first--of--block-type` | the preceding block has a different type, or there is none |
| `is--last--of--block-type` | the following block has a different type, or there is none |
| `has--headline` | the block has a headline, or follows a Heading block |
| `previous--has--same--backgroundColor` | the preceding block uses the same theme |
| `next--has--same--backgroundColor` | the following block uses the same theme |
| `previous--has--different--backgroundColor` | the preceding block uses a different theme |
| `next--has--different--backgroundColor` | the following block uses a different theme |
| `has--block-width--${width}` | always, from the `blockWidth:noprefix` field, or `default` when it is empty |
| `has--block-alignment--${alignment}` | always, from the `align:noprefix` field, or `center` when it is empty |
| `has--background-color--${theme}` | always, from the block's theme, or `default` when it has none |

When VLT compares themes, a block without a theme, or a missing neighbor, counts as `default`.

You will see these classes throughout VLT's own stylesheets, and in the examples later in this training.
For example, VLT's listing styles use two of them to remove the space below a Grid listing when the next block is another listing with the same background, so the pair reads as one band of color:

```scss
.block.listing.grid {
  &.next--has--same--backgroundColor.next--is--same--block-type {
    .listing-item:last-child {
      padding-bottom: 0 !important;
      border-bottom: none !important;
    }
  }
}
```

Because the extenders are registered in configuration, a project can add its own to inject any class it needs.

## Create a New Project with Cookieplone

This training uses Cookieplone 2.0 to generate the project.
If you have not used Cookieplone before, the [Cookieplone guide](https://6.docs.plone.org/install/create-project-cookieplone.html) lists the tools it needs.

From the folder where you keep your projects, run:

```shell
uvx cookieplone project
```

The `project` argument selects the **Plone 6 Project** template.
Without it, Cookieplone first asks you to choose a category and a template.

Cookieplone then asks a series of questions.
Accept the defaults, except for the project title:

| Question | Default | Answer |
| --- | --- | --- |
| Project Title | `Project Title` | `Robotarium` |
| Project Slug (Used for repository id) | `robotarium` | accept |
| Python Package Name | `robotarium` | accept |
| Use Volto as frontend? | Yes | accept |
| all other questions | | accept |

The title determines the other names.
Cookieplone derives the slug `robotarium` from it, and uses the slug for the output folder and the Python package name.
It also derives the name of the frontend add-on, `volto-robotarium`, without asking, and it picks the Plone and Volto versions for you.
At the time of writing, it generated a project with Plone 6.2.2 and Volto 19.4.1.

```{important}
Every path in this training of the form {file}`frontend/packages/volto-robotarium/…` uses that add-on name.
If you build something other than a Robotarium, the add-on is called `volto-` followed by your project slug, and you should adjust the paths accordingly.
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
    └── packages/volto-robotarium/     <- your project add-on
```

## Installing Volto Light Theme

VLT is shipped as two add-ons that you must install together:

- the frontend Volto add-on `@kitconcept/volto-light-theme`, which is also a theme add-on,
- the backend Plone add-on `kitconcept.voltolighttheme`, which provides the site customization behaviors.

```{note}
This training uses VLT 8.0.0, which requires Volto 19.
The [VLT compatibility table](https://volto-light-theme.readthedocs.io/reference/compatibility.html) lists the Volto versions that each VLT version supports.
```

You first declare both add-ons in your project, and then install everything with a single command.

### Step 1: Declare the Frontend Packages

VLT supports all core blocks, and it also supports blocks from a set of recommended add-ons that provide the basic blocks for your website.
Including them is not required, and you can pick only the ones you want to use.

VLT does not install the recommended block add-ons for you, so you add them to your project add-on yourself, together with VLT.
Open {file}`frontend/packages/volto-robotarium/package.json` and add them to its `dependencies`:

```json
{
  "dependencies": {
    "@eeacms/volto-accordion-block": "^12.0.0",
    "@kitconcept/volto-banner-block": "^1.2.1",
    "@kitconcept/volto-bm3-compat": "^1.0.0-alpha.1",
    "@kitconcept/volto-button-block": "^5.0.0",
    "@kitconcept/volto-carousel-block": "^3.0.0",
    "@kitconcept/volto-dsgvo-banner": "^4.0.0",
    "@kitconcept/volto-heading-block": "^2.5.0",
    "@kitconcept/volto-highlight-block": "^5.0.0",
    "@kitconcept/volto-introduction-block": "^1.4.1",
    "@kitconcept/volto-light-theme": "^8.0.0",
    "@kitconcept/volto-logos-block": "^4.0.0",
    "@kitconcept/volto-separator-block": "^5.0.0",
    "@kitconcept/volto-slider-block": "^7.0.0",
    "@plonegovbr/volto-social-media": "^3.0.0-alpha.0"
  }
}
```

```{note}
These are the known good versions for VLT 8.0.0. The up-to-date list lives in the [recommended add-ons reference](https://volto-light-theme.readthedocs.io/reference/recommended-addons.html) of the VLT documentation.
```

`@kitconcept/volto-bm3-compat` is not a block add-on.
VLT already depends on it, and you list it here because the block you build in chapter 3 imports from it.

Installing a package is not enough: Volto also has to load it as an add-on.
In the same {file}`package.json`, Cookieplone generated two empty keys, `"addons": []` and `"theme": ""`.
List the add-ons in `addons`, and declare VLT as the `theme`:

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
  ],
  "theme": "@kitconcept/volto-light-theme"
}
```

VLT needs both keys, because it is both a regular add-on and a theme add-on.

```{important}
VLT must be the last entry in `addons`.
Volto applies add-ons in the order you list them, and VLT's configuration extends the blocks that the other add-ons register, so it has to run after theirs.

Your project add-on is applied after all of them, because Volto applies the add-ons that an add-on declares before the add-on itself.
```

### Step 2: Declare the Python Package

Edit {file}`backend/pyproject.toml` and add `kitconcept.voltolighttheme` to the `dependencies` array that Cookieplone generated:

```toml
dependencies = [
    "Products.CMFPlone==6.2.2",
    "plone.api",
    "plone.restapi",
    "plone.volto",
    "kitconcept.voltolighttheme==8.0.0",
]
```

Keep the Plone version that Cookieplone generated for you, if it differs from the one shown here.

### Step 3: Install Everything

Both manifests are now edited, so install the whole project in one step, from the project root:

```shell
make install
```

This installs the backend and the frontend, and creates a Plone site with the id `Plone`.

### Step 4: Start the Servers and Install VLT in Plone

Start your development environment, from the project root, in two terminals:

```shell
# Terminal 1 - Backend
make backend-start

# Terminal 2 - Frontend
make frontend-start
```

Once the frontend is running, open http://localhost:3000.
The first time you open the site, a cookie consent dialog from `@kitconcept/volto-dsgvo-banner` covers the page.
Choose one of its options to close it.

Then log in at http://localhost:3000/login with the user `admin` and the password `admin`, and install the backend add-on:

1. Go to http://localhost:3000/controlpanel/addons.
2. In the list of available add-ons, select **Volto Light Theme: Install** to show its details.
3. Select **Install**.

### Step 5: Activate Behaviors for Plone Site

The backend add-on ships five behaviors.
None of them is enabled automatically, because each one adds fields to the edit form of the content type you apply it to, and you should opt into the ones you want.

| Behavior | Shown in the Behaviors tab as | What it adds |
| --- | --- | --- |
| `voltolighttheme.header` | Header customizations for sites/subsites | Site logo, complementary logo, fat menu switch, intranet header switch, site flag, and site actions |
| `voltolighttheme.theme` | Theme colors customizations for sites/subsites | Five color fields for the navigation, fat menu, breadcrumbs, and footer. See {ref}`light-theme-behavior-colors-label`. |
| `voltolighttheme.footer` | Footer customizations for sites/subsites | Footer logos with their size and container width, footer links, and the footer colophon text |
| `kitconcept.footer` | kitconcept specific footer customizations | The footer layout of kitconcept distributions: a footer logo, an address, three link columns, and a sponsor logo with its link |
| `kitconcept.sticky_menu` | Sticky menu | Icon links fixed to the right edge of the screen, their colors, and a switch to show them on mobile |

The header fields work as follows:

Site logo
:   The main logo, at the top left of the header.

Complementary logo
:   A second logo on the right side of the header. Only the intranet header shows it.

Fat menu switch
:   The fat menu is the panel that opens below the navigation when you select a main section. It is enabled by default.

Intranet header switch
:   Replaces the default header with a layout intended for intranet sites.

Site flag
:   A short text shown in a colored pill at the top of the header.

Site actions
:   Links shown at the top right of the header, each with a title, a target URL, and an option to open it in a new tab.

To activate the behaviors:

1. Go to http://localhost:3000/controlpanel/dexterity-types/Plone%20Site.
2. In the **Behaviors** tab, select the behaviors from the table above that you want.
3. Select **Save**.

This training uses the first three.
Leave `kitconcept.footer` disabled while you follow it: when it is active, VLT renders kitconcept's footer layout, which sets its own footer background colors and replaces the footer gradient that you define in the next chapter.

The behaviors add their fields to the content type they are applied to.
Applied to the Plone Site, they configure the whole site.
Applied to a subsite, they configure that branch instead, and each page uses the settings of its nearest ancestor that has them.

(light-theme-behavior-colors-label)=

#### What the theme behavior does

The behavior adds five empty, optional fields to the **Theming** tab of the edit form, each rendered with the `colorPicker` widget.
When an editor fills in a field, VLT sets the matching custom property:

| Field | Label in the form | Custom property it sets |
| --- | --- | --- |
| `header_foreground` | Navigation Text Color | `--header-foreground` |
| `accent_foreground_color` | Fat Menu / Breadcrumbs Text Color | `--accent-foreground-color` |
| `accent_color` | Fat Menu Background Color | `--accent-color` |
| `secondary_foreground_color` | Footer Font Color | `--secondary-foreground-color` |
| `secondary_color` | Footer Background Color | `--secondary-color` |

There is no field for the primary color pair.
The header background follows `--primary-color`, which no field of the behavior sets, and the navigation text color has its own field, `header_foreground`.

VLT writes the values that editors choose into a `:root` rule at the top of the document head.
Your project's stylesheet comes after that rule, and the design tokens that you will define in the next chapter use the same `:root` selector.
When both set the same property, your stylesheet wins, and the value that the editor chose has no effect.

```{important}
Decide who owns each of these five properties.
If editors should be able to change a color, leave its property out of your stylesheet.

The Robotarium's stylesheet sets `--accent-color`, `--accent-foreground-color`, and `--secondary-color` in the next chapter.
On the Robotarium, the Fat Menu Background Color, Fat Menu / Breadcrumbs Text Color, and Footer Background Color fields therefore have no effect, while Navigation Text Color and Footer Font Color still work.
```

```{note}
Behaviors can be added in new releases, and this table reflects `kitconcept.voltolighttheme` 8.0.0.
The authoritative list is the behavior registration in the add-on itself, at {file}`backend/src/kitconcept/voltolighttheme/behaviors/configure.zcml` in the [VLT repository](https://github.com/kitconcept/volto-light-theme).
See the [site customization guide](https://volto-light-theme.readthedocs.io/conceptual-guides/site-customization.html) for what each field does.
```

Your site now has the VLT site customization fields available.

## File Structure Setup

Set up the recommended file structure in your project add-on's `src` folder.
Cookieplone already created part of it, so you are filling in the gaps rather than starting from nothing:

```console
src/
├── components/          # exists, empty
│   └── blocks/          # new
├── config/
│   ├── settings.ts      # exists, sets the default language
│   └── blocks.ts        # new
├── index.ts             # exists, calls installSettings()
└── theme/               # new
    ├── blocks/
    ├── _variables.scss
    └── _main.scss
```

From {file}`frontend/packages/volto-robotarium/src`:

```shell
mkdir -p components/blocks config theme/blocks
touch config/blocks.ts theme/_variables.scss theme/_main.scss
```

```{warning}
Do not overwrite the generated {file}`index.ts` and {file}`config/settings.ts`.
The generated `settings.ts` sets your site's `defaultLanguage`, and `index.ts` already calls it.
Every later step in this training that shows one of these two files is showing an **edit**, not a replacement.
```

Whenever you add new files to your project, restart the frontend, because hot reload does not pick them up.

(light-theme-insertion-points-label)=

### The Two Theme Insertion Points

Two of those filenames are load-bearing.
Volto scans every add-on for {file}`theme/_variables.scss` and {file}`theme/_main.scss`, and injects whichever it finds into the theme's stylesheet at two different points:

| File | Injected | Use it for |
| --- | --- | --- |
| {file}`theme/_variables.scss` | **before** VLT's own variables | the few SCSS variables VLT compiles with |
| {file}`theme/_main.scss` | **after** all of VLT's styles | everything else, including all your custom properties |

The order is what makes each one useful.
No other filename is special: `theme/blocks/` and anything else you add are ordinary partials that become part of the build only because {file}`_main.scss` imports them.

```{note}
Volto skips these two files for whichever add-on is registered as the `theme`.
They work for {file}`volto-robotarium` precisely because VLT, not your project, is the theme add-on.
```

(light-theme-custom-properties-label)=

#### Prefer CSS custom properties

Almost all of your theming should be CSS custom properties written in {file}`_main.scss`, not SCSS variables.

VLT is built as a custom-property system: the color pairs, the semantic properties, the container widths, and the block themes are all custom properties, resolved in the browser. That is what lets you override them per block, per section, and at runtime—a block theme works by re-declaring `--theme-color` on one block, which no build-time variable could do. Setting your design tokens as custom properties in `:root` is the normal path, and the next chapter sets these, among others:

```scss
// src/theme/_main.scss
:root {
  --accent-color: #3b5759;
  --accent-foreground-color: #fff;
  --link-foreground-color: #157a7a;
}
```

{file}`_variables.scss` is the narrow exception, for values VLT **computes with at build time**. VLT declares its SCSS variables with `!default`, so each one applies only when nothing has already set it. Since {file}`_variables.scss` is injected first, anything you assign there wins—and it is the *only* place they can be changed, because VLT's stylesheets have already used the values by the time {file}`_main.scss` is injected:

```scss
// src/theme/_variables.scss
$default-container-width: 1120px;
```

Two kinds of value belong there:

- **Breakpoints**, which cannot be custom properties at all, since media queries cannot read them.
- **The three container widths.** VLT declares `--layout-container-width`, `--default-container-width`, and `--narrow-container-width` from the SCSS variables of the same name, and also uses the SCSS values in media and container queries. Setting the SCSS variable updates both, so you never set the custom property yourself.

The rule of thumb: custom properties for anything meant to vary per block, per section, or at runtime—which is nearly everything, and all of the color system. SCSS variables only for the handful of values VLT compiles into media queries and mixins.

## Checkpoint

Restart both servers and confirm the install landed before moving on. Most trouble in later chapters traces back to one of these:

- The site at http://localhost:3000 renders in VLT's styling, not Volto's default Pastanaga theme. If it looks unchanged, VLT is listed in `addons` but not declared as the `theme`.
- Editing a page and selecting a Text block shows a **Background color** control in the **Styling** section of the block settings. This confirms VLT's block configuration is applied.
- The add-ons control panel lists **Volto Light Theme: Install** among the installed add-ons, and the Plone Site content type shows the `voltolighttheme` behaviors as enabled.
- Adding a temporary rule to {file}`src/theme/_main.scss`, such as `body { border-top: 4px solid red; }`, shows that border after a restart. If it does not, your add-on is not being picked up, and no amount of CSS in later chapters will apply. Remove the rule afterward.

## Further Reading

This training covers the parts of VLT you need to build a project. The theme's own documentation goes deeper on each topic:

- [Color system](https://volto-light-theme.readthedocs.io/conceptual-guides/color-system.html)
- [Layout](https://volto-light-theme.readthedocs.io/conceptual-guides/layout.html)
- [Vertical spacing](https://volto-light-theme.readthedocs.io/conceptual-guides/vertical-spacing.html)
- [Install guide](https://volto-light-theme.readthedocs.io/how-to-guides/install.html)
- [Site customization](https://volto-light-theme.readthedocs.io/conceptual-guides/site-customization.html)
