---
myst:
  html_meta:
    "description": ""
    "property=og:description": ""
    "property=og:title": ""
    "keywords": ""
---

(plone5-embed-label)=

# Using starzel.votable_behavior in ploneconf.site

In this part you will:

- Integrate your own third party package into your site.

Topics covered:

- Permissions
- Workflows

````{sidebar} Get the code!
Get the code for this chapter ({doc}`More info <code>`) using this command in the buildout directory:

```shell
TODO
```
````

```{only} not presentation
- We want to use the votable behavior, so that our reviewers can vote.
- To show how to use events, we are going to auto-publish talks that have reached a certain rating.
- We are not going to let everybody vote everything.
```

First, we must add our package as a dependency to ploneconf.site.

```{only} not presentation
We do this in two locations. The egg description {file}`setup.py` needs {samp}`starzel.votable_behavior` as a dependency.
Else no source code will be available.

The persistent configuration needs to be installed when we install our site. This is configured in GenericSetup.
```

We start by editing {file}`setup.py`

```{code-block} python
:emphasize-lines: 8
:linenos:

...
zip_safe=False,
install_requires=[
    'setuptools',
    'plone.app.dexterity [relations]',
    'plone.app.relationfield',
    'plone.namedfile [blobs]',
    'starzel.votable_behavior',
    # -*- Extra requirements: -*-
],
...
```

Next up we modify {file}`profiles/default/metadata.xml`

```{code-block} xml
:emphasize-lines: 4
:linenos:

<metadata>
  <version>1002</version>
    <dependencies>
      <dependency>profile-starzel.votable_behavior:default</dependency>
    </dependencies>
</metadata>
```

... only:: not presentation

> What a weird name. profile- is a prefix you will always need nowadays. Then comes the egg name, and the part after the colon is the name of the profile. The name of the profile is defined in zcml. So far I've stumbled over only one package where the profile directory name was different than the GenericSetup Profile name.
>
> Now the package is there, but nothing is votable. That is because no content type declares to use this behavior. We can add this behavior via the control panel, export the settings and store it in our egg. Let's just add it by hand now.

To add the behavior to talks, we do this in {file}`profiles/default/types/talk.xml`

```{note}
After changing the {file}`metadata.xml` you have to restart your site since unlike other GenericSetup XML files that file is cached.

Managing dependencies in {file}`metadata.xml` is good practice. We can't rely on remembering what we'd have to do by hand.
In Plone 4 we should also have added {samp}`<dependency>profile-plone.app.contenttypes:plone-content</dependency>` like the [documentation for plone.app.contenttypes](https://5.docs.plone.org/external/plone.app.contenttypes/docs/README.html#installation-as-a-dependency-from-another-product) recommends.

Read more: <https://5.docs.plone.org/develop/addons/components/genericsetup.html#dependencies>
```

```{code-block} xml
:emphasize-lines: 4
:linenos:

<property name="behaviors">
  <element value="plone.dublincore"/>
  <element value="plone.namefromtitle"/>
  <element value="starzel.voting"/>
</property>
```

... only:: not presentation

> Now you can reinstall your Plone site.
>
> Everybody can now vote on talks. That's not what we wanted. We only want reviewers to vote on _pending_ Talks.
> This means the permission has to change depending on the workflow state. Luckily, workflows can be configured to do just that.
> Since Talks already have their own workflow we also won't interfere with other content.
>
> First, we have to tell the workflow that it will be managing more permissions. Next, for each state we have to configure which role has the two new permissions.
>
> That is a very verbose configuration, maybe you want to do it in the web interface and export the settings.
> Whichever way you choose, it is easy to make a simple mistake. I will just present the XML way here.

The config for the Workflow is in {file}`profiles/default/workflows/talks_workflow.xml`

```{code-block} xml
:emphasize-lines: 7-8, 12-21, 27-34, 40-45
:linenos:

<?xml version="1.0"?>
<dc-workflow workflow_id="talks_workflow" title="Talks Workflow" description=" - Simple workflow that is useful for basic web sites. - Things start out as private, and can either be submitted for review, or published directly. - The creator of a content item can edit the item even after it is published." state_variable="review_state" initial_state="private" manager_bypass="False">
 <permission>Access contents information</permission>
 <permission>Change portal events</permission>
 <permission>Modify portal content</permission>
 <permission>View</permission>
 <permission>starzel.votable_behavior: View Vote</permission>
 <permission>starzel.votable_behavior: Do Vote</permission>
 <state state_id="pending" title="Pending review">
  <description>Waiting to be reviewed, not editable by the owner.</description>
  ...
  <permission-map name="starzel.votable_behavior: View Vote" acquired="False">
   <permission-role>Site Administrator</permission-role>
   <permission-role>Manager</permission-role>
   <permission-role>Reviewer</permission-role>
  </permission-map>
  <permission-map name="starzel.votable_behavior: Do Vote" acquired="False">
   <permission-role>Site Administrator</permission-role>
   <permission-role>Manager</permission-role>
   <permission-role>Reviewer</permission-role>
  </permission-map>
  ...
 </state>
 <state state_id="private" title="Private">
  <description>Can only be seen and edited by the owner.</description>
  ...
  <permission-map name="starzel.votable_behavior: View Vote" acquired="False">
   <permission-role>Site Administrator</permission-role>
   <permission-role>Manager</permission-role>
  </permission-map>
  <permission-map name="starzel.votable_behavior: Do Vote" acquired="False">
   <permission-role>Site Administrator</permission-role>
   <permission-role>Manager</permission-role>
  </permission-map>
  ...
 </state>
 <state state_id="published" title="Published">
  <description>Visible to everyone, editable by the owner.</description>
  ...
  <permission-map name="starzel.votable_behavior: View Vote" acquired="False">
   <permission-role>Site Administrator</permission-role>
   <permission-role>Manager</permission-role>
  </permission-map>
  <permission-map name="starzel.votable_behavior: Do Vote" acquired="False">
  </permission-map>
  ...
 </state>
  ...
</dc-workflow>
```

```{only} not presentation
We have to reinstall our product again.

But this time, this is not enough. Permissions get updated on workflow changes. As long as a workflow change didn't happen, the talks have the same permissions as ever.

Luckily, there is a button for that in the ZMI Workflow view {guilabel}`Update security settings`.

After clicking on this, only managers and Reviewers can see the Voting functionality.

Lastly, we add our silly function to auto-approve talks.

You quickly end up writing many event handlers, so we put everything into a directory for eventhandlers.
```

For the events we need an {file}`events` directory.

Create the {file}`events` directory and add an empty {file}`events/__init__.py` file.

Next, register the events directory in {file}`configure.zcml`

```{code-block} xml
:linenos:

<include package=".events" />
```

Now write the ZCML configuration for the events into {file}`events/configure.zcml`

```{code-block} xml
:linenos:

<configure
    xmlns="http://namespaces.zope.org/zope">

  <subscriber
    for="starzel.votable_behavior.interfaces.IVotable
         zope.lifecycleevent.IObjectModifiedEvent"
    handler=".votable.votable_update"
    />

</configure>
```

```{only} not presentation
This looks like a MultiAdapter. We want to get notified when an IVotable object gets modified. Our method will receive the votable object and the event itself.
```

And finally, our event handler in {file}`events/votable.py`

```{code-block} python
:linenos:

from plone.api.content import transition
from plone.api.content import get_state
from starzel.votable_behavior.interfaces import IVoting


def votable_update(votable_object, event):
    votable = IVoting(votable_object)
    if get_state(votable_object) == 'pending':
        if votable.average_vote() > 0.5:
            transition(votable_object, transition='publish')
```

```{only} not presentation
We are using a lot of plone api here. Plone API makes the code a breeze. Also, there is nothing really interesting.
We will only do something if the workflow state is pending and the average vote is above 0.5.
As you can see, the {samp}`transition` Method does not want the target state, but the transition to move the state to the target state.

There is nothing special going on.
```
