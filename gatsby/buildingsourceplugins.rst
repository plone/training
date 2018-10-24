Building Source Plugins
=======================

In the previous section on source plugins we already covered what they are and how to use them.
We'll be going a bit in-depth here to understand how they work internally and how to get onto building one.


How It Works
------------

Source plugins run on GatsbyJS build time to pull data from a source, cache it, create nodes and a lot more.

We've already gone through `export.createPages` for dynamically creating pages.
Similarly, here since we're creating nodes the `export.sourceNodes` will be used in `gatsby-node.js` to work with source nodes.

Roughly, the main function for a source plugin would look like:

.. code-block:: javascript

   ...
  exports.sourceNodes = async (
    { actions, cache, getNode, getNodes, store },
    { baseUrl }
  ) => {
   ...

First function parameter object with `actions`, `cache`, `getNode` etc are all passed in from Gatsby, while the second parameter object is passed in from plugin options (`gatsby-config.js`).

For instance the `gatsby-config.js` for this would look like:

.. code-block:: none

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


The complete list of plugin options and their function for `gatsby-source-plone` is listed in the `documentation <https://collective.github.io/gatsby-source-plone/reference/plugin_options/>`_.


Gatsby Node
-----------

To create a node we use `createNode` action which is a part of the `actions` passed into all functions implementing the Gatsby API.

Note that each node needs to have a property called `internal` which is an object which looks like:

.. code-block:: none

  internal: {
	  type: "SampleType",
	  contentDigest: crypto
	        .createHash(`md5`)
	        .update(JSON.stringify(sampleData))
	        .digest(`hex`),
	  mediaType: "text/html"
  }

'type' can be any string which represents the type of the this particular node allowing nodes of same type of be queried in GraphQL with `allTypeName`.

.. note::
  Content digest ensures Gatsby does not do extra work if the data of the node has not changed and helps with caching.
  `crypto` is an external library which we are using to create content digest which should be installed by `npm install --save crypto`.


Exercise
++++++++

We want to create a single Gatsby node using some sample data.

You need to make sure it works by checking the result in GraphiQL.

Hints: use any sample data and spread it to the node, but make sure it has all the fields that are mentioned above.


..  admonition:: Solution
    :class: toggle

    .. code-block:: none

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