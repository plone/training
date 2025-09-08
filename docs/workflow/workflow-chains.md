---
myst:
  html_meta:
    "description": ""
    "property=og:description": ""
    "property=og:title": ""
    "keywords": ""
---

# Multi-chain Workflows

Multiple workflows can be very useful in case you have concurrent processes.

For example, an object may be published, but require translation.

You can track the review state in the main workflow and the translation state in another.

If you index the state variable for the second workflow in the catalog
(the state variable is always available on the indexable object wrapper
you only need to add an index with the appropriate name to `portal_catalog`)
you can search for all objects pending translation, for example using a *Collection*.

Workflows are mapped to types via the `portal_workflow` tool.
There is a default workflow, indicated by the string `(Default)`.
Some types have no workflow, which means that they hold no state information and typically inherit permissions from their parent.

It is also possible for types to have *multiple workflows*.
You can list multiple workflows by separating their names by commas.

This is called a *workflow chain*.

```{note}
In Plone, the workflow chain of an object is looked up by multi-adapting the object and the workflow to the `IWorkflowChain` interface.

The adapter factory should return a tuple of string workflow names (`IWorkflowChain` is a specialisation of `IReadSequence`, i.e. a tuple).

The default looks at the mappings in the `portal_workflow` tool,
but it is possible to override the mapping, e.g. by using a custom adapter registered for some marker interface,
which in turn could be provided by a type-specific behavior.
```

Multiple workflows applied in a single chain co-exist in time.

Typically, you need each workflow in the chain to have a different state variable name.
The standard `portal_workflow` API (in particular, `doActionFor()`, which is used to change the state of an object) also assumes the transition ids are unique.

If you have two workflows in the chain and both currently have a `submit` action available,
only the first workflow will be transitioned if you do `portal_workflow.doActionFor(context, ‘submit’)`.

Plone will show all available transitions from all workflows in the current object’s chain in the `State` drop-down,
so you do not need to create any custom UI for this.

Plone always assumes the state variable is called `review_state` (which is also the variable indexed in `portal_catalog`).
Therefore, the state of a secondary workflow won’t show up unless you build some custom UI (User Interface).

In terms of security, remember that the role-to-permission (and group-to-local-role) mappings are event-driven
and are set after each transition.

If you have two concurrent workflows that manage the same permissions,
the settings from the last transition invoked will apply.

If they manage different permissions (or there is a partial overlap) then only the permissions managed
by the most-recently-invoked workflow will change, leaving the settings for other permissions untouched.
