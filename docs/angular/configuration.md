---
myst:
  html_meta:
    "description": ""
    "property=og:description": ""
    "property=og:title": ""
    "keywords": ""
---

# Managing The Plone Configuration From The Angular Project

We have been customizing our Plone backend instance in order to comply with our project needs.

Everything has been done through the Plone web interface, which is handy but not safe
(what if our server crashes and we need to build a new one with the same configuration,
what if we want to setup a development instance, how to manage the changes, etc.).

It would be much better to manage the entire Plone configuration from our Angular project
just like the rest of our code.

Fortunately, two tools will help us to achieve that:

- [collective.themesitesetup](https://github.com/collective/collective.themesitesetup/) allowing to manage a Plone configuration as part of a Plone theme,
- [plonetheme-upload](https://github.com/datakurre/plonetheme-upload) allowing to push a Plone theme from a local NPM project to a remote Plone backend.

## Creating A Theme To Handle The Configuration

```{note}
`collective.themesitesetup` is deployed by default on our Heroku instance.

If you use your own backend, you will need to deploy it.
```

We need to go to our Plone backend, then in {menuselection}`Site Setup --> Theming` we create a new theme.
Let's name it `plonecustom` for instance.

As we do not really want to customize our backend theme, it will be very simple.
The only file we will need here for now is `manifest.cfg`.
It will just be a copy of our default Barceloneta manifest:

```ini
 [theme]
 title = plonecustom
 description =
 rules = /++theme++barceloneta/rules.xml
 prefix = /++theme++barceloneta
 doctype = <!DOCTYPE html>
 enabled-bundles =
 disabled-bundles =

# Resources must be registered either here in the Diazo bundle or in registry.xml
development-css = /++theme++barceloneta/less/barceloneta.plone.less
production-css = /++theme++barceloneta/less/barceloneta-compiled.css
tinymce-content-css = /++theme++barceloneta/less/barceloneta-compiled.css
development-js =
production-js =

[theme:genericsetup]
```

As you can see, we have added an extra section named `[theme:genericsetup]`.
That's how collective.themesitesetup gets enabled.

Now we need to save our current Plone configuration into our theme.

We need to use the `collective.themesitesetup` export feature available here:
`http://whatever.herokuapp.com/Plone/++theme++plonecustom/@@export-site-setup`.

Obviously we do not need to export everything, in our current case we just want to get the comment feature related configuration and the content type configuration, so we just select `typeinfo` and `plone.app.registry`.

After clicking on `Export`, our theme will contain a new folder named `install`.

Now we can download our theme from the Theming control panel and extract the resulting .zip file in our Angular project which now contains a folder named `./plonecustom`.

## Pushing The Plone Configuration From The Angular Project

Let's add `plonetheme-upload` to our development dependencies:

```shell
npm install plonetheme-upload --dev
```

And let's add a new script in our {file}`package.json`:

```js
"scripts": {
  ...
  "update-backend": "plonetheme-upload --enable plonecustom http://whatever.herokuapp.com/Plone"
}
```

And now we can push our local `./plonecustom` to our Plone backend using the following command:

```shell
npm run update-backend
```
