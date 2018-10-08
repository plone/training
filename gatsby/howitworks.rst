How it works
============

  .. image:: ./_static/gatsby-schema.png
    :scale: 50%

There are basically three steps:

1) Fetch data
-------------
You can configure Gatsby to fetch data from different sources like local files (csv, json, ecc), Markdown files or some remote
api/cms.

This is done with `source plugins`. Community created `several plugins <https://www.gatsbyjs.org/plugins/>`_ that can fetch data from various sources.

2) Build
--------
In this step there are three main technologies involved: GraphQL, React and Webpack.
GraphQL is a query language used to create apis where you can create queries that generates exactly the data that you need (and only the data that you need).
It is used to store and serve fetched data in a common and easily to access way.

The second component is ReactJS.
React is a javascript library that allows to create powerful and reusable interfaces.
It works with a basic rule: everything is a component, and every interface is built with a set of components.
Components let you split the UI into independent, reusable pieces, and think about each piece in isolation.
Conceptually, components are like JavaScript functions. They accept arbitrary inputs (called “props”) and return React elements describing what should appear on the screen.

In Gatsby all pages are React components that takes in input some data (if needed) from GraphQL and displays some informations.

The last component is Webpack.
Webpack is a module bundler.
It is the tool that takes all the resources (pages, stylesheets, images and other dependencies), combine
them together and generate a set of static pages that will be the final Gatsby site.
In development mode, it exposes the builded site to a certain http port (to see what we are developing) and rebuild it
everytime we create/edit/delete a file in the source-code.

3) Deploy
---------
The output of Gatsby is a simple set of static resources: html, css and js files, so you can deploy them basically evarywhere (Amazon S3, Netlify, GitHub pages, Apache, Surge.sh, etc)