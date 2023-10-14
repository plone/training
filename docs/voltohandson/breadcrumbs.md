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

We want to hide breadcrumbs from the homepage and change the styling a bit.

We can do it by using bare styling, since Volto injects CSS classes in the body that help us to style depending on the object, the Content Type and the path.
Volto does it very much like Plone does.

```less
//breadcrumbs
.contenttype-plone-site .ui.secondary.vertical.segment.breadcrumbs {
  display: none;
}

.ui.secondary.vertical.segment.breadcrumbs {
  background-color: @white;
  border-bottom: none;
  .ui.breadcrumb {
    .divider {
      color: @black;
    }
    .section {
      color: @black;

      &.active {
        color: @black;
      }
    }
  }
}
```
