---
myst:
  html_meta:
    "description": ""
    "property=og:description": ""
    "property=og:title": ""
    "keywords": ""
---

(exportimport-label)=

# Migrating with collective.exportimport

Export all content and settings that you want to keep from an old site and import it to a fresh site.

This approach allows you to migrate from Plone 4 to 6, from Python 2 to 3 and from Archetypes to Dexterity in one migration-step and is recommended for large and complex migrations.

The recommended tool for this is https://github.com/collective/collective.exportimport. An alternative is transmogrifier (see the training {ref}`training:transmogrifier-label`)

In export-import migrations you can shortcut most of the individual steps required for complex inplace migrations:

```{image} _static/exportimport-migration.png
:alt: The shortcut of a exportimport-migration.
```

## History

## When to use it


## How does it work?


## Step 1: Cleanup (optional)


## Step 2: Installation

You need to prepare the old site and the new site.

Both, the old site (the one with the 4.3 database) and the new site (without a database) need to be extended to have `collective.exportimport` and its dependencies made available.

### Installation in Plone 4.3

Since plone.restapi is not shipped with Plone 4.3 you need to add it to the buildout and pinn the latest version that supports Python 2 and Archetypes.

I recommend using custom config-files for that. Here is a `export.cfg`:

```ini
[buildout]
extends = buildout.cfg

eggs +=
    collective.exportimport

[versions]
# allways use the newest version!
collective.exportimport = 1.6
# Use the latest 7.x version for py2 and at support
plone.restapi = 7.8.0
pyrsistent = 0.15.7
hurry.filesize = 0.9
ijson = 3.1.4
```

### Installation in Plone 6.0

For Plone 6 you shoud use the version of restapi that is shipped with Plone.
You only need to add exportimport and pinn its dependencies:

Here is a `import.cfg`:

```ini
[buildout]
extends = buildout.cfg

eggs +=
    collective.exportimport

[versions]
# allways use the newest version!
collective.exportimport = 1.6
# Use the version that is shipped with your Plone version
# plone.restapi = 8.22.0
pyrsistent = 0.18.1
hurry.filesize = 0.9
ijson = 3.1.4
```


## Basic use and options

There is no need to install `collective.exportimport` in the extensions controlpanel.

Open the export-form `/@@export_content` and configure what you want to export.

## Step 3: Test export and import out-of-the-box



## Step 4: Extend default export and import

* Extension-strategy
* Hooks

### Add your own extension packages

For the old site:

```console
cd src
git clone https://github.com/starzel/contentexport.git
cd contentexport
```

Update your `export.cfg`:

```ini
[buildout]
extends = buildout.cfg

eggs +=
    collective.exportimport
    contentexport

auto-checkout +=
    contentexport

[sources]
contentexport = fs contentexport

[versions]
# allways use the newest version!
collective.exportimport = 1.6
# Use the version that is shipped with your Plone version
# plone.restapi = 8.22.0
pyrsistent = 0.18.1
hurry.filesize = 0.9
ijson = 3.1.4
```






```console
cd src
git clone https://github.com/starzel/contentimport.git
cd contentimport
```



## Step 5: Run all exports and import at once


## Step 6: Add fixes, changs and extensions


## Some more advanced examples


## Export from Plone 4.3

* dependencies (version-pinns)
* installation

## Import to Plone 6

* installation and use
* example

## Extending exportimport

* Custom packages based on https://github.com/starzel/minimal
  * contentexport
  * contentimport
* use `ExportAll`
* extend `CustomExportContent`
* extend `CustomImportContent`

## Advanced use-cases

* See https://github.com/collective/collective.exportimport/#faq-tips-and-tricks


## Further reading

```{seealso}

[Documentation of collective.exportimport](https://github.com/collective/collective.exportimport/#readme)

Talks:

* [A new hope for migrations and upgrades](https://www.youtube.com/watch?v=6xoXXyGnk4U) - Talk at Ploneconf 2021 (online).
* [collective.exportimport: Tips, tricks and deploying staging content](https://www.youtube.com/watch?v=SfHPKgeA0I0) - Talk at Ploneconf 2021 (online).
* [Make Plone Migrations fun again with collective.exportimport](https://www.youtube.com/watch?v=HEBF5VqlUc8) - Talk at World Plone Day 2021


Transmogrifier-Training:
{ref}`transmogrifier-label`

```
