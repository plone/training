# Volto Client - Server duality

Volto is based on the following three main components of the overall architecture:

- the Plone + Zope backend server
- the Volto Nodejs SSR server
- the Javascript code that runs in the browser

Volto includes a Server-Side Rendering HTTP server which uses the code that
runs in the Client (the browsers) and renders it to a single HTML string that
can be served as the initial loaded page.

So Volto websites work (in basic mode) even with Javascript disabled. All the
HTML received by browser should contain the markup needed to render all the
content on the page.

Once the HTML is loaded by the browser, the Volto Javascript client bundle is
interpreted and executed. Volto, the React app is then created in the browser
memory. From now on, the browser will no longer fetch HTML from the server, but
instead communicate via JSON with Plone, the backend server. The JSON-based
communication protocol, all the available endpoints, etc. are provided by the
[plone.restapi](https://github.com/plone/plone.restapi) package.

Sometimes view components have code that fetches content via async network
calls. In case that content should be rendered together with the rest of
the generated HTML, you need to follow the
[AsyncConnect](../addons/asyncconect) chapter.
