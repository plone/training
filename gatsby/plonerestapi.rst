Fetching Data Using Plone REST.API
==================================

Now that we have an idea of how to create nodes, we can move on to retrieving data from a Plone site and creating nodes with that data.

All the data from a Plone site is available in the JSON format using the `plone.restapi <https://plonerestapi.readthedocs.io/en/latest/introduction.html>`_.

We will be working a lot with this API while working on the Gatsby source-plugin, so it is recommended that you have an API browser to explore the API.
Install `Postman <https://www.getpostman.com/>`_ and do go through the quick guide to working with plone.restapi:

https://plonerestapi.readthedocs.io/en/latest/exploring.html#exploring-api-postman-onboarding

.. note::

  We will use the same endpoints for loading the site in a browser, but set the header ``Accept: application/json``.
  This header tells the endpoint to return JSON data in the response for us to process.

Exploring The Plone REST.API
----------------------------

We will use https://plonedemo.kitconcept.com/en as our source Plone site, since it's already been configured with the plone.restapi and is all ready for our usage.

Let us start with the root itself.
Send a GET request to https://plonedemo.kitconcept.com/en.
This returns the JSON data for the root of the Plone site.

.. code-block:: json

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

Let us explore the ``items`` array from the response and click on https://plonedemo.kitconcept.com/en/frontpage.
We see that it gives a similar response as we got for the root.
This way all the content objects have equivalent JSON data which our plugin can process and use to create nodes.


Exercise
++++++++

Create a node for the Plone document at https://plonedemo.kitconcept.com/en/demo/a-page.
Test the node created from the retrieved data by displaying some data in the ``index`` or any other page.

Hints: Use Postman to check the data from the endpoint.
Refer to the previous section for creating nodes.
The Axios library can be used for handling HTTP requests.

.. note::

  Make sure you send an asynchronous request with the Axios library with ``await``.
  If not, the function will finish execution before the data is even retrieved and pass it as ``undefined``.
    
.. note:: 
  Read more about GET requests with Axios in the `official docs <https://www.npmjs.com/package/axios#example>`_.

..  admonition:: Solution
    :class: toggle

    .. code-block:: javascript

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


    .. code-block:: jsx

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





