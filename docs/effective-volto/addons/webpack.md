---
myst:
  html_meta:
    "description": "Extend Webpack setup from an add-on with `razzle.extend.js`"
    "property=og:description": "Extend Webpack setup from an add-on with `razzle.extend.js`"
    "property=og:title": "Extend Webpack setup from an add-on with `razzle.extend.js`"
    "keywords": "Volto, Plone, Webpack, Volto add-on"
---

# Extend Webpack setup from an add-on with `razzle.extend.js`

Just like you can extend Razzle's configuration from the project, you can do so
with an addon, as well. You should provide a `razzle.extend.js` file in your
addon root folder. An example of such file where the theme.config alias is
changed, to enable a custom Semantic theme inside the addon:

```js
const analyzerPlugin = {
  name: 'bundle-analyzer',
  options: {
    analyzerHost: '0.0.0.0',
    analyzerMode: 'static',
    generateStatsFile: true,
    statsFilename: 'stats.json',
    reportFilename: 'reports.html',
    openAnalyzer: false,
  },
};

const plugins = (defaultPlugins) => {
  return defaultPlugins.concat([analyzerPlugin]);
};
const modify = (config, { target, dev }, webpack) => {
  const themeConfigPath = `${__dirname}/theme/theme.config`;
  config.resolve.alias['../../theme.config$'] = themeConfigPath;

  return config;
};

module.exports = {
  plugins,
  modify,
};
```
