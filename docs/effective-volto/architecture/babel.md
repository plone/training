---
myst:
  html_meta:
    "description": "Babel"
    "property=og:description": "Babel"
    "property=og:title": "Babel"
    "keywords": "Volto, Plone, Webpack, Babel, JavaScript"
---

# Babel

Volto uses [Babel](https://babeljs.io/) as the tool to convert our flavour of
JavaScript to one that can be loaded by the browsers. For example, we write
code in JSX, which is a superset of JavaScript. Browser don't know how to
interpret this code, so our bundler, [Webpack](./webpack) will "transpile" the
code with Babel to something that any browser can use.

To understand Volto's Babel configuration, read its [babel.js file](https://github.com/plone/volto/blob/d7b6db3db239d09ceafee61dacf14fa7acec9b4b/babel.js)

By default, Babel is used to transpile only Volto source code and all its
addons. Babel is not used for any other code, especially the one that lives in
`node_modules`. This is important to understand. You may encounter a situation
where you have a third-party library that's distributed as ESModule or some
other flavour of JavaScript that's not compatible with the way Volto bundles
the rest of the code. In this case, you'll have to instruct Babel to include
that library's path in its list of processed paths, and you can do that by
tweaking the webpack configuration. See the [Addons webpack](../addons/webpack)
chapter for this.
