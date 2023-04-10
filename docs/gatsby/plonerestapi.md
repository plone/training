---
myst:
  html_meta:
    "description": ""
    "property=og:description": ""
    "property=og:title": ""
    "keywords": ""
---

# Fetching Data Using Plone REST.API

Now that we have an idea of how to create nodes, we can move on to retrieving data from a Plone site and creating nodes with that data.

All the data from a Plone site is available in the JSON format using {doc}`plone6docs:plone.restapi/docs/source/index`.

We will be working a lot with this API while working on the Gatsby source-plugin.
It is recommended that you have an API browser to explore the API.

Install [Postman](https://www.postman.com/), then go through the quick guide to working with {doc}`plone6docs:plone.restapi/docs/source/usage/exploring`.

```{note}
We will use the same endpoints for loading the site in a browser, but set the header `Accept: application/json`.
This header tells the endpoint to return JSON data in the response for us to process.
```

## Exploring The Plone REST.API

We will use <https://demo.plone.org> as our source Plone site, since it's already been configured with the `plone.restapi` and is all ready for our usage.

Let us start with the root itself.
Send a GET request to <https://demo.plone.org>.
This returns the JSON data for the root of the Plone site.

```json
{
  "@components": {
      "breadcrumbs": {
          "@id": "https://demo.plone.org/@breadcrumbs"
      },
      "navigation": {
          "@id": "https://demo.plone.org/@navigation"
      },
      "workflow": {
          "@id": "https://demo.plone.org/@workflow"
      }
  },
  "@id": "https://demo.plone.org",
  "@type": "LRF",
  "UID": "7306e5d778be477f8b40bccaad1ecae7",
  "contributors": [],
  "created": "2018-10-13T13:25:31+00:00",
  "creators": [
      "admin"
  ],
  "description": "",
  "effective": null,
  "exclude_from_nav": true,
  "expires": null,
  "id": "en",
  "is_folderish": true,
  "items": [
      {
          "@id": "https://demo.plone.org/media",
          "@type": "LIF",
          "description": "",
          "review_state": "published",
          "title": "Media"
      },
      {
          "@id": "https://demo.plone.org/frontpage",
          "@type": "Document",
          "description": "The ultimate Open Source Enterprise CMS",
          "review_state": "published",
          "title": "Welcome to Plone 5"
      },
      {
          "@id": "https://demo.plone.org/demo",
          "@type": "Folder",
          "description": "Vestibulum dignissim erat id eros mollis vitae tempus leo ultricies. Cras dapibus suscipit consectetur. Integer tincidunt feugiat tristique. Sed et arcu risus. Nam venenatis, tortor ac tincidunt amet.",
          "review_state": "published",
          "title": "Demo"
      }
  ],
  "items_total": 3,
  "language": "en",
  "layout": "folder_listing",
  "modified": "2018-10-13T13:25:32+00:00",
  "parent": {
      "@id": "https://plonedemo.kitconcept.com",
      "@type": "Plone Site",
      "description": "",
      "title": ""
  },
  "review_state": "published",
  "rights": "",
  "subjects": [],
  "title": "English",
  "version": "current"
}
```

Let us explore the `items` array from the response and click on `https://demo.plone.org/frontpage`.
We see that it gives a similar response as we got for the root.
This way all the content objects have equivalent JSON data which our plugin can process and use to create nodes.

### Exercise

Create a node for the Plone document at `https://demo.plone.org/demo/a-page`.
Test the node created from the retrieved data by displaying some data in the `index` or any other page.

Hints: Use Postman to check the data from the endpoint.
Refer to the previous section for creating nodes.
The Axios library can be used for handling HTTP requests.

```{note}
Make sure you send an asynchronous request with the Axios library with `await`.
If not, the function will finish execution before the data is even retrieved and pass it as `undefined`.
```

```{note}
Read more about GET requests with Axios in the [official docs](https://www.npmjs.com/package/axios#example).
```

````{dropdown} Solution
:animate: fade-in-slide-down
:icon: question

```javascript
exports.sourceNodes = async ({ actions }) => {
  const { createNode } = actions;

  const { data } = await axios.get('https://demo.plone.org/demo/a-page', {
    headers: {
      accept: "application/json",
    }
  });

  let documentNode = {
    ...data,
    id: data["@id"],
    internal: {
      type: "PloneDocument",
      contentDigest: crypto
        .createHash(`md5`)
        .update(JSON.stringify(data))
        .digest(`hex`),
      mediaType: "text/html"
    },
    parent: '',
    children: [],
  }

  createNode(documentNode);
  return;
}
```

```jsx
import React from 'react'
import { graphql } from 'gatsby'

import Layout from '../components/layout'

export default ({ data }) => (
  <Layout>
    {data.allPloneDocument.edges.map(({ node }) => (
      <div key={node.id}>
        <h3>{node.title}</h3>
        <p>{node.description}</p>
      </div>
    ))}
  </Layout>
)

export const query = graphql`
  query {
    allPloneDocument {
      edges {
        node {
          id
          title
          description
        }
      }
    }
  }
`;
```
````
