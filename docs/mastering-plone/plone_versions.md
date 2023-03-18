---
myst:
  html_meta:
    "description": "What's New in Plone?"
    "property=og:description": "What's New in Plone?"
    "property=og:title": "What's New in Plone?"
    "keywords": "New, Plone, release, notes, changes"
---

(plone-versions-label)=

# What's new Plone 6?

Plone is stable.  
Plone is developing.  

Is this contradictory?


(plone-versions-6-label)=

## Plone 6

% TODO wording: implemented on top of REST API?

Plone 6 comes with Volto, a new React based frontend for Plone, implemented on top of the Plone REST API.
This combines the stability, maturity, and security of the Plone backend with a modern, mature, user friendly and well maintained frontend.  
Volto provides a block based new editing experience.
Pages are assembled by content snippets, blocks.

Plone 6 continues to allow the current server side rendering and [Diazo](https://docs.plone.org/external/diazo/docs/index.html) theming without Volto.
This will be referred to as "Plone Classic UI".
The classic Barceloneta based frontend in Plone 6 is modernized to use [Bootstrap 5](https://getbootstrap.com/).
This frontend will stay in place to give developers and users time to adapt to Volto and to provide an easy upgrade path for existing projects.

Plone 6 will be a long term support (LTS) release.
We anticipate it will be around for several years.

Plone 6 supports Python 3 only and runs on top of Zope 5.

## Upgrade from earlier Plone versions

Sites on earlier versions can be upgraded.
  
Training {doc}`/migrations/index`  
Documentation {ref}`plone6docs:upgrade-guide-label`

