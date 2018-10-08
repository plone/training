Data
====

You can create entire sites only with static pages, but the power of Gatsby is how easily 
we could get data from several sources and use it to dynamically generate pages.

As we said, data could be pulled from different sources: files (markdown, csv, json), databases, api, cms.
Gatsby’s data layer lets you pull data from these (and any other source) directly into your components.

GraphQL
-------

GraphQL is a query language developed by Facebook that allows to create api endpoints that can be queried with a particular syntax that describes exactly what kind of data we need (only desired values) and it returns only that data.

.. note::  For more detailed informations, you could read the `official documentation <https://graphql.org/>`_ and `tutorial <https://www.howtographql.com/>`_.

Gatsby uses GraphQL to expose stored data in a common way, and allows page components to access to it and retrieve only the desired informations.

Not only fetched data are stored in GraphQL. Gatsby uses GraphQL data also to expose some common informations (site metadata) and to show what plugins are installed.

GraphQL has a powerful tool called `GraphiQL` that helps to inspect what data can be queried and to test the queries.
If we inspect the console output when we start development server, we can see these lines:

.. code-block:: console
    
    View GraphiQL, an in-browser IDE, to explore your site's data and schema

        http://localhost:8000/___graphql


Now let's try to open `http://localhost:8000/___graphql <http://localhost:8000/___graphql>`_ and see how it works.

  .. image:: ./_static/graphiql.png
    :scale: 50%

There are three columns:

- Query builder
- Results
- Schema explorer

Site metadata
-------------

As we'll see in the next chapters, there are several configuration files in every project, that allows us to customize different aspects of the site.
There is a file (gatsby-config.js) where we can set some general site metadata that can be queried with GraphQL and used in pages.

For example, if we need to show the sitename in every page, we don't want to write it in every page, because it can change in the future.
We could also read it from a common place and use it in our pages.

If we open `gatsby-config.js`, we'll se something like this:

.. code-block:: json

    module.exports = {
        siteMetadata: {
            title: 'Gatsby Default Starter',
        },
        plugins: [
            'gatsby-plugin-react-helmet',
            {
            resolve: `gatsby-plugin-manifest`,
            options: {
                name: 'gatsby-starter-default',
                short_name: 'starter',
                start_url: '/',
                background_color: '#663399',
                theme_color: '#663399',
                display: 'minimal-ui',
                icon: 'src/images/gatsby-icon.png', // This path is relative to the root of the site.
            },
            },
            'gatsby-plugin-offline',
        ],
    }

`siteMetadata` is the section that we need to focus on.


Exercise
++++++++

Read this value from GraphQL and insert it our pages. And then try to change the title.

Hints:

First of all, try to query the title in GraphiQL tool, and then use it in our component.
That's the syntax to use GraphQL queries in a page component:

.. code-block:: none

    ...
    import { graphql } from "gatsby"
    ...

    export default ({ data }) => (
        ...
        <h1>{data.site.siteMetadata.title}</h1>
        ...
    )

    export const query = graphql`
        query {
            site {
            siteMetadata {
                title
            }
            }
        }
    `