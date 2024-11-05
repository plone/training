---
myst:
  html_meta:
    "description": "Introduction of the voting story – REST API services and React components"
    "property=og:description": "Introduction of the voting story – REST API services and React components"
    "property=og:title": "Reusable features packaged in add-ons – the voting story"
    "keywords": "Plone, Volto, React, add-on, development, developer, women in IT, REST API"
---


(voting-story-label)=

# Roundtrip [The voting story] frontend, backend, and REST

You will enhance the Plone Conference site with the following behavior:

Talks have been submitted.
The jury votes for talks to be accepted or rejected.

````{card}
  In this part you will:
  
  - build your own Plone add-ons for backend and frontend.
  
  Topics covered:
  
  - Storing data in annotations
  - Custom REST API service
  - Backend package creation with {term}`Cookieplone`
  - Frontend package creation with {term}`Cookieplone`
  - Create React components to display voting behavior in frontend
  - Permissions
  
  The **voting story** spreads about the next chapters:
  
  ```{toctree}
  ---
  name: toc-voting-story
  maxdepth: 2
  ---

  behaviors_2
  endpoints
  volto_actions
  permissions
  ```
````


Jury members shall vote for talks to be accepted or rejected.

For this we need:

- A behavior that stores the vote data in annotations
- A REST service for the frontend to communicate with
- A frontend component that displays votes and provides the ability to vote

```{note}
It is recommended to follow the training by building step by step a new backend add-on and a new frontend add-on.

The complete working code can be found here:
https://github.com/collective/training.votable
https://github.com/collective/volto-training-votable
```


(voting-story-backend-package-label)=

## Create a backend package

We use [Cookieplone](https://github.com/plone/cookieplone) to create a new backend add-on.

Install `Cookieplone`:

```shell
pipx install cookieplone
```

We use `Cookieplone` to create a new package.
Go to directory `sources` of your backend and run:

```shell
cd backend/sources
pipx run cookieplone
```

In the following chapters we assume the package is named `training.votable`.


## Integrate backend package in training setup

Before we implement our features, we integrate the add-on by

- installing the add-on as a Python package
- updating the Zope configuration to load the add-on
- restarting the backend

Open `requirements.txt` and add your add-on to be installed as Python package.

```ini
-e sources/training.votable
```

Open `instance.yml` and add the add-on to tell Plone to load your add-on.
With this the site administrator can activate the add-on per site.

```yaml
zcml_package_includes: training.votable, ploneconf.site
```

To apply the changes of the configuration, please build and restart the backend with:

```shell
make build
make start
```

The add-on can now be activated for our site `Plone`.
Please head over to http://localhost:8080/Plone/prefs_install_products_form and activate / install the new add-on.


(voting-story-frontend-package-label)=

## Create a Volto add-on

We will use `Cookieplone` to create an add-on.

If not already done or needs to be updated, install/update `Cookieplone` with:

```shell
pipx install cookieplone
```

Now the frontend add-on can be generated.
We call it 'volto-training-votable' to indicate that it is the corresponding part to our recently created backend package `training.votable`.

We generate the package in our frontend and integrate it for development.

```shell
cd frontend/packages
pipx run cookieplone
```

Choose "volto-training-votable" as name for your add-on.

## Integrate frontend add-on in training setup

Check {file}`volto.config.js` to include the add-on in your app:

```shell
const addons = ['volto-training-votable', 'volto-ploneconf'];
const theme = '';

module.exports = {
  addons,
  theme,
};
```

Be sure keep the main (project policy) package at the end of the array `addons`.
By this the main package can override add-ons configurations.

Check {file}`packages.json` to include the add-on in your app:

```shell

  "dependencies": {
    "@plone/volto": "workspace:*",
    "@plone/registry": "workspace:*",
    "volto-training-votable": "workspace:*",
    "volto-ploneconf": "workspace:*"
  },
```

Check `pnpm-workspace.yaml` to let "volto-training-votable" be present in the pnpm workspace.

```xml
packages:
  # all packages in direct subdirs of packages/
  - 'core/packages/*'
  - 'packages/*'
  - 'packages/volto-training-votable/packages/volto-training-votable'
```

Install and start

```shell
make install
make start
```

You are now ready to implement your voting behavior in your new frontend add-on created in `frontend/packages/volto-training-votable/`.
