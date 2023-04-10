---
myst:
  html_meta:
    "description": ""
    "property=og:description": ""
    "property=og:title": ""
    "keywords": ""
---

# Pages

The core part of a website is pages.

Every site has at least one HTML page (for example a single page application or a landing page).

GatsbyJS is a static site generator, so it has the concept of pages itself.
The only difference is that they are not standard HTML documents, but internally they are React components that will be converted into static HTML at build time.

ReactJS is a good choice because it allows us to add more functionality to the page that can be dynamically generated.

If we see the file structure of our `hello-world` project, we can see that there is a `pages` folder with some JavaScript files:

```console
...
├── src
│   |...
│   └── pages
│       ├── 404.js
│       ├── index.js
│       └── page-2.js
...
```

Let us see how the `index.js` file is made.

This page is the home page of our example site.

```{literalinclude} _snippets/index_orig.js
:language: jsx
```

As we said previously, pages are not basic HTML documents, but they are React components.
You can see that React components are written in a particular syntax called `JSX`.
`JSX` allows us to mix pure JavaScript with some HTML tags.
Components are functions (or ES6 classes) that accept some data and renders some HTML.

```{note}
You can see more information in the official [ReactJS documentation](https://legacy.reactjs.org/docs/components-and-props.html).
```

## Exercise

Try to edit `index.js` file and see how the home page will change.

```{note}
Remember that with `gatsby develop` command, there is a webpack dev-server running with hot reload.
Every time we make some changes, the page will automatically update.
```

````{dropdown} Solution
:animate: fade-in-slide-down
:icon: question

```{literalinclude} _snippets/index.js
:emphasize-lines: 8,9
:language: jsx
```
````

### Components

Another thing that we can see in this file, is the use of `Link` and `Layout` components.

A component is basically a building block of our user interface.

It can be a particular "piece of interface" with a specific layout, markup or functionality.

Because components are functions, they can accept parameters (props) and return a value (an HTML-ish string) based on the given parameters.

For example the `<Link>` component is used to create links between page components where we pass a `to` property that is used to create a link to "page-2" page.

`<Layout>` component is a custom component created by the default starter that gives some basic styles to every component wrapped into it.

Let us ignore it right now.

```{note}
Routing and links are managed under the hood with [reach-router](https://reach.tech/router) library.
```

## Exercise

Create a new page and link it in the index.

````{dropdown} Solution
:animate: fade-in-slide-down
:icon: question

Create a new `ploneconf.js` file and write this code:

```{literalinclude} _snippets/ploneconf.js
:language: jsx
```
````

Components are very useful when you need to reuse a certain pattern in different pages.

Usually components are located in a `components` folder and imported where needed (like `Layout`).

```{note}
In `components/layout.js` there is an example of a custom component that adds some styles and uses other components.
```
