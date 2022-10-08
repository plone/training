---
myst:
  html_meta:
    "description": "Hide the breadcumbs on the siteroot"
    "property=og:description": "Hide the breadcumbs on the siteroot"
    "property=og:title": "Hide breadcumbs on the siteroot"
    "keywords": "Plone, Volto, Training, Theme, Breadcrumbs"
---

(voltohandson-breadcrumbs-label)=

# Breadcrumbs

## Hiding them from the App first level component

We want to hide breadcrumbs from the homepage.

We can do it by using bare styling, since Volto injects CSS classes in the body that help us to style depending on the object, the content type and the path.
Volto does it very much like Plone does.

```less
.contenttype-plone-site .ui.secondary.vertical.segment.breadcrumbs {
  display: none;
}
```
