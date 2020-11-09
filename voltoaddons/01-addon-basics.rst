Basics of Volto addons development
==================================

Volto: an overview
------------------

One of the basic aspects of Volto is that it provides Server-Side Rendering
(SSR): when you first load a Volto page you'll get HTML code identical in its
markup to the React-rendered output of that page. The HTML page will also load
a bunch of JS files which, when loaded, finally bring Volto to run as a Single
Page Application (SPA) in the browser.

Another basic fact, Volto is a React app which is transpiled from JSX and
ECMAScript 6 using Babel, then bundled, chunked and minified by Webpack.

For this basic infrastructure setup Volto relies on the Razzle library, which
provides an extensible Webpack SSR-enabled setup with convenient split of
server/client entrypoints and dual server/client Hot-Module-Reload (HMR).

The first Webpack entrypoint, the Volto server, is powered by ExpressJs.
It runs the Volto React code and components, then sends them to the browser as
a normal HTML page. It also proxies some of the Plone resources, such as files
and images.

Check if there's already a Razzle plugin, for example ``.scss`` support can be
To generate the second entrypoint, the client-only bundle, Webpack will need
Webpack to transpile .js and .jsx files with Babel, load .less files, css,
and Volto addons.  The base is provided by Razzle, with instructions for
etc) the files that represent the code and resources of Volto, the Volto project
have to enhance the Razzle configuration with the appropriate Webpack loader.
images and svgs. For any other file type (for example .scss, .ts, etc) you'll
simply added by adding ``scss`` to the razzle.config.js ``plugins`` list.
to know how to find, load and potentially mutate (compress, transpile, minify,

To summarize: Volto runs as a Single Page Application packaged by Webpack,
which uses loaders such as Babel (for ES6 js/jsx files) or less-loader for
``.less`` files.

Bootstrap a new Volto project
-----------------------------

Although it's possible to run Volto with npm as the Node package manager, the
community has settled, for now, to the Yarn Classic (v1.x) package manager.
Yarn is used as an installer, to run scripts but also as a "virtual
environment", by using its workspaces feature. Typically you'll start Volto
applications with ``yarn start``, use ``yarn test`` but you can also integrate
the ``mrs-developer`` library and run ``yarn missdev`` to do tasks similar to
mr.developer in Buildout projects.

To bootstrap a new Volto project, you can use either create-volto-app:

.. code-block:: bash

    npm -g i @plone/create-volto-app

or the new yeoman-based generator-volto:

.. code-block:: bash

    npm install -g yo
    npm install -g @plone/generator-volto
    yo @plone/volto myvoltoproject

The yo-based generator partially integrates addons (it can generate
a package.json with addons and workspaces already specified).

Addons - first look
-------------------

Although still in their infancy, 2020 is the year of the Volto addons.  The
Bethoven Sprint was a key moment in taking a common decision on how to load the
addons and what capabilities they should have.  Once the addons configuration
mechanism was added to Volto, many open source generic addons were published.
The collective/awesome-volto repo tracks of most of them (submit PRs if there's
anything missing!).

An addon can be almost anything that a Volto project can be. Addons can:

- provide additional views and blocks
- override or extend Volto's builtin views, blocks, settings
- shadow (customize) Volto's (or another addon's) modules
- register custom routes
- provide custom Redux actions and reducers
- register custom Express middleware for Volto's server process
- tweak Volto's webpak configuration, load custom Razzle and Webpack plugins
- even provide a custom theme, just like a regular Volto project does.

Basically, anything that a Volto project can do in terms of extending Volto
with new functionality, an addon can do as well.

As for implementation, Volto addons are just JS CommonJS packages with an
additional feature: they provide helper functions that can mutate Volto's
configuration registry. These are the "addon configuration loader". To make
things easy, addons should be distributed as source, non transpiled. Their
``main`` entry in ``package.json`` should point to ``src/index.js``, which
should be an ES6 module with a default export, the addon configuration loader:

.. code-block:: jsx

    export default (config) => {
        return config
    };

The ``config`` object that is passed is the Volto ``configuration registry``,
the singleton module referenced throughout the Volto and projects as
``~/config``. The addon can mutate the properties of config, such as
``settings``, ``blocks``, ``views``, ``widgets`` or its dedicated
``addonRoutes`` and ``addonReducers``.

Note: the addon configuration loading mechanism is inspired by Razzle, which
uses a similar get the config, return the config pass-through mechanism for it
plugins.

The resolution order is: Volto declares the initial configuration, it applies
the addon configuration and then the project configuration is loaded last,
enabling the project to override any configuration.

So: ``Volto => addons => project``.

To load an addon, the project needs to specify the addon in its
``project.json`` ``addons`` key:

.. code-block:: js

    ...,
    "addons": [
        "volto-slate:asDefault,somethingElse",
        "@eeacms/volto-object-widget",
    ],
    ...

Notice that the addons should be named by their package name, plus any
additional optional configuration loaders that are exported by the addon's
``src/index.js``.

Bootstrap an addon
------------------

Let's start creating an addon. We'll create a new package:
``@plone/datatable-tutorial``. Inside your Volto project, bootstrap the addon
by running:

.. code-block:: shell

    mkdir -p src/addons/datatable-tutorial
    cd datatable-tutorial
    npm init

Note: the namespace ``@plone`` (or any other) is not required and is optional.
We're using namespaces to group addons under a common "group". There is no
shared addon namespace right now for Volto addons as the NPM Collective
organization doesn't belong to the Plone community.

Use ``@plone/datatable-tutorial`` as the package name and ``src/index.js`` as
the package main. Create ``src/index.js`` with the following content:

.. code-block:: jsx

    export default (config) => config;

Back to the project, you can edit jsconfig.json and add your addon:

.. code-block:: json

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

.. code-block:: json

    "datatable-tutorial": {
        "url": "https://github.com/collective/datatable-tutorial.git",
        "path": "src",
        "package": "@plone/datatable-tutorial",
        "branch": "master"
    }

Then run ``yarn develop``, which will bring the package in ``src/addons`` and
adjust ``jsconfig.json``.

When developing addons that have third-party depedencies, you need to add the
addon as workspace to the Volto project. Change the Volto project's
``package.json`` to something like:

.. code-block:: json

    "private": "true",
    "workspaces": [
        "src/addons/datatable-tutorial"
    ],

To be able to add dependencies to the addon you need to add them via the
workspaces root, by running something like:

.. code-block:: sh

    yarn workspaces info
    yarn workspace @plone/datatable-tutorial add @fast-csv/parse

Note: there are several addon templates, such as
https://github.com/nzambello/voltocli or
https://github.com/eea/volto-addon-template

While the community settles on what constitutes best practice for an addon's
essential files, you should be aware that an addon is just a simple
``package.json`` and an ``index.js`` file. Everything else is up to you, just
make sure to point the ``main`` in ``package.json`` to ``src/index.js``.

Create a new block
------------------

- Create DataTable/DataTableView.jsx

.. code-block:: jsx

    import React from 'react';

    const DataTableView = (props) => {
      return <div>Table here...</div>;
    };

    export default DataTableView;

- Create DataTable/DataTableEdit.jsx

.. code-block:: jsx

    import React from 'react';
    import DataTableView from './DataTableView';

    const DataTableEdit = (props) => {
      return (
        <div>
          <DataTableView {...props} />
        </div>
      );
    };

    export default DataTableEdit;

We're reusing the block view component inside the edit, this makes the block
development fast.

- Create DataTable/index.js. This step is optional, but it makes imports nicer
  across the project. Make sure to adjust the subsequent code, if you don't add
  this file:

.. code-block:: jsx

    export DataTableView from './DataTableView';
    export DataTableEdit from './DataTableEdit';

- Register the block in src/index.js

.. code-block:: jsx

    import tableSVG from '@plone/volto/icons/table.svg';

    import DataTableView from './DataTable/DataTableView';
    import DataTableEdit from './DataTable/DataTableEdit';

    export { DataTableView, DataTableEdit };

    export default (config) => {
        config.blocks.blocksConfig.dataTable = {
            id: 'dataTable',
            title: 'Data Table',
            icon: globeSVG,
            group: 'common',
            view: DataTableView,
            edit: DataTableEdit,
            restricted: false,
            mostUsed: false,
            sidebarTab: 1,
            security: {
              addPermission: [],
              view: [],
            },
        };
        return config;
    }

Create the new block in Volto, save the page.

Improving the block edit
~~~~~~~~~~~~~~~~~~~~~~~~

Now for the simplest block sidebar:

.. code-block:: jsx

    import React from 'react';
    import { Segment, Form } from 'semantic-ui-react';
    import { SidebarPortal, Field } from '@plone/volto/components';
    import DataTableView from './DataTableView';

    const DataTableEdit = (props) => {
      const { selected, onChangeBlock, block, data } = props;
      return (
        <div>
          <SidebarPortal selected={selected}>
            <Segment.Group raised>
              <header className="header pulled">
                <h2>Data table</h2>
              </header>

              <Form>
                <Field
                  id="file"
                  widget="pick_object"
                  title="Pick file"
                  value={data.file}
                  onChange={(id, value) =>
                    onChangeBlock(block, { ...data, [id]: value })
                  }
                />
              </Form>
            </Segment.Group>
          </SidebarPortal>
          <DataTableView />
        </div>
      );
    };

    export default DataTableEdit;

We want to show a field to browse to a file. Notice the ``widget`` parameter of
the field. This widget is not registered by default in Volto, let's register
it, add this in ``index.js``:

.. code-block:: jsx

    import { ObjectBrowserWidgetMode } from '@plone/volto/components/manage/Widgets/ObjectBrowserWidget';

    ...

    if (!config.widgets.widget.pick_object)
        config.widgets.widget.pick_object = ObjectBrowserWidgetMode('link');
