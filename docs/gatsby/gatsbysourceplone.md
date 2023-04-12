---
myst:
  html_meta:
    "description": ""
    "property=og:description": ""
    "property=og:title": ""
    "keywords": ""
---

# gatsby-source-plone

With the previous sections on source nodes, retrieving data from `plone.restapi`, and finally using the search traversal method, we have understood how our source-plugin works at base level.

Great work!

`gatsby-source-plone` is basically this plugin with additional helpful features and functionality to handle all kinds of data, caching and so on in an optimal manner.

First remove whatever code we have written in `gatsby-node.js`, as our plugin will be taking care of all that internally.
Then install `gatsby-source-plone` with `npm install gatsby-source-plone`.

Before we can use the plugin, we need to configure it to be used with GatsbyJS.

## Configuration

All of the settings for the `gatsby-source-plone` plugin is in the `gatsby-node.js`:

```javascript
{
  resolve: 'gatsby-source-plone',
  options: {
    baseUrl: 'https://demo.plone.org'
  },
},
```

**baseUrl** is the Plone site from which data is to be sourced from.
It can be a Plone site root or a Plone folder to be used as root.

**searchParams** although not used in the example, it is worth noting.
It is used to limit retrieved content objects by a search parameter.
This allows users to use and display only filtered content in the generated static site.
For examples and more detailed explanation refer to the [docs](https://collective.github.io/gatsby-source-plone/reference/search_parameters/).

**token** is the `JWT` (JSON Web Token) for `plone.restapi`.
This is used in some Plone sites that require authentication to query data.
For configuring authentication with `JWT` and [dotenv](https://github.com/motdotla/dotenv), read the full [documentation](https://collective.github.io/gatsby-source-plone/reference/authentication/) for a step by step reference.

```{note}
<https://demo.plone.org> which was earlier used in the examples requires authentication to query for data.
```

```{warning}
This tutorial previously used `https://plonedemo.kitconcept.com/en` in its examples because it did not require authorization.
The Plone Foundation now actively maintains a [Plone 6 demo](https://demo.plone.org).
Browsing its API requires a basic authorization token.
We have updated all references to use the Plone 6 demo.
All that means the examples might not work. 
```

```{todo}
Update this training to use a site that does not require a basic authorization token.
```

Once configured with basic settings, all the data of the Plone Site specified will be available for query via GraphQL.

To test the plugin you could use the sample configuration mentioned above.

## Exercise

Run the development server with `gatsby develop` and navigate to GraphQL explorer at <http://localhost:8000/___graphql>.

Explore different content object types and also take a look at the breadcrumbs data.

Hints: Query all objects of a type with `allPloneEvent`, `allPloneNewsItem` and so on.
Breadcrumbs data for every content node is available to us with `allPloneBreadcrumbs`.

````{dropdown} Solution
:animate: fade-in-slide-down
:icon: question

```text
{
  allPloneNewsItem {
    edges {
      node {
        id
      }
    }
  }

  allPloneEvent {
    edges {
      node {
        id
      }
    }
  }

  allPloneBreadcrumbs {
    edges {
      node {
        id
      }
    }
  }
}
```
````
