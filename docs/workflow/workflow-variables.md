---
myst:
  html_meta:
    "description": ""
    "property=og:description": ""
    "property=og:title": ""
    "keywords": ""
---

# Workflow Variables

```{warning}
This section is not ready for prime time
```

State changes result in a number of variables being recorded, such as the actor (the user that invoked the transition),
the action (the id of the transition), the date and time and so on.

The list of variables is dynamic, so each workflow can define any number of variables linked to TALES expressions that
are invoked to calculate the current value at the point of transition.

Of course, the workflow keeps track of the current state.

The state is exposed as a special type of workflow variable called the state variable.
Most workflows in Plone uses the name review_state as the state variable.

Workflow variables are recorded for each state change in the workflow history.

This allows you to see when a transition occurred, who effected it, and what state the object was in before or after.

In fact, the "current state" of the workflow is internally considered to be the most recent entry in the workflow history.

Workflow variables are also the basis for worklists.

They are basically canned queries run against the current state of workflow variables.

Plone's review portlet shows all current worklists from all installed workflows.

This can be a bit slow, but it does meant that you can use a single portlet to display an amalgamated list of all items
on all worklists that apply to the current user. Most Plone workflows have a single worklist that matches on the review_state variable,
e.g. showing all items in the pending state.
