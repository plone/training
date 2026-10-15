---
myst:
    html_meta:
        "description": "Production notes for Blicca add-on bundles: version pinning, clean uninstall, and known pitfalls."
        "property=og:description": "Production notes for Blicca add-on bundles: version pinning, clean uninstall, and known pitfalls."
        "property=og:title": "Production notes and pitfalls"
        "keywords": "Plone, Blicca, production, version pinning, uninstall, pitfalls"
---

(blicca-production-label)=

# Production notes and pitfalls

Your overrides work.
This chapter collects what you need to know before you ship them.

## Version pinning

The versions of `@plone/mockup` and `@patternslib/patternslib` in your `package.json` must match the Mockup version that `plone.staticresources` ships.
Module federation negotiates shared modules through version ranges.
If the versions drift too far apart, module federation loads two instances, and registrations end up in the wrong registry.

On every Plone upgrade, align the versions, and rebuild the bundle.
Check the browser console for module federation warnings.

Some techniques also need a minimum Mockup version in the Plone bundle.
The shared Svelte runtime needs Mockup 5.6.9, the override under the default component key needs Mockup 5.6.11, and this add-on is built against Mockup 5.6.14 with Patternslib 9.11.

## Clean uninstall

The uninstall profile removes what the default profile added:

- Bundle records are removed with `remove="true"` in {file}`profiles/uninstall/registry/bundles.xml`.
- Whole records, such as `plone.mark_special_links`, are reset with a plain value.
- Single dictionary keys, such as our entries in `plone.patternoptions`, cannot be removed declaratively.
  The `post_uninstall` handler in {file}`setuphandlers.py` removes them in Python:

```python
PATTERN_OPTION_KEYS = ("markspeciallinks", "contentbrowser")


def post_uninstall(context):
    registry = getUtility(IRegistry)
    options = dict(registry.get("plone.patternoptions") or {})
    remaining = {k: v for k, v in options.items() if k not in PATTERN_OPTION_KEYS}
    if remaining != options:
        registry["plone.patternoptions"] = remaining
```

## Known pitfalls

Forgotten build
: `static/bundles/` is empty, and the remote bundle returns a 404 error.
Run `pnpm run build` first, then install.

Missing trigger class
: Options alone don't run a pattern.
When a pattern "does nothing", first check the trigger, then the options.

Missing `purge="false"`
: Without it, your `plone.patternoptions` import overwrites the options of the Plone core and of other add-ons.

Two Svelte runtimes
: The selection list renders an empty slot, and the console shows `Cannot read properties of null (reading 'nodes')`.
The host and the add-on don't share the Svelte runtime.
Either the Plone bundle is older than Mockup 5.6.9, or the `svelte` and `svelte/` shares are missing in your webpack configuration.
See {ref}`blicca-svelte-override-label`.

The default component wins again
: You registered your component under the default key, but the content browser still renders the original.
The Plone bundle is older than Mockup 5.6.11, which re-registered the default component on every widget initialization.
Register your component under a custom key, and activate it with `componentRegistryKeys`, see {ref}`blicca-svelte-override-scoping-label`.

Lazy component registration
: With a typo in a custom registry key, the content browser silently falls back to the default component.

## Where to go next

- The [Patternslib documentation](https://patternslib.com/) for the pattern API.
- The [Mockup source](https://github.com/plone/mockup) as a cookbook of real-world patterns.
- The [plone.staticresources source](https://github.com/plone/plone.staticresources) for how the core bundle is built and registered.
- {doc}`Mockup and Patternslib in the Plone documentation <plone:classic-ui/mockup>`.
