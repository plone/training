---
myst:
  html_meta:
    "description": ""
    "property=og:description": ""
    "property=og:title": ""
    "keywords": ""
---

# What Is The Plone Angular SDK

The [Plone Angular SDK](https://www.npmjs.com/package/@plone/restapi-angular) is an Angular
package (named `@plone/restapi-angular` as it belongs to the Plone NPM organization).

It is a high-level integration layer between Angular and the {doc}`Plone REST API <plone6docs:plone.restapi/docs/source/index>`.

It provides:

- services to dialog with the Plone backend,
- ready-to-use components (for instance `<plone-navigation>` or `<plone-breadcrumbs>`),
- traversing.

## Traversing

Traversing is a key feature when working with a CMS.
Angular core, like the other major JS frameworks, uses routing.
Routing works perfectly for applications, but it is not suitable for web sites (as the site structure is not predictable).

The Traversal service implemented by [Angular traversal](https://github.com/guillotinaweb/angular-traversal) replaces the default Angular routing.

It uses the current location to determine the backend resource (the **context**) and the desired rendering (the **view**).

The view is the last part of the current location and is prefixed by `@@`.
If no view is specified, it defaults to `view`.

The rest of the location is the resource URL.

Example: `/news/what-about-traversal/@@edit`

When traversing to the location, the resource will be requested from the backend,
and the result will become the current context, accessible from any component in the app.

According to the value of the `@type` property of the context, the appropriate component will be used to render the view.

```{note}
We can also use another criteria than `@type` by registring a custom marker
(the package comes with an `InterfaceMarker` which marks context according the `interfaces` attribute,
which is supposed to be a list.

(At the moment, the Plone REST API does not expose this attribute).
```

## A New Integration Approach For Plone

Creating pure frontend applications to publish Plone-managed information rather than customizing the Plone web interface has several benefits:

- those web sites look better and fit the expectations of today's visitors and customers,
- they are faster and can work offline, which makes them more suitable for mobile,
- frontend development is more approachable than Plone development, and a constantly growing amount of web developers master this kind of technology.
