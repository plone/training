---
myst:
  html_meta:
    "description": "Migrating Plone"
    "property=og:description": "Migrating Plone"
    "property=og:title": "Migrating Plone"
    "keywords": "Versions, Upgrade, Migration, Relaunch, Changes"
---

(migrations-label)=

# Migrating Plone

## Intro

* Who are you (name/country/company)
* What do you want to learn?
* What are your experiences with migrations so far?
* If you have brought a migration for the practive-part of the training:
    * What are the source- and target-versions?
    * Will you migrate to Volto?
    * What it special about it (e.g. content-types, size, features, design)?


## What are Migrations?

### Plone Versions

Like most software, Plone changes over time.
These changes are reflected in different releases of Plone.

The [release-schedule](https://plone.org/download/release-schedule) specifies, which versions are supported and for how long.

```{figure} https://plone.org/download/release-schedule/plone-release-schedule-2022-12-13.png/@@images/image
:alt: The Plone release schedule
```

Maintenance support
: Bug fixes and small new features are added.
  Around the end of maintenance support, a final release will be done.

Security support
: Plone security hotfixes will be made available for this series.
  For more information, see the [security update policy](https://plone.org/security/update-policy).

From the moment Plone 6 was released, Plone 6.0.x was under maintenance support, and Plone 5.2.x will be under security support when Plone 6.1 is released.
That means new features are being developed for Plone 6.1.x while bugfixes are being developed for Plone 6.0.x.

Plone intends to provide stable releases (for example, 5.2.14 is a stable release of the 5.2.x series).
Only bugfixes and changes that extend or improve an existing feature—as long as they don't break anything—make it into a bugfix release.


### What's in a Plone version?

In fact, it is even more complicated, because Plone consists of about 250 separate Python packages, all of which have their own versions and history.
Many of these Python packages are developed and released "inside" the Plone and Zope projects, but Plone also depends on more generic Python packages developed by third parties.
A Plone release such as Plone 5.2.6 (https://dist.plone.org/release/5.2.6/) pins all of these packages to a specific version, which altogether comprise a Plone version.

Each Plone version has a detailed change log that lists all changes that made it into that release, as compared to the previous release.
For an example see https://plone.org/download/releases/5.2.8.

```{note}
You can overrride the version of individual packages if a newer version has a feature or bugfix that you need.
Then you may be using Plone version 5.2.6, but `plone.app.contenttype = 2.2.2` instead of `2.2.2` with its version pinned for Plone 5.2.6.
You can do that, but at your own risk!
Only the officially pinned version are tested with each other.
```


### Why do we need to upgrade?

If you want to use a new feature or bugfix that your version does not yet have, then you need to upgrade.

That could be as simple as changing an `extends` in your buildout (or your cookieplone-based installation).

```ini
extends = https://dist.plone.org/release/5.2.6/versions.cfg
```

Would become the following.

```ini
extends =  https://dist.plone.org/release/5.2.9/versions.cfg
```

After changing the versions, you also need to run the installation, which reads the versions and downloads the updated packages from PyPI into your environment.

But you not only need to change the version of Plone you use, but you also need to update the database.

Since a Plone site stores content and settings in its database, these may need to be modified to reflect changes in the logic or configuration of Plone.
This is done by upgrade steps, or code that runs and updates the database to work with the new version.


## Update, Upgrade, Migration, or Relaunch?

Changing from `5.2.6` to `5.2.9` is usually not a migration, but an update or upgrade, more specifically a bugfix update.

Your could use the following:

Hotfix-Upgrade
: Adding a Hotfix to Plone without changing anything else.

Update
: Bugfix version changes, for example, `5.2.6` to `5.2.9` without additional changes.

Upgrade
: Bugfix or minor version change that gives you at least one new feature.
  For example, `5.2.6` to `5.2.9`, while adding `collective.easyform`, or even `5.0.8` to `5.1.7` when you don't change anything else.

Relaunch
: This includes the design, graphical appearance or theme, frontend libraries (such as Bootstrap), and content or content structure.

Migration
: The process of getting a database from one version of Plone to another version.

To make it even more confusing people use *Major Update* or *Major Upgrade* when in fact they are doing a *Relaunch*.

Good communication to manage expectations and imaginations is key!
Make sure that everyone knows what you are planning to do, no matter what you call it.

It can help to approach every non-trivial upgrade as a relaunch.
It is usually much easier to scale down expectations than up.

```{note}
Arguing for a required switch of a Python 2.7 installation of Plone 5.2.6 to Python 3 (while staying on 5.2.6) is hard without taking the opportunity to change the mobile navigation.

Suddenly it's a relaunch and everyone is excited.
```


(migrations-major-changes-label)=

## Dealing with major changes in Plone

In the history of Plone so far, there were three major changes:

* Plone 5.0: Dexterity replaces Archetypes
* Plone 5.2: Support for Python 3
* Plone 6.0: Volto as the new default frontend

Each of these major changes requires special treatment during an upgrade that makes upgrading much more complex.


(migrations-plone-5.0-dexterity-replaces-archetypes-label)=

### Plone 5.0: Dexterity replaces Archetypes

With Plone 5.0 the default framework for content types switched from Archetypes to Dexterity.

Up through Plone 5.2.x, there is a built-in migration from Archetypes to Dexterity, but it only supports Python 2.
See [Migration](https://pypi.org/project/plone.app.contenttypes) in the latest stable release of `plone.app.contenttypes` for details on the migration of custom and default content types to Dexterity.

Using [collective.exportimport](https://pypi.org/project/collective.exportimport/) you can export Archetypes content and import it as Dexterity content.


(migrations-plone-5.2-support-for-python-3-label)=

### Plone 5.2: Support for Python 3

Plone 5.2 added support for Python 3, while Plone 6.0 dropped support for Python 2.
This means that you can use Plone 5.2 to upgrade to Python 3.

This requires that you run Plone in Python 3 and only use code that supports Python 3.
It also requires that you migrate the database in a separate step from Python 2 to 3 while Plone is not running.

See the upgrade guides {doc}`plone6docs:backend/upgrading/version-specific-migration/upgrade-to-python3` and {doc}`plone6docs:backend/upgrading/version-specific-migration/upgrade-zodb-to-python3` for detailed information on these steps.

Using [`collective.exportimport`](https://pypi.org/project/collective.exportimport/), you can export content from Python 2 and import it in Python 3.


(migrations-plone-6.0-volto-as-new-frontend-label)=

### Plone 6.0: Volto as new frontend

Plone 6.0 comes with a new default frontend called {term}`Volto`.
It is written in React, and expects some subtle but important changes.

See {doc}`plone6docs:backend/upgrading/version-specific-migration/migrate-to-volto` for the specific migration steps.


### Transition periods for major changes

To make these major changes easier to manage, Plone provides a transition for all of these scenarios:

* You can use Dexterity starting with Plone 4.0, and use Archetypes until Plone 5.2 (as long as you use Python 2).
* Plone 5.2 can run with Python 2.7 and with Python 3, so you can first upgrade to 5.2 in Python 2 and then migrate to Python 3.
* Volto can be used with Plone 5.2 (even in 4.3, but please don't) and Plone 6 still has the Classic UI frontend, which is unlikely to go away in the near future.


```{note}
Another hurdle for upgrades between major version is that they have different themes:

* 4.x: Sunburst
* 5.x: Barceloneta
* 6.x: Pastanaga (Volto) / Barceloneta with Bootstrap 5 (Classic UI)
```


### What is a complex migration?

* Whenever you need to deal with one or more of the major changes in Plone.
* When you have to make changes to custom content or code.
* When you have to deal with outdated add-ons, such as `LinguaPlone`.


## Migration strategies

### In-place migrations

An in-place migration means the content and settings of a Plone installation are being updated while Plone is running.

In-place migrations can get very complex if you need to deal with multiple important changes.

```{image} _static/inplace-migration.png
:alt: The different steps of a complex inplace-migration.
```

These are discussed in the chapter {doc}`inplace`.


### Export/Import Migrations

This means you export all content and settings that you want to keep from an old site and import it into an empty, new site.

In export-import migrations, you can shortcut most of the individual steps required for complex in-place migrations:

```{image} _static/exportimport-migration.png
:alt: The shortcut of a exportimport-migration.
```

These are discussed in the chapter {ref}`exportimport-label`


## Dealing with problems and bugs

* Search for your issue. It is unlikely that you are the first person to encounter it.
* Ask in the Forum: https://community.plone.org/
* Ask in the Chat: https://discord.com/invite/zFY3EBbjaj
* Create a Ticket: https://github.com/plone/Products.CMFPlone/issues/
