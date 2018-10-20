Pages
=====

Pages can be considered similar to HTML documents in a basic website as they behave that way, but here, internally
they are React components instead with way more functionality and can even be dynamically generated.

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

.. code-block:: none

  import React from 'react'
  import { Link } from 'gatsby'  

  const IndexPage = () => (
    <div>
      <h1>Gatsby Site</h1>
      <p>Welcome to your new Gatsby site.</p>
      <p>Now go build something great.</p>
      <Link to="/page-2/">Go to page 2</Link>
    </div>
  )  
  export default IndexPage

As we said previously, pages are not basic html documents, but they are React components.
You can see that React components are written in a particular syntax called `JSX` that allows to mix pure javascript with
some html tags.
Components are functions (or es6 classes) that accept some data and renders some html.

.. note:: You can see more infos in the official `ReactJS documentation <https://reactjs.org/docs/components-and-props.html>`_


Exercise
++++++++

Try to edit `index.js` file and see how the homepage will change.

.. note:: remember that with `gatsby develop` command, there is a webpack dev-server running with hot reload,
so every time we make some changes, the page will automatically update.

..  admonition:: Solution
    :class: toggle

    .. code-block:: none

      <div>
        <h1>Hi Plone people</h1>
        <p>Welcome to your new Gatsby site.</p>
        <p>Now go build something great.</p>
        <Link to="/page-2/">Go to page 2</Link>
      </div>


Components
----------

Another thing that we can see in this file, is the use of `Link` component.
A component is basically a building block of our user interface.
It can be a particular "piece of interface" with a specific layout, markup or functionality.
The fact that components are functions, they can accept parameters (props) and return a valued based on the given parameters.

For example the `<Link>` component is used to create links between page components where we pass a "to" property that
is used to create a link to "page-2" page.

.. note:: Routing and links are managed with `reach-router <https://reach.tech/router>`_ library.


Exercise
++++++++

Create a new page and link it in the index.

..  admonition:: Solution
    :class: toggle

    Create a new ploneconf.js file and weite this code:

    .. code-block:: none

        import React from 'react'
        import { Link } from 'gatsby'

        const PloneconfPage = () => (
          <div>
            <h1>Ploneconf training</h1>
            <p>That's a page created at the training.</p>
            <Link to="/">Go to the homepage</Link>
          </div>
        )

        export default PloneconfPage


Components are very useful when you need to reuse a certain pattern in different pages.
Usually components are located in a `components` folder and imported where needed.

Exercise
++++++++

Create a new component that renders the page title in a common way, and use it in every page.

..  admonition:: Solution
    :class: toggle

    Create `components` folder and a new file `header.js`

    .. code-block:: none

        import React from 'react'
      
        export default Header = ({label}) => (
          <div
            className="header"
            style={{
                backgroundColor: blue;
                color: rgb(255, 255, 255);
                padding: 1em;
                fontSize: 72px;
                textAlign: center;
            }}
          >
            {label}
          </div>
        )

    Then we need to import `Header` component in our pages (index.js for example), and use it.

    .. code-block:: none
      
        ...
        import Header from '../components/header';
        
        const PloneconfPage = () => (
          <div>
            <Header label="Ploneconf Tokyo 2018" />
            <h1>Welcome to Ploneconf trainings</h1>
            <p>That's a page created at the training.</p>
            <Link to="/">Go to the homepage</Link>
          </div>
        )
    