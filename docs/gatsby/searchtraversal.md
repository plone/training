---
myst:
  html_meta:
    "description": ""
    "property=og:description": ""
    "property=og:title": ""
    "keywords": ""
---

# Search Traversal Method Of Retrieving Data

In the previous chapter we covered how to fetch data for a single content object.
For our source-plugin we will need to fetch the data for all the content objects in a Plone site and process it into nodes.

One of the strategies that we experimented with and adopted for the source-plugin was "Search Traversal".

## Getting The Full List Of Content

Make a GET request to `https://demo.plone.org/@search`.

```json
{
  "@id": "https://demo.plone.org/@search",
  "items": [
      {
          "@id": "https://demo.plone.org",
          "@type": "LRF",
          "description": "",
          "review_state": "published",
          "title": "English"
      },
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
  ]
}
```

With a call to `@search` endpoint we can see a flat list of results as shown above.

There is limited information here.
To build a node we need more data.
We could try calling the `@id` endpoint and see what it returns.

Send a GET request to the `id` of one of these objects, say `https://demo.plone.org/frontpage`.

```json
{
  "@components": {
      "breadcrumbs": {
          "@id": "https://demo.plone.org/frontpage/@breadcrumbs"
      },
      "navigation": {
          "@id": "https://demo.plone.org/frontpage/@navigation"
      },
      "workflow": {
          "@id": "https://demo.plone.org/frontpage/@workflow"
      }
  },
  "@id": "https://demo.plone.org/frontpage",
  "@type": "Document",
  "UID": "5938b3c2c0e147b18fbf20d32842eb06",
  "allow_discussion": null,
  "changeNote": "",
  "contributors": [],
  "created": "2018-10-13T13:25:31+00:00",
  "creators": [
      "admin"
  ],
  "description": "The ultimate Open Source Enterprise CMS",
  "effective": null,
  "exclude_from_nav": false,
  "expires": null,
  "id": "frontpage",
  "is_folderish": false,
  "language": "en",
  "layout": "document_view",
  "modified": "2018-10-13T13:25:31+00:00",
  "parent": {
      "@id": "https://demo.plone.org",
      "@type": "LRF",
      "description": "",
      "review_state": "published",
      "title": "English"
  },
  "relatedItems": [],
  "review_state": "published",
  "rights": "",
  "subjects": [],
  "table_of_contents": null,
  "text": {
      "content-type": "text/html",
      "data": "<p>Edit this site and test Plone 5 now!</p>",
      "encoding": "utf-8"
  },
  "title": "Welcome to Plone 5",
  "version": "current"
}
```

That is exactly what we need.

Now we need to combine these two calls to get the complete data set from the site content:

```javascript
const data = await fetchData(baseUrl + '/@search');

const items = await Promise.all(
  data.items.map(async item => {
    const url = item['@id'];
    return await fetchData(url);
  })
);
```

Then we use the same process as before to create the node structure and create Gatsby nodes using the `createNode` action.

The full code for basic search traversal:

```javascript
const crypto = require('crypto');
const axios = require('axios');

const fetchData = async url => {
  const { data } = await axios.get(url, {
    headers: {
      accept: "application/json",
    }
  });

  return data;
}

exports.sourceNodes = async ({ actions }) => {
  const { createNode } = actions;

  const baseUrl = 'https://demo.plone.org';

  console.log('Fetching items list');
  const data = await fetchData(baseUrl + '/@search');

  console.log('Fetching item data');
  const items = await Promise.all(
    data.items.map(async item => {
      const url = item['@id'];
      return await fetchData(url);
    })
  );

  console.log('Creating node structure');
  const nodes = items.map(item => {
    let node = {
      ...item,
      internal: {
        type: 'Plone' + item['@type'].replace(' ', ''),
        contentDigest: crypto
          .createHash(`md5`)
          .update(JSON.stringify(item))
          .digest(`hex`),
        mediaType: 'text/html',
      },
      id: item["@id"],
      parent: '',
      children: [],
    };

    return node;
  });

  console.log('Creating nodes');
  nodes.map(node => createNode(node));
}
```

Let us review the steps:

- Use the `@search` endpoint to get a full list of content objects.
- Then iterate over the `@id` property of each object in the list and send GET requests to retrieve full data.
- Create nodes for each of the objects with this data.

```{note}
We prepend `Plone` to the type and remove spaces for it to automatically handle all Plone native types and follow Gatsby specifications for it to be queried using GraphQL.
```

```{note}
We use the <https://demo.plone.org> here directly for development purposes but in a real-world case, use the `baseUrl` passed in from plugin options in `gatsby-config.js`.
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

Once we have this complete data, we can process it and create Gatsby nodes for all of them.

### Exercise

Now that you have the search traversal method implemented, all the data form the Plone site is available using GraphQL.

Run the development server with `gatsby develop` and navigate to GraphiQL explorer at <http://localhost:8000/___graphql>.

Try to get data for a particular page with id `https://demo.plone.org/demo/a-news-item`.

````{dropdown} Solution
:animate: fade-in-slide-down
:icon: question

Since it is a News Item, we can directly use GraphQL to query for `ploneNewsItem`:

```text
{
  ploneNewsItem (id: {eq: "https://demo.plone.org/demo/a-news-item"}) {
    id
    title
    description
  }
}
```

Similarly you can get data for other content objects and even lists of objects.
````
