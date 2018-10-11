Source plugins
==============

Now that we learned how to create pages and access dynamic data with GraphQL, we can start fetching some data from external sources.

Source plugins are the tools that can do this job. Every plugin is specialized in getting data from a different source.

..note :: There are a lot of plugins for almost every need. In GatsbyJS website, you can find a complete list of `official plugins <https://www.gatsbyjs.org/plugins/>`_.

Let's start with a basic one: `gatsby-source-filesystem` a plugin that transforms files in GraphQL nodes.

.. code-block:: none
  
    npm install --save gatsby-source-filesystem

After that, we need to enable the plugin in our project. To do this, we need to add it into `gatsby-config.js` file.

.. code-block:: none

  ...
  plugins: [
    {
      resolve: `gatsby-source-filesystem`,
      options: {
        name: `src`,
        path: `${__dirname}/src/`,
      },
    }
  ]
  ...

Now restart the development server. If you open GraphiQL page, you'll see new possible queries.

Exercise
++++++++

Create a new page called "files-list.js" that displays a list of all files with some informations (path, size, extension) found with some query.

..  admonition:: Solution
    :class: toggle

    .. code-block:: none

      import React from "react"
      import { graphql } from "gatsby"
      import Header from '../components/header';

      export default ({ data }) => {
        return (
          <div>
            <Header />
            <h1>Here is a list of files</h1>
            <table>
              <thead>
                <tr>
                  <th>relativePath</th>
                  <th>prettySize</th>
                  <th>extension</th>
                  <th>birthTime</th>
                </tr>
              </thead>
              <tbody>
                {data.allFile.edges.map(({ node }, index) => (
                  <tr key={index}>
                    <td>{node.relativePath}</td>
                    <td>{node.prettySize}</td>
                    <td>{node.extension}</td>
                    <td>{node.birthTime}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )
      }

      export const query = graphql`
        query {
          allFile {
            edges {
              node {
                relativePath
                prettySize
                extension
                birthTime(fromNow: true)
              }
            }
          }
        }
      `