---
myst:
  html_meta:
    "description": "Razzle"
    "property=og:description": "Razzle"
    "property=og:title": "Razzle"
    "keywords": "Volto, Plone, Webpack, Razzle"
---

# Razzle

[Razzle](https://razzlejs.org) is a library and Webpack boilerplate generator for isomorphic JavaScript applications.
Isomorphic applications are applications that can run the same code on the client (browsers) and on the server (backend).

Razzle is extensible and Volto is built upon that extensible framework. Volto defines its own Razzle customization, via its `razzle.config.js`.
It allows to extend the Webpack configuration both from the core (vanilla Volto), a project and even a Volto addon (using a `razzle.extend.js` file, which is a Volto-developed standard).
It also allows to tap into the most important development artifacts and extend them (ESLint config, etc).
It defines the Babel configuration baseline, and allows you to extend it as well.
It has all the modern development tools (HMR, etc) and a plugin system that you can use from your projects.

```{note}
While Razzle is stable, it doesn't see a lot of active development. A possible replacement could be [vite.js](https://vitejs.dev/) and there's already a Proof of Concept that integrates it with Volto.
```
