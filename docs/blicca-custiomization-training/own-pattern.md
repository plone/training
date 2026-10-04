---
myst:
    html_meta:
        "description": "Build and register your own Patternslib pattern for Blicca, and ship it as a module federation remote bundle."
        "property=og:description": "Build and register your own Patternslib pattern for Blicca, and ship it as a module federation remote bundle."
        "property=og:title": "Your own pattern"
        "keywords": "Plone, Blicca, Patternslib, BasePattern, webpack, module federation, bundle"
---

(blicca-own-pattern-label)=

# Your own pattern

In this chapter, we write a pattern from scratch, and ship it in our own bundle.
At the end, a badge appears on every element that carries the class `pat-blicca`.

## A class-based pattern

The file {file}`resources/pat-blicca/blicca.js` contains a pattern in the current Patternslib style:

```js
import { BasePattern } from "@patternslib/patternslib/src/core/basepattern";
import Parser from "@patternslib/patternslib/src/core/parser";
import registry from "@patternslib/patternslib/src/core/registry";

export const parser = new Parser("blicca");
parser.addArgument("color", "#0083be");
parser.addArgument("label", "Blicca override active");

class Pattern extends BasePattern {
    static name = "blicca";
    static trigger = ".pat-blicca";
    static parser = parser;

    init() {
        const badge = document.createElement("span");
        badge.textContent = `★ ${this.options.label}`;
        this.el.style.outline = `2px dashed ${this.options.color}`;
        this.el.append(badge);
    }
}

registry.register(Pattern);
```

Three things matter here:

- The `trigger` is a plain CSS selector.
- The `Parser` declares the options, and fills them from `data-pat-blicca` attributes, including inheritance from parent elements.
- `registry.register(Pattern)` makes the registry scan the document, including content that arrives later through modals, `pat-inject`, or the folder contents view.

## The bundle around it

The webpack setup comes from `@patternslib/dev`, and the module federation plugin turns the bundle into a remote.
The entry point {file}`resources/index.js` only contains a dynamic import, exported as default:

```js
export default import("./overrides");
```

The dynamic import creates a split point.
Webpack needs it to negotiate the shared dependencies with the Plone bundle at runtime, before our code runs.
The default export matters, too.
Since Mockup 5.6.13, the module federation helper of the Plone bundle awaits the exported promise of every remote, and the Patternslib registry, since 9.11, waits for that before its initial scan of the page.
Your patterns and components are therefore registered before the first scan, no matter how fast the remote loads.

The profile registers the built bundle in {file}`profiles/default/registry/bundles.xml`:

```xml
<records
    interface="plone.base.interfaces.IBundleRegistry"
    prefix="plone.bundles/blicca-staticresourceoverride"
    >
  <value key="enabled">True</value>
  <value key="jscompilation">++plone++blicca.staticresourceoverride/bundles/blicca.staticresourceoverride-remote.min.js</value>
  <value key="depends">plone</value>
</records>
```

The `depends` value makes sure that the bundle loads after the host.

## Exercise

Start the watcher:

```shell
pnpm run watch
```

Edit a page, and give a paragraph the class `pat-blicca` in the TinyMCE source view.
Save and observe the badge and the dashed outline.

Now pass options through the markup:

```html
<p class="pat-blicca" data-pat-blicca="color: #d63384">With option.</p>
```

Then make it your own.
Add a new option to the parser, and use it in `init()`.

## Checkpoint

The badge and the outline appear on your paragraph.
Changing `data-pat-blicca` changes the result.
