# Shortcuts

## `@root` / `@package`

Volto has in place shortcuts to refer to special places in code. This helps in the build when working on a Volto project (when Volto is used as a library) or in a pure Volto core build.

Both `@root` and `@package` points to the current top level of either our Volto project or in pure Volto core.

```{deprecated} Volto 17.0.0
Since `@package` naming is confusing, specially in an add-on environment, it will be deprecated from Volto 17.0.0 on, in favor of `@root`. In the meanwhile, both shortcuts are enabled.
```
