(volto-custom-addon-label)=

# Extending Volto With Custom Add-on Package

````{sidebar} Volto chapter
```{figure} _static/volto.svg
:alt: Volto Logo
```

This chapter is about the React frontend Volto.

Solve the same tasks in classic frontend in chapter {doc}`eggs1`
````

~~~{sidebar} Get the code! ({doc}`More info <code>`)
Code for the beginning of this chapter:

```
git checkout TODO tag to checkout
```

Code for the end of this chapter:

```
git checkout TODO tag to checkout
```
~~~

As soon as you have repeating needs in Volto projects, you will want to move the code to an add-on that can be applied to multiple projects. One of several ways to start with a new add-on is the Yeoman generator we already used to initiate a Volto app.

(volto-custom-addon-preparation-label)=

If you haven't prepared Yeoman and the generator:

```bash
npm install -g yo
npm install -g @plone/generator-volto
```

Create a sandbox project

```bash
yo @plone/volto sandbox-volto-custom-addon
```

You see a dialog like this

```{code-block} console
:emphasize-lines: 6,9
:linenos: true

yo @plone/volto sandbox-volto-custom-addon
Getting latest Volto version
Retrieving Volto's yarn.lock
Using latest released Volto version: 11.1.0
? Project description A Volto-powered Plone frontend
? Would you like to add addons? true
? Addon name, plus extra loaders, like: volto-addon:loadExtra,loadAnotherExtra @greenthumb/volto-custom-addon
? Would you like to add another addon? false
? Would you like to add workspaces? true
```

@greenthumb/volto-custom-addon is the scoped package name of your add-on.

Go to the app folder:

```bash
cd sandbox-volto-custom-addon
```

You now have a Volto app configured for an add-on. An add-on is a Node package. It will live in the folder: {file}`src/addons/volto-custom-addon`.

Create your add-on with the generator:

```bash
yo @plone/volto:addon @greenthumb/volto-custom-addon
```

Update {file}`package.json`:

```bash
"private": true,
"workspaces": [
    "src/addons/*"
],
"addons": [
    "@greenthumb/volto-custom-addon"
],
```

Update {file}`jsconfig.json`:

```json
{
    "compilerOptions": {
        "paths": {
            "@greenthumb/volto-custom-addon": [
                "addons/volto-custom-addon/src"
            ]
        },
        "baseUrl": "src"
    }
}
```

Install and start

```bash
$ yarn
$ yarn start
```

(volto-custom-addon-final-label)=

```{admonition} Step to the next chapter and come back here for a release.
We will create a new block type in the next chapter {doc}`volto_custom_addon2`. We will do this in an add-on to apply the feature to multiple projects.
```

```{NOTE}
Coming back here with the new block type, you can now release the new add-on to npm. @greenthumb is your space. See <https://www.npmjs.com/package/release>
```

## Enrich an existing project with your new released add-on

You already released your add-on. Go on with {file}`package.json` and add your new add-on.

Update `package.json`:

```bash
"addons": [
  …
  "@greenthumb/volto-custom-addon"
],
"workspaces": [
  "src/addons/*"
],
"dependencies": {
  …
  "@greenthumb/volto-custom-addon": "1.0.1"
},
```

Modify versions as necessary.

Install new add-on and restart Volto:

```bash
$ yarn
$ yarn start
```

## Create a new project with your new released add-on

```bash
yo @plone/volto my-volto-project --addon collective/volto-custom-addon
```

Install and start

```bash
$ yarn
$ yarn start
```

## Footnotes

[yarn workspaces](https://classic.yarnpkg.com/en/docs/workspaces/)

: Workspaces are a new way to set up your package architecture. It allows you to setup multiple packages in such a way that you only need to run yarn install once to install all of them in a single pass.

[mrs.developer](https://www.npmjs.com/package/mrs-developer)

: Pull a package from git and set it up as a dependency for the current project codebase.
