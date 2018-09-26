Pages
=====

Pages are the basic components of a GatsbyJS site.

If we see the file structure of our `hello-world` project, we can see that there is a `pages` folder with some js files:

.. code-block:: console

    ...
    ├── src
    │   |...
    │   └── pages
    │       ├── 404.js
    │       ├── index.js
    │       └── page-2.js
    ...

Let's see how is made `index.js` file. This page is the homepage of our example site.

.. code-block:: js

    import React from 'react'
    import { Link } from 'gatsby'

    import Layout from '../components/layout'

    const IndexPage = () => (
    <Layout>
        <h1>Hi Plone people</h1>
        <p>Welcome to your new Gatsby site.</p>
        <p>Now go build something great.</p>
        <Link to="/page-2/">Go to page 2</Link>
    </Layout>
    )

    export default IndexPage

As you can see, pages are not basic html documents, but they are React components.

TODO: intro to reactjs

In develop mode, the pages are converted in html files and served by webpack.
Using webpack has several advantages in development.
One of the most important is `hot reloading`: source files are constantly "watched" when the development server is running,
and when they change, the application will be re-built and your changes will be immediately shown in the browser
withot manually reloading it at every save.

Another thing that we can see in this file, is the use of `Link` component.
This is a React component that Gatsby uses to create links between page components.
When building, it "translates" these components into proper <a> tags.
Routing is managed with reach-router library.

Exercise
++++++++

- Try to edit `index.js` file and see how the homepage will update without a refresh.
- Create a new page and link it in the index
