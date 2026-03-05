---
myst:
  html_meta:
    "description": "How to edit, customize, and enhance your Plone project for optimal deployment"
    "property=og:description": "How to edit, customize, and enhance your Plone project for optimal deployment"
    "property=og:title": "Customize your Plone project for deployment"
    "keywords": "edit, Plone, project, add-ons, Volto, OAuth, GitHub"
---

# Customize your project

[Please fill this form](https://forms.gle/ihYVZxmnypwBnZk39).

Plone offers a wealth of features right out of the box. You can extend these capabilities using {term}`TTW` modifications, such as creating new content types, altering the default workflow, or configuring the top-level navigation. For additional functionalities not covered by Plone, you can either develop your own solutions or integrate existing add-ons.

## Project packages

A Plone project is composed by, at least, a backend Python package and a frontend React package. These packages, generated for you during the creation of the code base, are responsible for configuring the project and integrating third-party add-ons.

The packages for this training are:

`pybr25.core`
:   Package metadata located at {file}`backend/pyproject.toml` and code at {file}`backend/src/pybr25/core`.

`volto-pybr25-core`
:   Package metadata located at {file}`frontend/packages/volto-pybr25-core/package.json` and code at {file}`frontend/packages/volto-pybr25-core/src`.

## Integrate add-ons

Both Plone frontend and backend in your project support add-on integration. Add-ons can be specific to either the frontend or backend, or they can be collaborative packages enhancing both components.

Plone backend add-ons
:   These are Python packages available on PyPI.
    [Awesome Plone](https://github.com/collective/awesome-plone) offers a curated list of these add-ons.

Plone frontend add-ons
:   Written in JavaScript or TypeScript, these are released as npm packages.
    Check out [Awesome Volto](https://github.com/collective/awesome-volto) for a collection of frontend add-ons.

### Change the default theme

We'll illustrate the process of integrating an add-on named `Volto Light Theme`, which provides a new theme for Volto. This add-on is composed by a frontend component, named `@kitconcept/volto-light-theme`, and a backend component named `kitconcept.voltolighttheme`.

#### Backend: incorporate a new dependency

First, we need to add the package as a dependency on the Python project by editing {file}`backend/pyproject.toml` and append `kitconcept.voltolighttheme` to the `dependencies` section. This will ensure the add-on will be available to Python.

```{code-block} toml
:emphasize-lines: 6
:caption: {file}`backend/pyproject.toml`

dependencies = [
    "Products.CMFPlone==6.1.3",
    "plone.api",
    "plone.restapi",
    "plone.volto",
    "kitconcept.voltolighttheme",
]
```

Then we tell Zope to load the add-on run-time configurations by editing {file}`backend/src/pybr25/core/dependencies.zcml` and append `kitconcept.voltolighttheme`.

```{code-block} xml
:emphasize-lines: 6
:caption: {file}`backend/src/pybr25/core/dependencies.zcml`

<?xml version="1.0" encoding="utf-8"?>
<configure xmlns="http://namespaces.zope.org/zope">
  <include package="plone.restapi" />
  <include package="plone.volto" />
  <include package="plone.app.caching" />
  <include package="kitconcept.voltolighttheme" />
</configure>
```

And, if we want to have this add-on installed when we create a new website, edit {file}`backend/src/pybr25/core/profiles/default/metadata.xml` and append `profile-kitconcept.voltolighttheme:default`.

```{code-block} xml
:emphasize-lines: 8
:caption: {file}`backend/src/pybr25/core/profiles/default/metadata.xml`

<?xml version="1.0" encoding="utf-8"?>
<metadata>
  <version>1000</version>
  <dependencies>
    <dependency>profile-plone.volto:default</dependency>
    <dependency>profile-plone.app.caching:default</dependency>
    <dependency>profile-plone.app.caching:with-caching-proxy</dependency>
    <dependency>profile-kitconcept.voltolighttheme:default</dependency>
  </dependencies>
</metadata>
```


#### Frontend: incorporate two new dependencies

Edit {file}`frontend/packages/volto-pybr25/package.json`, add `@kitconcept/volto-light-theme` and `@plone-collective/volto-image-editor` to the `addons` and `dependencies` sections, as shown below:

```json
"addons": [
  "...more add-ons",
  "@plone-collective/volto-image-editor",
  "@kitconcept/volto-light-theme"
],
"dependencies": {
  "...more dependencies": "*",
  "@kitconcept/volto-light-theme": "7.3.1",
  "@plone-collective/volto-image-editor": "1.0.0-alpha.1"
}
```

Also, edit the {file}`frontend/volto.config.js` and change the theme to be `@kitconcept/volto-light-theme`:

```js
const addons = ['volto-pybr25'];
const theme = '@kitconcept/volto-light-theme';

module.exports = {
  addons,
  theme,
};
```

#### Reinstalling the Project

Execute `make install` from the repository root to install the new add-on and update both the {file}`backend/uv.lock` and {file}`frontend/pnpm-lock.yaml`.

#### Restarting the Project

Start your project with `make backend-start` and `make frontend-start` in different shells.
Navigate to http://localhost:3000.

You should see the new theme applied to your project

#### Committing Changes

Format your codebase with `make check`, then commit and push the changes:

```shell
git add backend frontend
git commit -m "Add Volto Light Theme"
git push
```

## Update behaviors for the Plone site

To ensure the behaviors manually applied to the Plone Site persist after the site is re-created, we need to add them via Generic Setup.

Create a new file {file}`backend/src/pybr25/core/profiles/default/types/Plone_Site.xml` with the following content:

```xml
<?xml version="1.0" encoding="utf-8"?>
<object xmlns:i18n="http://xml.zope.org/namespaces/i18n"
        meta_type="Dexterity FTI"
        name="Plone Site"
>

  <!-- Enabled behaviors -->
  <property name="behaviors"
            purge="false"
  >
    <element value="voltolighttheme.header" />
    <element value="voltolighttheme.theme" />
    <element value="voltolighttheme.footer" />
    <element value="kitconcept.footer" />
  </property>


</object>
```

## Modify the default content

As you can see, the default content available just after the site creation is generic, but we can change that as well.

Feel free to edit the content of the site, upload images, design the frontpage with new blocks. When the content pleases you, stop the backend process and then run the following commands:

```shell
cd backend
make update-example-content
```

Now, if you run `git status` you should see changes to files under {file}`backend/src/pybr25/core/setuphandlers/examplecontent`. This is the location where `plone.exportimport` will look for the content to be for your Plone site upon creation.

Now we are going to add these changes to our repository by running:

```shell
cd ../
make check
git add backend
git commit -m "Update example content"
git push
```

Which will trigger a run of the GitHub actions CI workflow, and if no error occurs, producing a new version of the backend container image.
