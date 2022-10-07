---
myst:
  html_meta:
    "description": ""
    "property=og:description": ""
    "property=og:title": ""
    "keywords": ""
---

# Editing your project

There are some changes possible in the project without writing code by just editing configuration.
A popular change is adding an add-on.

## About Add-Ons

Both Plone Frontend and Plone Backend allows adding add-ons.
Dependent on the add-on it could consist out of one part, like only for Plone Backend or only Plone Frontend.
Or it needs to install add-ons in both, working together.
If the latter is the case these are two differnent components.

Plone Frontend add-ons are written in Javascript and are released as NPM packages.
The Plone community maintains a curated list of Plone Frontend add-ons named [Awesome Volto](https://github.com/collective/awesome-volto).

Plone Backend add-ons are written in Python and are released on the Python Package Index (PyPI).
The Plone community maintains a curated list of Plone Backend and Plone Classic UI add-ons named [Awesome Plone](https://github.com/collective/awesome-plone).


## Starting the servers

After a [new project](new-project.md) was created lets check every thing runs as expected.

### Frontend
On a terminal, run the following code to start the frontend server:

```{code-base} shell
make start-frontend
```
After a while you should see:

TODO: Add image here

### Backend

On a second terminal, run the following code to start the backend server:

```{code-base} shell
make start-frontend
```

After a while you should see:

TODO: Add image here

## Check Local access

http://training.localhost:3000

## Stopping the servers

On both terminals press `Ctrl-c`.

# Adding OAuth Support

As an example for this training we add a new authentication method:
Login with GitHub.

There is already a plugin available consisting out of one module for Plone Frontend and another for Plone Backend.

The Plugin needs am application key from Github.

First you need to create a new application on GitHub ...

### Backend

Add `pas.plugins.authomatic`

### Frontend

Add @plonecollective/volto-authomatic
