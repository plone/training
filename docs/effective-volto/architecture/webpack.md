---
myst:
  html_meta:
    "description": "Webpack"
    "property=og:description": "Webpack"
    "property=og:title": "Webpack"
    "keywords": "Volto, Plone, Webpack"
---

# Webpack

In a typical modern web application architecture, we have two parts:

- the backend server, which serves HTML pages to visitors
- JavaScript code that gets executed in the visitor's browser and this
  constitutes the "client application"

In older Plone versions (up to Plone 5), all JavaScript code was bundled
(concatenated, minified) into several static JS files that were delivered to
the browsers. Deciding which static resources are defined, how they get
combined, etc, was the job of the Plone Resource Registry.

With Plone 6, both Classic and Volto Frontend, [Webpack](https://webpack.js.org/)
is used as the tool that gathers all the required JS application code and bundles them
into static JS files which are loaded by the browsers.

So Webpack, in our case, is the **bundler**. Given an "entrypoint", it statically
analyzes all JavaScript code for imports and will discover all the code that
needs to be included in the delivered bundle.

But the client web application is not only simple "classic" JavaScript. Volto
itself uses Ecmascript Modules (.esm) and a superset of JavaScript, the JSX syntax.

So, included with webpack is the following functionality (all via plugins):

- convert JSX to JavaScript code (via Babel plugin)
- transpiling ESM modules to CommonJS require-based JavaScript modules (Babel)
- concatenate and provide "bundle and chunk loaders" for the multiple JS files
- compiling LESS and SASS files to CSS, using their loader plugins
- bundling the multiple CSS files together
- loading other resources, such as images
- sometimes (depending on size), wholly including static images into the
  JavaScript bundles

There is a tendency in the industry to dismiss Webpack and Babel as being
complicated and slow. For now it is the solution that provides the optimum
amount of features and flexibility, while benefiting from the fact that it's
the mainstream solution for these tasks. As alternative solutions are developed
and mature, we may migrate Volto's basic tooling setup to one such solution.
