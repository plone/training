---
About: Migrating website content into a Plone site using Transmogrifier
Level: Intermediate Developers
---

(transmogrifier-label)=

# Migrating Content with Transmogrifier

**Training Objective**

This training will cover the necessary steps to export your current site's content
and migrate it to a new Plone site. The import process uses an add-on called
'Transmogrifer'.

In the [Calvin and Hobbes universe](https://www.gocomics.com/calvinandhobbes/1987/03/23), the Transmogrifier is an invention of Calvin's that would turn one thing into another.
Similarly, [collective.transmogrifier](https://github.com/mjpieters/collective.transmogrifier)
provides support for building pipelines that turn one thing into another, hence greatly facilitating content import and export.
This is a life saver when you need to migrate content from one site to another, regardless of the CMS platform.

```{toctree}
:caption: Transmogrifer
:hidden: true
:maxdepth: 3

Export Current Site Content <export>
Transmogrifier Basics <basics>
Before Running the Import <before-import>
Writing the Import Pipeline <pipeline>
Writing Custom Blueprints <blueprints>
Running the Import <import>
Advanced Pipeline Tips <advanced-import>
Advanced Blueprint Tips <advanced-blueprint>
```

```{toctree}
:caption: Plone Trainings
:hidden: true
:maxdepth: 3
:name: plone-trainings-transmogrifer-toc
```

```{seealso}
- <https://docs.plone.org/external/collective.transmogrifier/docs/source/index.html>
```

% The following items are hidden in this toctree to prevent Sphinx warnings.

```{toctree}
:hidden: true

users-migration
```
