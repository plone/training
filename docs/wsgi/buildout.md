---
myst:
  html_meta:
    "description": ""
    "property=og:description": ""
    "property=og:title": ""
    "keywords": ""
---

(wsgi-buildout-label)=

# Buildout for the training

The buildout for the training is [here](https://github.com/collective/wsgitraining_buildout)

The buildout consists of self contained configuration files for the topics covered in the chapters.
It also contains an add on package called wsgitrainging.site.
We need the `mr.developer` extension to be able to use the `wsgitraining.site` package, but also because we want a source checkout of `plone.recipe.zope2instance` to get the latest features.
wsgitraining.site has a couple of browser views needed for demonstrations and tests throughout the training.
The specific buildout configurations can be build with `buildout -c <feature.cfg>`.
Notes in the specific training sections show the command line to invoke.
