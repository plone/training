Copying The Plone Site
======================

The end goal of the plugin along with GatsbyJS is to generate a static site which is an exact copy of the Plone site it sourced data from.

Breaking this into steps:
- Create pages for each content object and ensure tree structure by retaining parent and items relationships
- Display HTML, images and files in content objects correctly
- Handle navigation in the site with a Navbar and Breadcrumbs Breadcrumbs


Page Creation
-------------

``exports.createPages`` is the API used in ``gatsby-node.js`` for creating pages from nodes.

For instance, to create pages for all nodes of type ``PloneFolder``:

.. code-block:: javascript

  const path = require('path');

  exports.createPages = async ({ graphql, actions }) => {
    const { createPage } = actions;

    // Get data via GraphQL
    const result = await graphql(`
      {
        allPloneFolder {
          edges {
            node {
              _path
            }
          }
        }
      }
    `);

    // Create pages for each PloneFolder item
    result.data.allPloneFolder.edges.forEach(({ node }) => {
      createPage({
        path: node._path,
        component: path.resolve('./src/templates/Folder.js'),
      });
    });
  };

The ``_path`` property is very helpful to us to create pages since it is unique to all nodes and even files and images are linked to the nodes they are present in, with the ``_path`` value.
This backlinking will be explained in the later sections.
So basically it can be used to set the relative path of a node in the static site generated and also to get the required images and files.


Handling Different Data Types
-----------------------------

For generating pages for each content object, the same process as illustrated by the code above can be followed.
The only major change would be that we would be using a ``default.js`` template instead and separate components for each type.
This would internally check what type of node is being used for page creation and return the matching component.

The ``default.js`` template:

.. code-block:: jsx

  const componentFor = data => {
    if (data) {
      if (data.ploneCollection) {
        return (
          <Folder
            data={data.ploneCollection}
          />
        );
      } else if (data.ploneDocument) {
        return (
          <Document
            data={data.ploneDocument}
          />
        );
      } else if (data.ploneEvent) {
        return (
          <Event
            data={data.ploneEvent}
          />
        );
      } else if (data.ploneFolder) {
        return (
          <Folder
            data={data.ploneFolder}
          />
        );
      } else if (data.ploneNewsItem) {
        return (
          <NewsItem
            data={data.ploneNewsItem}
          />
        );
      } else {
        return null;
      }
    } else {
      return null;
    }
  };

  const DefaultLayout = ({ data }) => <Layout>{componentFor(data)}</Layout>;

  // Query for all the different types from GraphQL
  // Fragments for each type are defined in their relevant components
  export const query = graphql`
    query DefaultTemplateQuery($path: String!) {
      ploneCollection(_path: { eq: $path }) {
        ...Collection
      }
      ploneDocument(_path: { eq: $path }) {
        ...Document
      }
      ploneEvent(_path: { eq: $path }) {
        ...Event
      }
      ploneFolder(_path: { eq: $path }) {
        ...Folder
      }
      ploneNewsItem(_path: { eq: $path }) {
        ...NewsItem
      }
    }
  `;

To understand what happens in the components, let us take the example of the ``Folder`` component:

.. code-block:: jsx

  import React from 'react';
  import { graphql, Link } from 'gatsby';

  const Folder = ({ data, title }) => (
    <nav key={data._id}>
      <h1>{title ? title : data.title}</h1>
      <p>
        <strong>{data.description}</strong>
      </p>
      <ul>
        {data.items.filter(item => item.title).map(item => (
          <li key={item._path}>
            <Link to={item._path}>{item.title}</Link>
          </li>
        ))}
      </ul>
    </nav>
  );

  export default Folder;

  export const query = graphql`
    fragment Folder on PloneFolder {
      _id
      title
      description
      items {
        _path
      }
      _path
    }
  `;

Here, the fragment is used by ``default.js`` to get the relevant data of the ``Folder`` content object and is passed in to the Folder component as ``data``.
The ``Folder`` component now displays the title and description of the Folder itself and a list of child items.

.. note::

  See how we can use ``_path`` for directly linking between GatsbyJS pages.
  
