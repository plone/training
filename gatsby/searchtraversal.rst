Search Traversal Method Of Retrieving Data
==========================================

In the previous chapter we covered how to fetch data for a single content object.
For our source-plugin we'll need to fetch the data for all the content objects in a Plone site and process it into nodes.

One of the strategies that we experimented with and adopted for the source-plugin was `Search Traversal`.


Getting The Full List Of Content
--------------------------------

Make a GET Request to `https://plonedemo.kitconcept.com/en/@search`:

.. code-block:: none

  {
    "@id": "https://plonedemo.kitconcept.com/en/@search",
    "items": [
        {
            "@id": "https://plonedemo.kitconcept.com/en",
            "@type": "LRF",
            "description": "",
            "review_state": "published",
            "title": "English"
        },
        {
            "@id": "https://plonedemo.kitconcept.com/en/media",
            "@type": "LIF",
            "description": "",
            "review_state": "published",
            "title": "Media"
        },
        {
            "@id": "https://plonedemo.kitconcept.com/en/frontpage",
            "@type": "Document",
            "description": "The ultimate Open Source Enterprise CMS",
            "review_state": "published",
            "title": "Welcome to Plone 5"
        },
   ...


We see that the `@search` endpoint at the Plone root returns a flat list of all content objects in the site.
We also noted that sending GET requests to the the `@id` gives the data for that particular content object as response.

Combining these, we use the `@search` endpoint to get a full list of objects and then iterate over the `@id` property of each to get the complete data of each object.

.. code-block:: javascript

  const data = await fetchData(baseUrl + '/@search');

  const items = await Promise.all(
    data.items.map(async item => {
      const url = item['@id'];
      return await fetchData(url);
    })
  );

Then we use the same process as before to create the node structure and create Gatsby nodes using the `createNode` action.

The full code for basic search traversal:

.. code-block:: javascript

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

    const baseUrl = 'https://plonedemo.kitconcept.com/en';

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

.. note::
  We prepend `Plone` to the type and remove spaces for it to automatically handle all Plone native types and follow Gatsby specifications for it to be queried using GraphQL.

.. note::
  We use the `https://plonedemo.kitconcept.com/en` here directly for development purposes but in a real-world case, use the `baseUrl` passed in from plugin options in `gatsby-config.js`.

Once we have this complete data, we can process it and create Gatsby nodes for all of them.

Exercise
++++++++

Now that we have all the data from the Plone site being fetched and available using GraphQL, try to get data for this particular page with id `https://plonedemo.kitconcept.com/en/demo/a-news-item`.

..  admonition:: Solution
    :class: toggle

    Since we it is a News Item, we can directly use GraphQL to query for `ploneNewsItem`:

    .. code-block:: none

    {
      ploneNewsItem (id: {eq: "https://plonedemo.kitconcept.com/en/demo/a-news-item"}) {
        id
        title
        description
      }
    }

