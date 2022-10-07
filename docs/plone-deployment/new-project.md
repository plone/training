---
myst:
  html_meta:
    "description": ""
    "property=og:description": ""
    "property=og:title": ""
    "keywords": ""
---

# A new Plone 6 project

## Creating the structure with cookiecutter

```{code-block} shell
cookiecutter gh:collective/cookiecutter-plone-starter
```

## A Tour of your Codebase

### CI Configuration

{file}`/.github`

### Frontend {file}`/frontend`

### Backend {file}`/backend`

### Devops {file}`/devops`

### Documentation {file}`/docs`

### Makefile {file}`/Makefile`

TODO: Explain why we use make


## Installing the codebase and dependencies

On the root of the project repository, run:

```{code-base} shell
make install
```
```{note}
This command could take a long time on the first time you run it, as it will download and install all Plone dependencies and also all NPM packages used by Volto.
```