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

Talks are submitted. The jury votes for talks to be accepted or rejected.

````{card}
  In this part you will:
  
  - build your own Plone add-ons for backend and frontend.
  
  Topics covered:
  
  - Storing data in annotations
  - Custom REST API service
  - Backend package creation with {term}`plonecli`
  - Frontend package creation with Volto generator
  - Create React components to display voting behavior in frontend
  - Permissions
  
  The **voting story** spreads about the next chapters:
  
  ```{toctree}
  ---
  name: toc-voting-story
  maxdepth: 2
  numbered: 1
  ---

  behaviors_2
  endpoints
  volto_actions
  permissions
  ```
```````




Jury members shall vote for talks to be accepted or rejected.

For this we need:

- A behavior that stores the vote data in annotations
- A REST service for the frontend to communicate with
- A frontend component that displays votes and provides the ability to vote


(voting-story-backend-package-label)=

## Create a backend package

{term}`plonecli` is a tool to generate Plone backend packages and several features of a Plone backend add-on.
To install plonecli, run once:

```shell
pip install plonecli --user
```

We use plonecli to create a new package.

```shell
plonecli create addon backend/sources/training.votable
```

We press {kbd}`Enter` to all questions *except* 

```shell
--> Plone version [{PLONE_BACKEND_VERSION}]: {PLONE_BACKEND_VERSION}

--> Python version for virtualenv [python3]: python
```

The new package is created in directory `sources`.


## Integrate package in training setup

Before we implement our feature, we integrate the add-on by

- installing the add-on as a Python package
- updating the Zope configuration to load the add-on
- restarting the backend

Open `requirements.txt` and add your add-on to be installed as Python package.

```ini
-e sources/training.votable
```

Open `instance.yml` and add the add-on to tell Plone to load your add-on. With this the site administrator can activate the add-on per site.

```yaml
    load_zcml:
        package_includes: ["training.votable"]
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

We will use the Volto generator to create an add-on. Please install the tool once with:

```shell
npm install -g @plone/generator-volto
```

Now the frontend add-on can be generated. We call it 'volto-training-votable' to indicate that it is the corresponding part to our recently created backend package.

```shell
cd frontend
yo @plone/volto:addon
```

Choose "volto-training-votable" as name for your add-on.

Check {file}`package.json` to include the add-on in your app:

```shell
"private": true,
"workspaces": [
    "src/addons/*"
],
"addons": [
    "volto-custom-addon"
],
```

Install and start

```shell
make install
yarn start
```

We are now ready to implement our voting behavior in our new frontend add-on created in `frontend/src/addons/volto-training-votable/`.