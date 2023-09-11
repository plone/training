---
myst:
  html_meta:
    "description": "Protect endpoint, views and more with permissions"
    "property=og:description": "Protect endpoint, views and more with permissions"
    "property=og:title": "Permissions"
    "keywords": "Plone, permission, security"
---

(permissions-label)=

# Permissions [voting story]

In this part you will:

- Add and use permissions

Topics covered:

- permissions, roles


(permissions-adding-label)=

## Adding permissions


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

Let's add a file {file}`permissions.zcml` and define three permissions for viewing, editing and clearing votes.

```{code-block} xml
:linenos:

<configure
  xmlns="http://namespaces.zope.org/zope"
  xmlns:zcml="http://namespaces.zope.org/zcml"
  i18n_domain="plone">

  <configure zcml:condition="installed AccessControl.security">

    <permission
        id="training.votable.view_vote"
        title="training.votable: View Votes"
        />

    <permission
        id="training.votable.can_vote"
        title="training.votable: Can Vote"
        />

    <permission
        id="training.votable.clear_votes"
        title="training.votable: Clear Votes"
        />

  </configure>

</configure>
```

In some places we have to reference the Zope 2 permission strings. It is best practice to provide a static variable for this.

We provide this in {file}`__init__.py`

```{code-block} python
:linenos:

ViewVotesPermission = "training.votable: View Votes"
CanVotePermission = "training.votable: Can Vote"
ClearVotesPermission = "training.votable: Clear Votes"
```

(permissions-using-label)=

## Using our permissions

We can add now restriction on accessing the `@votes` endpoint POST service in {file}`/src/training/votable/api/configure.zcml`

```{code-block} xml
:emphasize-lines: 11
:linenos:

<configure
  xmlns="http://namespaces.zope.org/zope"
  xmlns:browser="http://namespaces.zope.org/browser"
  i18n_domain="training.votable">

  <plone:service
    method="POST"
    for="training.votable.behaviors.votable.IVotableMarker"
    factory=".voting.VotingPost"
    name="@votes"
    permission="training.votable.can_vote"
    />

</configure>
```

And we can add a permission check inside Python code on the current user on the context by

```{code-block} python
:emphasize-lines: 6-10
:linenos:

class VotingDelete(Service):
    """Unlock an object"""

    def reply(self):
        alsoProvides(self.request, IDisableCSRFProtection)
        can_clear_votes = api.user.has_permission(
            ClearVotesPermission, obj=self.context
        )
        if not can_clear_votes:
            raise Unauthorized("User not authorized to clear votes.")
        voting = IVotable(self.context)
        voting.clear()
        return vote_info(self.context, self.request)
```


(permissions-defaults-label)=

## Provide defaults

After protecting services we do now want to assign the permissions to roles.
For example the users with role "Reviewer" should be able to vote.

The persistent configuration is managed in {file}`profiles/default/rolemap.xml`

```{code-block} xml
:linenos:

<?xml version="1.0"?>
<rolemap>
  <permissions>

    <permission name="training.votable: View Votes" acquire="True">
      <role name="Authenticated"/>
      <role name="Site Administrator"/>
      <role name="Manager"/>
    </permission>
    <permission name="training.votable: Can Vote" acquire="True">
      <role name="Reviewer"/>
    </permission>
    <permission name="training.votable: Clear Votes" acquire="True">
      <role name="Site Administrator"/>
      <role name="Manager"/>
    </permission>
    
  </permissions>
</rolemap>
```
