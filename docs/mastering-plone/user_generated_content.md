---
myst:
  html_meta:
    "description": ""
    "property=og:description": ""
    "property=og:title": ""
    "keywords": ""
---

(user-content-label)=

# Workflow, Roles and Permissions
How do prospective speakers submit talks? We let them register on the site and grant right to create talks. For this we go back to changing the site through-the-web.

````{card} Backend chapter

Get the code! ({doc}`More info <code>`)

Code for the beginning of this chapter:

```shell
git checkout events
```

Code for the end of this chapter:

```shell
git checkout user_generated_content
```
````

```{card}
In this chapter we:

- allow self-registration
- constrain which content types can be added to the talk folder
- grant local roles
- create a custom workflow for talks
```


(user-content-self-reg-label)=

## Self-registration

- Go to the Security control panel at <http://localhost:8080/Plone/@@security-controlpanel> and Enable self-registration
- Leave "Enable User Folders" off unless you want a community site, in which users can create any content they want in their home folder

(user-content-constrain-types-label)=

## Constrain types

- On the talk folder select [Restrictions…](http://localhost:8080/Plone/the-event/talks/folder_constraintypes_form) from the _Add new_ menu. Only allow adding talks.

(user-content-local-roles-label)=

## Grant local roles

- Go to _Sharing_ and grant the role _Can add_ to the group _logged-in users_. Now every logged-in user can add content in this folder (and only this folder).

By combining the constrain types and the local roles on this folder, we have made it so only logged-in users can create and submit talks in this folder.

(user-content-custom-workflow-label)=

## A custom workflow for talks

We still need to fix a problem: Authenticated users can see all talks, including those of other users, even if those talks are in the private state. Since we don't want this, we will create a modified workflow for talks. The new workflow will only let them see and edit talks they created themselves and not the ones of other users.

- Go to the {menuselection}`ZMI --> portal_workflow`
- See how talks have the same workflow as most content, namely {guilabel}`(Default)`
- Go to the tab {guilabel}`Contents`, check the box next to {guilabel}`simple_publication_workflow`, click {guilabel}`copy` and {guilabel}`paste`.
- Rename the new workflow from _copy_of_simple_publication_workflow_ to _talks_workflow_.
- Edit the workflow by clicking on it: Change the Title to _Talks Workflow_.
- Click on the tab {guilabel}`States` and click on {guilabel}`private` to edit this state. In the next view select the tab {guilabel}`Permissions`.
- Find the table column for the role {guilabel}`Contributor` and remove the permissions for {guilabel}`Access contents information` and {guilabel}`View`. Note that the {guilabel}`Owner` (i.e. the Creator) still has some permissions.
- Do the same for the state {guilabel}`pending`
- Go back to {file}`portal_workflow` and set the new workflow {file}`talks_workflow` for talks. Click {file}`Change` and then {file}`Update security settings`.

```{note}
The add-on [plone.app.workflowmanager](https://pypi.org/project/plone.app.workflowmanager) provides a much nicer graphical user interface for this. The problem is you need a big screen to work with complex workflows.
```

Done.

(user-content-fs-label)=

## Move the changes to the file system

We don't want to do these steps for every new conference by hand so we move the changes into our package.

### Import/Export the Workflow

- export the GenericSetup step _Workflow Tool_ in <http://localhost:8080/Plone/portal_setup/manage_exportSteps>.

- drop the file {file}`workflows.xml` into {file}`profiles/default` an clean out everything that is not related to talks.

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

- drop {file}`workflows/talks_workflow/definition.xml` in {file}`profiles/default/workflows/talks_workflow/definition.xml`. The other files are just definitions of the default-workflows and we only want things in our package that changes Plone.

### Enable self-registration

To enable self-registration you need to change the global setting that controls this option.
Most global setting are stored in the registry. You can modify it by adding the following to {file}`profiles/default/registry.xml`:

```xml
<record name="plone.enable_self_reg">
  <value>True</value>
</record>
```

### Grant local roles

Since the granting of local roles applies only to a certain folder in the site we would not always write code for it but do it by hand. But for testability and repeatability (there is a conference every year!) we should create the initial content structure automatically.

So let's make sure some initial content is created and configured on installing the package.

To run arbitrary code during the installation of a package we use a [post_handler](https://5.docs.plone.org/develop/addons/components/genericsetup.html#custom-installer-code-setuphandlers-py)

Our package already has such a method registered in {file}`configure.zcml`. It will be automatically run when (re-)installing the add-on.

```{code-block} xml
:emphasize-lines: 7
:linenos:

<genericsetup:registerProfile
    name="default"
    title="ploneconf.site"
    directory="profiles/default"
    description="Installs the ploneconf.site add-on."
    provides="Products.GenericSetup.interfaces.EXTENSION"
    post_handler=".setuphandlers.post_install"
    />
```

This makes sure the method {py:meth}`post_install` in {file}`setuphandlers.py` is executed after the installation. The method already exists doing nothing. You need to extend it to do what we want.

```{code-block} python
:emphasize-lines: 2-3, 7-10, 26-27, 30-65
:linenos:

# -*- coding: utf-8 -*-
from plone import api
from Products.CMFPlone.interfaces import constrains
from Products.CMFPlone.interfaces import INonInstallable
from zope.interface import implementer

import logging

logger = logging.getLogger(__name__)
PROFILE_ID = 'profile-ploneconf.site:default'


@implementer(INonInstallable)
class HiddenProfiles(object):

    def getNonInstallableProfiles(self):
        """Hide uninstall profile from site-creation and quickinstaller"""
        return [
            'ploneconf.site:uninstall',
        ]


def post_install(context):
    """Post install script"""
    # Do something at the end of the installation of this package.
    portal = api.portal.get()
    set_up_content(portal)


def set_up_content(portal):
    """Create and configure some initial content.
    Part of this code is taken from upgrades.py
    """
    # Create a folder 'The event' if needed
    if 'the-event' not in portal:
        event_folder = api.content.create(
            container=portal,
            type='Folder',
            id='the-event',
            title=u'The event')
    else:
        event_folder = portal['the-event']

    # Create folder 'Talks' inside 'The event' if needed
    if 'talks' not in event_folder:
        talks_folder = api.content.create(
            container=event_folder,
            type='Folder',
            id='talks',
            title=u'Talks')
    else:
        talks_folder = event_folder['talks']

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
    logger.info('Added and configured {0}'.format(talks_folder.absolute_url()))


def uninstall(context):
    """Uninstall script"""
    # Do something at the end of the uninstallation of this package.
```

Once we reinstall our package a folder {file}`talks` is created with the appropriate local roles and constraints.

We wrote similar code to create the folder _The Event_ in {doc}`upgrade_steps`.
We need it to make sure a sane structure gets created when we create a new site by hand or in tests.

You would usually create a list of dictionaries containing the type, parent and title plus optionally layout, workflow state etc. to create an initial structure. In some projects it could also make sense to have a separate profile besides `default` which might be called `demo` or `content` that creates an initial structure and maybe another `testing` that creates dummy content (talks, speakers etc) for tests.

#### Exercise 1

Create a profile `content` that runs its own post_handler in {file}`setuphandlers.py`.

````{dropdown} Solution
:animate: fade-in-slide-down
:icon: question

Register the profile and the upgrade step in {file}`configure.zcml`

```xml
<genericsetup:registerProfile
    name="content"
    title="PloneConf Site initial content"
    directory="profiles/content"
    description="Extension profile for PloneConf Talk to add initial content"
    provides="Products.GenericSetup.interfaces.EXTENSION"
    post_handler=".setuphandlers.post_content"
    />
```

Also add a {file}`profiles/content/metadata.xml` so the default profile gets automatically installed when installing the content profile.

```xml
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
        'type': 'Folder',
        'title': u'The Event',
        'id': 'the-event',
        'description': u'Plone Conference 2020',
        'default_page': 'frontpage-for-the-event',
        'state': 'published',
        'children': [{
            'type': 'Document',
            'title': u'Frontpage for the-event',
            'id': 'frontpage-for-the-event',
            'state': 'published',
            },
            {
            'type': 'Folder',
            'title': u'Talks',
            'id': 'talks',
            'layout': 'talklistview',
            'state': 'published',
            },
            {
            'type': 'Folder',
            'title': u'Training',
            'id': 'training',
            'state': 'published',
            },
            {
            'type': 'Folder',
            'title': u'Sprint',
            'id': 'sprint',
            'state': 'published',
            },
        ]
    },
    {
        'type': 'Folder',
        'title': u'Talks',
        'id': 'talks',
        'description': u'Submit your talks here!',
        'state': 'published',
        'layout': '@@talklistview',
        'allowed_types': ['talk'],
        'local_roles': [{
            'group': 'AuthenticatedUsers',
            'roles': ['Contributor']
        }],
    },
    {
        'type': 'Folder',
        'title': u'News',
        'id': 'news',
        'description': u'News about the Plone Conference',
        'state': 'published',
        'children': [{
            'type': 'News Item',
            'title': u'Submit your talks!',
            'id': 'submit-your-talks',
            'description': u'Task submission is open',
            'state': 'published', }
        ],
    },
    {
        'type': 'Folder',
        'title': u'Events',
        'id': 'events',
        'description': u'Dates to keep in mind',
        'state': 'published',
    },
]
```

Add the method {py:meth}`post_content` to {file}`setuphandlers.py`. We pointed to that when registering the import step. And add some fancy logic to create the content from `STRUCTURE`.

```{code-block} python
:linenos:

from zope.lifecycleevent import modified


def post_content(context):
    portal = api.portal.get()
    for item in STRUCTURE:
        _create_content(item, portal)


def _create_content(item_dict, container, force=False):
    if not force and container.get(item_dict['id'], None) is not None:
        return

    # Extract info that can't be passed to api.content.create
    layout = item_dict.pop('layout', None)
    default_page = item_dict.pop('default_page', None)
    allowed_types = item_dict.pop('allowed_types', None)
    local_roles = item_dict.pop('local_roles', [])
    children = item_dict.pop('children', [])
    state = item_dict.pop('state', None)

    new = api.content.create(
        container=container,
        safe_id=True,
        **item_dict
    )
    logger.info('Created {0} at {1}'.format(new.portal_type, new.absolute_url()))

    if layout is not None:
        new.setLayout(layout)
    if default_page is not None:
        new.setDefaultPage(default_page)
    if allowed_types is not None:
        _constrain(new, allowed_types)
    for local_role in local_roles:
        api.group.grant_roles(
            groupname=local_role['group'],
            roles=local_role['roles'],
            obj=new)
    if state is not None:
        api.content.transition(new, to_state=state)

    modified(new)
    # call recursively for children
    for subitem in children:
        _create_content(subitem, new)


def _constrain(context, allowed_types):
    behavior = constrains.ISelectableConstrainTypes(context)
    behavior.setConstrainTypesMode(constrains.ENABLED)
    behavior.setLocallyAllowedTypes(allowed_types)
    behavior.setImmediatelyAddableTypes(allowed_types)
```

A huge benefit of this implementation is that you can add any object-attribute as a new item to {py:data}`item_dict`. {py:meth}`plone.api.content.create` will then set these on the new objects. This way you can also populate fields like {py:attr}`text` (using {py:class}`plone.app.textfield.RichTextValue`) or {py:attr}`image` (using {py:class}`plone.namedfile.file.NamedBlobImage`).
````
