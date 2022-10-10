---
myst:
  html_meta:
    "description": "Integrate with Volto’s asyncConnect for SSR"
    "property=og:description": "Integrate with Volto’s asyncConnect for SSR"
    "property=og:title": "Integrate with Volto’s asyncConnect for SSR"
    "keywords": "Volto, Plone, SSR, SPA"
---

# Integrate with Volto’s asyncConnect for SSR

We already know that Volto provides full server-side rendering of the React
components, making it an isomorphic application.

How does that work? In simplified pseudocode, it works like this:

- in server.jsx we have code like `react-dom.renderToString(<Router/>)`
- the Router renders its declared components, which is the `App` and its
  direct child, the `View` component

Now, here is where it gets tricky: the View component should have the content
from the backend for the current URL, but it that content is fetched via an
async backend endpoint call.

So we need a mechanism to "stop" the processing of the renderToString and make
it wait until the backend content has arrived. In Volto this is solved with
the `asyncConnect()` HOC helper, which is a port of [redux-connect][1]

The internal implementation uses Redux and the "trick" is to prepopulate the
Redux store with the information that would be needed in your components:

Here's an example where the `asyncPropsExtenders` configuration is used to
prefetch a `footer-links` page from the backend and include it with every SSR:

```js
  config.settings.asyncPropsExtenders = [
    ...(config.settings.asyncPropsExtenders || []),
    {
      path: '/',
      extend: (dispatchActions) => {
        const action = {
          key: 'footer',
          promise: ({ location, store }) => {
            // const currentLang = state.intl.locale;
            const bits = location.pathname.split('/');
            const currentLang =
              bits.length >= 2 ? bits[1] || DEFAULT_LANG : DEFAULT_LANG;

            const state = store.getState();
            if (state.content.subrequests?.[`footer-${currentLang}`]?.data) {
              return;
            }

            const url = `/${currentLang}/footer-links`;
            const action = getContent(url, null, `footer-${currentLang}`);
            return store.dispatch(action).catch((e) => {
              // eslint-disable-next-line
              console.log(
                `Footer links folder not found: ${url}. Please create as folder
                named footer-links in the root of your current language`,
              );
            });
          },
        };
        return [...dispatchActions, action];
      },
    },
  ];
```

Note: this example is a low-tech "frontend-er only" solution. In real life you
will probably want to devise a mechanism where that footer-links information is
automatically included with every content request.

Notice the extender mechanism, we register a "modifier" for the current list of
"async connect dispatch actions".

```
config.settings.asyncPropsExtenders = [
  ...config.settings.asyncPropsExtenders,
  {
    path: '/',
        extend: (dispatchActions) => dispatchActions.filter(asyncAction=>
            asyncAction.key !== 'breadcrumb')
  }
]
```

[1]: https://github.com/makeomatic/redux-connect/
