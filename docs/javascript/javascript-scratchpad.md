---
myst:
  html_meta:
    "description": ""
    "property=og:description": ""
    "property=og:title": ""
    "keywords": ""
---

# Scratchpad

Scratchpad for text snippets to be included somewhere else in the training.

## General Advises

```{note}
When providing static resources (JS/Less/CSS) for Plone 5 resource registry, use [plone.resource](https://pypi.org/project/plone.resource) based resources instead of Zope browser resources.
The latter are cached heavily and you won't get your changes built with Zope resources.
```

```{note}
A bundle can depend on another.
This is mainly used for the order of inclusion in the rendered content.
Currently, it doesn't hook in the require JavaScript dependency mechanism.

This means, each bundle gets all their dependencies compiled in, which raise the response payload unnecessarily.
To avoid this, add your resources to existing bundles, like the `plone` bundle.
```

```{note}
The mockup grunt infrastructure is build with a convention over configuration approach in mind.

It is actually very picky about a lot of things: locations of your bundle files, location of your bundle LESS files, location of your pattern JavaScript and LESS files and the require JavaScript IDs of those.

Bundles have to be named `mockup-bundles-BUNDLENAME`, patterns have to be named `mockup-patterns-PATTERNNAME`.
```

```{note}
There is currently no API to build JavaScript and Less resources programmatically after importing them.
Both build steps need the Client side RequireJS respectively Less compilers.

The resources are downloaded to your browser, compiled there and re-upload to the Plone server, where they are stored in ZODB as `` plone.resource <https://pypi.org/project/plone.resource>`_ `` resources.

We can pre-build everything using standard JavaScript and Less development frameworks, e.g. via `mockup`'s Grunt infrastructure.
```

## Structure

About this training
: Training Agenda
  : DAY1

    : Framework Tools
      Create Mockup Pattern
      Integrate Other (Non-Mockup based) JavaScript

    DAY2

    : Practicing

Preparing for the training
: About JavaScript, Mockup, Patternslib and Plone 5

  : History of everything, What's what.

Installation Mockup

Development environment

: JavaScript and editor support
  Code Linter
  Grunt
  Bower
  Testing

Whirlwind tour through Mockup, Patternslib and JavaScript in Plone 5

: Short explanation of the code tree / main modules:
  Mockup
  Patternslib
  Plone 5

Developing a Pattern

: A Barebone Pattern

  : Based on collective.minimalpattern

    Pattern explained

  Adding a bower.json dependency

  Testing the Pattern

Integrating the Pattern

: Integration in Plone 5
  Integration in Plone 4
  Integration in Mockup w/out Plone

No-Pattern JavaScript in Plone

> The require JS (JavaScript) way
>
> The old, require JS-less way

Using other Frameworks in Plone

> Angular JS
> React JS

Comparison to other frameworks

> Patternslib and Web Components
> Patternslib and React Components
> Patternslib and Angular JS directives
> Plone and ES 6
