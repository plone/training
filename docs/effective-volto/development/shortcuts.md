---
myst:
  html_meta:
    "description": "Shortcuts"
    "property=og:description": "Shortcuts"
    "property=og:title": "Shortcuts"
    "keywords": "Volto, Plone, Webpack, JavaScript, Packaging"
---

# Shortcuts

Volto provides the following available names for JavaScript and LESS imports:

## `@root` / `@package`

Volto has in place shortcuts to refer to special places in code. This helps in the build when working on a Volto project (when Volto is used as a library) or in a pure Volto core build.

Both `@root` and `@package` points to the current top level of either our Volto project or in pure Volto core.

```{deprecated} Volto 17.0.0
Since `@package` naming is confusing, specially in an add-on environment, it will be deprecated from Volto 17.0.0 on, in favor of `@root`. In the meanwhile, both shortcuts are enabled.
```

## volto-themes

The `volto-themes` name always points to the current Volto Semanticu-UI themes folder, so it can resolve to either `node_modules/@plone/volto/theme/themes` or `../theme/themes`, etc, depending on how Volto is run.

## volto-original

This name allows access to the original, unshadowed modules. When shadowing one
of Volto's modules, you can access the original file and use it in the
override.
