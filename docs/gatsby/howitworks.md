---
myst:
  html_meta:
    "description": ""
    "property=og:description": ""
    "property=og:title": ""
    "keywords": ""
---

# How it works

There are basically three steps:

## 1) Fetch data

You can configure GatsbyJS to fetch data from different sources like headless CMSs, SaaS services, APIs, databases, your file system and more.

This is done with `source plugins`.

The active GatsbyJS community has [several plugins](https://www.gatsbyjs.com/plugins/) that can fetch data from various sources.

## 2) Build

In this step there are three main technologies involved: GraphQL, React and Webpack.

GraphQL is a query language used to create APIs where you can create queries that generates exactly the data that you need (and only the data that you need).
It is used to store and serve fetched data in a common and easily to access way.

The second component is ReactJS: a JavaScript library that allows to create powerful and reusable interfaces.

It works with a basic rule: everything is a component, and every interface is built with a set of components.
Components let you split the UI into independent, reusable pieces, and think about each piece in isolation.

Conceptually, components are like JavaScript functions. They accept arbitrary inputs (called "props") and return React elements describing what should appear on the screen.

In GatsbyJS all pages are React components that receive data (if needed) from GraphQL and display some information.

It also is very flexible in its project structure allowing you to choose the way you want it to be, libraries you want to use, methods of styling and much more.

The last component is Webpack: a module bundler.

It is a tool that takes all the resources (pages, style sheets, images and other dependencies), combines them together, and generates a set of static pages that will be the final GatsbyJS site.

In development mode, it exposes the built site to a certain HTTP port (to see what we are developing) and rebuild it every time we create/edit/delete a file in the source code.

## 3) Deploy

The output of GatsbyJS is a set of static resources: HTML, CSS and JavaScript files.
You can deploy them wherever you deploy static files (Amazon S3, Netlify, GitHub pages, Apache, [Surge.sh](https://surge.sh/), and so on).
