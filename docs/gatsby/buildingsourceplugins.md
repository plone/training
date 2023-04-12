---
myst:
  html_meta:
    "description": ""
    "property=og:description": ""
    "property=og:title": ""
    "keywords": ""
---

# Building Source Plugins

In the previous section on source plugins we already covered what they are and how to use them.

Now we will be going a bit in-depth here to understand how they work internally and how to get onto building one.

Our final goal is to build a GatsbyJS source plugin that can query all the data from a Plone site.

This requires the Plone site to have [plone.restapi](https://pypi.org/project/plone.restapi/) configured.

```{note}
plone.restapi is a RESTful hypermedia API for Plone.
Read more about it in the documentation of {doc}`Plone REST API <plone6docs:plone.restapi/docs/source/index>`.
```

Then this plugin can be used to generate a static site from a Plone site, containing pages, structure and all of its contents.

Let us dive into understanding how to create nodes.

## Comparing Plone Site and GatsbyJS Site

A Plone site has different types of content objects including `Document`, `News Item`, `Folder` and so on.

Each of these content objects has pages dedicated to them.

`Folder` content object natively has children, which are content objects inside of them.

This way there is a page structure as well.

```{note}
Plone even allows custom types.
Read more about this in {doc}`plone6docs:plone.restapi/docs/source/endpoints/content-types`).
```

Each of these content objects can be compared to nodes in GatsbyJS.

Similar to what we did in the "Dynamic Pages" section, pages can be created for each of these nodes.

The `plone.restapi` gives us data of children in `Folders` along with content itself.

This allows us to setup internal linking to ensure the structure as the Plone site.

Navigation and breadcrumb data as well is provided by `plone.restapi`.

These also can be made into nodes and directly used in GatsbyJS.

## How It Works

Before we get into using the `plone.restapi`, let us first understand how node creation works.

Source plugins run on GatsbyJS build time to pull data from a source, cache it, create nodes and a lot more.

To create nodes, we will be using `exports.sourceNodes` API in `gatsby-node.js`.

This is a lifecycle API similar to `exports.createPages` which we used earlier for dynamically creating pages.

```{note}
Read more about `sourceNodes` API in the [docs](https://www.gatsbyjs.com/docs/reference/config-files/gatsby-node/#sourceNodes).
```

It works similar to page creation but has a couple actions and helpers to aid us in creating nodes specifically.

Roughly, the main function for a source plugin in `gatsby-node.js` would look like:

```jsx
 ...
exports.sourceNodes = async (
  { actions, cache, getNode, getNodes, store },
  { baseUrl }
) => {
 ...
```

The first function parameter object with `actions`, `cache`, `getNode`, are all passed in from GatsbyJS, while the second parameter object is passed in from plugin options (`gatsby-config.js`).

For instance, the plugins part of `gatsby-config.js` in this case would look like:

```javascript
plugins: [
  {
    resolve: 'gatsby-source-plone',
    options: {
      baseUrl: 'https://demo.plone.org',
    },
  }
]
```

```{note}
`exports.sourceNodes` is an `async` function.
This means that it works asynchronously and returns a promise.
It is usually used in combination with `await` for processes that requires pausing of execution of function including fetching of data or asynchronous processing.
The [MDN docs](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/async_function) has detailed information about its working.
```

## GatsbyJS Node

To create a node we use the `createNode` action which is a part of the `actions` passed into all functions implementing the GatsbyJS API.

```{note}
GatsbyJS offers a whole list of actions creators wrapped with a dispatch as `actions`.
Read more about them in the [GatsbyJS docs](https://www.gatsbyjs.com/docs/reference/config-files/actions/).
```

The structure of any node would look like this at the base level:

```javascript
let node = {
  sampleData: "Sample Data",

  id: "sampleId",
  internal: {
    type: "sampleType",
    contentDigest: crypto
      .createHash(`md5`)
      .update(JSON.stringify(sampleData))
      .digest(`hex`),
      mediaType: "text/html"
  },
  parent: '',
  children: [],
}
```

Note that each node needs to have a property called `internal` which is an object containing some information about the node for GatsbyJS to process.

`type` is a string which represents the type of this particular node, allowing nodes of the same type be queried in GraphQL with `allTypeName`.

```{note}
While `type` can be any string, ensure that it is unique and has no spaces or special characters which cannot be handled by GraphQL.
```

```{note}
Content digest ensures GatsbyJS does not do extra work if the data of the node has not changed and helps with caching.
`crypto` is an external library which we are using to create content digest.
You can install it by `npm install --save crypto`.
```

### Exercise

We want to create a single GatsbyJS node using some sample data.

You need to make sure it works by checking the result in GraphiQL.

Hints: use any sample data and spread it to the node, but make sure it has all the fields that are mentioned above.

````{dropdown} Solution
:animate: fade-in-slide-down
:icon: question

In `gatsby-node.js`:

```javascript
const crypto = require('crypto');

exports.sourceNodes = async ({ actions }) => {
  const { createNode } = actions;

  const sampleData = {
    eventData: "Plone Conf 2018",
  }

  let testNode = {
    ...sampleData,
    id: "test",
    internal: {
      type: "event",
      contentDigest: crypto
        .createHash(`md5`)
        .update(JSON.stringify(sampleData))
        .digest(`hex`),
      mediaType: "text/html"
    },
  }

  createNode(testNode);
  return;
}
```

Now in <http://localhost:8000/___graphql>, you can query it with:

```text
{
  allEvent {
    edges {
      node {
        id
        eventData
      }
    }
  }
}
```
````
