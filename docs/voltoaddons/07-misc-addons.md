---
html_meta:
  "description": ""
  "property=og:description": ""
  "property=og:title": ""
  "keywords": ""
---

# Add-ons - advanced topics

## Q&A

Is it possible to customize Volto with an add-on?

: Yes, the code path used is the same, so you can use the same convention.
  Make sure you have the `src/customizations` folder inside your add-on. And
  remember, the customization resolution order follows the same order as the
  add-ons listed in the `addons` key of package.json inside the project.

Can I customize an add-on?

: You can customize files from an add-on with the same algorithm used for
  Volto.  In the `src/customizations` folder, move any Volto customized
  files to the `src/customizations/volto` and then customize the add-on by
  reconstructing the full path (for example
  `@plone-collective/datatable-tutorial/CellRenderer/Progress.jsx` would be the
  full path for the file that customizes
  `datatable-tutorial/src/CellRenderer/Progress.jsx`).

Can I have a theme in an add-on?

: Yes, you can alias the `../../theme.config` with a `razzle.extend.js`
  file in the add-on root folder. Just don't make changes to the
  `theme.config` in the project and don't add any files in the project's
  theme folder.

```jsx
const modify = (config, { target, dev }, webpack) => {
  const themeConfigPath = `${__dirname}/theme/theme.config`;
  config.resolve.alias['../../theme.config$'] = themeConfigPath;
  config.resolve.alias['../../theme.config'] = themeConfigPath;

  return config;
};

module.exports = {
  modify,
};
```

How can I avoid customizing components?

: If the component is somehow configurable from Volto's configuration
  registry, for example the default views, the widgets or the route
  renderers, you could wrap them in another component and replace the
  original component in the configuration. Or you could simply customize the
  component with the shadowing mechanism, but inside the new component simply
  reference `@plone/volto-original/.../path/to/Component` and reuse/wrap
  the original one.

Can I extend Volto's Express server?

: You can register custom Express middleware. You could, for example, include
  a custom http proxy for ElasticSearch, expose it to the Volto frontend and
  avoid security issues. See volto-corsproxy for a redux-integrated CORS
  proxy

## Bundle optimization

Once you start approaching the project delivery, you'll need to check your
bundle sizes. Nobody wants to make their visitors wait for a 2 MB gzipped file
before the application becomes interactive.

Volto integrates a solution to split the generated JS code in "chunks", which
will then be loaded on-demand (when the component that uses them is loaded in
browser).

When dealing with React components, it's easy:

```jsx
const Select = loadable(() => import('react-select'));
```

But for libraries it's a bit more difficult, as you have to manifest the
library as a React component, which gets passed as parameter to a render prop:

```jsx
const D3 = loadable.lib(() => import('d3'));

const FormattedValue = ({ value }) => {
  return (
    <D3 fallback={null}>
      {(d3) => d3.format(value)}
    </D3>
  );
};
```

You can analyze your bundle by running:

```sh
BUNDLE_ANALYZE=true yarn build
```

If you're running automated builds you can configure a new bundle analyzer with
static output, to save the report in a static html file. See
webpack-bundle-analyzer docs.

To optimize this scenario Volto provides the `injectLazyLibs` HOC, which
deferrs rendering the wrapped component until the third-party dependency is
fully loaded.
