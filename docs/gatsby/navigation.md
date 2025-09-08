---
myst:
  html_meta:
    "description": ""
    "property=og:description": ""
    "property=og:title": ""
    "keywords": ""
---

# Navigation

We have covered page creation and displaying data.

As the amount of the content and pages increases, navigation is important so that a user does not get lost deep in a site.

`gatsby-source-plone` provides Breadcrumb and root Navigation data, making this task fairly simple.

## Breadcrumbs

Since breadcrumbs depend on the page you are in, it needs to be dynamically created for each page.

So the approach is to query it in each page as they are created and pass it on to the Breadcrumb component.

```text
ploneBreadcrumbs(_path: { eq: $path }) {
  items {
    _id
    _path
    title
  }
}
```

Here `items` is an array of items where each one is a breadcrumb.

This data can be appropriately styled and used in a breadcrumb bar.

## Navigation

This is the common topbar in all the views of the site.

It allows quick jumping between root folders (depending on customization).

Unlike breadcrumbs, we can use a static query here (which queries data initially and then just uses existing data).

```jsx
const NavBar = ({ active }) => (
  <StaticQuery
    query={graphql`
      query NavbarQuery {
        ploneNavigation(_path: { eq: "/" }) {
          items {
            _id
            _path
            title
          }
        }
      }
    `}
    render={data => (
      <nav>
    ...
```

Similar to breadcrumbs as mentioned above, we get an array which can be used to display the navbar.
