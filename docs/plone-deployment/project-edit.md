---
myst:
  html_meta:
    "description": "A comprehensive guide on customizing and enhancing your Plone project for deployment."
    "property=og:description": "Learn how to edit, customize, and enhance your Plone project for optimal deployment."
    "property=og:title": "Customizing Your Plone Project for Deployment"
    "keywords": "Edit, Plone, Project, Add-ons, Volto, OAuth, GitHub"
---

# Customize Your Project

[Please fill this form](https://forms.gle/npDRESAud4ntDnUz7)

Plone offers a wealth of features right out of the box. You can extend these capabilities using {term}`TTW` modifications, such as creating new content types, altering the default workflow, or configuring the top-level navigation. For additional functionalities not covered by Plone, you can either develop your own solutions or integrate existing add-ons.

## Project packages

A Plone project is composed by, at least, a backend Python package and a frontend ReactJS package. These packages, generated for you during the creation of the codebase, are responsible for configuring the project and integrating third-party add-ons.

The packages for this training are:

- **ploneconf2025.core**: Package metadata located at `backend/pyproject.toml` and code at `backend/src/ploneconf2025/core`.
- **volto-ploneconf2025-core**: Package metadata located at `frontend/packages/volto-ploneconf2025-core/package.json` and code at `frontend/packages/volto-ploneconf2025-core/src`.

## Integrating Add-ons

Both Plone Frontend and Backend in your project support add-on integration. Add-ons can be specific to either the Frontend or Backend, or they can be collaborative packages enhancing both components.

- **Plone Backend Add-ons**: These are Python packages available on PyPI. [Awesome Plone](https://github.com/collective/awesome-plone) offers a curated list of these add-ons.
- **Plone Frontend Add-ons**: Written in JavaScript or TypeScript, these are released as NPM packages. Check out [Awesome Volto](https://github.com/collective/awesome-volto) for a collection of Frontend add-ons.

### Changing the default theme

We'll illustrate the process of integrating an add-on named `Volto Light Theme`, which provides a new theme for Volto. This add-on is composed by a frontend component, named `@kitconcept/volto-light-theme`, and a backend component named `kitconcept.voltolighttheme`.

#### Backend: Incorporating a New Dependency

First, we need to add the package as a dependency on the Python project by editing {file}`backend/pyproject.toml` and append `kitconcept.voltolighttheme` to the `dependencies` section. This will ensure the add-on will be available to Python.

Then we tell Zope to load the add-on run-time configurations by editing {file}`backend/src/ploneconf2025/core/dependencies.zcml` and append `kitconcept.voltolighttheme`

And, if we want to have this add-on installed when we create a new website, edit {file}`backend/src/ploneconf2025/core/profiles/default/metadata.xml` and append `kitconcept.voltolighttheme`


#### Frontend: Incorporating a New Dependency

Edit {file}`frontend/packages/volto-ploneconf2025/package.json` and append `@kitconcept/volto-light-theme` to the `addons` and `dependencies` sections, as shown below:

```json
"addons": [
  "...more add-ons",
  "@kitconcept/volto-light-theme"
],
"dependencies": {
  "...more dependencies": "*",
  "@kitconcept/volto-light-theme": "7.3.1"
}
```

Also, edit the {file}`frontend/volto.config.js` and change the theme to be `@kitconcept/volto-light-theme`:

```js
const addons = ['volto-ploneconf2025'];
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

## Modifying the default content

As you can see, the default content available just after the site creation is generic, but we can change that as well.

Feel free to edit the content of the site, upload images, design the frontpage with new blocks. When the content pleases you, stop the backend process and then run the following commands:

```shell
cd backend
make update-example-content
```

Now, if you run `git status` you should see changes to files under `backend/src/ploneconf2025/core/setuphandlers/examplecontent`. This is location where `plone.exportimport` will look for the content to be to your Plone site upon creation.

Now we are going to add these changes to our repository by running:

```shell
cd ../
make check
git add backend
git commit -m "Update example content"
git push
```

Which will trigger a run of the GitHub actions CI workflow, and if no error occurs, producing a new version of the backend container image.
