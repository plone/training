---
myst:
  html_meta:
    "description": "Configure who can edit what"
    "property=og:description": "Configure who can edit what"
    "property=og:title": "Workflow, Roles and Permissions"
    "keywords": "Plone, Volto, workflow, role, local role, permission"
---

(user-content-label)=

# Workflow, Roles and Permissions

How do prospective speakers submit talks?
We let them register on the site and grant right to create talks.
For this we go back to changing the site through-the-web.

```{card}
In this part you will:

- Allow self-registration
- Constrain which content types can be added to the (folderish) talk page
- Grant local roles
- Create a custom workflow for talks

Tools and techniques covered:

- workflow
- local roles
```

````{card} Backend chapter

Checkout `ploneconf.site` at tag "searchable":

```shell
git checkout searchable
```

The code at the end of the chapter:

```shell
git checkout user_generated_content
```

More info in {doc}`code`
````


(user-content-self-reg-label)=

## Self-registration

- Go to the control panel {guilabel}`security`  at <http://localhost:3000/controlpanel/security> and enable self-registration.
- Leave "Enable User Folders" off unless you want a community site, in which users can create any content they want in their home folder.
- Select the option 'Use email address as login name'.


(user-content-constrain-types-label)=

## Constrain types to be addable

- On the page `schedule` select {guilabel}`Restrictions…` <http://localhost:8080/Plone/schedule/folder_constraintypes_form> from the {guilabel}`Add new_` menu. 
  Restrict to adding only talks.
  This action is by now only available in Classic Plone.


(user-content-local-roles-label)=

## Grant local roles

- Go to {guilabel}`Sharing` and grant the role _Can add_ to the group _logged-in users_. 
  Now every logged-in user can add content in this folder (and only this folder).

By combining the constrain types and the local roles on this folder, we have achieved, that only logged-in users can create and submit talks in this folderish page.


(user-content-custom-workflow-label)=

## A custom workflow for talks

We still need to fix a problem: Authenticated users can see all talks, including those of other users, even if those talks are in the private state.
Since we do not want this, we will create a modified workflow for talks.
The new workflow will only let them see and edit talks they created themselves and not the ones of other users.

- Go to the {menuselection}`ZMI --> portal_workflow`
- See how talks have the same workflow as most content, namely {guilabel}`(Default)`
- Go to the tab {guilabel}`Contents`, check the box next to {guilabel}`simple_publication_workflow`, click {guilabel}`copy` and {guilabel}`paste`.
- Rename the new workflow from _copy_of_simple_publication_workflow_ to _talks_workflow_.
- Edit the workflow by clicking on it: Change the Title to _Talks Workflow_.
- Click on the tab {guilabel}`States` and click on {guilabel}`private` to edit this state. In the next view select the tab {guilabel}`Permissions`.
- Find the table column for the role {guilabel}`Contributor` and remove the permissions for {guilabel}`Access contents information` and {guilabel}`View`. Note that the {guilabel}`Owner` (that's the creator) still has some permissions.
- Do the same for the state {guilabel}`pending`
- Go back to {file}`portal_workflow` and set the new workflow {file}`talks_workflow` for talks. Click {file}`Change` and then {file}`Update security settings`.

The new workflow allows contributors to see and edit talks they created themselves but not the ones of other contributors.


(user-content-fs-label)=

## Move the changes to the file system

We don't want to do these steps for every new conference by hand so we move the changes into our package.

### Export and import the workflow

- Export the GenericSetup step _Workflow Tool_ in <http://localhost:8080/Plone/portal_setup/manage_exportSteps>.

- Drop the file {file}`workflows.xml` into {file}`src/ploneconf/site/profiles/default` an clean out everything that is not related to talks.

  ```xml
  <?xml version="1.0"?>
  <object name="portal_workflow" meta_type="Plone Workflow Tool">
   <object name="talks_workflow" meta_type="Workflow"/>
   <bindings>
    <type type_id="talk">
     <bound-workflow workflow_id="talks_workflow"/>
    </type>
   </bindings>
  </object>
  ```

- Drop {file}`workflows/talks_workflow/definition.xml` in {file}`src/ploneconf/site/profiles/default/workflows/talks_workflow/definition.xml`.
  The other files are just definitions of the default-workflows and we only want things in our package that changes Plone.

### Enable self-registration

To enable self-registration you need to change the global setting that controls this option.
Most global setting are stored in the registry. You can modify it by adding the following to {file}`src/ploneconf/site/profiles/default/registry/main.xml`:

```{code-block} xml
<record name="plone.enable_self_reg">
  <value>True</value>
</record>
```

### Grant local roles and constrain types to be addable

Since the granting of local roles applies only to a certain folder in the site we would not always write code for it but do it by hand.
But for testability and repeatability (there is a conference every year!) we should create the initial content structure automatically and also apply needed local roles.

We are setting up the initial content of a conference site in an upgrade step explained in {ref}`upgrade step code <upgrade-steps-pycode-label>`.
Let's enhance this by setting local roles and constrain types.
Add the following lines to `cleanup_site_structure`.

```{code-block} python
:linenos:

from Products.CMFPlone.interfaces import constrains


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

Once we apply the upgrade step or reinstall our package a page {file}`talks` is created with the appropriate local roles and constraints.


## Exercise

We wrote similar code to create the pages in {doc}`upgrade_steps`.
We need it to make sure a sane structure gets created when we create a new site by hand or in tests.

You would usually create a list of dictionaries containing the type, parent and title plus optionally workflow state etc. to create an initial structure.
In some projects it could also make sense to have a separate profile besides `default` which might be called `demo` or `content` that creates an initial structure and maybe another `testing` that creates dummy content (talks, speakers etc) for tests.

> Create an optional GenericSetup profile `content` that creates the content, grants local roles and sets constraints.

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
