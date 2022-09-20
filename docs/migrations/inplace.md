---
myst:
  html_meta:
    "description": ""
    "property=og:description": ""
    "property=og:title": ""
    "keywords": ""
---

(inplace-label)=

# In-place migrations

## When to use them and when not

## What to do?

## Upgrade-Steps

## Helpers

## Frequent Problems

* Can take a long time (AT => DX)
* Invalid data. See [Growing pains: PosKeyErrors and other malaises](https://www.youtube.com/watch?v=SwxN3BBxAM8) and https://www.starzel.de/blog/zodb-debugging

## Examples

* Large: dipf-www as a large inplace-migration with 4.3 => 6.0-pre-alpha
* Small: Something from 5.0 to 5.1 or 5.2 to 6.0?

## Further reading

```{seealso}

Documentation:

* {ref}`plone6docs:plone-upgrade-guide-label`

Helper-Packages:

* [collective.migrationhelpers](https://github.com/collective/collective.migrationhelpers) - Helpers and examples to use during migrations. Useful to copy & paste the code from here to your own packages.
* [plone.app.upgrade](https://github.com/plone/plone.app.upgrade/) - Upgrade steps of the Plone core and some useful helpers.
* [ftw.upgrade](https://github.com/4teamwork/ftw.upgrade) - An upgrade control panel and upgrade helpers for plone upgrades.

Talks:

* [Migrations! Migrations! Migrations!](https://www.youtube.com/watch?v=ZIN1qmhMHJ4) - Talk at Ploneconf 2019 in Ferrara.
* [How to upgrade sites to Plone 5](https://www.youtube.com/watch?v=bQ-IpO-7F00) - Talk at Ploneconf 2015 in Bucharest.
* [Archetypes to Dexterity Migration](https://vimeo.com/110992921) - Talk at Ploneconf 2014 in Bristol.
* [Migrations, Upgrades and Relaunches](https://www.youtube.com/watch?v=1Qx0JALp3lQ) - Talk at Ploneconf 2013 in Brazilia.
```