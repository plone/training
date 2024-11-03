---
myst:
  html_meta:
    "description": "Volto and Plone development - installation steps for JavaScript Beginners"
    "property=og:description": "Volto and Plone development - installation steps for JavaScript Beginners"
    "property=og:title": "Installation steps for JavaScript Beginners"
    "keywords": "Plone, Volto, Training, Installation"
---

# Installation

```{warning}
For the most up-to-date information on how to get started with Volto you can check the [official documentation](https://6.docs.plone.org/volto/index.html).
```

Getting started with Volto involves setting up a development environment, understanding its core concepts, and exploring its features. Here's a step-by-step guide to help you begin your journey with Volto:

## Prerequisites

Before you start working with this training, ensure you have the following prerequisites:

- <a target="_blank" href="https://nodejs.org/en">Node.js LTS (>=20.x)</a> - (<a target="_blank" href="https://6.docs.plone.org/install/install-from-packages.html#nvm">see instructions for installation</a>)
- <a target="_blank" href="https://www.python.org/">Python</a> - See below for specific versions.
- <a target="_blank" href="https://pipx.pypa.io/stable/">pipx</a>
- <a target="_blank" href="https://github.com/nvm-sh/nvm?tab=readme-ov-file#installing-and-updating">nvm</a>
- <a target="_blank" href="https://www.gnu.org/software/make/">GNU make</a>
- <a target="_blank" href="https://www.docker.com/get-started">Docker</a> (if using the Plone docker images - <a target="_blank" href="https://6.docs.plone.org/install/containers/index.html">see instructions for installation and usage</a>)

The versions of Python that are supported in Volto depend on the version of Plone that you use.

| Plone | Python       | Volto        |
| ----- | ------------ | ------------ |
| 6.0   | 3.8-3.12     | 17.0 or 18.0 |
| 5.2   | 2.7, 3.6-3.8 | 15.0         |

Depending on the operating system that you are using, some of the following pre-requisites might change.
They assume you have a macOS/Linux machine.

## Bootstrap a new Plone stack

To bootstrap a new Plone project(with both backend and frontend), you can use [Cookieplone](https://github.com/plone/cookieplone).
You can use pipx to run cookieplone (<a target="_blank" href="https://6.docs.plone.org/install/create-project-cookieplone.html#generate-the-project">see instructions for installation</a>):

```shell
pipx run cookieplone project
```

You will be presented with a series of prompts. You can also specify the addons you want to install along with the project. You can type the name of the project as `tutorial-project` and name of the addon as `volto-teaser-tutorial` when prompted for the addons.

```shell
[11/17] Volto Addon Name (volto-project-title): volto-teaser-tutorial
```

You can accept the rest of the default values in square brackets (`[default-option]`) by hitting the {kbd}`Enter` key, or enter your preferred values.
For the training, we will use the default values for the rest of the prompts.

## Install the project

To work on your project, you need to install both the frontend and backend.

Change your current working directory to `tutorial-project`.

```shell
cd tutorial-project
```

To install both the Plone backend and frontend, use the following command.

```shell
make install
```

## Start Plone

Plone 6 has two servers: one for the frontend, and one for the backend.
As such, we need to maintain two active shell sessions, one for each server, to start your Plone site.

### Start Plone backend

In the currently open session, issue the following command.

```shell
make backend-start
```

### Start Plone frontend

Create a second shell session in a new window.
Start the Plone frontend with the following command.

```shell
make frontend-start
```

Open a browser at the following URL to visit your Plone site.

http://localhost:3000

You can then login with admin/admin at <a target="_blank" href="http://localhost:3000/login">http://localhost:3000/login</a>.

## Volto addon

Using Cookieplone we should already have a working Volto project with provided addon. You can find the addon in packages/volto-teaser-tutorial.

```{note}
You might have noticed that we have `volto.config.js` in the root of the project. This is the volto configuration file allowing us to configure Volto and register addons.The addons list points to the addon we just installed. Cookieplone takes care of registering the addon for us.
```

## Workspaces

pnpm workspaces are a way to manage multiple packages in a single repository. Volto is a monorepo, so we use workspaces to manage the Volto project and its addons along with other packages.

We can define workspaces directly in the package.json file of a our project. However, it's common practice to use the `pnpm-workspace.yaml` file for more complex workspace configurations. This is taken care for us by Cookieplone.

```yaml
packages:
  # all packages in direct subdirs of packages/
  - "core/packages/*"
  - "packages/*"
```

All the packages in the `packages` directory will be included in the workspace.

The dependencies section maps the package names to the workspace. The `workspace:*` specifier tells pnpm to resolve these dependencies from other packages within the same workspace rather than fetching them from the npm registry.

```json
  "dependencies": {
    "@plone/volto": "workspace:*",
    "@plone/registry": "workspace:*",
    "volto-teaser-tutorial": "workspace:*"
  },
```

### Managing add-on dependencies

To be able to add dependencies to the add-on, you need to add them via the
workspaces machinery by running something like (at the Volto project root):

```shell
pnpm workspaces info
pnpm workspace volto-teaser-tutorial add papaparse
```

## Addons - first look

Volto add-ons are just plain JavaScript packages with an
additional feature: they provide helper functions that mutate Volto's
configuration registry.

Their `main` entry in `package.json` should point to `src/index.js`,
which should be an ES6 module with a default export.
Here is the default add-on configuration loader:

```js
export default (config) => {
  return config;
};
```

### typescript configuration

Every addon supports custom typescript configuration using `tsconfig.json` in the root of the addon package. This file defines how the typeScript compiler should process the code in our addon.

You can inspect the tsconfig.json file in the volto-teaser-tutorial package.

The basic ones are self explanatory. Note that we have path mapping inside `compilerOptions` for all the packages that this addon depends on.

```js
{
  "compilerOptions": {
    "paths": {
      "@plone/volto/*": ["../../core/packages/volto/src/*"],
      "volto-teaser-tutorial/*": ["./src/*"]
    }
  },
}
```

This option allows you to set up module resolution paths. The mappings provided allow typescript to resolve modules using custom paths:

`@plone/volto/*` maps to files in `../../core/packages/volto/src/*`, allowing us to import from this directory using the @plone/volto prefix.
`volto-teaser-tutorial/*` maps to `./src/*`, allowing local imports from the src directory of the volto-teaser-tutorial package.

## Documentation and Resources

Refer to the <a target="_blank" href="https://6.docs.plone.org/volto/index.html">official Volto documentation</a> for in-depth guides, tutorials, and examples.

Join the Volto community, participate in discussions, and ask questions on the Volto GitHub repository or the <a target="_blank" href="https://plone.org/news-and-events/news/2021/join-plone-chat-now-at-discord">Plone community chat on Discord</a>.

```{warning}
Getting started with Volto may seem complex at first, but with practice and exploration, you'll become more comfortable with its features and capabilities. It offers a powerful and flexible platform for building modern web applications with React and Plone.
```
