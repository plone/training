---
myst:
  html_meta:
    "description": "Configuration Registry"
    "property=og:description": "Configuration Registry"
    "property=og:title": "Configuration Registry"
    "keywords": "Volto, Plone, Configuration"
---

# Configuration Registry

To provide customization and a centralized configuration, Volto holds all its
settings in a global singleton object. That is, in a JavaScript-running
browser window, there will be one single instance of that JavaScript object.
The advantage of the global configuration registry is the simplicity in working
with it.

To use it in your custom code, you simply do:

```
import config from '@plone/volto/registry';
```

The configuration registry object has several branches:

- `settings`
- `views`
- `blocks`
- `addonRoutes` and `addonReducers`
- `components`

This is the object that gets passed to the `applyConfig` configuration
initializers. You can read it and mutate it at Volto's project and addons
initialization.
