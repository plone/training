---
myst:
  html_meta:
    "description": "Jest"
    "property=og:description": "Jest"
    "property=og:title": "Jest"
    "keywords": "Volto, Plone, Testing, Jest, CI"
---

# Jest

Jest is the standard "de facto" NodeJS test runner.

```{warning}
If there is one complaint that can be addressed to the JavaScript frontend development tooling is that there's no shared way of solving common problems. The main difficulty in setting up Jest for Volto and Volto projects is configuring it for properly "accepting" the way Volto loads its code, via Webpack.
```

## Standard setup

Jest does not use Volto's or the project webpack configuration, but its own way of compiling the code under test. Jest needs to know how to compile and process these resources, some of them are automatically and already configured but could be that if you'd need to extend for supporting the resources you are importing in your code.

The Jest setup is done at `package.json` of your project under the key `jest`. Vanilla Volto repo has also its own.

## Config for projects and for add-ons

Jest in Volto does not use the full configuration object from Volto. It uses a special subset of configuration, simpler than the original one, suitable for having more predictable test results. This configuration is loaded from: [test-setup-config.js][1] file at Volto's root. By taking a look at it, you could see the default configuration.

You can override or extend anything in the default configuration by using the configuration object as you would do normally in code:

[1]: https://github.com/plone/volto/blob/42f2dfc8abc0defa5f3ebef5bcfb6265342ffdc7/test-setup-config.js

```js
beforeEach(() => {
  config.settings.legacyTraverse = false;
});
```

## Transforms

To deal with the resources that your code is using (importing), Jest is using its own "transforms", which it performs as part of running the tests. There is a transform for every common type of resource: `js`, `jsx`, `svg`, `less`, `png`, `jpg`, `gif`, and so on. You can take a look at them at the root of your project or in vanilla Volto repo in `package.json`.

```json
"jest": {
  "transform": {
    "^.+\\.js(x)?$": "babel-jest",
    "^.+\\.(png)$": "jest-file",
    "^.+\\.(jpg)$": "jest-file",
    "^.+\\.(svg)$": "./jest-svgsystem-transform.js"
  },
}
```

You can add your own in your projects, if required.

## Modulemapper

There are some import mapping in place to "mock" some paths that the components need.
If your components imports resources from other packages other than Volto, you need to add it to this list.

```json
  "moduleNameMapper": {
    "@plone/volto/(.*)$": "<rootDir>/src/$1",
    "@plone/volto-slate": "<rootDir>/packages/volto-slate/src",
    "~/config": "<rootDir>/src/config",
    "~/../locales/${lang}.json": "<rootDir>/locales/en.json",
    "(.*)/locales/(.*)": "<rootDir>/locales/$2",
    "load-volto-addons": "<rootDir>/jest-addons-loader.js",
    "@package/(.*)$": "<rootDir>/src/$1",
    "@root/config": "<rootDir>/jest-addons-loader.js",
    "@root/(.*)$": "<rootDir>/src/$1",
    "@voltoconfig": "<rootDir>/jest-addons-loader.js",
    "\\.(css|less|scss|sass)$": "identity-obj-proxy"
  },
```

If you are using a custom add-on in development mode, and the component under test is importing a resource from it, you should declare it here like:

```json
  "moduleNameMapper": {
    "@kitconcept/volto-blocks-grid": "<rootDir>/src/addons/volto-blocks-grid/src",
  }
```

## Caveats

When testing addons there are some caveats that you should take care of in the regards of the Jest configuration to support it. The add-on generator already takes care of it and sets up the appropiate configuration.

### `jest-addon.config.js`

This is an "escape hatch" for providing an alternative jest configuration that gets added to the default one. This is a `CommonJS` file:

```js
module.exports = {
  testMatch: ['**/src/addons/**/?(*.)+(spec|test).[jt]s?(x)'],
  collectCoverageFrom: [
    'src/addons/**/src/**/*.{js,jsx,ts,tsx}',
    '!src/**/*.d.ts',
  ],
  moduleNameMapper: {
    '@plone/volto/cypress': '<rootDir>/node_modules/@plone/volto/cypress',
    '@plone/volto/babel': '<rootDir>/node_modules/@plone/volto/babel',
    '@plone/volto/(.*)$': '<rootDir>/node_modules/@plone/volto/src/$1',
    '@package/(.*)$': '<rootDir>/src/$1',
    '@kitconcept/volto-blocks-grid/(.*)$':
      '<rootDir>/src/addons/volto-blocks-grid/src/$1',
    '~/(.*)$': '<rootDir>/src/$1',
    'load-volto-addons':
      '<rootDir>/node_modules/@plone/volto/jest-addons-loader.js',
  },
  transform: {
    '^.+\\.js(x)?$': 'babel-jest',
    '^.+\\.css$': 'jest-css-modules',
    '^.+\\.less$': 'jest-css-modules',
    '^.+\\.scss$': 'jest-css-modules',
    '^.+\\.(png)$': 'jest-file',
    '^.+\\.(jpg)$': 'jest-file',
    '^.+\\.(svg)$': './node_modules/@plone/volto/jest-svgsystem-transform.js',
  },
  coverageThreshold: {
    global: {
      branches: 0,
      functions: 0,
      lines: 5,
      statements: 5,
    },
  },
};
```

The `@plone/scripts` `addon` command already takes care of configuring the build for it to work correctly:

```json
    "test": "RAZZLE_JEST_CONFIG=src/addons/volto-blocks-grid/jest-addon.config.js razzle test --passWithNoTests",
```

You can also use the `RAZZLE_JEST_CONFIG` environment variable for providing and additional jest config to your test run.
