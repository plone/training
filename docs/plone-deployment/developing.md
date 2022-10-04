---
myst:
  html_meta:
    "description": ""
    "property=og:description": ""
    "property=og:title": ""
    "keywords": ""
---

# Developing the Project

## Installing the codebase and dependencies

On the root of the project repository, run:

```{code-base} shell
make install
```
```{note}
This command could take a long time on the first time you run it, as it will download and install all Plone dependencies and also all NPM packages used by Volto.
```

## Starting the servers

### Frontend
On a terminal, run the following code to start the frontend server:

```{code-base} shell
make start-frontend
```
After a while you should see:

TODO: Add image here

### Backend

On a terminal, run the following code to start the backend server:

```{code-base} shell
make start-frontend
```
