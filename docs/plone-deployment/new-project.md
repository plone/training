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

We use [make](https://www.gnu.org/software/make/) here because it is well understood, just works, is mature and wide spread available.
For build and deployment this is an important criteria.
Future plans are to use make's dependency management and include capabilities more here, and in the dependent Makefiles.

## Installing the codebase and dependencies

On the root of the project repository, run:

```{code-base} shell
make install
```
```{note}
This command could take a long time on the first time you run it, as it will download and install all Plone dependencies and also all NPM packages used by Volto.
```