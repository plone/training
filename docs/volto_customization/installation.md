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

Before you start working with Volto, ensure you have the following prerequisites:

- <a target="_blank" href="https://nodejs.org/en">Node.js LTS (16.x)</a> - (<a target="_blank" href="https://6.docs.plone.org/install/install-from-packages.html#nvm">see instructions for installation</a>)
- <a target="_blank" href="https://www.python.org/">Python</a> - See below for specific versions.
- <a target="_blank" href="https://www.docker.com/get-started">Docker</a> (if using the Plone docker images - <a target="_blank" href="https://6.docs.plone.org/install/containers/index.html">see instructions for installation and usage</a>)

The versions of Python that are supported in Volto depend on the version of Plone that you use.

| Plone | Python       | Volto        |
| ----- | ------------ | ------------ |
| 6.0   | 3.8-3.11     | 16.0 or 17.0 |
| 5.2   | 2.7, 3.6-3.8 | 15.0         |

Depending on the operating system that you are using, some of the following pre-requisites might change.
They assume you have a macOS/Linux machine.

## Bootstrap a new Volto project

To bootstrap a new Volto project, you can use Yeoman [@plone/generator-volto](https://github.com/plone/generator-volto).
First, install it as a global tool (<a target="_blank" href="https://6.docs.plone.org/volto/recipes/creating-project.html">see instructions for installation</a>):

```{code-block} shell
npm install -g yo
npm install -g @plone/generator-volto
```

Then you can bootstrap the project with:

```{code-block} shell
yo @plone/volto volto-tutorial-project
```

The yo-based generator partially integrates add-ons (it can generate a
`package.json` with add-ons and workspaces already specified). When prompted
to add add-ons, choose `false`.

Now you can start your newly created Volto project:

```{code-block} shell
cd volto-tutorial-project
yarn start
```

You can then login with admin/admin at http://localhost:3000/login.

## Bootstrap an add-on

Let's start creating an add-on. We'll create a new package:
`volto-teaser-tutorial`. Inside your Volto project, bootstrap
the add-on by running (in the Volto project root):

```{code-block} shell
yo @plone/volto:addon
```

Note: You can also use the namespace like `@plone-collective/volto-teaser-tutorial` (or any other) is not required and is
optional. We're using namespaces for scoped package under some organisation.

Use `volto-teaser-tutorial` as the package name. After the
scaffolding of the add-on completes, you can check the created files in
`src/addons/volto-teaser-tutorial`.

Back to the project, you can edit `jsconfig.json` and add your add-on:

```{code-block} json
{
  "compilerOptions": {
    "baseUrl": "src",
    "paths": {
      "volto-teaser-tutorial": ["addons/volto-teaser-tutorial/src"]
    }
  }
}
```

```{note}
The `jsconfig.json` file is needed by Volto to identify development
packages. You are not strictly limited to Volto add-ons in its use, you
could, for example, use this to make it easier to debug third-party
JavaScript packages that are shipped transpiled.
```

### Volto addon script

Alternatively, if you already have an addon pushed to a remote repository and you want to create a volto development stack with it, you can use our addon script to easily scaffold a dev environment without creating a project externally.

```{code-block} shell
npx -p @plone/scripts addon clone [options] <source> [destination]
```

This command downloads the volto-teaser-tutorial add-on from its git repository's main branch, and will generate a project with the latest Volto version.

```{code-block} shell
npx -p @plone/scripts addon clone https://github.com/kitconcept/volto-teaser-tutorial.git --branch main
```

### (Optional) Use mrs-developer to sync add-on to GitHub

You can also immediately push the package to GitHub, then use `[mrs-developer]`
to manage the package and `jsconfig.json` changes.

Install mrs-developer as a development dependency by running:

```{code-block} shell
yarn add -W -D mrs-developer
```

Create a `mrs.developer.json` in your project with the following content (adjust it according
to your names and repository location):

```{code-block} json
{
  "volto-teaser-tutorial": {
    "url": "https://github.com/<namespace>/volto-teaser-tutorial.git",
    "path": "src",
    "package": "volto-teaser-tutorial",
    "branch": "main"
  }
}
```

Then run `yarn develop`, which will bring the package in `src/addons` and
adjust `jsconfig.json`.

### Add the add-on as workspace

The Volto project becomes a monorepo, with the Volto project being the "workspace root" and each add-on needs to be a "workspace", so that yarn knows that it should include that add-on location as a package and install its dependencies.

You could treat workspaces as major "working environment" for your project. So a yarn install would also install dependencies from `src/addons/*`

Change the Volto project's `package.json` to include something like:

```{code-block} json
{
  "private": "true",
  "workspaces": [
    "src/addons/volto-teaser-tutorial" // or simply src/addons/*
  ]
}
```

```{note}
Don't be scared by that `"private": "true"` in the Volto project `package.json`.
It's only needed to make sure you can't accidentally publish the package to NPM.
```

### Managing add-on dependencies

To be able to add dependencies to the add-on, you need to add them via the
workspaces machinery by running something like (at the Volto project root):

```{code-block} shell
yarn workspaces info
yarn workspace volto-teaser-tutorial add papaparse
```

````{note}
There are several other add-on templates, such as
[voltocli](https://github.com/nzambello/voltocli) or
[eea/volto-addon-template](https://github.com/eea/volto-addon-template).
You could very well decide not to use any of them, and instead bootstrap a new
add-on by running:

```{code-block} shell
mkdir -p src/addons/volto-teaser-tutorial
cd src/addons/volto-teaser-tutorial
npm init
```

Remember, an add-on is just a JavaScript package that exports
a configuration loader. Just make sure to point the `main` in
`package.json` to `src/index.js`.
````

### Load the add-on in Volto

To tell Volto about our new add-on, add it to the `addons` key of the Volto
project `package.json`:

```{code-block} js
// ...
"addons": ["volto-teaser-tutorial"]
// ...
```

## Add-ons - first look

Volto add-ons are just plain JavaScript packages with an
additional feature: they provide helper functions that mutate Volto's
configuration registry.

Their `main` entry in `package.json` should point to `src/index.js`,
which should be an ES6 module with a default export.
Here is the default add-on configuration loader:

```{code-block} js
export default (config) => {
  return config;
};
```

**Pro-Tip 💡**

```{note}
If you want to register a specific profile of an addon, wrap the configuration in a function and provide it after a colon(:) next to addon name. You can also provde a comma seperated multiple loaders profiles. Note the main configuration will be loaded always.
```

```{code-block} js
export function simpleLink(config) {
  return installSimpleLink(config);
}

export function tableButton(config) {
  return installTableButton(config);
}
```

```
 ...
"addons": [
"volto-slate:tableButton,simpleLink",
"@eeacms/volto-tabs-block",
]
...

```

## Documentation and Resources

Refer to the <a target="_blank" href="https://6.docs.plone.org/volto/index.html">official Volto documentation</a> for in-depth guides, tutorials, and examples.

Join the Volto community, participate in discussions, and ask questions on the Volto GitHub repository or the <a target="_blank" href="https://plone.org/news-and-events/news/2021/join-plone-chat-now-at-discord">Plone community chat on Discord</a>.

```{warning}
Getting started with Volto may seem complex at first, but with practice and exploration, you'll become more comfortable with its features and capabilities. It offers a powerful and flexible platform for building modern web applications with React and Plone.
```
