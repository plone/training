---
myst:
  html_meta:
    "description": "Debugging with Volto"
    "property=og:description": "Debugging with Volto"
    "property=og:title": "Debugging with Volto"
    "keywords": "Volto, Plone, Lighthouse, Optimization"
---

# Debugging with Volto

Low effort: `console.log()`. Don't leave it in production code, unless you
really mean it.

React Developer tools allows you to inspect live components. You can check the
component hierarchy, inspect props, hooks, HOCs, etc.

Redux Dev Tools allows you to observe the Redux actions and inspect the store
state.

You can add `debugger` lines in your code, to trigger breakpoints in the browser. To debug the server, you need to hook the [Chrome DevTools](https://nodejs.org/en/docs/guides/debugging-getting-started). Note that there's multiple threads hooked into the inspector (server, client, hotreload process), so you'll have to find the one that coresponds to the server.
