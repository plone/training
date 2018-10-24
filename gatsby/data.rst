Data
====

If we want, we could create entire sites only with static pages, but with GatsbyJS we can also get data from external sources and use it to dynamically generate pages.

Data could be pulled from different sources: files (markdown, csv, json), databases, api, CMS.

GatsbyJS data layer lets you pull data from these (and any other source) directly into your page components with GraphQL.

GraphQL
-------

GraphQL is a query language developed by Facebook. It allows to create api endpoints that can be queried with a particular syntax that describes exactly what kind of data we need (only desired values) and it returns only that data.

.. note::  For more detailed information, you could read the `official documentation <https://graphql.org/>`_ and `tutorial <https://www.howtographql.com/>`_.

GatsbyJS uses GraphQL to expose stored data in a common way, and allows page components to access to it and retrieve only the desired informations.

GatsbyJS uses GraphQL also to expose some common informations (site metadata for example) and to show what plugins are installed.

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

**Query builder** is where we are going to write our queries. Queries (and responses) are json objects, and that object will be returned as a response, filled with required data.

**Results** is the section where the response is showed after the query.

**Schema explorer** is where to inspect what is the structure of the data that we can query.

Site metadata
-------------

There are different configuration files in a GatsbyJS project, that allows us to customize different aspects of the site.

There is a file called `gatsby-config.js` where we can set some site metadata that can be queried with GraphQL and used in pages.

One metadata that we could set, is the site title.

If we look at the demo site, we could see that there is an header with some text. This is the site title, read from the metadata config (we will see later how to read it in a component).

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

`siteMetadata` is the section that we need to focus on. And the value of `title` is exactly what we see in the header.

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

Now that we have seen how to query some data from GraphQL, let's see how use that infos in components.

There are two ways to inject data into components depending on whether the component is a page component (index.js file), or not (Layout component).

Let's start with the first one: we need to change our index.js page like this:

.. code-block:: none
    :emphasize-lines: 1,5,8,14-22

    import { graphql } from "gatsby"

    export default ({ data }) => (
        ...
        <h4>This is the site title: {data.site.siteMetadata.title}</h3>
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

First of all, we imported a new module `graphql`. This is used on the bottom of the file, to generate the query.

When we add a GraphQL query in our page component, the result is passed to the component as property called `data`.

In that property, we have the result of the query (with the same data structure).

.. note::
    To see what informations are in `data` property, try to put a ``console.log(data)`` in the component.

    To do that, we need to change the returned value of the arrow function, because () automatically returns everything is inside them, and we wants to add some logic before returning the value. So the change should be like this:

    .. code-block:: none

        export default ({ data }) => {
            console.log(data);
            return (
                ...
                <h4>This is the site title: {data.site.siteMetadata.title}</h3>
                ...
            )
        
        }

This method could be used in every page component, but if we break up our layout in several pieces (components), we need to use a different approach using "StaticQuery" components.

This is very useful because we can't expose a GraphQL query in components that are not page components, and with these "StaticQuery" components, we could avoid passing useless properties through the components hierarchy that are only needed by a certain leaf.

.. note:: Passing props to too many levels is called `props drilling` in ReactJS, and is always better to avoid it.

If we look at `Layout` component in ``components/layout.js`` file, we could see an example of `StaticQuery` to read the site title:

.. code-block:: none

    import { StaticQuery, graphql } from 'gatsby'
    ...

    const Layout = ({ children }) => (
        <StaticQuery
            query={graphql`
            query SiteTitleQuery {
                site {
                siteMetadata {
                    title
                }
                }
            }
            `}
            render={data => (
                ...
                <Header siteTitle={data.site.siteMetadata.title} />
                ...
            )}
        />
    )

In this case, the query is an attribute of the <StaticQuery> tag.

.. note::
    StaticQuery is different from standard components that we have seen before, because it uses a ReactJS pattern called `render props <https://reactjs.org/docs/render-props.html>`_.

    This pattern is used when there are different components of the interface that needs the same piece of code/logic and we do not want to duplicate the same code.

    A component that implements that pattern, has some logic hidden inside (for example how to perform a GraphQL query) and takes a function (as `render` property) that expose some data (the result of the query) and returns a React element and calls it instead of implementing its own render logic.