---
myst:
  html_meta:
    "description": "Controlling security with workflow"
    "property=og:description": "Controlling security with workflow"
    "property=og:title": ""
    "keywords": ""
---

(workflow-label)=

# Plone Workflow

About
: Controlling security with workflow

Level
: All levels

Status
: Work in progress

```{warning}
This chapter is still work in progress!
```

Workflow is used in Plone for three distinct, but overlapping purposes:

- To keep track of metadata, chiefly an object’s *state*;
- To create content review cycles and model other types of processes;
- To manage object security.

When writing content types, we will often create custom workflows to go with them.

Plone’s workflow system is known as DCWorkflow.
It is a *states-and-transitions* system, which means that your workflow starts in a particular *state*
(the *initial state*) and then moves to other states via *transitions* (also called *actions* in CMF).

When an object enters a particular state (including the initial state), the workflow is given a chance to update **permissions** on the object.

A workflow manages a number of permissions – typically the “core” CMF permissions like
{guilabel}`View`, {guilabel}`Modify portal content` and so on – and will set those on the object at each state change.

Note that this is event-driven, rather than a real-time security check: only by changing the state is the security information updated.

This is why you need to click {guilabel}`Update security settings` at the bottom of
the `portal_workflow` screen in the ZMI when you change your workflows’ security settings and want to update existing objects.

```{toctree}
:caption: Workflow
:hidden: true
:maxdepth: 3

introduction
roles-and-permissions
local-roles
dynamic-roles
placeful-workflow
workflow-chains
workflow-variables
generic-setup-export-import
```

```{toctree}
:caption: Plone Trainings
:hidden: true
:maxdepth: 3
:name: plone-trainings-workflow-toc
```

TODO:

- Add a use case story thread that runs through each of the sections to illustrate how each concept works
- Add in more screen shots of the {term}`TTW` (Trough-The_web) experience of using workflows in Plone
