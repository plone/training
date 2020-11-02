What is a Volto addon?
======================

Basic anatomy of Volto
----------------------

Assuming you're familiar already with Volto and how it loads, you'll already
know that Volto provides Server Side Rendering, that is, when you load a Volto
page you'll first load an HTML page, in theory identical in its markup to the
final desired output of that page. This HTML page will also load a bunch of JS
files which, when loaded, finally bring Volto to run as a Single Page
Application in the browser.

You'll also probably know that Volto is a React app which is transpiled from
JSX and ECMAScript 6 using Babel, then bundled, chunked and minified by
Webpack.

For this most basic infrastructure setup, Volto relies on the Razzle library,
which provides an extensible Webpack SSR-enabled setup with convenient split of
server/client entrypoints and dual server/client Hot-Module-Reload.

The first Webpack entrypoint, the Volto server, is powered by ExpressJs.
It runs the Volto React code and components, then sends them to the browser as
a normal HTML page. It also proxies some of the Plone resources, such as files
and images.

Note: For advanced use-cases, it's possible to hitch on Volto's Express
server and run additional applications, such as proxies for internal services.

When generating the client-side files, Webpack will need to know how to find,
how to load and, potentially, how to mutate (compress, transpile, minify, etc)
the files that represent the code and resources of the Volto, Volto project and
Volto addons. The base is provided by Razzle, with instructions for Webpack to
transpile .js and .jsx files with Babel, load .less files, css, images and
svgs. For any other file type (for example .scss, .ts, etc) you'll have to
enhance the Razzle configuration with the appropriate Webpack loader. Check if
there's already a Razzle plugin, for example ``.scss`` support can be simply
added by adding ``scss`` to the razzle.config.js ``plugins`` list.

To summarize: Volto runs as a Single Page Application packaged by Webpack,
which uses loaders such as Babel (for ES6 js/jsx files) or less-loader for
``.less`` files.

Bootstrap a Volto project
-------------------------

Although it's possible to run Volto with npm as the Node package manager, the
community has settled, for now, to the Yarn Classic (v1.x) package manager.
Yarn is used as an installer, to run scripts but also as a "virtual
environment" by using its workspaces feature. Typically you'll start Volto
applications with ``yarn start``, use ``yarn test`` but you can also integrate
the mrs-developer library and run ``yarn missdev`` to do tasks similar to
mr.developer in Buildout projects.

To bootstrap a new Volto project, you can use either create-volto-app:

.. code-block:: bash

    npm -g i @plone/create-volto-app

or, using the new yeoman-based generator-volto:

.. code-block:: bash
    npm install -g yo
    npm install -g @plone/generator-volto
    yo @plone/volto myvoltoproject

The yo-based generator partially integrates addons (it can generate
a package.json with addons and workspaces already specified).

Addons - a first look
---------------------

Although still in their infancy, 2020 is the year of Volto addons. The addons
configuration mechanism was added to Volto and with it many open source generic
addons were published. The collective/awesome-volto repo tracks most of them.

An addon can be anything that a Volto project can be. They can:

- provide additional views and blocks
- override or extend Volto's builtin views, blocks, settings
- shadow Volto's (or another addon's) modules
- register custom routes
- provide custom Redux actions and reducers
- register custom Express middleware for Volto's server process
- tweak Volto's webpak configuration
- load Razzle webpack plugins
- and they can even provide a custom theme, just like the Volto project does.

Basically, anything that a Volto project can do in terms of extending Volto
with new functionality, an addon can do as well.

In implementation, the Volto addons are JS npm packages with an additional
feature: they provide helper functions that can mutate Volto's configuration
registry. These are the "addon configuration loader". To make things easy,
addons should be distributed as source, non transpiled. Their ``main`` entry in
``package.json`` should point to ``src/index.js``, which should be an ES6
module with a default export, the addon configuration loader:

.. code-block:: jsx

    export default (config) => {
        return config
    };

The ``config`` object that is passed is the Volto ``configuration registry``,
the singleton module referenced throughout the Volto and projects as
``~/config``. The addon can mutate the properties of config, such as
``settings``, ``blocks``, ``views``, or its dedicated ``addonRoutes`` and
``addonReducers``.

Note: the addon configuration loading mechanism is inspired by Razzle, which
uses a similar get the config, return the config pass-through mechanism for it
plugins.

The resolution order is: Volto declares the initial configuration, it applies
the addon configuration and then the project configuration is loaded last,
enabling the project to override any configuration.

So: ``Volto => addons => project``.

To load an addon, the project needs to specify the addon in its project.json
``addons`` key:

.. code-block:: js

    ...,
    "addons": [
        "volto-slate:asDefault,somethingElse",
        "@eeacms/volto-object-widget",
    ],
    ...

Notice that the addons should be named by their package name, plus any
additional optional configuration loaders.

Bootstrap an addon
------------------

Let's start creating an addon. We'll create a new package:
``@plone/datatable-tutorial``. Inside your Volto project, bootstrap the addon
by running:

.. code-block:: shell

    mkdir -p src/addons/datatable-tutorial
    cd datatable-tutorial
    npm init

Note: the namespace ``@plone`` is not required and it can be anything. We're
using namespaces because in practice you'll probably want to group your addons
under a common namespace. There is no shared addon namespace right now for
Volto addons.

Use ``@plone/datatable-tutorial`` as the package name and ``src/index.js`` as
the package main. Create ``src/index.js`` with the following content:

.. code-block: jsx

    export default (config) => config;

Back to the project, you should edit jsconfig.json and add your addon:

.. code-block: json

    {
        "compilerOptions": {
            "baseUrl": "src",
            "paths": {
                "@plone/datatable-tutorial": [
                    "addons/datatable-tutorial/src"
                ],
            }
        }
    }

You can also immediately push the package to Github then use mrs-developer to
manage the package and jsconfig.json changes. Add to mrs-developer.json:

.. code-block: json

    "datatable-tutorial": {
        "url": "https://github.com/collective/datatable-tutorial.git",
        "path": "src",
        "package": "@plone/datatable-tutorial",
        "branch": "master"
    }

Then run ``yarn develop``, which will bring the package in ``src/addons`` and
adjust ``jsconfig.json``.


When developing addons that have third-party depedencies, you need to add the
addon as a workspace to the Volto project. Change the Volto project's
package.json to something like:

.. code-block: json

    "private": "true",
    "workspaces": [
        "src/addons/datatable-tutorial"
    ],

To add dependencies to the addon you need to add them via the workspaces root,
by running something like:

.. code-block: sh

    yarn workspaces info
    yarn workspace @plone/datatable-tutorial add react-color


Note: there are several addon templates, such as
https://github.com/nzambello/voltocli or
https://github.com/eea/volto-addon-template

While the community settles on what constitutes best practice for an addon's
essential files, you should be aware that an addon is just a simple
package.json and an index.js file. Everything else it's up to you.

Glossary
--------

- addons: a JS package that integrates with Volto's configuration registry
- addon configuration loader: a function with signature ``config => config``.
- Razzle: a tool that simplifies SPA and SSR configuration for ReactJS
- Webpack: we tool that loads and bundles code and web resources using loaders
- Babeljs: a Javascript compiler that "transpiles" newer standards JS to
  something that any browser can load.
