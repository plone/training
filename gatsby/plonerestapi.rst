Fetching Data Using Plone REST.API
==================================

All the data from a Plone site is available in the JSON format using the `plone.restapi <https://plonerestapi.readthedocs.io/en/latest/introduction.html>`_.

We'll be working a lot with this API while working on the Gatsby source-plugin, so it is recommended that you have an API browser to explore the API.
Install `Postman <https://www.getpostman.com/>`_ and do go through the quick guide to working with plone.restapi:

https://plonerestapi.readthedocs.io/en/latest/exploring.html#exploring-api-postman-onboarding

.. note:: We're using the same endpoints as for loading the site on a browser but setting the header `Accept: application/json` is what retrieves JSON data for us.

Exploring The Plone REST.API
----------------------------

We'll be using https://plonedemo.kitconcept.com/en as our source Plone site, since it's already been configured with the plone.restapi and is all ready for our usage.

Let's start with the root itself: A GET Request to `https://plonedemo.kitconcept.com/en` would give the JSON data for the root of the Plone site.

.. code-block:: none

  {
    "@components": {
        "breadcrumbs": {
            "@id": "https://plonedemo.kitconcept.com/en/frontpage/@breadcrumbs"
        },
        "navigation": {
            "@id": "https://plonedemo.kitconcept.com/en/frontpage/@navigation"
        },
        "workflow": {
            "@id": "https://plonedemo.kitconcept.com/en/frontpage/@workflow"
        }
    },
    "@id": "https://plonedemo.kitconcept.com/en/frontpage",
    "@type": "Document",
    "UID": "5938b3c2c0e147b18fbf20d32842eb06",
    "allow_discussion": null,
    "changeNote": "",
    "contributors": [],
    "created": "2018-10-13T13:25:31+00:00",
    "creators": [
        "admin"
    ],
   ...

Let us explore the the `items` array from the response and click on `https://plonedemo.kitconcept.com/en/frontpage`.
We see that it gives a similar response as we got for the root.
This way, all the content objects have equivalent JSON data which our plugin can process and use to create nodes.


Exercise
++++++++

Create a node for a the Plone document at `https://plonedemo.kitconcept.com/en/demo/a-page` and test the by displaying some data in the `index` or any other page.

Hints: use Postman to check the data from the endpoint and process accordingly. Axios library can be used for ease of handling HTTP requests.

.. note:: 
    Minor errors may arise when Gatsby node specific fields are overwritten by spreading the Plone object data.
    For now, they can be fixed by defaulting them to the node field data: `node.parent` is an empty string and `node.children` an empty array.

..  admonition:: Solution
    :class: toggle

    .. code-block:: none

    exports.sourceNodes = async ({ actions }) => {
      const { createNode } = actions;

      const { data } = await axios.get('https://plonedemo.kitconcept.com/en/demo/a-page', {
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


    .. code-block:: none

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





