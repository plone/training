---
myst:
  html_meta:
    "description": "Linters"
    "property=og:description": "Linters"
    "property=og:title": "Linters"
    "keywords": "Volto, Plone, Webpack, Eslint, Prettier, Stylelint"
---

# Linters

Volto provides working configuration for the following linters:

## ESlint

[eslint](https://eslint.org/) is used for JavaScript code checking. A working
`.eslintrc.js` file is shipped with every Volto project. In your addons, you
can customize the ESLint configuration by including a `eslint.extend.js` file.
For example this file adds a new path to eslint's resolve alias map:

```js
const path = require('path');

module.exports = {
  modify(defaultConfig) {
    const aliasMap = defaultConfig.settings['import/resolver'].alias.map;
    const addonPath = aliasMap.find(
      ([name]) => name === '@eeacms/volto-searchlib',
    )[1];

    const searchlibPath = path.resolve(`${addonPath}/../searchlib`);
    aliasMap.push(['@eeacms/search', searchlibPath]);

    return defaultConfig;
  },
};
```

## Prettier

Volto integrates [prettier](https://prettier.io/) for code formatting, in the
form of an eslint plugin.

## Stylelint

Volto integrates [stylelint](https://stylelint.io/) for CSS/Less/SCSS code
linting.
