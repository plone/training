---
myst:
  html_meta:
    "description": "Bundle analyzing"
    "property=og:description": "Bundle analyzing"
    "property=og:title": "Bundle analyzing"
    "keywords": "Volto, Plone, Bundle, Performance, Optimization"
---

# Bundle analyzing

Once you start developing your custom Volto project, you'll load a lot of third
party code, your own code, etc. In short, you'll be asking your visitors to
load, parse and execute a lot of JavaScript code.

One of the key techniques to avoid loading all Volto code at once is to use the
[Webpack code splitting](https://webpack.js.org/guides/code-splitting/) feature,
which allows the big JavaScript files to be split and load "on demand", as soon
as new components require it. See more about this in the
[Lazy Loading](./lazyloading) chapter.

To understand how much of an impact, and how to further optimize the chunking
process, Volto includes integration with the [Webpack Bundle Analyzer](https://www.npmjs.com/package/webpack-bundle-analyzer).
To trigger it, run:

```
yarn analyze
```

This will trigger a production build (`yarn build`) and then open a browser at
[http://localhost:8888](http://localhost:8888) where you can see the way your
JS static resources bundle has been split into chunks and the content of each
chunk.
