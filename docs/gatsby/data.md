---
myst:
  html_meta:
    "description": ""
    "property=og:description": ""
    "property=og:title": ""
    "keywords": ""
---

# Data

If we want, we could create entire sites only with static pages, but with GatsbyJS we can also get data from external sources and use it to dynamically generate pages.

Data could be pulled from different sources: files (Markdown, CSV, JSON), databases, API, CMS.

The GatsbyJS data layer lets you pull data from these (and any other source) directly into your page components with GraphQL.

## GraphQL

GraphQL is a query language developed by Facebook.
It allows a developer to create API endpoints that can be queried with a particular syntax that describes exactly what kind of data we need (only desired values) and it returns only that data.

```{note}
For more detailed information, you could read the [official documentation](https://graphql.org/).
And the [tutorial](https://www.howtographql.com/).
```

GatsbyJS uses GraphQL to expose stored data in a common way, allowing page components to access the data and returning only the desired information.

GatsbyJS uses GraphQL also to expose some common information (site metadata for example) and to show what plugins are installed.

GraphQL has a powerful tool called `GraphiQL` that helps to inspect what data can be queried and to test the queries.

If we inspect the console output when we start development server, we can see these lines:

```console
View GraphiQL, an in-browser IDE, to explore your site's data and schema

    http://localhost:8000/___graphql
```

Now let us try to open [http://localhost:8000/\_\_\_graphql](http://localhost:8000/___graphql) and see how it works.

> ```{image} ./_static/graphiql.png
> :scale: 50%
> ```

There are three columns:

- Query builder
- Results
- Schema explorer

**Query builder** is where we are going to write our queries.
Queries (and responses) are JSON objects, and that object will be returned as a response, filled with required data.

**Results** is the section where the response is shown after the query.

**Schema explorer** is where to inspect the structure of the data that we can query.

## Site metadata

There are different configuration files in a GatsbyJS project that allow us to customize different aspects of the site.

There is a file called `gatsby-config.js` where we can set some site metadata that can be queried with GraphQL and used in pages.

One metadata that we could set is the site title.

If we look at the demo site, we could see that there is a header with some text.

This is the site title, read from the metadata config (we will see later how to read it in a component).

If we open `gatsby-config.js`, we'll se something like this:

```{literalinclude} _snippets/gatsby-config.js
:emphasize-lines: 2-4
:language: none
:lines: 1-5
```

`siteMetadata` is the section that we need to focus on.
The value of `title` is exactly what we see in the header.

If we try to go to GraphiQL page, we could try to access this information with the following query:

```none
query {
    site {
        siteMetadata {
            title
        }
    }
}
```

```{note}
`query` is a keyword that means that we are requesting data.
If we need to modify the data, we need to use `mutation`.
```

Now that we have seen how to query some data from GraphQL, let us see how to use that information in components.

There are two ways to inject data into components depending on whether the component is a page component (`index.js` file), or not (Layout component).

Let us start with the first one.
We need to change our `index.js` page like this:

```{literalinclude} _snippets/index_graphql.js
:emphasize-lines: 3,7,10,17-25
:language: jsx
```

First of all, we imported a new module `graphql`.
This is used on the bottom of the file to generate the query. Note the use of backticks around the query definition.

Then we declare in `IndexPage` that we are using `data`, the results of the `graphql` query.

When we add a GraphQL query in our page component, the result is passed to the component as a property called `data`.
In that property, we have the result of the query (with the same data structure).

````{note}
To see what information are in the `data` property, try to put a `console.log(data)` in the component.

To do that, we need to change the returned value of the arrow function, because `()` automatically returns everything inside them, and we want to add some logic before returning the value.

The change should be like this:

```jsx
export default ({ data }) => {
    console.log(data);
    return (
        //...
        <h4>This is the site title: {data.site.siteMetadata.title}</h4>
        //...
    )

}
```
````

This method could be used in every page component, but if we break up our layout in several pieces (components), we need to use a different approach using a wrapper component provided by GatsbyJS called `StaticQuery`.
This is very useful because we cannot expose a GraphQL query in components that are not page components.
With these "StaticQuery" components, we could avoid passing useless properties through the components hierarchy that are only needed by a certain leaf.

```{note}
In ReactJS, passing props to too many levels is called [prop drilling](https://kentcdodds.com/blog/prop-drilling/).
It is always better to avoid it, if we can.
```

If we look at the `Layout` component in `components/layout.js` file, we could see an example of `StaticQuery` to read the site title:

```jsx
import { StaticQuery, graphql } from 'gatsby'
//...

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
            //...
            <Header siteTitle={data.site.siteMetadata.title} />
            //...
        )}
    />
)
```

In this case, the query is an attribute of the `<StaticQuery>` tag.

```{note}
StaticQuery is different from standard components that we have seen before, because it uses a ReactJS pattern called [render props](https://legacy.reactjs.org/docs/render-props.html).

This pattern is used when there are different components of the interface that need the same piece of code/logic and we do not want to duplicate the same code.

A component that implements that pattern has some logic hidden inside (for example how to perform a GraphQL query).
It takes a function (as `render` property) that expose some data (the result of the query) and returns a React element that could use that data.
```
