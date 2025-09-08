---
myst:
  html_meta:
    "description": ""
    "property=og:description": ""
    "property=og:title": ""
    "keywords": ""
---

(plone5-reusable-label)=

# Making Our Package Reusable

In this part you will:

- Add Permissions

Topics covered:

- Permissions

The package contains some problems.

- No permission settings, Users can't customize who and when users can vote
- We do things, but don't trigger events. Events allow others to react.

(plone5-reusable-permissions-label)=

## Adding permissions

```{only} presentation
- Zope 2 Permissions
- Zope 3 Permissions
```

````{only} not presentation
Permissions have a long history, there are two types of permissions.

In Zope2, a permission was just a string.

In ZTK, a permission is an object that gets registered as a Utility.

We must support both, in some cases we have to reference the permission by their Zope2 version, in some by their ZTK Version.

Luckily, there is a zcml statement to register a permission both ways in one step.

```{seealso}
The configuration registry was meant to solve a problem, but we will now stumble over a problem that did not get resolved properly.

Our permission is a utility. Our browser views declare this permission as a requirement for viewing them.

When our browser views get registered, the permissions must exist already. If you try to register the permissions after the views, Zope won't start because it doesn't know about the permissions.
```
````

Let's modify the file {file}`configure.zcml`

```{code-block} xml
:emphasize-lines: 5-13
:linenos:

<configure xmlns="...">

  <includeDependencies package="." />

  <permission
      id="starzel.votable_behavior.view_vote"
      title="starzel.votable_behavior: View Vote"
      />

  <permission
      id="starzel.votable_behavior.do_vote"
      title="starzel.votable_behavior: Do Vote"
      />

  <include package=".browser" />

  ...

</configure>
```

In some places we have to reference the Zope 2 permission strings. It is best practice to provide a static variable for this.

We provide this in {file}`__init__.py`

```{code-block} python
:linenos:

...
DoVote = 'starzel.votable_behavior: Do Vote'
ViewVote = 'starzel.votable_behavior: View Vote'
```

(plone5-reusable-permissions2-label)=

## Using our permissions

```{only} not presentation
As you can see, we created two permissions, one for voting, one for viewing the votes.

If a user is not allowed to see the votes, she does not need access to the vote viewlet.

While we are at it, if a user can't vote, she needs no access to the helper view to actually submit a vote.
```

We can add this restriction to {file}`browser/configure.zcml`

```{code-block} xml
:emphasize-lines: 13, 21
:linenos:

<configure
  xmlns="http://namespaces.zope.org/zope"
  xmlns:browser="http://namespaces.zope.org/browser"
  i18n_domain="starzel.votable_behavior">

  <browser:viewlet
    name="voting"
    for="starzel.votable_behavior.interfaces.IVotable"
    manager="plone.app.layout.viewlets.interfaces.IBelowContentTitle"
    template="templates/voting_viewlet.pt"
    layer="..interfaces.IVotableLayer"
    class=".viewlets.Vote"
    permission="starzel.votable_behavior.view_vote"
    />

  <browser:page
    name="vote"
    for="starzel.votable_behavior.interfaces.IVotable"
    layer="..interfaces.IVotableLayer"
    class=".vote.Vote"
    permission="starzel.votable_behavior.do_vote"
    />

  ...

</configure>
```

````{only} not presentation
We are configuring components, so we use the component name of the permission, which is the {samp}`id` part of the declaration we added earlier.

```{seealso}
So, what happens if we do not protect the browser view to vote?

The person could still vote, by handcrafting the URL. Browser Views run code without any restriction, it is your job to take care of security.

But... if a person has no access to the object at all, maybe because the site is configured that Anonymous users cannot access private objects, the unauthorized users will not be able to submit a vote.

That is because Zope checks security permissions when trying to find the right object. If it can't find the object due to security constraints not met, no view ill ever be called, because that would have been the next step.
```

We now protect our views and viewlets. We still show the option to vote though.

We must add a condition in our page template, and we must provide the condition information in our viewlet class.
````

Lets move on to {file}`browser/viewlets.py`.

```{code-block} python
:emphasize-lines: 9, 19-22
:linenos:

# ...

from starzel.votable_behavior import DoVote


class Vote(base.ViewletBase):

#   ...
    can_vote = None

    def update(self):

#       ...

        if self.is_manager is None:
            membership_tool = getToolByName(self.context, 'portal_membership')
            self.is_manager = membership_tool.checkPermission(
                ViewManagementScreens,
                self.context,
            )
            self.can_vote = membership_tool.checkPermission(
                DoVote,
                self.context,
            )

#  ...
```

And the template in {file}`browser/templates/voting_viewlet.pt`

```{code-block} xml
:emphasize-lines: 7, 13
:linenos:

<tal:snippet omit-tag="">
  <div class="voting">

    ...

    <div id="notyetvoted" class="voting_option"
            tal:condition="view/can_vote">
      What do you think of this talk?
      <div class="votes"><span id="voting_plus">+1</span> <span id="voting_neutral">0</span> <span id="voting_negative">-1</span>
      </div>
    </div>
    <div id="no_ratings" tal:condition="not: view/has_votes">
      This talk has not been voted yet.<span tal:omit-tag="" tal:condition="view/can_vote"> Be the first!</span>
    </div>

  ...

  </div>

...

</tal:snippet>
```

```{only} not presentation
Sometimes subtle bugs come up because of changes. In this case I noticed that I should only prompt people to vote if they are allowed to vote!
```

(plone5-reusable-defaults-label)=

## Provide defaults

```{only} not presentation
Are we done yet? Who may vote now?

We have to tell that someone.

Who has which permissions is managed in Zope. This is persistent, and persistent configuration is handled by GenericSetup.
```

The persistent configuration is managed in another file: {file}`profiles/default/rolemap.xml`

```{code-block} xml
:linenos:

<?xml version="1.0"?>
<rolemap>
  <permissions>
    <permission name="starzel.votable_behavior: View Vote" acquire="True">
      <role name="Anonymous"/>
    </permission>
    <permission name="starzel.votable_behavior: Do Vote" acquire="True">
      <role name="Anonymous"/>
    </permission>
  </permissions>
</rolemap>
```
