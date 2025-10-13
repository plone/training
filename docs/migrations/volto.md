---
myst:
  html_meta:
    "description": "Migrate to Volto"
    "property=og:description": "Migrate to Volto"
    "property=og:title": "Migrate to Volto"
    "keywords": "Migration, Volto"
---

(migrate-to-volto-label)=

# Migrate to Volto

Please read the chapter {ref}`plone6docs:backend-migrate-to-volto-label` of the Plone Upgrade Guide. This explains mostly why you need to do what and how to use the form `@@migrate_to_volto` by hand.

You can (and should) use the power of that feature in your exportimport-based migration as described in https://github.com/collective/collective.exportimport#migrate-to-volto

The package `contentimport` has a version of `@@import_all` called `@@import_to_volto` that contains all the code used for that.

This will transform the imported content to work with Volto:

* Change html to blocks
* Turn Collections into Documents with Listing Blocks
* Turn Folders into (folderish) Documents
* Integrate default-pages into these Documents

A rather new alternative to that solution is to use [`collective.transmute`](https://github.com/collective/collective.transmute) to convert the data exported with `collective.exportimport` before it is imported so that the migration to Volto is already done by importing the converted data with `plone.exportimport`](https://github.com/plone/plone.exportimport).

Instead of using https://github.com/plone/blocks-conversion-tool to transform html to volto blocks it uses the new package [`collective.html2blocks`](https://collective.github.io/collective.html2blocks/) for that task.

```{seealso}
See {ref}`Prepare data with collective.transmute for import with plone.exportimport <transmute-label>`
```
