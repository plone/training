---
myst:
    html_meta:
        "description": "Replace a Blicca core pattern with your own implementation, using the Patternslib pattern blacklist."
        "property=og:description": "Replace a Blicca core pattern with your own implementation, using the Patternslib pattern blacklist."
        "property=og:title": "Replacing a core pattern"
        "keywords": "Plone, Blicca, Patternslib, blacklist, markspeciallinks, override"
---

(blicca-replace-pattern-label)=

# Replacing a core pattern

Sometimes tweaking options is not enough, and you want your own implementation of a core pattern.
In this chapter, we replace `markspeciallinks`, and external links get a different icon.

## Why load order is not enough

The registry rule from {ref}`blicca-intro-label` applies.
**First registration wins.**
Mockup registers its patterns in an asynchronously loaded chunk, so the exact timing between the host and your remote is not guaranteed.
Racing the host is not a strategy.

Patternslib provides an official switch instead: the pattern blacklist.

```{note}
Patternslib 9.11, shipped with Mockup 5.6.12 and later, adds a second switch, the `replace` option.
See {ref}`blicca-replace-option-label` at the end of this chapter.
```

## The blacklist preload

The file {file}`static/pattern-blacklist.js` is a tiny, unbuilt JavaScript file:

```js
window.__patternslib_patterns_blacklist = (
    window.__patternslib_patterns_blacklist || []
).concat(["markspeciallinks"]);
```

The profile registers it as its own bundle, without a `depends` value:

```xml
<records
    interface="plone.base.interfaces.IBundleRegistry"
    prefix="plone.bundles/blicca-preload"
    >
  <value key="enabled">True</value>
  <value key="jscompilation">++plone++blicca.staticresourceoverride/pattern-blacklist.js</value>
</records>
```

It renders before the Plone bundle and runs synchronously, while Mockup registers its patterns in an async chunk.
The original pattern therefore never gets registered.

Two things make this ordering reliable.
First, the `depends` field only knows "after": an empty value means "as early as possible", and `*` means "after all other bundles", so `depends="*"` would be exactly the wrong choice here.
Bundles without dependencies render in the alphabetical order of their registry record names, and `plone.bundles/blicca-preload` sorts before `plone.bundles/plone`.
Second, even a synchronous script that renders after the Plone bundle still runs before Mockup's async pattern chunk.
The blacklist takes effect at registration time, so the position among the synchronous scripts does not matter.

```{note}
Bundles are just files.
This one needs no build at all.
```

## The replacement

The blacklist blocks any registration under the blocked name, including yours.
Therefore, the replacement in {file}`resources/markspeciallinks/markspeciallinks.js` registers under its own name, but with the original trigger:

```js
import $ from "jquery";
import mockupParser from "@patternslib/patternslib/src/core/mockup-parser";
import MarkSpecialLinks from "@plone/mockup/src/pat/markspeciallinks/markspeciallinks";

export default MarkSpecialLinks.extend({
    name: "blicca-markspeciallinks",
    trigger: ".pat-markspeciallinks",
    parser: null,

    async init() {
        this.options = $.extend(
            true,
            {},
            this.defaults,
            mockupParser.getOptions(this.el, "markspeciallinks"),
        );
        this.protocol_icon_map = {
            ...this.protocol_icon_map,
            https: "box-arrow-up-right",
            http: "box-arrow-up-right",
        };
        return this.constructor.__super__.init.call(this);
    },
});
```

Note the three tricks:

- We extend the original class, and reuse its whole implementation.
- We register under the name `blicca-markspeciallinks`, with the original trigger `.pat-markspeciallinks`.
- The Mockup parser reads options based on the pattern name, and our name differs.
  Therefore, `init()` fetches the original's options itself with `mockupParser.getOptions()`, including the inheritance from the `<body>`.

(blicca-replace-option-label)=

## The `replace` option

Since Patternslib 9.11, shipped with Mockup 5.6.12 and later, the registry can replace a registration:

```js
import $ from "jquery";
import registry from "@patternslib/patternslib/src/core/registry";
import MarkSpecialLinks from "@plone/mockup/src/pat/markspeciallinks/markspeciallinks";

export default MarkSpecialLinks.extend({
    // Same name, same trigger, and the options keep working.
    name: "markspeciallinks",
    trigger: ".pat-markspeciallinks",
    replace: true,

    async init() {
        this.protocol_icon_map = {
            ...this.protocol_icon_map,
            https: "box-arrow-up-right",
            http: "box-arrow-up-right",
        };
        return this.constructor.__super__.init.call(this);
    },
});
```

For class-based patterns, pass the option to the registry: `registry.register(Pattern, Pattern.name, { replace: true })`.

Compared with the blacklist recipe, two of the three building blocks disappear.
There is no preload bundle, and no options bridge, because the pattern keeps its name and the Mockup parser reads `data-pat-markspeciallinks` as before.
It works because the registry now waits for the module federation remotes before its initial scan, see {ref}`blicca-own-pattern-label`.
The replacement is in place for the first scan, no matter whether the Plone bundle or your add-on registered first.
If a replacement arrives after the registry was initialized, the registry logs a warning: elements that were already initialized keep the previous pattern, only new elements get the replacement.

The blacklist still wins over a replacement, so both switches can coexist.
This chapter keeps the blacklist recipe as the main path, because it works on every Mockup 5 bundle and because it makes registration, names, and triggers visible.
Once your site runs Mockup 5.6.12 or later, the `replace` option is the shorter way.

## Exercise

Change the icon that external links get.
Pick any name from [Bootstrap Icons](https://icons.getbootstrap.com/).
As a bonus, additionally set `rel="noopener noreferrer"` on external links.

## Checkpoint

External links show your icon.
The console confirms that the original was skipped:

```console
registry: Pattern name markspeciallinks is blacklisted.
```
