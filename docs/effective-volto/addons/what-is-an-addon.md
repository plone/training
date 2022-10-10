---
myst:
  html_meta:
    "description": "What is a Volto add-on"
    "property=og:description": "What is a Volto add-on"
    "property=og:title": "What is a Volto addon"
    "keywords": "Volto, Plone, Webpack, Volto add-on"
---

# What is a Volto add-on

There are several advanced scenarios where we might want to have more control
and flexibility beyond using the plain Volto project to build a site.

We can build Volto add-on products and make them available as generic
JavaScript packages that can be included in any Volto project. By doing so we
can provide code and component reutilization across projects and, of course,
benefit from open source collaboration.

```{note}
By declaring a JavaScript package as a "Volto addon", Volto provides
several integration features: language features (so they can be transpiled
by Babel), whole-process customization via razzle.extend.js and
integration with Volto's configuration registry.
```

The addon can be published to an NPM registry or directly installed from github
by Yarn. By using [mrs-develop](https://github.com/collective/mrs-developer),
it's possible to have a workflow similar to zc.buildout's mr.developer, where
you can "checkout" an addon for development.

An addon can be **almost anything that a Volto project can be**. They can:

- provide additional views and blocks
- override or extend Volto's builtin views, blocks, settings
- shadow (customize) Volto's (or another addon's) modules
- register custom routes
- provide custom Redux actions and reducers
- register custom Express middleware for Volto's server process
- tweak Volto's Webpack configuration, load custom Razzle and Webpack plugins
- even provide a custom theme, just like a regular Volto project does.
