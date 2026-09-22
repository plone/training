---
myst:
  html_meta:
    "description": "Introduction of the voting story – REST API services and React components"
    "property=og:description": "Introduction of the voting story – REST API services and React components"
    "property=og:title": "Create an add-on [The voting story]"
    "keywords": "Plone, Volto, React, add-on, development, developer, women in IT, REST API"
---

(voting-story-label)=

# Create an add-on [The voting story]

This chapter is a multi-part case study in which you will create an add-on to allow members of the conference program committee to vote for talk proposals.

````{card}
  In this part you will:
  
  - create your own Plone add-on with a backend and frontend
  - install the add-on in the main project in development mode
  
  Topics covered:
  
  - Add-on creation with {term}`Cookieplone`
````

```{toctree}
---
name: toc-voting-story
maxdepth: 1
hidden:
---

behaviors_2
endpoints
volto_actions
permissions
```

## The add-on concept

Program committee members shall vote for talks to be accepted or rejected.

For this we need:

- A behavior that stores the vote data in annotations
- A REST service for the frontend to communicate with
- A frontend component that displays votes and provides the ability to vote

Implementing this as a behavior in an add-on will make it possible to reuse the voting feature with other projects in the future.

```{note}
We recommend to follow the training step by step.

You can refer to the complete working add-on here:
https://github.com/collective/mastering-plone-votable-add-on
```


(voting-story-boilerplate-label)=

## Create the add-on

Use {term}`Cookieplone` to create the boilerplate for a new monorepo add-on.
Do this in the folder that contains the `mastering-plone-project`, not in the project folder.
The new add-on will go in its own git repository.

```shell
uvx cookieplone monorepo_addon
```

For {guilabel}`Add-on Title` enter `Mastering Plone Votable Add-on`.
For {guilabel}`Python Package Name` enter `ploneconf.votable`.
You can accept the defaults for the other questions.

When Cookieplone is finished, you should have a new folder `mastering-plone-add-on` that has its own `backend` and `frontend` subfolders.

```{tip}
The add-on template is similar to the project template, but adjusted for the add-on use case:
- It includes configuration to run continuous integration with multiple versions of Plone and Python.
- It includes commands to release the add-on on PyPI and npm.
```


(voting-story-install-add-on-label)=

## Install the development add-on in the project

The `mastering-plone-project` doesn't know about the new add-on.
We have to install it.

In {file}`mastering-plone-project/backend`, add the path to the backend add-on as an editable dependency.

```shell
uv add --editable ../../mastering-plone-votable-add-on/backend
```

"Editable" means that the add-on is installed as a link to the other folder you created.
Any changes made there will be immediately available without re-installing the add-on.

In {file}`mastering-plone-project/frontend/package.json`, add the frontend add-on to the dependencies.

```{code-block} json
:emphasize-lines: 5

  "dependencies": {
    "@plone/volto": "workspace:*",
    "@plone/registry": "workspace:*",
    "volto-ploneconf-site": "workspace:*",
    "volto-ploneconf-votable": "workspace:*"
  },
```

In {file}`mastering-plone-project/frontend/pnpm-workspace.yaml`, add the frontend add-on's path to the pnpm workspace.

```{code-block} yaml
:emphasize-lines: 6

packages:
  # all packages in direct subdirs of packages/
  - 'core/packages/*'
  - 'packages/*'
  - 'packages/**/packages/*'
  - '../../mastering-plone-votable-add-on/frontend/packages/*'
```

In {file}`mastering-plone-project/frontend/volto.config.js`, add the frontend add-on to the list of active add-ons.

```{code-block} js
:linenos:
:emphasize-lines: 1

const addons = ['volto-ploneconf-votable', 'volto-ploneconf-site'];
const theme = '';

module.exports = {
  addons,
  theme,
};
```

```{tip}
Be sure keep the main (project policy) package at the end of the array `addons`.
This way the main package can override add-on configurations.
```

Then run `make frontend-install`.

Finally, start the backend and frontend of the project.
Then go to the Add-ons control panel in Site Setup and install the Mastering Plone Votable Add-on.

````{tip}
Using local paths as the source for the add-ons only works if everyone working on your project has checked out the add-on repository in the same location.

If the add-on repository is on GitHub, you can add it from there.

For the backend:

```shell
uv add git+https://github.com/collective/mastering-plone-votable-add-on#subdirectory=backend
```

(However, in this case it cannot be installed in editable mode.)

For the frontend, edit {file}`mastering-plone-project/frontend/mrs.developer.json`.

```{code-block} json
:linenos:
:emphasize-lines: 10-19

{
  "core": {
    "output": "./",
    "package": "@plone/volto",
    "url": "git@github.com:plone/volto.git",
    "https": "https://github.com/plone/volto.git",
    "tag": "19.2.0",
    "filterBlobs": true
  },
  "volto-ploneconf-votable": {
    "develop": true,
    "output": "./packages",
    "package": "volto-ploneconf-votable",
    "path": "frontend/packages/volto-ploneconf-votable",
    "url": "git@github.com:collective/mastering-plone-votable-add-on.git",
    "https": "https://github.com/collective/mastering-plone-votable-add-on.git",
    "branch": "main",
    "filterBlobs": true
  }
}
```

Then run `make frontend-install`.

In this case you do not need a new entry in {file}`pnpm-workspace.yaml`, because mrs-developer clones the add-on repository in {file}`mastering-plone-project/frontend/packages`.
````

# Next steps

You are now ready to implement your voting behavior in the new add-on repository.

The **voting story** continues in the next chapters:

```{toctree}
---
maxdepth: 1
---

behaviors_2
endpoints
volto_actions
permissions
```
