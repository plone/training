---
myst:
  html_meta:
    "description": "Inside Volto"
    "property=og:description": "Inside Volto"
    "property=og:title": "Inside Volto"
    "keywords": "Volto, Plone, Volto project, Volto architecture"
---

# Inside Volto

As with any large complex application, there are multiple facets to Volto, and
some of them may be strange or unfamiliar to developers used only to Plone
classic development. But, if viewed in the context of the wider modern frontend
development world, Volto is no longer a strange beast.

To list some of the things that Volto is:

- A **Single Page Application**, based on React that runs in client browsers
- An **Express-powered HTTP server** that can completely generate full HTML pages
  server-side. See the [Server Side Rendering](./client-ssr) chapter for more.
- A CMS UI to interact with Plone, the backend
- An extensive, extensible **development API** to easily develop custom websites and
  capabilities for the CMS UI

There are two ways of running Volto:

- **Standalone** (to develop Volto itself)
- as a **Volto Project** (for your own custom use, to develop a new website).

Running Volto standalone is simple: make a clone of Volto from Github, run
`yarn` to download its dependencies, then `yarn start` to simply start Volto.
This is useful for developing Volto, but it is not the way to use it, if you
want to develop your own custom Volto website.

The second method of running Volto is to use the **Volto App generator** and
bootstrap (based on a fixed scaffolding) a new JavaScript package that can
piggy-back on Volto and treat it as a library. We call this the "Volto
project".


The next steps, after bootstrapping the new Volto project, is to make it your
own. The community has settled, for now, to use [Yarn
Classic](https://classic.yarnpkg.com/lang/en/) as the default JavaScript
package manager, so, to add dependencies on new third-party
JavaScript packages, you'd run:

```
yarn add react-slick
```

to make the react-slick library available to your Volto project.

You can use this Volto Project scaffold to develop a complete Volto-powered
website, without needing to do anything else. You can use the `<root>/src/` folder to
host your custom JavaScript code and the `<root>/theme` folder to customize the
Volto theme and create your custom look and feel.

But to enable a greater modularity and reusability of code, you can create new
JavaScript packages that are deeply integrated with Volto, the so-called "Volto
addons".

## Volto codebase

Looking inside Volto's source code, we find several points of interest:

- `server.js`, `start-server.js` and the `express-middleware` folders contain
  code for the Express HTTP server, with the counterparts `client.js` and
  `start-client.jsx` for the browser client bundle.
- the `components` folder is the biggest, with two separate branches: `theme`
  and `manage`. The `theme` folder hosts components that are more basic and are
  always available to the anonymous visitors, while the `manage` branch hosts
  more advanced components, the CMS UI, blocks, widgets, etc.
- `store.js`, `middleware`, `actions` and the `reducers` are the centralized
  data store. See the [Redux](./redux) chapter for more details.
- `registry.js` and the `config` folder will constitute the Volto configuration
  registry, a deep JavaScript object that holds settings and configuration.
  The registry can be altered by Volto projects and Addons. It doesn't have the
  fancy features of the component registry of ZCA, but it's easier to reason
  and easily inspectable.
- the `theme.js` and the parent folder `theme` are Volto's Pastanaga theme,
  materialized as a Semantic-UI theme.

## Deep dive into Volto

To start Volto in development mode, we do `yarn start`. If you peek inside [Volto's
package.json][1] at
the script that's executed for that, you'll notice it simply says `razzle
start`. So, when we start Volto, we actually start Razzle. See the
[Razzle chapter](./razzle) for more details.

Running in development mode provides automatic reload of changed code
(hot reloading) and better debugging (unminified source code maps, etc).

Razzle provides two entrypoints for webpack: the server and the client bundles.

### Volto HTTP server

The server uses Expressjs uses `renderToString` from `react-dom/server` to
provide server-side rendering of the HTML pages. From these generated HTML
pages, the client bundle will be loaded by the browsers.

The HTTP server is extensible via Express middleware and Volto provides an API
to declare and load them from Volto Projects and Addons.

### Volto as Single Page Application

Once the browser loads the client bundle, Volto mounts a location-based React
Router and uses the App component as the top level component, plus other
defined child routes. The View render component will be found and instantiated.
Check the `src/routes.js` module to see all available routes. Notice that the
generic `View` component is close to the last in the list of default routes,
this allows routes to take precedence over the content matching.

On a content page view, the `View` component is rendered by App's router
matching. Once the `View` component is mounted, it triggers a network call to
fetch the JSON representation of the current context content. Based on the
response content, it will lookup for a view component that matches the content
(so, for example, news items can have their own custom views, etc).

The `DefaultView`, which is used when there's no custom content-type based view
component found, is also "blocks-enabled". It will lookup two keys in the
content, the `blocks` and `blocks_layout`. See the [Volto Blocks](./blocks)
chapter for more details.

The main View component has a "route detector" that will trigger the
`getContent` action whenever the route (window location) changes, so new
content will be fetched and a new view is rendered acordingly.

[1]: https://github.com/plone/volto/blob/d7b6db3db239d09ceafee61dacf14fa7acec9b4b/package.json#L33
