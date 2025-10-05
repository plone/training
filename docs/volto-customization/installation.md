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
For the most up-to-date information on how to get started with Volto you can check the {doc}`official documentation <plone6docs:volto/index>`.
```

Getting started with Volto involves setting up a development environment, understanding its core concepts, and exploring its features. Here's a step-by-step guide to help you begin your journey with Volto:

## Prerequisites

Before you start working with this training, ensure you have the following prerequisites, according to Plone 6 Documentation.

{doc}`plone6docs:install/create-project-cookieplone`


## Bootstrap a new Plone stack

To bootstrap a new Plone project(with both backend and frontend), you can use [Cookieplone](https://github.com/plone/cookieplone).
You can use uvx to run Cookieplone to generate a project.

```shell
uvx cookieplone project
```

You will be presented with a series of prompts.
You can also specify the add-ons you want to install along with the project.
When prompted for {guilabel}`Volto Addon Name`, enter `volto-teaser-tutorial`.

```shell
[11/17] Volto Addon Name (volto-project-title): volto-teaser-tutorial
```

You can accept the rest of the default values in square brackets (`[default-option]`) by hitting the {kbd}`Enter` key, or enter your preferred values.
For the training, we will use the default values for the rest of the prompts.

## Install the project

To work on your project, you need to install both the frontend and backend.

Change your current working directory to `project-title`.

```shell
cd project-title
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

You can then login with admin/admin at http://localhost:3000/login

## Volto addon

Using Cookieplone we should already have a working Volto project with provided add-on. You can find the add-on in packages/volto-teaser-tutorial.

```{note}
You might have noticed that we have {file}`volto.config.js` in the root of the project. This is the Volto configuration file allowing us to configure Volto and register add-ons. The add-ons list points to the add-on we just installed. Cookieplone takes care of registering the add-on for us.
```

## Workspaces

pnpm workspaces are a way to manage multiple packages in a single repository. Volto is a monorepo, so we use workspaces to manage the Volto project and its add-ons along with other packages.

We can define workspaces using the `pnpm-workspace.yaml` file in root of our project. This is taken care for us by Cookieplone.

```yaml
packages:
  # all packages in direct subdirs of packages/
  - "core/packages/*"
  - "packages/*"
```

All the packages in the {file}`packages` directory will be included in the workspace.

The dependencies section maps the package names to the workspace. The `workspace:*` specifier tells pnpm to resolve these dependencies from other packages within the same workspace rather than fetching them from the npm registry.

```json
  "dependencies": {
    "@plone/volto": "workspace:*",
    "@plone/registry": "workspace:*",
    "volto-teaser-tutorial": "workspace:*"
  },
```

```{note}
We don't need to pin a specific workspace before we publish or release our project. pnpm takes care of dynamically updating the versions of these packages when you do `pnpm pack` or `pnpm publish`.

```

### Managing add-on dependencies

To be able to add dependencies to the add-on, you need to add them via the
workspaces machinery by running something like (at the Volto project root):

```shell
pnpm --filter volto-teaser-tutorial add papaparse
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

### TypeScript configuration

Earlier, add-ons required a custom {file}`tsconfig.json` setup for TypeScript.
Now, TypeScript support is available by default in Volto projects and add-ons, so you no longer need extra configuration.

## Documentation and Resources

Refer to the [official Volto documentation](https://6.docs.plone.org/volto/index.html) for in-depth guides, tutorials, and examples.

Join the Volto community, participate in discussions, and ask questions on the Volto GitHub repository or the [Plone community chat on Discord](https://plone.org/news-and-events/news/2021/join-plone-chat-now-at-discord)

```{warning}
Getting started with Volto may seem complex at first, but with practice and exploration, you'll become more comfortable with its features and capabilities. It offers a powerful and flexible platform for building modern web applications with React and Plone.
```
