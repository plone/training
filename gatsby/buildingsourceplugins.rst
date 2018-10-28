Building Source Plugins
=======================

In the previous section on source plugins we already covered what they are and how to use them.
Now we will be going a bit in-depth here to understand how they work internally and how to get onto building one.

Our final goal is to build a GatsbyJS source plugin that can query all the data from a Plone site which has `plone.restapi <https://plonerestapi.readthedocs.io/en/latest/introduction.html>`_ configured.
Then this can be used to generate a static site from a Plone site, containing pages, structure and all content.

Let us dive into understanding how to create nodes.


How It Works
------------

Source plugins run on GatsbyJS build time to pull data from a source, cache it, create nodes and a lot more.

We have already gone through ``exports.createPages`` for dynamically creating pages in the previous section.
Here we are creating source nodes, hence ``exports.sourceNodes`` will be used in ``gatsby-node.js``.
It works similar to page creation but has a couple actions and helpers to aid us in creating nodes specifically.

Roughly, the main function for a source plugin would look like:

.. code-block:: javascript

   ...
  exports.sourceNodes = async (
    { actions, cache, getNode, getNodes, store },
    { baseUrl }
  ) => {
   ...

The first function parameter object with ``actions``, ``cache``, ``getNode``, are all passed in from GatsbyJS, while the second parameter object is passed in from plugin options (``gatsby-config.js``).

For instance, the ``gatsby-config.js`` in this case would look like:

.. code-block:: javascript

  ...
  plugins: [
    {
      resolve: 'gatsby-source-plone',
      options: {
        baseUrl: 'https://plonedemo.kitconcept.com/en',
      },
    }
  ]
  ...


GatsbyJS Node
-------------

To create a node we use ``createNode`` action which is a part of the ``actions`` passed into all functions implementing the GatsbyJS API.
The structure of any node would look like this at the base level:

.. code-block:: javascript

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


Note that each node needs to have a property called ``internal`` which is an object containing some information about the node for GatsbyJS to process.
``type`` is a string which represents the type of this particular node, allowing nodes of the same type be queried in GraphQL with ``allTypeName``.

.. note::
 
  While ``type`` can be any string, ensure that it unique and has no spaces or special characters which cannot be handled by GraphQL.


.. note::

  Content digest ensures GatsbyJS does not do extra work if the data of the node has not changed and helps with caching.
  ``crypto`` is an external library which we are using to create content digest. 
  You can install it by ``npm install --save crypto``.


Exercise
++++++++

We want to create a single GatsbyJS node using some sample data.

You need to make sure it works by checking the result in GraphiQL.

Hints: use any sample data and spread it to the node, but make sure it has all the fields that are mentioned above.


..  admonition:: Solution
    :class: toggle

    .. code-block:: javascript

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

    Now in `localhost:8000/___graphql`, you can query it with:

    .. code-block:: none

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


