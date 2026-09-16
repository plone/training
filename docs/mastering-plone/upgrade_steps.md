---
myst:
  html_meta:
    "description": "Provide upgrade steps for your changes."
    "property=og:description": "Provide upgrade steps for your changes."
    "property=og:title": "Upgrade steps"
    "keywords": "Plone, upgrade, versions"
---

(upgrade-steps-label)=

# Upgrade steps

```{card}
In this part you will:

- Write code to update, create and move content
- Enable features with upgrade steps

Tools and techniques covered:

- upgrade steps
```

````{card}

Check out `mastering-plone-project` at tag `schema`:

```shell
git checkout schema
```

The code at the end of the chapter:

```shell
git checkout upgrade_steps
```

More info in {doc}`code`
````

You recently changed the site configuration, when you added the behavior `ploneconf.featured` or when you turned talks into events in the chapter {doc}`events`.

When projects evolve you sometimes want to modify various things while the site is already up and brimming with content and users.
Upgrade steps are pieces of code that run when upgrading from one version of an add-on to a newer one.
They can do just about anything.
We will use an upgrade step to enable the new behavior instead of reinstalling the add-on.

Upgrade steps help make sure that changes are applied to multiple instances of the site in a consistent way.
For example, you might have multiple environments (development, staging, production) or multiple developers working on their own local copies of the site.
Once an upgrade step is defined, it can be applied in the same way to all of these, instead of making changes manually through the web.


(upgrade-steps-add-steps-label)=

## Add upgrade steps

We will create an upgrade step that:

- runs the typeinfo step, i.e. loads the GenericSetup configuration stored in `profiles/default/types.xml` and `profiles/default/types/...` so we don't have to reinstall the add-on to have our changes from above take effect.
- cleans up existing talks that might be scattered around the site in the early stages of creating it.
  We will move all talks to a (folderish) page `talks` (unless they already are there).

Upgrade steps can be registered in their own ZCML file to prevent cluttering the main {file}`configure.zcml`.

Update the file {file}`backend/src/ploneconf/site/upgrades/configure.zcml`:

```{code-block} xml
:linenos:
<configure
    xmlns="http://namespaces.zope.org/zope"
    xmlns:genericsetup="http://namespaces.zope.org/genericsetup"
    >

  <genericsetup:upgradeSteps
      profile="ploneconf.site:default"
      source="1000"
      destination="1001"
      >
    <genericsetup:upgradeDepends
        title="Update types"
        description="Run the typeinfo import step"
        import_steps="typeinfo"
        />
    <genericsetup:upgradeStep
        title="Clean up site structure"
        description="Move talks to to their page"
        handler="ploneconf.site.upgrades.v1001.cleanup_site_structure"
        />
  </genericsetup:upgradeSteps>

</configure>
```

The `upgradeDepends` directive runs the normal `typeinfo` import step, which is the one that processes the files in the profile's `types` folder.
The `upgradeStep` directive runs a custom handler that we will add below.

````{tip}
Have a look at Generic Setup import steps in the ZMI at http://localhost:8080/Plone/portal_setup/manage_importSteps to find the import step id.

```{figure} _static/import_steps.png
:alt: Import steps

Import step ids for upgradeDepends
```
````

The upgrade step is registered to run when the profile version increased from 1000 to 1001.
The current version is stored in {file}`profiles/default/metadata.xml`.
Change it to:

```xml
<version>1001</version>
```

Now let's add a file {file}`backend/src/ploneconf/site/upgrades/v1001.py` with our custom `cleanup_site_structure` handler code.

(upgrade-steps-pycode-label)=

```{code-block} python
:linenos:

from plone import api

import logging


logger = logging.getLogger(__name__)


def cleanup_site_structure(setup_tool):
    portal = api.portal.get()

    # Create the expected site structure
    if "training" not in portal:
        api.content.create(
            container=portal, type="Document", id="training", title="Training"
        )

    if "schedule" not in portal:
        schedule_folder = api.content.create(
            container=portal, type="Document", id="schedule", title="Schedule"
        )
    else:
        schedule_folder = portal["schedule"]
    schedule_folder_url = schedule_folder.absolute_url()

    if "location" not in portal:
        api.content.create(
            container=portal, type="Document", id="location", title="Location"
        )

    if "sponsors" not in portal:
        api.content.create(
            container=portal, type="Document", id="sponsors", title="Sponsors"
        )

    if "sprint" not in portal:
        api.content.create(
            container=portal, type="Document", id="sprint", title="Sprint"
        )

    # Find all talks
    brains = api.content.find(portal_type="talk")
    for brain in brains:
        if schedule_folder_url in brain.getURL():
            # Skip if the talk is already somewhere inside the target folder
            continue
        obj = brain.getObject()
        # Move talk to the folder '/schedule'
        api.content.move(source=obj, target=schedule_folder, safe_id=True)
        logger.info(f"{obj.absolute_url()} moved to {schedule_folder_url}")
```

We create the required site structure if it does not exist yet.
The code makes extensive use of `plone.api` as discussed in the chapter {doc}`api`.


(upgrade-steps-run-steps-label)=

## Run upgrade steps

After restarting the site we can run the upgrade step:

- Go to the {guilabel}`Add-ons` control panel <http://localhost:3000/controlpanel/addons>.
  The add-on `ploneconf.site` should now be marked with an {guilabel}`Update` label and have a button to upgrade from 1000 to 1001.
- Run the upgrade step by clicking on it.

On the console you should see logging messages like:

```
2024-09-15 11:26:14,114 INFO    [ploneconf.site.upgrades.v1001:83][waitress-0] http://localhost:3000/talks/test-talk moved to http://localhost:3000/schedule
```

Alternatively you can also select which upgrade steps to run like this:

- In the ZMI go to _portal_setup_
- Go to the tab {guilabel}`Upgrades`
- Select {guilabel}`ploneconf.site` from the dropdown and click {guilabel}`Choose profile`
- Run the upgrade step.

```{seealso}
<https://5.docs.plone.org/develop/addons/components/genericsetup.html#upgrade-steps>
```


(upgrade-steps-summary-label)=

## Summary

- You wrote your first upgrade step.
- You ran the upgrade step to apply changes to the existing site.
