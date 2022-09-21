---
myst:
  html_meta:
    "description": ""
    "property=og:description": ""
    "property=og:title": ""
    "keywords": ""
---

(migrations-label)=

# Migrating Plone

## Intro

* What do you want to learn?
* What are your experiences with migrations so far?
* What are your next use-cases?


## What are Migrations?

### Plone Versions

Like most software Plone changes over time.
These changes are reflected in different releases of Plone.

The [release-schedule](https://plone.org/download/release-schedule) specifies, which versions are supported for how long.

```{figure} https://plone.org/download/plonereleaseschedule-2022-09-12.png/@@images/image
:alt: The Plone release schedule
```

* **Maintenance support**: Bug fixes and small new features are added. Around the end of maintenance support, a last release will be done.
* **Security support**: Plone security hotfixes will be made available for this series.
  For more information, see the [security update policy](https://plone.org/security/update-policy).

Currently Plone 6.0.x is under maintenance support and Plone 5.2.x is under security support.
That means new features are being developed for Plone 6.1.x and bugfixes are being developed for Plone 6.0.x

Plone wants to offer stable releases (e.g. 5.2.8 is a stable release of the 5.2.x series).
Only bugfixes and changes that extend or improve a existing feature - as long as they don't break anything - make it into a bugfix-release.


### What's in a Plone version?

In fact it is even more complicated because Plone consists of about 250 separate Python packages all of which have their own versions and history.
A Plone-release, e.g. Plone 5.2.6 (https://dist.plone.org/release/5.2.6/) pinns all of these packages to a specific version and that alltogether is than a Plone version.

Each Plone version has a detailed changelog that lists all changes that made it into that release as compared to the previous release.
For a example see https://plone.org/download/releases/5.2.8

```{note}
You can overrride the version of individual packages if a newer version has a feature or bugfix that you need.
Then you may be using Plone Version 5.2.6 but `plone.app.contenttype = 2.2.2` instead of `2.2.2` with is the version pinned for Plone 5.2.6.
You can do that but at your own risk!
Only the officially pinned version are tested with each other.
```

### Why do we need to upgrade?

If you want to use a new feature or bugfix that your Version does not yet have you need to upgrade.

That could be as simple as changing a extends in your buildout from

```ini
extends = https://dist.plone.org/release/5.2.6/versions.cfg
```

to

```ini
extends =  https://dist.plone.org/release/5.2.9/versions.cfg
```

But you not only need to change the version of Plone you use but also need to update the database.

Since a Plone site stores content and settings in its database these may need to be modified to reflect changes in the logic or configuration of Plone.
This is done by upgrade steps, code that runs and updates the database to fix with the new version.

## Update, Upgrade, Migration or Relauch?

Changing from `5.2.6` to `5.2.9` is usually not a migration but a update or upgrade, more specifically a bugfix-update.

Your could use the following:

* **Hotfix-Upgrade**: Adding a Hotfix to Plone without changing anything else.
* **Update**: Bugfix Version changes. E.g. `5.2.6` to `5.2.9` without additional changes.
* **Upgrade**: Bugfix or Minor version change that gives you at least one new feature. E.g. `5.2.6` to `5.2.9` while adding `collective.easyform` or even `5.0.8` to `5.1.7` when you don't change anything else.
* **Relaunch**: The design, content-structure or mayor version changes.
* **Migration**: The process of getting a Database from one version of Plone to another version.

To make it even more confusing people use *Mayor Update* or *Mayor Upgrade* when in fact they are doing a *Relaunch*.

Good communication to manage expectations and imaginations is key!
Make sure that everyone knows what you are planning to do, no matter what you call it.

It can help to approach every non-trivial upgrade as a relaunch.
It is usually much easier to scale down expectations that up.

```{note}
Arguing for a required switch of a Python 2.7 installation of Plone 5.2.6 to Python 3 (while staying on 5.2.6) is hard without taking the opportunity to change the mobile navigation.

Suddenly it's a relaunch and everyone is excited.
```

## Dealing with Mayor Changes in Plone

In the history of Plone there were so far three mayor changes:

* Plone 5.0: Dexterity replaces Archetypes
* Plone 5.2: Support for Python 3
* Plone 6.0: Volto as new default frontend

Each of these mayor changes require special treatment during an upgrade that make upgrading much more complex.

To make these mayor changes easier to manage Plone allows a transition period for all of these:

* You can use Dexterity starting with Plone 4.3 and can use Archetypes until Plone 5.2 (as long as you use Python 2)
* Plone 5.2 runs in Python 2 and in Python 3 so you can first upgrade to 5.2 in Python 2 and then to Python 3.
* Volto can be used with Plone 5.2 (even 4.3, but please don't!) and Plone 6 still has the Classic frontend (which is unlikely to go away in the near future).

Another hurdle for upgrades between mayor version is that they have different themes:

* 4.x: Sunburst
* 5.x: Barceloneta
* 6.x: Pastanaga (Volto) / Barceloneta with Bootstrap 5 (Classic)

## What is a complex migration?

* Whenever you need to deal with one of the mayor changes in Plone
* When you have to make changes to custom content or code
* When you have to deal with outdated add-ons

## Migration Strategies

### Inplace Migrations

A inplace migration means the content and settings of a Plone installation are being updated while Plone is running.
These upgrades use a builtin tool and basically run upgrade-steps that are collected in [plone.app.upgrade](https://github.com/plone/plone.app.upgrade/).

This approach is recommended for all upgrades of minor version and can work fine for most mayor upgrades.
When dealing with mayor changes in Plone or with very large or complex installations a export-import based migration (see below) is often the better solution.

During in-place migrations it is advisable to **not make large leaps** in version numbers.
A single upgrade should not try to bridge multiple major version numbers.

Going from Plone 4.0 to Plone 5.1 is fine.

If you are at Plone 2.5 and want to upgrade to the latest Plone 5, you should approach this in several steps:

- First upgrade from Plone 2.5 to the latest Plone 3 version (3.3.6).
- Then upgrade from Plone 3 to the latest Plone 4 version.
- Then upgrade from Plone 4 to the latest Plone 5 version.


### Export-import Migrations

Export all content and settings that you want to keep from an old site and import it to a fresh site.

This approach allows you to migrate from Plone 4 to 6, from Python 2 to 3 and from Archetypes to Dexterity in one migration-step and is recommended for large and complex migrations.

The recommended tool for this is https://github.com/collective/collective.exportimport. An alternative is transmogrifier (see the training {ref}`training:transmogrifier-label`)

## Dealing with problems and bugs

* Forum
* Chat
* Tickets
