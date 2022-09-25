# Volto Anatomy

As with any large complex application, there are multiple facets to Volto, and
some of them may be strange or unfamiliar to developers used only to Plone
classic development. But, if viewed in the context of the wider modern frontend
development world, Volto is no longer a strange beast, but a relatively
conformist application.

To list some of the things that Volto is:

- A Single Page Application, based on React that runs in client browsers
- An Express-powered HTTP server that can completely generate full HTML pages
  server-side. See the [Server Side Rendering](./client-ssr) chapter for more.
- A CMS UI to interact with Plone, the backend
- An extensive, extensible development API to easily develop custom websites and
  capabilities for the CMS UI

There are two ways of running Volto:

- Standalone (to develop Volto itself)
- as a Volto Project (for your own custom use, to develop a new website).

Running Volto standalone is simple: make a clone of Volto from Github, run
`yarn` to download its dependencies, then `yarn start` to simply start Volto.
This is useful for developing Volto, but it is not the way to use it, if you
want to develop your own custom Volto website.

The second method of running Volto is to use the Volto App generator and
bootstrap (based on a fixed scaffolding) a new Javascript package that can
piggy-back on Volto and treat it as a library. We call this the "Volto
project".


The next steps, after bootstrapping the new Volto project, is to make it your
own. The community has settled, for now, to use [Yarn
Classic](https://classic.yarnpkg.com/lang/en/) as the default Javascript
package manager, so, to add dependencies on new third-party
Javascript packages, you'd run:

```
yarn add react-slick
```

to make the react-slick library available to your Volto project.

You can use this Volto Project scaffold to develop a complete Volto-powered
website, without needing to do anything else. You can use the `<root>/src/` folder to
host your custom Javascript code and the `<root>/theme` folder to customize the
Volto theme and create your custom look and feel.

But to enable a greater modularity and reusability of code, you can create new
Javascript packages that are deeply integrated with Volto, the so-called "Volto
addons".

## Deep dive into Volto

To start Volto in development mode, we do `yarn start`. If you peek inside [Volto's
package.json](https://github.com/plone/volto/blob/d7b6db3db239d09ceafee61dacf14fa7acec9b4b/package.json#L33) at
the script that's executed for that, you'll notice it simply says `razzle
start`. So, when we start Volto, we actually start Razzle. See the
[Razzle chapter](./razzle) for more details.

Running in development mode provides automatic reload of changed code
(hot reloading) and better debugging (unminified source code maps, etc).
