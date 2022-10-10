---
myst:
  html_meta:
    "description": "Volto views"
    "property=og:description": "Volto views"
    "property=og:title": "Volto views"
    "keywords": "Volto, Plone, Volto views"
---

# Volto views

Writing a "custom view templates" is one of the most basic tasks in classic
Plone development. The Volto blocks, powered by the Pastanaga Editor, make
this task a less frequent occurrence in Volto development, but it's still
possible to follow the same development model, to attach custom views to Plone
content.

A Volto content view is a really simple React component.

```
import React from 'react';
import { Container, Image } from 'semantic-ui-react';

const PersonView = ({ content }) => (
  <Container className="view-wrapper">
  <div className="person">{content.fullname}</div>
  </Container>
);
```

In the Volto configuration registry, you can assign views in the following keys:

- `layoutViews`, to map the context `layout` property to a Volto view component
- `contentTypesViews` to map a content type to a view
- `errorViews`
- `defaultView`

In Volto the DefaultView is blocks-enabled, so you can easily enable the blocks
behavior for any content type. The resolution order is:

- get view by type
- get view by layout
- get default view

## Router views

For generic, views, that aren't attached to the context content, you need to
write a new route.

The view component can be any React component, and you register that route like
so:

```
config.addonRoutes.push({ path: '/**/chat', component: Chat });
```

You should also register the route as `nonContentRoute`, which avoids
triggering the content, breadcrumbs, navigation, etc for routes that are not
based on actual Plone content:

```
config.settings.nonContentRoutes.push("/chat")
```

## External routes

Because Volto is a Single Page Application, all internal links use the
"router", which uses the browser window location history to avoid having to
fully refresh the page whenever new content is loaded.

If we integrate Volto with "external pages", content that lives under the same
domain name, but it's served differently based on rewrite rules at the HTTP
proxy server level, we'll need to instruct Volto to know that those URLs are
"foreign" and it should treat all internal links as external, fully triggering
a browser location change, instead of faking it as a Single Page Application:

```
config.settings.externalRoutes = [
  { match: "/external-page" },
  { match: "/calendar" },
];
```
