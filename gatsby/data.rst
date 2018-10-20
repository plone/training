Data
====

You can create entire sites only with static pages, but the power of Gatsby is how easily 
we could get data from several sources and use it to dynamically generate pages.

As we said, data could be pulled from different sources: files (markdown, csv, json), databases, api, cms.
Gatsby’s data layer lets you pull data from these (and any other source) directly into your components.

GraphQL
-------

GraphQL is a query language developed by Facebook that allows to create api endpoints that can be queried with a particular syntax that describes exactly what kind of data we need (only desired values) and it returns only that data.

.. note::  For more detailed information, you could read the `official documentation <https://graphql.org/>`_ and `tutorial <https://www.howtographql.com/>`_.

Gatsby uses GraphQL to expose stored data in a common way, and allows page components to access to it and retrieve only the desired information.

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

As we'll see in the next chapters, there are different configuration files in every project, that allows us to customize different aspects of the site.
There is a file (gatsby-config.js) where we can set some general site metadata that can be queried with GraphQL and used in pages.

For example, if we need to show the sitename in every page, we don't want to write it in every page, because it can change in the future.
We could also read it from a common place and use it in our pages.

If we open `gatsby-config.js`, we'll se something like this:

.. code-block:: none

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

If we try to go to GraphiQL page, we could try to access this information with the following query:

.. code-block:: none

    query {
        site {
            siteMetadata {
                title
            }
        }
    }

.. note:: `query` is a keyword that means that we are requesting data. If we need to modify the data, we need to use `mutation`.

Now that we have seen how to query some data from GraphQL, let's insert this in our pages.

Change our index.js page like this:

.. code-block:: none
    :emphasize-lines: 3,5,8,14-22

    import React from "react"
    import Header from '../components/header';
    import { graphql } from "gatsby"

    export default ({ data }) => (
        <div>
            <Header label="Ploneconf Tokyo 2018" />
            <h3>About {data.site.siteMetadata.title}</h3>
            <p>Welcome to your new Gatsby site.</p>
            <p>Now go build something great.</p>
            <Link to="/page-2/">Go to page 2</Link>
        </div>
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

As you can see, first of all, we imported a new module `graphql`. This is used on the bottom of the file,
to generate our query.

When we add a GraphQL query in our component, the result is automatically passed to the component as a prop called `data`.

In that prop, we have the required informations, in the same data structure of the query.

This method could be used in every page component, but if we break up our layout in several pieces (components) like we do in the previous chapter with the header,
we need to use a different approach using `StaticQuery` components.

This is very useful because we can't expose a GraphQL query in components that are not page components, and with these `StaticQuery` components
we could avoid passing useless props through the components hierarchy that are only needed by a certain leaf.

.. note:: passing props to too many levels is called `props drilling` in ReactJS, and is always better avoid it.

For example, if we want to access some data in a component like our `Header`, we need to use this syntax:

.. code-block:: none
    :emphasize-lines: 3,5,8,14-22

    import React from 'react'
    import { StaticQuery, Link, graphql } from "gatsby"

    export default Header = () => (
        <StaticQuery
            query={
                graphql`
                    query {
                        site {
                            siteMetadata {
                                title
                            }
                        }
                    }
                `
            }
            render={data => (
                <div className="header">
                    <h1>{data.site.siteMetadata.title}</h1>
                </div>
            )}
        </StaticQuery>
    )

