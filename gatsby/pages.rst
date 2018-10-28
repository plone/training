Pages
=====

The core part of a website are pages.

Every site has at least one HTML page (for example a single page application or a landing page).

GatsbyJS is a static site generator, so it has the concept of pages itself.

The only difference is that they are not standard HTML documents, but internally they are React components that will be converted into static HTML at build time.

ReactJS is a good choice because it allows us to add more functionalities to the page that can be dynamically generated.

If we see the file structure of our `hello-world` project, we can see that there is a `pages` folder with some JavaScript files:

.. code-block:: console

    ...
    ├── src
    │   |...
    │   └── pages
    │       ├── 404.js
    │       ├── index.js
    │       └── page-2.js
    ...

Let's see how is made ``index.js`` file. This page is the homepage of our example site.

.. literalinclude:: _snippets/index_orig.js
  :language: jsx

As we said previously, pages are not basic HTML documents, but they are React components.

You can see that React components are written in a particular syntax called ``JSX``.

``JSX`` allows us to mix pure JavaScript with some HTML tags.

Components are functions (or ES6 classes) that accept some data and renders some HTML.

.. note::

  You can see moreinformations in the official `ReactJS documentation <https://reactjs.org/docs/components-and-props.HTML>`_


Exercise
++++++++

Try to edit ``index.js`` file and see how the homepage will change.

.. note::

  Remember that with ``gatsby develop`` command, there is a webpack dev-server running with hot reload.
  
  Every time we make some changes, the page will automatically update.

..  admonition:: Solution
    :class: toggle

    .. literalinclude:: _snippets/index.js
      :language: jsx
      :emphasize-lines: 8,9

Components
----------

Another thing that we can see in this file, is the use of ``Link`` and ``Layout`` components.

A component is basically a building block of our user interface.

It can be a particular "piece of interface" with a specific layout, markup or functionality.

Because components are functions, they can accept parameters (props) and return a value (an HTML-ish string) based on the given parameters.

For example the ``<Link>`` component is used to create links between page components where we pass a ``to`` property that is used to create a link to "page-2" page.

``<Layout>`` component is a custom component created by the default starter that gives some basic styles to every component wrapped into it.

Let's ignore it right now.

.. note::

  Routing and links are managed under the hood with `reach-router <https://reach.tech/router>`_ library.


Exercise
++++++++

Create a new page and link it in the index.

..  admonition:: Solution
    :class: toggle

    Create a new ``ploneconf.js`` file and write this code:

    .. literalinclude:: _snippets/ploneconf.js
      :language: jsx

Components are very useful when you need to reuse a certain pattern in different pages.

Usually components are located in a ``components`` folder and imported where needed (like ``Layout``).

.. note::
  
  In ``components/layout.js`` there is an example of a custom component that adds some styles and uses other components.
