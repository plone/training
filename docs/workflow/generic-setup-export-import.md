---
myst:
  html_meta:
    "description": ""
    "property=og:description": ""
    "property=og:title": ""
    "keywords": ""
---

# Using GenericSetup to Manage Plone Workflows

Workflows provide a great amount of flexibility inside of Plone. They have many moving parts such as states, transitions, permissions, variables, worklist and groups. Plone gives you the ability to configure all of these items through the web via the ZMI, but moving these settings to another environment as part of a release or migration can be error prone.

The GenericSetup tool inside of plone, which has the id of `portal_setup`, provides a way to serialize the current state of your workflow polices into a XML file that can be put into your own custom add-on packages. Using this export/import tool, you can now track changes to your workflow polices inside of your source control tools and create releases that allow exact replication of the settings to new or existing environments.

## Getting Started

Creating a workflow from scratch using the XML format is tricky at best. It is recommended that you start from the ZMI and copy/paste an existing workflow that most closely matches your business need and use it as a starting point. The changes to the workflow can be configured via the ZMI and then exported to the filesystem for inclusion in your product.

## Exporting Workflow Policies

Once your workflow is working locally for your needs, you can export your workflow using the `portal_setup` tool in the ZMI.

1. Login to the ZMI and click `portal_setup`
2. Click the `Export` tab
3. Check the box for `Workflow Tool` (and optionally `Placeful Workflow Policies`)
4. Click the button at the bottom of the page to `Export selected steps`

This will download a files called `setup_tool-[sometimestamp].tar.gz` to your local computer. This tarball will include the `workflows.xml` profile that describes all of the content to workflow policy bindings as well as the export of each workflow policy as an xml file.

These will be the files you will place in your custom product's profiles directory so it can be imported when using it in another instance. You will need to modify the `workflows.xml` file prior to importing since it contains all of the bindings and you will only want to include bindings that are specific to your custom add-on.

Example `workflows.xml`:

```xml
<?xml version="1.0"?>
<object name="portal_workflow">
  <object name="example_workflow" meta_type="Workflow" />
  <object name="example_container_workflow" meta_type="Workflow" />
  <bindings>
    <type type_id="Example Type">
      <bound-workflow workflow_id="example_workflow" />
    </type>
    <type type_id="Example Container">
      <bound-workflow workflow_id="example_container_workflow" />
    </type>
  </bindings>
</object>
```

In this example, the rest of the bindings have been removed so we are only controlling the needed workflows for our product.

The tarball will have a directory called `workflows` that contains each workflow policy for the site.  You can remove all of the stock ones and just keep the policies referenced by your `workflows.xml` for import later.

Subsequent updates to your workflow polices can either be made directly on the files system and then re-imported into the site. Or you can make the changes via the ZMI, but you will need to remember to re-export them using this same process and placing the updated files back into your add-on code.

## Importing Workflow Policies

There are several options available for re-importing your workflows back into the site.  The `portal_setup` tool provides an option for doing a `Tarball Import`, but this doesn't allow you to keep your modified workflows alongside the code in your add-on product. It is recommended that you export your workflow polices using the steps above and place them in your add-on products *default* GenericSetup policy or include them as part of an upgrade step.

Typically, your GenericSetup profiles will be stored in the `profiles` directory of your add-on product. Each subdirectory of the `profiles` directory is usually registered as a separate GenericSetup extension profile or they are used as part of an upgrade step registered to one of these profiles.

Once you have wired the GenericSetup profile folder to your product using ZCML, you can now do the following to import your workflow policies to your current site.

1. Login to the ZMI and click `portal_setup`
2. Click the `Import` tab
3. Select your GenericSetup profile by either *id* or *title*
4. Select how you want to import your profile, if you have run the import already and your policies are part of the profile directly (not upgrade steps), you will want to select the option to `Apply all profiles`
5. Click the button to `Import all steps`

If you only want to run the `Workflow Tool` steps, you will need go to the `Advanced Import Tab` and select your profile by *id* or *title* and then check the box for just `Workflow Tool` and click `Import selected steps`.

Using upgrade profiles is similar, but you will instruct Plone to run a function when upgrading from one version to the next. This function will call up an already registered *migration profile* and run it against the site. These upgrade steps will only run if the version of your product doesn't satisfy the version requirements that were configured via ZCML.
