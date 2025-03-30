---
myst:
  html_meta:
    "description": "Volto add-ons development training module 1, add-ons basics"
    "property=og:description": "Volto add-ons development training"
    "property=og:title": "Volto add-ons development"
    "keywords": "Volto"
---

# Volto add-ons development

## Volto: an overview

One of the basic aspects of Volto is that it provides Server-Side Rendering
(SSR): when you first load a Volto page you'll get HTML code identical in its
markup to the React-rendered output of that page. The HTML page will also load
a bunch of JS files which, when loaded, finally bring Volto to run as a Single
Page Application (SPA) in the browser.

Another basic fact, Volto is a React app that is transpiled from JSX and
ECMAScript 6 using Babel, then bundled, chunked, and minified by Webpack.

For this basic infrastructure setup Volto relies on the Razzle library, which
provides an extensible Webpack SSR-enabled setup with a convenient split of
server/client entry points and dual server/client Hot-Module-Reload (HMR).

The first Webpack entry point will be used as the Volto *server* and uses
Express web framework for that. It runs the Volto React code and components
then sends them to the browser as a normal HTML page. It also proxies some
Plone resources, such as files and images. Once the HTML page is loaded by the
browser, all communication is done as JSON API messages.

To generate the second entry point, the *client*-only bundle, Webpack will need
to know how to find, load, and potentially mutate (compress, transpile, minify,
etc.) the files that represent the code and resources of Volto, the Volto
project, and Volto add-ons. The base is provided by Razzle, with instructions
for Webpack to transpile .js and .jsx files with Babel, load .less files, CSS,
images, and SVG files. For any other file type (for example, .scss, .ts, etc.)
you'll have to enhance the Razzle configuration with the appropriate Webpack
loader.

Check if there's already a Razzle plugin. For example `.scss` support can be
added by adding `scss` to the `razzle.config.js` `plugins` list.

To summarize: Volto runs as a Single Page Application packaged by Webpack,
which uses loaders such as Babel (for ES6 js/jsx files) or a [less-loader] for
`.less` files.

## Bootstrap a new Volto project

Although it's possible to run Volto with npm as the Node package manager, the
community has settled, for now, for the Yarn Classic (v1.x) package manager.
Yarn is used as an installer, to run scripts but also as a "virtual
environment", by using its workspaces feature. Typically you'll start Volto
applications with `yarn start` or `yarn test`. You can also integrate the
`mrs-developer` library, and run `yarn missdev` to do tasks similar to
mr.developer in Buildout projects. If you're not sure what these or any other
`yarn` commands do, it's a good idea to examine your project's `package.json`
file, in the `scripts` section, where you'll usually find those scripting
aliases defined.

To bootstrap a new Volto project, you can use a scaffolding tool based on
Yeoman named [@plone/generator-volto](https://github.com/plone/generator-volto).
First, install it as a global tool (use [NVM] if you're being asked for sudo
access):

```shell
npm install -g yo
npm install -g @plone/generator-volto
```

Then you can bootstrap the project with:

```shell
yo @plone/volto volto-tutorial-project
```

The yo-based generator partially integrates add-ons (it can generate a
`package.json` with add-ons and workspaces already specified). When prompted
to add add-ons, choose `false`.

Now you can start your newly created Volto project:

```shell
cd volto-tutorial-project
yarn start
```

You can then login with admin/admin at http://localhost:3000/login.

## Bootstrap an add-on

Let's start creating an add-on. We'll create a new scoped package:
`@plone-collective/datatable-tutorial`. Inside your Volto project, bootstrap
the add-on by running (in the Volto project root):

```shell
yo @plone/volto:addon
```

Note: the namespace `@plone-collective` (or any other) is not required and is
optional. We're using namespaces to group add-ons under a common "group".
Unfortunately, the NPM `@collective` scope is not available to the Plone
community.

Use `@plone-collective/volto-datatable-tutorial` as the package name. After the
scaffolding of the add-on completes, you can check the created files in
`src/addons/volto-datatable-tutorial`.

Back to the project, you can edit {file}`tsconfig.json` and add your add-on:

```json
{
    "compilerOptions": {
        "baseUrl": "src",
        "paths": {
            "@plone-collective/volto-datatable-tutorial": [
                "addons/volto-datatable-tutorial/src"
            ]
        }
    }
}
```

```{note}
The {file}`tsconfig.json` file is needed by Volto to identify development
packages. You are not strictly limited to Volto add-ons in its use, you
could, for example, use this to make it easier to debug third-party
JavaScript packages that are shipped transpiled.
```

```{attention}
Projects using Volto versions before 17 should still refer to {file}`jsconfig.json`.
```

### (Optional) Use mrs-developer to sync add-on to GitHub

You can also immediately push the package to GitHub, then use `[mrs-developer]`
to manage the package and {file}`tsconfig.json` changes.

Install mrs-developer as a development dependency by running:

```shell
yarn add -W -D mrs-developer
```

Create a `mrs.developer.json` with the following content (adjust it according
to your names and repository location):

```json
 {
     "volto-datatable-tutorial": {
         "url": "https://github.com/collective/datatable-tutorial.git",
         "path": "src",
         "package": "@plone-collective/volto-datatable-tutorial",
         "branch": "main"
     }
}
```

Then run `yarn develop`, which will bring the package in `src/addons` and
adjust {file}`tsconfig.json`.

### Add the add-on as workspace

The Volto project is itself a JavaScript package, and we want to "plug" here
other JavaScript packages that we will develop. The Volto project itself
becomes a monorepo, with the Volto project being the "workspace root" and each
add-on needs to be a "workspace", so that yarn knows that it should include that
add-on location as a package and install its dependencies.

Change the Volto project's `package.json` to include something like:

```json
{
    "private": "true",
    "workspaces": [
        "src/addons/volto-datatable-tutorial"
    ],
}
```

```{note}
Don't be scared by that `"private": "true"` in the Volto project `package.json`.
It's only needed to make sure you can't accidentally publish the package to NPM.
```

### Managing add-on dependencies

To be able to add dependencies to the add-on, you need to add them via the
workspaces machinery by running something like (at the Volto project root):

```shell
yarn workspaces info
yarn workspace @plone-collective/volto-datatable-tutorial add papaparse
```

````{note}
There are several other add-on templates, such as
[voltocli](https://github.com/nzambello/voltocli) or
[eea/volto-addon-template](https://github.com/eea/volto-addon-template).
You could very well decide not to use any of them, and instead bootstrap a new
add-on by running:

```shell
mkdir -p src/addons/datatable-tutorial
cd src/addons/datatable-tutorial
npm init
```

Remember, an add-on is just a JavaScript package that exports
a configuration loader. Just make sure to point the `main` in
`package.json` to `src/index.js`.
````

### Load the add-on in Volto

To tell Volto about our new add-on, add it to the `addons` key of the Volto
project `package.json`:

```js
// ...
"addons": ["@plone-collective/volto-datatable-tutorial"]
// ...
```

## Add-ons - first look

Although still in their infancy, 2020 was the year of the Volto add-ons.  The
Beethoven Sprint was a key moment in arriving at a consensus on how to load the
add-ons and what capabilities they should have. With a common understanding of
what exactly is an add-on, many new add-ons were published and can now be
integrated with unmodified Volto projects.

The [collective/awesome-volto](https://github.com/collective/awesome-volto)
repository tracks most of them (submit PRs if anything is missing!).

An add-on can be almost anything that a Volto project can be. They can:

- provide additional views and blocks
- override or extend Volto's builtin views, blocks, and settings
- shadow (customize) Volto's (or another add-on's) modules
- register custom routes
- provide custom Redux actions and reducers
- register custom Express middleware for Volto's server process
- tweak Volto's webpack configuration, load custom Razzle, and Webpack plugins
- even provide a custom theme, just like a regular Volto project does.

As for implementation, Volto add-ons are just plain JavaScript packages with an
additional feature: they provide helper functions that mutate Volto's
configuration registry. These are the "add-on configuration loaders".

```{note}
To make things easy, add-ons should be distributed as source, non-transpiled
code. Volto's Webpack setup integrates all development loaders (Babel
transpiling, less loading, and so on) if they are identified as Volto add-ons.
```

Their `main` entry in `package.json` should point to `src/index.js`,
which should be an ES6 module with a default export.
Here is the default add-on configuration loader:

```jsx
export default (config) => {
    return config
};
```

Any additional named `export` from the main script can be used as an add-on
optional configuration loader.

The `config` object that is passed is the Volto `configuration registry`,
the singleton module referenced throughout Volto and Volto projects,
by importing `@plone/volto/registry`. The add-on can mutate the properties of
the config, such as `settings`, `blocks`, `views`, `widgets`, or its dedicated
`addonRoutes` and `addonReducers`.

Note: the add-on configuration loading mechanism is inspired by Razzle, which
uses a similar "get the config, return the config" pass-through mechanism for
its plugins.

The resolution order is: Volto declares the initial configuration, it applies
the add-on configuration and then the project configuration is loaded last,
enabling the project to override any configuration.

So: {guilabel}`Volto → add-ons → project`.

To load an add-on, the project needs to specify the add-on in the `addons` key
of `project.json`. Optional configuration loaders are specified as
a comma-separated list after the `:` colon symbol.

```js
// ...
"addons": [
    "volto-slate:asDefaultBlock,simpleLink",
    "@eeacms/volto-tabs-block",
]
// ...
```

Notice that the add-ons should be named by their package name, plus any
additional optional configuration loaders that are exported by the add-on's
`src/index.js`.

## Develop a basic block

Now that the "infrastructure" is all set, we have our Volto project with the
add-on loaded, we can finally start developing for Volto!

### Create a new block

- Create `src/DataTable/DataTableView.jsx`

```jsx
import React from 'react';

const DataTableView = (props) => {
  return <div>Table here...</div>;
};

export default DataTableView;
```

- Create `src/DataTable/DataTableEdit.jsx`

```jsx
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
```

We're reusing the block view component referenced from the edit component, to
speed things up.

```{note}
We will be using [function
components](https://legacy.reactjs.org/docs/components-and-props.html#function-and-class-components)
here. There is no rule in Volto that requires choosing between class components or
function components. Pick whichever feels better. Volto itself uses both
styles. Although the function components are a newer API, and the use of hooks
can make things more compact and reusable, they can also become hard to track,
especially when multiple `useEffect` piles up in the same component. Don't
feel that you have to stick to one style only. Choose whichever feels right
for the task.
```

- Create `src/DataTable/index.js`. This step is optional, but it makes imports
  nicer across the project. In case you decide on omitting this file, make sure
  to adjust your code and imports accordingly.

```jsx
export DataTableView from './DataTableView';
export DataTableEdit from './DataTableEdit';
```

- Register the block in `src/addons/datatable-tutorial/src/index.js`

```jsx
import tableSVG from '@plone/volto/icons/table.svg';

import { DataTableView, DataTableEdit } from './DataTable';

export default (config) => {
  config.blocks.blocksConfig.dataTable = {
    id: 'dataTable',
    title: 'Data Table',
    icon: tableSVG,
    group: 'common',
    view: DataTableView,
    edit: DataTableEdit,
    restricted: false,
    mostUsed: true,
    sidebarTab: 1,
    security: {
      addPermission: [],
      view: [],
    },
  };
  return config;
};
```

Instantiate the new block in a Volto page then save the page. This is a small
development optimization. When changing code while developing, the HMR will
kick in and replace the content on the edit page with the one loaded initially
from the server. If you haven't saved the block yet, you'll need to recreate
it again.

### Improve the block edit

Now for the simplest block sidebar, edit `src/addons/datatable-tutorial/src/DataTableEdit.jsx`:

```jsx
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
              id="file_path"
              widget="object_browser"
              title="File"
              value={data.file_path || []}
              mode="link"
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
```

The `<Form>` component in our case is used only for styling purposes.

```{note}
We'll need a CSV file to play around while developing this add-on. We have
provided one for you to {download}`download <../_static/forest-areas.csv>`
```

[eea add-on template]: https://github.com/eea/volto-addon-template
[less-loader]: https://webpack.js.org/loaders/less-loader/
[mrs-developer]: https://github.com/collective/mrs-developer
[nvm]: https://github.com/nvm-sh/nvm
[voltocli]: https://github.com/nzambello/voltocli
