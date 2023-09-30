---
myst:
  html_meta:
    "description": "Webpack loaders"
    "property=og:description": "Webpack loaders"
    "property=og:title": "Webpack loaders"
    "keywords": "Volto, Plone, Webpack"
---

# Webpack loaders

In the process of "bundling" (creating the static code that gets loaded into
the browsers, webpack needs to be instructed on how to handle various types of
files. JavaScript/JSX code gets handled by the Babel compiler, etc.

Volto includes several other webpack loaders:

- `.less` files are loaded with the LESS Loader, pipelined through PostCSS
- `.scss` files are loaded with the SASS Loader, pipelined through PostCSS
- `.css` files are loaded directly
- `.svg` files, if placed in a folder called `icons`, can be loaded as React
  elements
- the file loader, for static resources such as images

PostCSS is a pluggable framework that enables enhancements and transformations of CSS.

## Add your own Webpack loader

Sometimes Razzle provides a plugin for your needed loader, which takes care of loading and passing the proper options to that Webpack loader. For example, to load the razzle-plugin-scss which is a [Razzle plugin][1], you need to export a `plugins` field in your `razzle.config.js` or `razzle.extend.js`.

```{note}
`razzle-plugin-scss` is included in Volto (both in 16 and 17) since the beginning of 2023.
Keeping the example here as reference for other Razzle plugins.
```

Here's an example `razzle.extend.js` that allows a Volto addon to load that Razzle plugin.
First, make sure to add the `razzle-plugin-scss` as Javascript package dependency of your addon.

```js
const plugins = (defaultPlugins) => {
  return defaultPlugins.concat(['scss']);
};

const modify = (config, { target, dev }, webpack) => {
  return config;
};

module.exports = {
  plugins,
  modify,
};
```

If there's no Razzle plugin, you'll have to write your own Razzle extender
plugin that inserts the proper rules. See the [Volto LESS Plugin][2] for an
example of how to define a new loader, with the [Bundle Analyzer][3] as
a simpler example for Volto Razzle/Webpack plugins.

[1]: https://razzlejs.org/docs/customization#plugins
[2]: https://github.com/plone/volto/blob/b3b9cf0286bee1101655c8d7e234ca7dae95709e/webpack-plugins/webpack-less-plugin.js
[3]: https://github.com/plone/volto/blob/b3b9cf0286bee1101655c8d7e234ca7dae95709e/webpack-plugins/webpack-bundle-analyze-plugin.js
