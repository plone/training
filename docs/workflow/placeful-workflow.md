---
myst:
  html_meta:
    "description": ""
    "property=og:description": ""
    "property=og:title": ""
    "keywords": ""
---

# Placeful Workflow

Sometimes you may want a specific section of the site to allow different permissions and roles than other areas
of the site such as providing an intranet are for internal staff to collaborate.
In the past, if you wanted to do this, you would need to make custom content types that were identical to the
standard types so you can attach an alternate workflow policy to them to limit access.

This causes extra boilerplate code and confusion amongst your users as they just want to create standard "Pages",
but in this area they may have to create "Intranet Pages".

Plone comes standard with a feature that addresses this specific issue.

Plone's "Workflow Policy Support" add-on is available, but not active by default and allows site administrators to
define workflow policies that only apply in specific sections of the site.

The name Placeful Workflow comes from the fact you do this in a specific place.

Placeful workflow allows you to define workflow policies that define content type to workflow mappings that can be applied
in any sub-folder of your Plone site.

## Getting Started

To get started with Placeful Workflow in Plone, you will need to first activate the add-on
via the {menuselection}`Site Setup -> Add-Ons` control panel.

Click {guilabel}`Activate` next to the "Workflow Policy Support" add-on and you will be ready to start assigning local policies to folders.

Create or go to any folder inside of your site and click the workflow state menu and you will now see an option for `Policy...`.

Select this option to begin assigning local workflow mappings to this folder.

By default, the Placeful Workflow product has created some default mappings for you:

- Intranet -- Sets the default workflow policy to `Intranet/Extranet`
- Old Plone -- Sets the default workflow policy to `Community Workflow`
- One State -- Sets the default workflow policy to `Single State Workflow`
- Simple Publication -- Sets the default workflow policy to `Simple Publication Workflow`

From the `Workflow Policies` control panel, you can create your own custom mappings and then assign them via the `Policy...` menu option per folder inside your site.

## Internals Of Placeful Workflow

This works by providing a more specific `adapter` for the `IWorkflowChain` interface defined by DCWorkflow.

It means that when you install this product, the `portal_workflow` tool is marked with an `IPlacefulWorkflow` interface,
and from then on, the adapter defined by the product is used when looking up the workflow chain for an object

```{tip}
A great example of the [marker pattern](https://5.docs.plone.org/external/plone.app.dexterity/docs/behaviors/providing-marker-interfaces.html)
```

- You add a *workflow policy* in the location where you want to have customized workflow assignments.

- A `policy` is basically just a mapping of workflows to content types.
  Like what you see in {menuselection}`ZMI -> portal_workflow -> workflows`

  - This policy can control workflow ''in'' the object where it is located, and *below* it

    - *In* means the policy applies to the object itself and its content.
    - *Below* means that the policy applies only to any contained items (and their contents as well), but not to the original object.

* All this can be handled by GenericSetup as well

  - `portal_placeful_workflow.xml` allows you to declare the presence of policies

  - This is accompanied by a folder of the same name (minus the 'xml' part, of course)

    - The folder contains one file per policy: `policy_name.xml` where *policy_name* is replaced by the actual name of your policy

  - Once you've generated a policy, you can add an 'import step' in GenericSetup to use it somewhere (this must be done in code)

portal_placeful_workflow.xml:

```xml
<?xml version="1.0"?>
<object name="portal_placeful_workflow" meta_type="Placeful Workflow Tool">
 <object name="intranet-content" meta_type="WorkflowPolicy"/>
</object>
```

intranet-content.xml:

```xml
<?xml version="1.0"?>
<object name="member-content" meta_type="WorkflowPolicy">
 <property name="title">Member Content Policy</property>
 <bindings>
  <default>
   <bound-workflow workflow_id="intranet_workflow"/>
  </default>
  <type default_chain="true" type_id="Document"/>
  <type default_chain="true" type_id="Event"/>
  <type default_chain="true" type_id="Folder"/>
  <type default_chain="true" type_id="Link"/>
  <type default_chain="true" type_id="News Item"/>
  <type default_chain="true" type_id="Topic"/>
 </bindings>
</object>
```

the setup:

```python
def set_intranet_workflow_policy(portal):
    # assume code that finds or creates the portal location where the policy should apply
    # the result of this code is 'folder'

    folder.manage_addProduct['CMFPlacefulWorkflow']\
        .manage_addWorkflowPolicyConfig()
    pc = getattr(folder, WorkflowPolicyConfig_id)
    pc.setPolicyIn('intranet-content')
    pc.setPolicyBelow('intranet-content')
```
