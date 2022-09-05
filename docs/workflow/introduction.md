---
myst:
  html_meta:
    "description": ""
    "property=og:description": ""
    "property=og:title": ""
    "keywords": ""
---

# Introduction To Workflows

## What Is A Workflow?

Workflow is the series of interactions that should happen to complete a task.
Business organizations have many kinds of workflow.

For example, insurance companies process claims, delivery companies track shipments, and schools accept applications for admission.

All these tasks involve several people, sometimes take a long time, and vary significantly from organization to organization.

The goal of workflow software is to streamline and track workflow activity.
Since different organizations have different workflow processes, workflow software must be flexible and easy to customize.

The workflow system inside of Plone is an example of a State Machine.

From [Wikipedia](https://en.wikipedia.org/wiki/Finite-state_machine):

```{eval-rst}
.. pull-quote:: A finite-state machine (FSM) or finite-state automaton (plural: automata), or simply a state machine, is a behavioral model used to design computer programs. It is composed of a finite number of states associated to transitions. A transition is a set of actions that starts from one state and ends in another (or the same) state. A transition is started by a trigger, and a trigger can be an event or a condition.
```

- Any object controlled by workflow is **always** in precisely one `state` from each workflow in its chain.
- The `state` in which an object is currently located controls what `transitions` are available to it
- Any workflow can be diagrammed, showing the available states and the transitions between them
  : - Diagrams like this can be of enormous help in understanding your workflow
    - You should always sketch up a diagram when you start figuring out the workflow you want

```{image} _static/simple_workflow.png
```

## What's In a Workflow?

### Workflows Control

- What `states` and `transitions` are available

- Which `permissions` will be managed (permissions not managed are left untouched from their current value by the workflow)

- Which `groups` will be managed (see `states` below for more about this)

- Which `variables` will be tracked by the workflow (values are set and stored every time a transition occurs)

- What `worklists` will be generated (you can return lists of content matching values tracked by `variables`

- What `scripts` are available to be used in conjunction with `transitions`

  - These are basic python scripts, and are not used much anymore now that `events` are available

### States Control

- What transitions are available **out**

- What `permissions` are assigned to which `roles` *locally* to the object

- What `groups` are assigned to which `roles` *locally* to the object

  - This is probably the least-used aspect of workflow
  - It can be spectacularly useful

### Transitions Control

- What `state` they will end in

- What conditions or `guards` are required for the transition to be available

  - These can be `permissions` of the user, `roles` a user has, `groups` to which the user belongs, or even the boolean value of *'TALES*' expressions

- What `scripts` will be executed before and after the transition occurs (again, not used much now that we have `events`)

- How the transition is triggered

  - This can be user-initiated *or* automatic

    - Automatic transitions happen when an object lands in a state from which they are a valid exit, **and** that object fulfills **all** conditions for the transition to be available.

    - If the conditions for the automated transition are **not** met, then the transition doesn't happen

      - Updating the object to meet the conditions will not kick it off
      - You'll have to back it out of the current `state` and re-do the transition that should have kicked it off

## How Does Workflow Work In Plone?

The tool in Plone that handles all workflow is called `portal_workflow`

- Types must be `workflow` aware

  - Types in Plone are made *WorkflowAware* by a base content mixin from CMFCore `WorkflowAware` (in `CMFCatalogAware`

- Workflow is assigned by *type*

  - Each type gets a *chain*
  - A chain can have more than one workflow in it

- `portal_workflow` is responsible for keeping track of all information about the workflow state of an object

  - A particular content object knows **nothing** about it's own workflow state
  - queries about the workflow of an object **must** be addressed to portal_workflow

```python
 >>> from plone import api
 >>> fpage = api.content.get("/front-page")
 >>> fpage.review_state
 Traceback (most recent call last):
   File "<stdin>", line 1, in <module>
 AttributeError: review_state
 >>> api.content.get_state(fpage)
 'published'
 >>> wft = api.portal.get_tool('portal_workflow')
 >>> wft.getChainFor(fpage)
 ('simple_publication_workflow',)
 >>> wft.getTransitionsFor(fpage)
 ({'description': 'If you submitted the item by mistake or want to perform additional edits, this will take it back.', 'title': 'Member retracts submission', 'url': 'http://nohost/Plone/front-page/content_status_modify?workflow_action=retract', 'id': 'retract', 'title_or_id': 'Member retracts submission', 'name': 'Retract'}, {'description': 'Sending the item back will return the item to the original author instead of publishing it. You should preferably include a reason for why it was not published.', 'title': 'Reviewer sends content back for re-drafting', 'url': 'http://nohost/Plone/front-page/content_status_modify?workflow_action=reject', 'id': 'reject', 'title_or_id': 'Reviewer sends content back for re-drafting', 'name': 'Send back'})
>>> with api.env.adopt_user('content'):
...     contrib-page = api.content.create(container=api.portal.get(), type="Document", title="Content Contrib Page")
...     [i['id'] for i in wft.getTransitionsFor(api.content.get("/content-contrib-page")]
...
['submit']
>>> with api.env.adopt_roles(roles=['Manager',]):
...     [i['id'] for i in wft.getTransitionsFor(contrib-page)]
...
['submit', 'publish']
```

- `portal_workflow` is security conscious, for all aspects of workflow it respects and validates the access levels of the current user

  - Users can only access the workflow information for which they have permissions

```python
>>> with api.env.adopt_user('site-admin'):
...     wft.getTransitionsFor(fpage)
...
>>> from pprint import pprint
>>> pprint(wft.getTransitionsFor(fpage))
({'description': 'If you submitted the item by mistake or want to perform
                  additional edits, this will take it back.',
  'id': 'retract',
  'name': 'Retract',
  'title': 'Member retracts submission',
  'title_or_id': 'Member retracts submission',
  'url': 'Plone/front-page/content_status_modify?workflow_action=retract'},
 {'description': 'Sending the item back will return the item to the original
                  author instead of publishing it. You should preferably include
                  a reason for why it was not published.',
  'id': 'reject',
  'name': 'Send back',
  'title': 'Reviewer send content back for re-drafting',
  'title_or_id': 'Reviewer send content back for re-drafting',
  'url': 'Plone/front-page/content_status_modify?workflow_action=reject'})
```

## Moving Content Through Workflows

- As stated above, any object with workflow is **always** in exactly **one** `state` for each workflow in it's chain.

> - When you initiate a transition, it is **instantaneous**.
>
> - What happens when this occurs?
>
>   1. The `BeforeTransitionEvent` is notified, and any subscribers to that event are executed
>   2. Any `before script` registered for the transition are executed.
>   3. The `transition` takes place
>
>   > - values are set for the variables registered by the workflow
>   >
>   > - the new `state` of the object is set
>   >
>   > - the new set of permissions values for roles and groups are calculated and updated
>   >
>   >   - first permissions are remapped
>   >   - then group -> role mappings are changed
>   >
>   > - the object is re-indexed for all *security related* indexes.
>
>   4. Any `after script` registered for the transition is executed
>   5. The `AfterTransitionEvent` is notified, and any subscribers to that event are executed
>
> In general, transitions are triggered by user action.  This takes place when a user clicks on the *state* menu in the Plone UI and selects an available transition, or when the user presses *save* from the **Change State** dialog found in the folder listing view.
>
> - As stated above, automatic transitions are found as a result of undergoing manual transitions.
>
>   - Step 3 above can actually be executed **multiple** times when a user triggers a `transition`.
>   - Events and scripts are executed for **each** transition that happens
>   - For this reason, when subscribing to workflow events, it's a good idea to check *which* transition just happened *before* taking any actions in your handler:

```python
def handleWorkflowTransition(ob, event):
    """ a handler meant to be used after a 'publish' transition """
    if event.transition != 'publish':
        return
    ...
```
