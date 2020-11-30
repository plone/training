========================
Volto add-ons development
========================

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

The first Webpack entrypoint will be used as the Volto *server* and uses
ExpressJs for that. It runs the Volto React code and components then sends
them to the browser as a normal HTML page. It also proxies some of the Plone
resources, such as files and images. Once the HTML page is loaded by browser,
all communication is done as JSON api messages.

To generate the second entrypoint, the *client*-only bundle, Webpack will need to
know how to find, load and potentially mutate (compress, transpile, minify,
etc) the files that represent the code and resources of Volto, the Volto
project and Volto add-ons. The base is provided by Razzle, with instructions for
Webpack to transpile .js and .jsx files with Babel, load .less files, css,
images and svgs. For any other file type (for example .scss, .ts, etc) you'll
have to enhance the Razzle configuration with the appropriate Webpack loader.

Check if there's already a Razzle plugin, for example ``.scss`` support can be
simply added by adding ``scss`` to the razzle.config.js ``plugins`` list.

To summarize: Volto runs as a Single Page Application packaged by Webpack,
which uses loaders such as Babel (for ES6 js/jsx files) or `less-loader`_ for
``.less`` files.

.. _less-loader: https://webpack.js.org/loaders/less-loader/

Bootstrap a new Volto project
-----------------------------

Although it's possible to run Volto with npm as the Node package manager, the
community has settled, for now, for the Yarn Classic (v1.x) package manager.
Yarn is used as an installer, to run scripts but also as a "virtual
environment", by using its workspaces feature. Typically you'll start Volto
applications with ``yarn start``, use ``yarn test`` but you can also integrate
the ``mrs-developer`` library and run ``yarn missdev`` to do tasks similar to
mr.developer in Buildout projects.

To bootstrap a new Volto project, you can use either create-volto-app:

.. code-block:: bash

    npm -g i @plone/create-volto-app
    create-volto-app myvoltoproject

or the new Yeoman-based generator-volto:

.. code-block:: bash

    npm install -g yo
    npm install -g @plone/generator-volto
    yo @plone/volto myvoltoproject

The yo-based generator partially integrates add-ons (it can generate a
``package.json`` with add-ons and workspaces already specified).

Addons - first look
-------------------

Although still in their infancy, 2020 is the year of the Volto add-ons.  The
Bethoven Sprint was a key moment in arriving at a consensus on how to load the
addons and what capabilities they should have. With a common understanding on
what exactly is an add-on, many new add-ons were published and can now be
integrated with unmodified Volto projects.

The `collective/awesome-volto`__ repo tracks most of them (submit PRs if
there's anything missing!).

.. __: https://github.com/collective/awesome-volto

An add-on can be almost anything that a Volto project can be. They can:

- provide additional views and blocks
- override or extend Volto's builtin views, blocks, settings
- shadow (customize) Volto's (or another add-on's) modules
- register custom routes
- provide custom Redux actions and reducers
- register custom Express middleware for Volto's server process
- tweak Volto's webpak configuration, load custom Razzle and Webpack plugins
- even provide a custom theme, just like a regular Volto project does.

As for implementation, Volto add-ons are just plain Javascript packages with an
additional feature: they provide helper functions that mutate Volto's
configuration registry. These are the "addon configuration loaders".

.. note::

    To make things easy, add-ons should be distributed as source, non
    transpiled. Volto's Webpack setup will load/transpile add-on packages if
    they are identified as Volto add-ons.

Their ``main`` entry in ``package.json`` should point to ``src/index.js``,
which should be an ES6 module with a default export, the add-on configuration
loader:

.. code-block:: jsx

    export default (config) => {
        return config
    };

Any additional named export from the main script can be used as an add-on
optional configuration loader.

The ``config`` object that is passed is the Volto ``configuration registry``,
the singleton module referenced throughout the Volto and projects as
``~/config``. The add-on can mutate the properties of config, such as
``settings``, ``blocks``, ``views``, ``widgets`` or its dedicated
``addonRoutes`` and ``addonReducers``.

Note: the add-on configuration loading mechanism is inspired by Razzle, which
uses a similar "get the config, return the config" pass-through mechanism for
its plugins.

The resolution order is: Volto declares the initial configuration, it applies
the add-on configuration and then the project configuration is loaded last,
enabling the project to override any configuration.

So: :menuselection:`Volto → add-ons → project`.

To load an add-on, the project needs to specify the add-on in its
``project.json`` ``addons`` key. Optional configuration loaders are specified
as a comma-separated list after the ``:`` colon symbol.

.. code-block:: js

    ...,
    "addons": [
        "volto-slate:asDefault,somethingElse",
        "@eeacms/volto-object-widget",
    ],
    ...

Notice that the add-ons should be named by their package name, plus any
additional optional configuration loaders that are exported by the add-on's
``src/index.js``.

Bootstrap an add-on
------------------

Let's start creating an add-on. We'll create a new scoped package:
``@plone-collective/datatable-tutorial``. Inside your Volto project, bootstrap
the add-on by running:

.. code-block:: shell

    mkdir -p src/addons
    cd src/addons

    npm install -g yo
    npm install -g @plone/generator-volto
    yo @plone/volto:addon

Note: the namespace ``@plone-collective`` (or any other) is not required and is
optional.  We're using namespaces to group add-ons under a common "group".
Unfortunately the NPM ``@collective`` scope is not available to the Plone
community.

Use ``@plone-collective/datatable-tutorial`` as the package name and
``src/index.js`` as the package main script. Create ``src/index.js`` with the
following content:

.. code-block:: jsx

    export default (config) => config;

Back to the project, you can edit ``jsconfig.json`` and add your add-on:

.. code-block:: json

    {
        "compilerOptions": {
            "baseUrl": "src",
            "paths": {
                "@plone-collective/datatable-tutorial": [
                    "addons/datatable-tutorial/src"
                ],
            }
        }
    }

.. note::

    The ``jsconfig.json`` file is needed by Volto to identify development
    packages. You are not strictly limited to Volto add-ons in its use, you
    could, for example, use this to make it easier to debug third-party
    Javascript packages that are shipped transpiled.

You can also immediately push the package to Github then use `mrs-developer`_
to manage the package and ``jsconfig.json`` changes. Add to
``mrs-developer.json``:

.. _mrs-developer: https://github.com/collective/mrs-developer

.. code-block:: json

    {
        "datatable-tutorial": {
            "url": "https://github.com/collective/datatable-tutorial.git",
            "path": "src",
            "package": "@plone-collective/datatable-tutorial",
            "branch": "master"
        }
   }

Then run ``yarn develop``, which will bring the package in ``src/addons`` and
adjust ``jsconfig.json``.

When developing add-ons that have third-party depedencies, you need to add the
addon as workspace to the Volto project. Change the Volto project's
``package.json`` to something like:

.. code-block:: json

    {
        "private": "true",
        "workspaces": [
            "src/addons/datatable-tutorial"
        ],
    }

.. note::
    Don't be scared by that `private:true` in the Volto project package.json,
    it's only needed to make sure you can't accidentally publish the package to
    NPM

To be able to add dependencies to the add-on you need to add them via the
workspaces machinery, by running something like (at the Volto project root):

.. code-block:: console

    yarn workspaces info
    yarn workspace @plone-collective/datatable-tutorial add @papaparse

.. note::
    There are several other add-on templates, such as `voltocli`_ or `EEA Add-on
    Template`_. You could very well decide not to use any of them and simply
    bootstrap a new add-on by running:

    .. code-block:: console

        mkdir -p src/addons/datatable-tutorial
        cd src/addons/datatable-tutorial
        npm init

    So, remember, an add-on is just a Javascript package that export
    a configuration loader. Just make sure to point the ``main`` in
    ``package.json`` to ``src/index.js``.

.. _voltocli: https://github.com/nzambello/voltocli
.. _`EEA Add-on Template`: https://github.com/eea/volto-addon-template
.. _`@plone/generator-volto`: https://github.com/plone/generator-volto

Create a new block
------------------

- Create ``DataTable/DataTableView.jsx``

.. code-block:: jsx

    import React from 'react';

    const DataTableView = (props) => {
      return <div>Table here...</div>;
    };

    export default DataTableView;

- Create ``DataTable/DataTableEdit.jsx``

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

We're reusing the block view component referenced from the edit component, to
speed things up.

.. note::

    We will be using `function components`__ here. There is no rule in Volto
    that requires choosing between class components or function components,
    pick whichever feels better. Volto itself uses both styles. Although the
    function components are newer API and the use of hooks can make things more
    compact and reusable, they can also become hard to track, specially when
    multiple ``useEffect`` pile up in the same component. Don't feel that you
    have to stick to one style only, choose whichever feels right for the task.

    .. __: https://reactjs.org/docs/components-and-props.html#function-and-class-components


- Create ``DataTable/index.js``. This step is optional, but it makes imports
  nicer across the project. In case you decide on omitting this file, make sure
  to adjust your code and imports accordingly.

.. code-block:: jsx

    export DataTableView from './DataTableView';
    export DataTableEdit from './DataTableEdit';

- Register the block in ``src/index.js``

.. code-block:: jsx

    import tableSVG from '@plone/volto/icons/table.svg';

    import DataTableView from './DataTable/DataTableView';
    import DataTableEdit from './DataTable/DataTableEdit';

    export { DataTableView, DataTableEdit };

    export default (config) => {
        config.blocks.blocksConfig.dataTable = {
            id: 'dataTable',
            title: 'Data Table',
            icon: tableSVG,
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

Instantiate the new block in a Volto page then save the page. This is a small
development optimization, when changing code while developing the HMR will kick
in and replace the content on the edit page with the one loaded initially from
the server, so if you're haven't saved the block yet, you'll need to recreate
it again.

Improve the block edit
~~~~~~~~~~~~~~~~~~~~~~

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

The ``<Form>`` component in our case is used only for styling purposes.

We want to show a field to browse to a file. Notice the ``widget`` parameter of
the field. This widget is not registered by default in Volto, let's register
it, add this in the add-on configuration loader in ``src/index.js``:

.. code-block:: jsx

    import { ObjectBrowserWidgetMode } from '@plone/volto/components/manage/Widgets/ObjectBrowserWidget';

    ...

    if (!config.widgets.widget.pick_object)
        config.widgets.widget.pick_object = ObjectBrowserWidgetMode('link');

By doing so we're instantiating a new ObjectBrowserWidget component that will
work in the "link" mode. We're registering a new widget called "pick_object".
By passing ``widget="pick_widget"`` to the ``<Field>`` component we're
instructing the form field machinery lookup the ``pick_object`` widget in the
widgets Volto registry.

.. note::

    We'll need a CSV file to play around while developing this add-on. We have
    provided one for you to :download:`download <../_static/forest-areas.csv>`
