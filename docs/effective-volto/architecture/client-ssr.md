---
myst:
  html_meta:
    "description": "Volto Client - Server duality"
    "property=og:description": "Volto Client - Server duality"
    "property=og:title": "Volto Client - Server duality"
    "keywords": "Volto, Plone, SSR"
---

# Volto Client - Server duality

Volto is based on the following three main components of the overall architecture:

- Plone (and Zope) backend server
- Volto Nodejs SSR server
- the Single Page Application JavaScript code that runs in the browser

## The Plone backend

To be able to work as a Volto backend, a Plone website needs to activate its
`plone.restapi` addon, which exposes several JSON-api based endpoints.

## Volto Nodejs server

Volto includes a Server-Side Rendering Nodejs-based HTTP server which runs the
same code that's served to the Client (the browsers) and renders it to a single HTML
string that can be served as the initial loaded page. This type of application
is called an **isomorphic application** and, in Volto, is built on top of the
[Razzle](./razzle) framework.

So Volto websites work (in basic mode) even with JavaScript disabled. All the
HTML received by browser should contain the markup needed to render all the
content on the page.

This server process is based on the popular [Express](https://expressjs.com/) framework.

## Volto - the SPA client bundle

Once the HTML is loaded by the browser, the Volto JavaScript client bundle is
interpreted and executed. Volto, the React app is then created in the browser
memory. From now on, the browser will no longer fetch HTML from the server, but
instead communicate via JSON with Plone, the backend server. The JSON-based
communication protocol, all the available endpoints, etc. are provided by the
[plone.restapi](https://github.com/plone/plone.restapi) package.

Sometimes view components have code that fetches content via async network
calls. In case that content should be rendered together with the rest of
the generated HTML, you need to follow the {doc}`../addons/asyncconnect` chapter.
