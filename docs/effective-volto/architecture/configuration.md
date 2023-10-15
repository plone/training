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

To import the singleton object, you simply do:

```
import config from '@plone/volto/registry';
```

The configuration registry object has several branches:

- `settings`
- `views`
- `blocks`
- `addonRoutes` and `addonReducers`
- `components`

You can easily inspect this configuration by `console.log`.

This configuration object is produced as a result of the following process:

- Volto defines a base configuration (check [plone/volto](https://github.com/plone/volto) `src/config` folder
- Volto passes this base configuration to the addons configuration loader chain
  (all the default exported `applyConfig` from the defined Volto addons)
- Each of these addons will directly change the configuration object, adding,
  removing or tweaking existing settings.
- Then it is passed to your custom Volto project `applyConfig`.
- And finally, it is made available as the singleton importable object.

This process is performed by the user's browser any time then (re)load a Volto
page. Any changes to the configuration object should be performed at this
"bootup", and not as a result of user interaction. The configuration registry
is local to a browser tab, it's not shared between tabs.
