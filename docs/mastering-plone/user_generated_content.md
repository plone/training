---
myst:
  html_meta:
    "description": "Configure who can edit what"
    "property=og:description": "Configure who can edit what"
    "property=og:title": "Workflow, roles and permissions"
    "keywords": "Plone, Volto, workflow, role, local role, permission"
---

(user-content-label)=

# Workflow, roles and permissions

```{card}
In this part you will:

- Allow self-registration
- Constrain which content types can be added to the schedule folder
- Grant local roles
- Create a custom workflow for talks

Tools and techniques covered:

- folder constraints
- local roles
- workflow
```

````{card}

Check out `mastering-plone-project` at tag `block`:

```shell
git checkout block
```

The code at the end of the chapter:

```shell
git checkout user_generated_content
```

More info in {doc}`code`
````

How do prospective speakers submit talks?
We let them register on the site and grant the right to create talks.
For this we go back to changing the site through the web.


(user-content-self-reg-label)=

## Self-registration

- Go to the {guilabel}`Security` control panel at <http://localhost:3000/controlpanel/security> and enable self-registration.
- Leave {guilabel}`Enable User Folders` off unless you want a community site, in which users can create any content they want in their home folder.
- Select the option {guilabel}`Use email address as login name`.


(user-content-constrain-types-label)=

## Constrain types to be addable

On the schedule page, select {guilabel}`Restrictions…` <http://localhost:8080/Plone/schedule/folder_constraintypes_form> from the {guilabel}`Add new` menu. 
Restrict to only allow adding talks.

```{note}
This action is only available in Plone's Classic UI frontend, and not its Volto frontend.
```


(user-content-local-roles-label)=

## Grant local roles

On the schedule page, go to {guilabel}`Sharing`.
Check the box for {guilabel}`Can add` for the group {guilabel}`Logged-in users`, and save.
Now every logged-in user can add content in this folder (and only this folder).

The {guilabel}`Can add` column grants the `Contributor` role to this group within this folder.

By combining the type constraints and the local roles on this folder, we have made it so that non-admin users can create and submit talks inside the schedule.


(user-content-custom-workflow-label)=

## A custom workflow for talks

We still need to fix a problem: Authenticated users can see all talks, including those of other users, even if those talks are in the private state.
Since we do not want this, we will create a modified workflow for talks.
The new workflow will only let them see and edit talks they created themselves and not the ones of other users.

- Go to the {menuselection}`ZMI --> portal_workflow`: http://localhost:8080/Plone/portal_workflow/manage
- See how talks have the same workflow as most content, namely {guilabel}`(Default)`
- Go to the tab {guilabel}`Contents`, check the box next to {guilabel}`simple_publication_workflow`, click {guilabel}`copy` and {guilabel}`paste`.
- Rename the new workflow from `copy_of_simple_publication_workflow` to `talks_workflow`.
- Edit the workflow by clicking on it: Change the Title to `Talks Workflow`.
- Click on the tab {guilabel}`States` and click on {guilabel}`private` to edit this state.
  In the next view select the tab {guilabel}`Permissions`.
- Find the table column for the role {guilabel}`Contributor` and remove the permissions for {guilabel}`Access contents information` and {guilabel}`View`. Note that the {guilabel}`Owner` role (that's the creator) still has some permissions.
- Do the same for the state {guilabel}`pending`
- Go back to {guilabel}`portal_workflow` and set the new workflow {file}`talks_workflow` for talks.
  Click {file}`Change` and then {file}`Update security settings`.

The new workflow allows contributors to see and edit talks they created themselves, but not talks submitted by other contributors until they are published.


(user-content-fs-label)=

## Move the changes to the file system

We don't want to do these steps for every new conference by hand so we move the changes into our Generic Setup profile.

### Export the workflow

- Export the Generic Setup step _Workflow Tool_ in <http://localhost:8080/Plone/portal_setup/manage_exportSteps>.

- Copy the file {file}`workflows.xml` into {file}`backend/src/ploneconf/site/profiles/default` and clean out everything that is not related to talks.

  ```xml
<?xml version="1.0"?><object meta_type="Plone Workflow Tool"
        name="portal_workflow"
>
  <object meta_type="Workflow"
          name="talks_workflow"
  />
  <bindings>
    <type type_id="talk">
      <bound-workflow workflow_id="talks_workflow" />
    </type>
  </bindings>
</object>
```

- Copy {file}`workflows/talks_workflow/definition.xml` into {file}`backend/src/ploneconf/site/profiles/default/workflows/talks_workflow/definition.xml`.
  (The other files are just definitions of the default workflows, and we only want things in our package that changes Plone.)

### Enable self-registration

To enable self-registration you need to change the global setting that controls this option.
Most global setting are stored in the registry. You can modify it by adding the following to {file}`src/ploneconf/site/profiles/default/registry/main.xml`:

```{code-block} xml
<record name="plone.enable_self_reg">
  <value>True</value>
</record>
```

### Grant local roles and constrain types to be addable

Since the granting of local roles applies only to a certain folder in the site, we could easily do it by hand instead of writing code for it.
But for testability and repeatability (there is a conference every year!), we should create the initial content structure automatically and also apply needed local roles.

Let's add an upgrade step to do this as well as importing the workflow and new registry setting.

Update the profile version in {file}`backend/src/ploneconf/site/profiles/default/metadata.xml`:

```{code-block} xml
:linenos:
:emphasize-lines: 3

<?xml version="1.0" encoding="utf-8"?>
<metadata>
  <version>1004</version>
  <dependencies>
    <dependency>profile-plone.volto:default</dependency>
    <dependency>profile-plone.app.caching:default</dependency>
    <dependency>profile-plone.app.caching:with-caching-proxy</dependency>
  </dependencies>
</metadata>
```

Register the new upgrade step in {file}`backend/src/ploneconf/site/upgrades/configure.zcml`:

```{code-block} xml
  <genericsetup:upgradeSteps
      profile="ploneconf.site:default"
      source="1003"
      destination="1004"
      >
    <genericsetup:upgradeDepends
        title="Add talks workflow"
        description="Run workflow and plone.app.registry import steps"
        import_steps="plone.app.registry workflow"
        />
    <genericsetup:upgradeStep
        title="Configure talk permissions"
        description="Configure local roles and type constraints for talk schedule"
        handler="ploneconf.site.upgrades.v1004.configure_talk_permissions"
        />
  </genericsetup:upgradeSteps>
```

Create the file {file}`backend/src/ploneconf/site/upgrades/v1004.py`:

```{code-block} python
:linenos:

from plone import api
from Products.CMFPlone.interfaces import constrains
import logging

logger = logging.getLogger(__name__)


def configure_talk_permissions(context):
    talks_folder = api.content.get("/schedule")

    # Allow logged-in users to create content
    api.group.grant_roles(
        groupname='AuthenticatedUsers',
        roles=['Contributor'],
        obj=talks_folder)

    # Constrain addable types to talk
    behavior = constrains.ISelectableConstrainTypes(talks_folder)
    behavior.setConstrainTypesMode(constrains.ENABLED)
    behavior.setLocallyAllowedTypes(['talk'])
    behavior.setImmediatelyAddableTypes(['talk'])
    logger.info(f'Added and configured {talks_folder.absolute_url()}')
```

Once we apply the upgrade step, the schedule page is updated with the appropriate local roles and constraints.


## Exercise

In {doc}`upgrade_steps` we wrote an upgrade step to create the basic page structure of the site.
But we want that to be created not only during an upgrade, but also when a new site is created by hand or in tests.

One way to do this is to create a list of dictionaries containing the type, parent and title plus optionally workflow state etc. to create an initial structure.
In some projects it could also make sense to have additional profiles besides `default`:

- a `demo` or `content` profile that creates the initial structure
- a `testing` profile that creates dummy content (talks, speakers etc) for tests

Create an optional Generic Setup profile `content` that creates the content, grants local roles and sets constraints.

````{dropdown} Solution
:animate: fade-in-slide-down
:icon: question

Register the profile in {file}`profiles.zcml`

```{code-block} xml

<genericsetup:registerProfile
    name="content"
    title="PloneConf Site initial content"
    directory="profiles/content"
    description="Extension profile to add initial content"
    provides="Products.GenericSetup.interfaces.EXTENSION"
    post_handler=".setuphandlers.post_handler_content"
    />
```

Also add a {file}`profiles/content/metadata.xml` so the default profile gets automatically installed when installing the content profile.

```{code-block} xml
<metadata>
  <version>1000</version>
  <dependencies>
    <dependency>profile-ploneconf.site:default</dependency>
  </dependencies>
</metadata>
```

Add the structure you wish to create as a list of dictionaries in {file}`setuphandlers.py`:

```{code-block} python
:linenos:

STRUCTURE = [
    {
        'type': 'Document',
        'title': 'Schedule',
        'id': 'schedule',
        'description': 'Talks of the conference',
        'state': 'published',
        'allowed_types': ['talk'],
        'local_roles': [{
            'group': 'AuthenticatedUsers',
            'roles': ['Contributor']
        }],
    },
    {
        'type': 'Document',
        'title': 'Training',
        'id': 'training',
        'state': 'published',
    },
    {
        'type': 'Document',
        'title': 'News',
        'id': 'news',
        'description': 'News about the Plone Conference',
        'state': 'published',
        'children': [{
            'type': 'News Item',
            'title': 'Submit your talks!',
            'id': 'submit-your-talks',
            'description': 'Talk submission is open',
            'state': 'published', }
        ],
    },
    {
        'type': 'Document',
        'title': 'Events',
        'id': 'events',
        'description': 'Dates to keep in mind',
        'state': 'published',
    },
    {
        'type': 'Document',
        'title': 'Sponsors',
        'id': 'sponsors',
        'state': 'published',
    },
    {
        'type': 'Document',
        'title': 'Sprint',
        'id': 'sprint',
        'description': 'Work together',
        'state': 'published',
    },
]
```

Add the method {py:meth}`post_handler_content` to {file}`setuphandlers.py`.
We pointed to that when registering the profile.
And add some fancy logic to create the content from `STRUCTURE`.

```{code-block} python
:linenos:

from Products.CMFPlone.interfaces import constrains
from zope.lifecycleevent import modified

import logging


default_profile = "profile-ploneconf.site:default"
logger = logging.getLogger(__name__)


def post_handler_content(context):
    portal = api.portal.get()
    for item in STRUCTURE:
        _create_content(item, portal)


def _create_content(item_dict, container, force=False):
    if not force and container.get(item_dict['id'], None) is not None:
        return

    # Extract info that can't be passed to api.content.create
    allowed_types = item_dict.pop('allowed_types', None)
    local_roles = item_dict.pop('local_roles', [])
    children = item_dict.pop('children', [])
    state = item_dict.pop('state', None)

    if not item_dict['id'] in portal:
        new_content = api.content.create(
            container=container,
            safe_id=True,
            **item_dict
        )
        logger.info(f'Created "{new_content.portal_type}" at "{new_content.absolute_url()}"')

    if allowed_types is not None:
        _constrain(new_content, allowed_types)
    for local_role in local_roles:
        api.group.grant_roles(
            groupname=local_role['group'],
            roles=local_role['roles'],
            obj=new_content)
    if state is not None:
        api.content.transition(new_content, to_state=state)

    modified(new_content)
    # call recursively for children
    for subitem in children:
        _create_content(subitem, new_content)


def _constrain(context, allowed_types):
    behavior = constrains.ISelectableConstrainTypes(context)
    behavior.setConstrainTypesMode(constrains.ENABLED)
    behavior.setLocallyAllowedTypes(allowed_types)
    behavior.setImmediatelyAddableTypes(allowed_types)
```

A huge benefit of this implementation is that you can add any object attribute as a new item to {py:data}`item_dict`.
{py:meth}`plone.api.content.create` will then set these on the new objects.
This way you can also populate fields like {py:attr}`text` (using {py:class}`plone.app.textfield.RichTextValue`) or {py:attr}`image` (using {py:class}`plone.namedfile.file.NamedBlobImage`).
````
