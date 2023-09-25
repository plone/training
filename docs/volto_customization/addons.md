---
myst:
  html_meta:
    "description": "Volto add-ons for beginners"
    "property=og:description": "Volto add-ons"
    "property=og:title": "Volto add-ons"
    "keywords": "Volto, Training"
---

# Volto add-ons

## Bootstrap a new Volto project

To bootstrap a new Volto project, you can use Yeoman [@plone/generator-volto](https://github.com/plone/generator-volto).
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

Let's start creating an add-on. We'll create a new package:
`volto-teaser-tutorial`. Inside your Volto project, bootstrap
the add-on by running (in the Volto project root):

```shell
yo @plone/volto:addon
```

Note: You can also use the namespace like `@plone-collective/volto-teaser-tutorial` (or any other) is not required and is
optional. We're using namespaces for scoped package under some organisation.

Use `volto-teaser-tutorial` as the package name. After the
scaffolding of the add-on completes, you can check the created files in
`src/addons/volto-teaser-tutorial`.

Back to the project, you can edit `jsconfig.json` and add your add-on:

```json
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

```shell
npx -p @plone/scripts addon clone [options] <source> [destination]
```

This command downloads the volto-teaser-tutorial add-on from its git repository's main branch, and will generate a project with the latest Volto version.

```shell
npx -p @plone/scripts addon clone https://github.com/kitconcept/volto-teaser-tutorial.git --branch main
```

### (Optional) Use mrs-developer to sync add-on to GitHub

You can also immediately push the package to GitHub, then use `[mrs-developer]`
to manage the package and `jsconfig.json` changes.

Install mrs-developer as a development dependency by running:

```shell
yarn add -W -D mrs-developer
```

Create a `mrs.developer.json` in your project with the following content (adjust it according
to your names and repository location):

```json
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

```json
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

```shell
yarn workspaces info
yarn workspace volto-teaser-tutorial add papaparse
```

````{note}
There are several other add-on templates, such as
[voltocli](https://github.com/nzambello/voltocli) or
[eea/volto-addon-template](https://github.com/eea/volto-addon-template).
You could very well decide not to use any of them, and instead bootstrap a new
add-on by running:

```shell
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

```js
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

```jsx
export default (config) => {
  return config;
};
```

**Pro-Tip 💡**

```{note}
If you want to register a specific profile of an addon, wrap the configuration in a function and provide it after a colon(:) next to addon name. You can also provde a comma seperated multiple loaders profiles. Note the main configuration will be loaded always.
```

```js
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
