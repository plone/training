================================
RequireJS And JavaScript Modules
================================

One of the great new features, Plone 5 gives us, is the ability to define and use JavaScript modules.

Most serious programming languages provide the concept of namespaces and module dependencies, like Python's :keyword:`import` mechanism.
Python code would be unmanageable, if we'd rely on the existence of global variables and objects in our own scripts.

But JavaScript doesn't have any concept for declaring dependencies.
Only the new and finalized ECMAScript 6 (ES6) standard finally comes with a module definition system (actually directly inspired by RequireJS and CommonJS), along other great features like proper variable scoping.

In Plone, we use `RequireJS <http://requirejs.org>`_ as a framework to define and load modules.

RequireJS is an implementation of the `Asynchronous Module Definition API <https://github.com/amdjs/amdjs-api/blob/master/AMD.md>`_.
The module definition and loading standard of CommonJS is used by NodeJS.
RequireJS adds the ability to load modules asynchronously, which can be better for performance.
The CommonJS module loading syntax can also be used in RequireJS.

But the main point why Plone uses RequireJS is, that there is a JavaScript based compiler, which allows us to build bundles (a combined, optimized and minified form with all dependencies) Through-The-Web.
RequireJS and CommonJS are also forward compatible with ES6's module definition standard.

Finally we can use JavaScript in Plone like it is a proper programming language!
No need to depend on the existence of global variables and a strict order, in which scripts have to be loaded.
You can still use legacy-style JavaScript, but Plone encourages you to enter the modern world of JavaScript development.


Defining A module
=================

In the past years, a common pattern of defining anonymous function calls has evolved.
This allows to better scope variables and not clutter the global namespace.
The pattern is discussed in depth at `JavaScript Module Pattern: In-Depth <http://www.adequatelygood.com/JavaScript-Module-Pattern-In-Depth.html>`_ and basically comes down to the following Pattern:

.. code-block:: javascript

    (function ($, _) {
        // now have access to globals jQuery (as $) and underscore (as _) in this code.
    }(jQuery, underscore));


If your code should be reused like a library, you can define a module export.

.. code-block:: javascript

    var my_module = (function ($, _) {
        var ret = {};
        ret.my_method = function () {
            // do something
        }
        return ret;
    }(jQuery, underscore));


RequireJS extends this pattern and removes the necessity for globals to refer to other modules.

In RequireJS, you're wrapping your code like this:

.. code-block:: javascript

    define(["jquery", "underscore"], function($, _) {
        // now have access to jQuery (as $) and underscore (as _), both defined as modules in the RequireJS configuration.
        var ret = {};
        ret.my_method = function () {
            // do something
        }
        return ret;
    });

No need for any globals anymore (except for the ``define`` and ``require`` methods)!

Also note, that the code within the RequireJS define wrapper is exactly the same as in the module pattern example above.
Using RequireJS doesn't mean, you have to rewrite everything.
It's about modularizing code.

To be able to use the defined module somewhere else, you need to be able to reference it by a module id.
You can pass it as very first argument to the ``define`` function, but you might better do that in the RequireJS configuration.

If you don't do it at all, it gets automatically assigned the name of the file.

For example, let's assume a project structure like follows and the ``define`` example from above living in a file called ``my_module.js``::

    index.html
    require.js
    my_project/
            |___main.js
            |___app/
                  |___/my_module.js

Let's do the RequireJS configuration in :file:`main.js` and use that as main entry point also to finally let something happen:

.. code-block:: javascript

    require.config({
      baseUrl: "my_project/",
      paths: {
          "app": "app/"
      }
    });
    require(['app/my_module'], function (my_module) {
        my_module.my_method();
    })


You can use your defined module as a dependency in another ``define`` module definition - if you
want to run some non-reusable code - as a dependency in a ``require`` call.

While you have to return a module export in ``define``, you don't need that for ``require``.
``require`` corresponds to the first form of the module pattern explained above.

When using in the browser (and not in NodeJS, for example), we have to include an entry point as script tag in our HTML markup:

.. code-block:: xml

    <script src="require.js"></script>
    <script src="my_module/main.js"></script>

Alternatively, you can define a script as main entry point in RequireJS as data attribute on the script tag, which loads require.js.
In that case, you could omit the configuration, because the entry point script is used as ``baseUrl``, if nothing else is defined:

.. code-block:: xml

    <script data-main="my_project/main.js" src="require.js"></script>


More information
================

More on RequireJS' API and how to include legacy code,
which doesn't use the ``define`` module definition pattern, see the `RequireJS API documentation <http://requirejs.org/docs/api.html#define>`_.
