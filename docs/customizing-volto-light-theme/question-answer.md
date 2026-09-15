---
myst:
  html_meta:
    "description": "Questions and answers"
    "property=og:description": "Questions and answers"
    "property=og:title": "Questions and answers"
    "keywords": "Plone, Volto, Training, Volto Light Theme"
---

# Questions and Answers

This chapter collects the questions that come up most often while working through the training, together with the answers you would otherwise have to dig out of the source.

## Setup

### My styles do not appear at all

Check three things, in order:

1. VLT is declared as the `theme`, not only as an add-on. It is both, and the `addons` entry alone does not apply the theme.
2. Your project add-on is applied after VLT. VLT must be the last entry in your add-on's `addons` list.
3. Your stylesheet is reachable from {file}`src/theme/_main.scss`. Volto only picks up that exact filename.

Restart the frontend after any of these. Adding files is not picked up by hot reload.

### Why is `theme/_main.scss` special?

Volto scans every add-on for {file}`theme/_variables.scss` and {file}`theme/_main.scss` and injects whichever it finds into two fixed points in the theme's stylesheet—variables before VLT's own, main after all of VLT's styles. The filenames are the contract; renaming them silently disables the hook.

### Where do I override `$spacing-large` or a breakpoint?

In {file}`src/theme/_variables.scss`. VLT declares its SCSS variables with `!default`, and that file is injected first, so your value wins. Assigning them from {file}`_main.scss` has no effect, because VLT's stylesheets have already been compiled by then.

## Styling

### Should I use `--theme-color` or `--primary-color`?

`--theme-color` and its companions are set per block by the selected block theme, and change as the editor picks a different one. The `--primary-color` family is site-wide. Inside a block, read the theme properties so the block adapts to whichever palette it is given; outside blocks, read the site-wide ones.

### My links are the same color as the surrounding text

That is the default. Links inherit `--theme-foreground-color` so they stay legible against any block theme. Define `--link-foreground-color` in your project to give them a color of their own.

### Where do the `next--is--...` classes in VLT's CSS come from?

From `config.settings.styleClassNameExtenders`. They describe each block's relationship to its neighbors—same type, same background, first or last of a run—so that vertical spacing can be expressed in CSS instead of in the components. The full list is in the first chapter.

## Blocks and widgets

### My alignment or width buttons appear but do nothing

The field name is almost certainly missing its `:noprefix` suffix. `align` and `align:noprefix` are two different fields, and only the second matches the style definition that injects `--block-alignment`. The same applies to `blockWidth:noprefix` and `size:noprefix`.

### What does `:noprefix` actually do?

It stops the StyleWrapper prefixing the generated CSS class with the field name. A field `align` with value `center` produces `has--align--center`; `align:noprefix` produces `center`. VLT registers its style definitions under the suffixed names, so the suffix is also what makes the lookup match.

### Can I reuse a Volto block id for my own block?

Avoid it. VLT restricts some core blocks—the legacy `hero` among them—and registering under the same key overwrites a core block rather than adding yours, which makes the result depend on add-on ordering. Give project blocks their own key.

### How do I add the background color control to a third-party block?

Register VLT's `defaultStylingSchema` as the block's `schemaEnhancer`, composing it with any enhancer the block already has:

```typescript
config.blocks.blocksConfig.<blockId> = {
  ...config.blocks.blocksConfig.<blockId>,
  schemaEnhancer: composeSchema(
    config.blocks.blocksConfig.<blockId>.schemaEnhancer,
    defaultStylingSchema,
  ),
};
```

## Components

### Should I shadow VLT's header, or swap it?

Swap it. VLT 8 resolves its structural components through the registry, so registering your own and naming it in `config.settings.vlt.components` replaces it without shadowing. Shadowing still works, but it binds you to an internal module path and hides which component is actually active.

### Slot or component swap?

Use a slot to add something to the layout. Swap a structural component to replace one. Slots are additive and several components can occupy one; a swap substitutes a single named role.

## Block Model v3

### Should I enable it?

Only once every block in your registry is v3-compatible. Block repositories advertise this with a "BMv3 ready" banner. A block left on the older model still renders, but it will not share the container structure of the surrounding page, and the difference shows.

### Do I need to set categories on VLT's blocks?

No. VLT already assigns them to the blocks it has migrated. Set `category` on your own blocks, and remember that a category only means something if your stylesheets act on the `category-*` class it produces.
