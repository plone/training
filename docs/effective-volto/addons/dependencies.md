---
myst:
  html_meta:
    "description": "Add-on dependencies"
    "property=og:description": "Add-on dependencies"
    "property=og:title": "Add-on dependencies"
    "keywords": "Volto, Plone, Volto add-ons, JavaScript, JavaScript dependencies"
---

# Add-on dependencies

Sometimes your addon depends on another addon. You can declare addon dependency
in your addon's `addons` key, just like you do in your project. By doing so,
that other addon's configuration loader is executed first, so you can depend on
the configuration being already applied. Another benefit is that you'll have
to declare only the "top level" addon in your project, the dependencies will be
discovered and automatically treated as Volto addons. For example, the Volto
addon volto-eea-kitkat, which is the Volto umbrela addon that registers
a default set of addons for the EEA websites, depends on many other addons:

```
{
  "name": "volto-eea-kitkat",
  ...
  "addons": [
    '@eeacms/volto-matomo',
    // ...
  ]
}
```

And of course, the dependency addon can depend, on its turn, on other addons
which will be loaded as well. Circular dependencies should be avoided.
