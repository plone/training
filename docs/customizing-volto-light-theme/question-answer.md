---
myst:
  html_meta:
    "description": "Questions and answers"
    "property=og:description": "Questions and answers"
    "property=og:title": "Questions and answers"
    "keywords": "Plone, Volto, Training, Volto Light Theme"
---

# Questions and Answers

This chapter collects the questions that come up most often while working through the training.
Each answer is short, and links to the section that explains it in full.

## Setup

### My styles do not appear at all

Check three things, in order:

1. VLT is declared as the `theme` in your add-on's {file}`package.json`, not only listed in `addons`. It needs both entries.
2. Your stylesheet is {file}`src/theme/_main.scss`, or is imported from it. Volto only picks up that exact filename.
3. You restarted the frontend after adding the file. Hot reload does not pick up new files.

See {ref}`light-theme-insertion-points-label`.

### Where do I override `$spacing-large` or a breakpoint?

In {file}`src/theme/_variables.scss`.
Assigning SCSS variables in {file}`_main.scss` has no effect, because VLT has already used their values by then.
See {ref}`light-theme-custom-properties-label`.

## Styling

### Should I use `--theme-color` or `--primary-color`?

`--theme-color` and its companions are set per block by the selected block theme, and change as the editor picks a different one. The `--primary-color` family is site-wide. Inside a block, read the theme properties so the block adapts to whichever palette it is given; outside blocks, read the site-wide ones.

### My links are the same color as the surrounding text

That is the default: links use the foreground color of the block theme they sit in.
Set `--link-foreground-color` in your project to give them a color of their own.

### An editor changed a color in the Theming tab, but the site ignores it

Your stylesheet probably sets the same property.
See {ref}`light-theme-behavior-colors-label` for how to decide who owns each color.

### My gradient palette shows an empty swatch, or unreadable buttons

Some VLT styles read `--theme-color` with `background-color` or `color`, which ignore a gradient.
See {ref}`the warning about gradient palettes <light-theme-gradient-themes-label>`.

### Where do the `next--is--...` classes in VLT's CSS come from?

From functions that VLT adds to `config.settings.styleClassNameExtenders`.
They describe each block's relationship to its neighbors, so that vertical spacing can be expressed in CSS instead of in the components.
See {ref}`light-theme-generated-classes-label` for the full list.

## Blocks and Widgets

### My alignment or width buttons appear but do nothing

Check two things in the field definition:

- The field name must end in `:noprefix`, as in `align:noprefix` and `blockWidth:noprefix`. Only those names match the style definitions that inject `--block-alignment` and `--block-width`.
- The `actions` must be the token names from `config.blocks`. Otherwise the widget stores a style object instead of a token.

See {ref}`light-theme-style-fields-label` and {ref}`Step 6 of the Cover block <light-theme-cover-actions-label>`.

### Can I reuse a Volto block id for my own block?

Avoid it.
Registering under an existing key replaces that block's configuration instead of adding a new block, and the result then depends on the order in which the add-ons are applied.
Give project blocks their own key.

### How do I add the background color control to a third-party block?

Compose VLT's `defaultStylingSchema` with the block's existing `schemaEnhancer`.
See {ref}`the tip at the end of Step 7 of the Cover block <light-theme-third-party-styling-label>`.

## Components

### Should I shadow VLT's header, or swap it?

Swap it.
VLT 8 resolves its structural components through the registry, so registering your own and naming it in `config.settings.vlt.components` replaces it without shadowing.
Shadowing still works, but it binds you to an internal module path and hides which component is actually active.
See {ref}`light-theme-swap-components-label`.

### Slot or component swap?

Use a slot to add something to the layout. Swap a structural component to replace one. Slots are additive and several components can occupy one; a swap substitutes a single named role.

## Block Model v3

### Should I enable it?

Only once every block that your site uses supports it.
See {ref}`light-theme-block-model-v3-label`.

### Do I need to set categories on VLT's blocks?

No. VLT already assigns them to the blocks it has migrated.
For your own blocks, reuse a category only when its rules fit the block, or add a category of your own, as explained in {ref}`light-theme-block-categories-label`.
