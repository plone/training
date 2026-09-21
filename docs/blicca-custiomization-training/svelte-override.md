---
myst:
    html_meta:
        "description": "Override a Svelte component of the Blicca content browser via the shared @plone/registry, the default component key, and one shared Svelte runtime."
        "property=og:description": "Override a Svelte component of the Blicca content browser via the shared @plone/registry, the default component key, and one shared Svelte runtime."
        "property=og:title": "Overriding a Svelte component"
        "keywords": "Plone, Blicca, Svelte, contentbrowser, plone registry, default key, componentRegistryKeys, module federation"
---

(blicca-svelte-override-label)=

# Overriding a Svelte component

The content browser is a Svelte app, and it is designed to be extended.
In this chapter, we replace its `SelectedItem` component with our own, and the selection list of every relation field renders with it.

## Where the hook is

The `pat-contentbrowser` looks up its `SelectedItem` component in the `@plone/registry` component registry.
It first checks a configurable registry key, and then falls back to the default key `pat-contentbrowser.SelectedItem`.
The lookup happens once per widget, when its selection list mounts.

Both keys are hooks for an add-on.
A registration under the default key replaces the component site-wide, without any configuration.
A registration under a custom key is activated per widget, or through pattern options.

Our override consists of two building blocks, plus an optional third one for scoping.

## Block 1: the component

The file {file}`resources/contentbrowser/SelectedItem.svelte` contains our variant.
The only hard requirement is the props interface of the original:

```html
<script>
    let { item, unselectItem } = $props();
</script>
```

The component receives `item`, the selected object with its catalog metadata, and `unselectItem`, a callback that removes it from the selection.
Everything else, such as markup, badges, and styling, is yours.
The same technique applies to other Svelte-based parts of the stack, such as the file manager.

## Block 2: registration

In {file}`resources/overrides.js`, we register the component under the default key:

```js
import plone_registry from "@plone/registry";
import BliccaSelectedItem from "./contentbrowser/SelectedItem.svelte";

plone_registry.registerComponent({
    name: "pat-contentbrowser.SelectedItem",
    component: BliccaSelectedItem,
});
```

That is all it takes.
Since Mockup 5.6.11, the pattern registers its own default component only if nothing is registered under that key yet.
The component registry itself overwrites silently.
An add-on registration therefore wins, no matter whether the add-on bundle initializes before or after the pattern.

```{note}
Before Mockup 5.6.11, the pattern registered the default component in its `init()`, on every widget initialization.
An add-on registration under the default key was reset by the next content browser that initialized.
On such a Plone bundle, use a custom key as described in {ref}`blicca-svelte-override-scoping-label`.
```

One detail makes this work.
The host and the add-on share a single Svelte runtime through module federation.
Svelte keeps its reactivity state in module-level variables, so a component compiled against a second copy of the runtime cannot be mounted by the host.
Both webpack configurations therefore declare the same singleton shares: `svelte` for the package itself, and the prefix `svelte/` for the subpath imports of compiled components, such as `svelte/internal/client`.
This is the relevant part of {file}`webpack.config.js`:

```js
shared: {
    svelte: {
        singleton: true,
        requiredVersion: package_json.dependencies["svelte"],
    },
    "svelte/": {
        singleton: true,
        requiredVersion: package_json.dependencies["svelte"],
    },
},
```

```{important}
The Plone bundle shares its Svelte runtime since Mockup 5.6.9.
With an older bundle, the selection list renders an empty slot, and the console shows `TypeError: Cannot read properties of null (reading 'nodes')`.
```

This makes a great live debugging story, if time permits.
Remove the two shares from {file}`webpack.config.js`, rebuild, and watch the error appear.

(blicca-svelte-override-scoping-label)=

## Block 3: scoping the override

Sometimes you don't want to replace the component everywhere.
Register it under a custom key instead:

```js
plone_registry.registerComponent({
    name: "blicca.SelectedItem",
    component: BliccaSelectedItem,
});
```

Then tell the content browser which key to use, with the pattern option `componentRegistryKeys.selectedItem`.
You have three ways to set it.

Site-wide
: Use the mechanism from {ref}`blicca-pattern-options-label`, in {file}`profiles/default/registry/patternoptions.xml`:

```xml
<element key="contentbrowser">{"componentRegistryKeys": {"selectedItem": "blicca.SelectedItem"}}</element>
```

Per widget
: Set the `data-pat-contentbrowser` attribute directly on the widget.

Conditionally
: Write an `IPatternsSettings` adapter, for example to activate the override only on certain content types.

With a custom key, the default component stays registered, and every widget without the option keeps it.
The override becomes a configuration decision instead of a build decision.

## Exercise

Restyle the component in {file}`resources/contentbrowser/SelectedItem.svelte`.
Show the review state with your workflow colors, render bigger preview images, or turn the item into a compact table row.

Then edit any page, and open {menuselection}`Categorization --> Related Items`.
Select an item, and watch your component render the selection.
Remove the item with your own remove button, and observe that the field value updates.

Finally, close the circle to {ref}`blicca-pattern-options-label`.
Register the component under a custom key, activate it in `plone.patternoptions`, and rebuild.
Then switch the override off again through the web, in {menuselection}`Site Setup --> Configuration Registry`, without touching the bundle.
The `post_uninstall` handler in {file}`setuphandlers.py` already removes the `contentbrowser` key when the add-on is uninstalled.

## Checkpoint

The content browser selection renders with your component, and removing an item clears the field value.

```{tip}
With the default key, the override needs a Plone bundle built from Mockup 5.6.11 or later.
With an older bundle, the default component wins again, and nothing seems to happen.

With a custom key, the registration is lazy.
On a wrong key, the content browser silently falls back to the default component.
When "nothing happens", first check the key for typos.
```
