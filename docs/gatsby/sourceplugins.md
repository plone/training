---
myst:
  html_meta:
    "description": ""
    "property=og:description": ""
    "property=og:title": ""
    "keywords": ""
---

# Source plugins

Now that we learned how to create pages and access dynamic data with GraphQL, we can start fetching some data from external sources.

Source plugins are the tools that can handle this job.

Every plugin is specialized in getting data from a different source.

```{note}
There are a lot of plugins for almost every need.
You can find a complete list of plugins on [GatsbyJS official website](https://www.gatsbyjs.com/plugins/).
```

Let us start with a basic one, `gatsby-source-filesystem`: a plugin that transforms files into GraphQL nodes.

```none
npm install --save gatsby-source-filesystem
```

After that, we need to enable the plugin in our project.
To do this, we need to add it into `gatsby-config.js` file.

```{literalinclude} _snippets/gatsby-config.js
:emphasize-lines: 8-12
:language: none
:lines: 1-13,15
```

Now restart the development server.

If we open `GraphiQL` page, we will see new possible queries.

## Exercise

Create a new page called "files-list.js" that displays a list of all files with some informations (path, size, extension) found with some query.

````{dropdown} Solution
:animate: fade-in-slide-down
:icon: question

```{literalinclude} _snippets/files-list.js
:language: jsx
```
````
