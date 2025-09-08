---
myst:
  html_meta:
    "description": ""
    "property=og:description": ""
    "property=og:title": ""
    "keywords": ""
---

# Copying The Plone Site

Now we have seen how the plugin and starter work together.

The end goal of the plugin along with GatsbyJS is to generate a static site which is an exact copy of the Plone site it sourced data from.

Once `gatsby-source-plugin` retrieves all the required data for us, the `gatsby-starter-plone` processes and uses this data to generate the static site.

Internally what `gatsby-starter-plone` does in steps is:

- Create pages for each content object and ensure tree structure by retaining parent and items relationships.
- Display HTML, images and files in content objects correctly.
- Handle navigation in the site with a Navbar and Breadcrumbs.

## Page Creation

`exports.createPages` is the API used in `gatsby-node.js` for creating pages from nodes.

To create pages for all nodes, first we query the list of all different types of nodes and use this list to create individual pages.

To illustrate how this process works, let us create pages for all nodes of type `PloneFolder`.

Later we can move on to include all the other types.

In `gatsby-node.js`:

```javascript
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
```

The `_path` property is helpful to create pages.
It is unique to all nodes.
Files and images are linked to the nodes in which they are present via the `_path` value.

This backlinking will be explained in the later sections.

Backlinking can be used to set the relative path of a node in the generated static site.
It can also get the required images and files.

## Handling Different Data Types

For generating pages for each content object, the same process as illustrated by the code above can be followed.
The only major change would be that we would be using a `default.js` template instead and separate components for each type.
This would internally check what type of node is being used for page creation and return the matching component.

In `gatsby-node.js` query for all data types:

```jsx
exports.createPages = async ({ graphql, actions }) => {
  const { createPage } = actions;
  const result = await graphql(`
    {
      allPloneDocument {
        edges {
          node {
            _path
          }
        }
      }
      allPloneEvent {
        edges {
          node {
            _path
          }
        }
      }
      allPloneFolder {
        edges {
          node {
            _path
          }
        }
      }
      allPloneNewsItem {
        edges {
          node {
            _path
          }
        }
      }
    }
  `);
  []
    .concat(
      result.data.allPloneDocument.edges,
      result.data.allPloneEvent.edges,
      result.data.allPloneFolder.edges,
      result.data.allPloneNewsItem.edges
    )
    .forEach(({ node }) => {
      createPage({
        path: node._path,
        component: path.resolve('./src/templates/default.js'),
      });
    });
  }
```

The `default.js` template:

```jsx
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
```

To understand what happens in the components, let us take the example of the `Folder` component:

```jsx
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
```

Here, the fragment is used by `default.js` to get the relevant data of the `Folder` content object and is passed in to the Folder component as `data`.

```{note}
Fragments are reusable GraphQL queries.
It also allows you to split up complex queries into smaller, easier to understand components.

In our case, even though all data is queried in `default.js` template, we split up the queries by type and place them in the relevant component.
These fragments are included back in the template as required.
This helps in maintainability as all the parts of a component, including the query, are placed together.
```

The `Folder` component now displays the title and description of the Folder itself and a list of child items.

```{note}
With the `Link` component and `_path` we can directly link between GatsbyJS pages.
```
