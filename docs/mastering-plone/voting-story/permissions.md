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

```{card}

In this part you will:

- Add custom permissions
- Protect the voting service using permissions
- Configure which roles get the permissions

Topics covered:

- Permissions
- The rolemap
```

````{card}

Check out `mastering-plone-votable-add-on` at tag `actions`:

```shell
git checkout actions
```

The code at the end of the chapter:

```shell
git checkout permissions
```

More info in {doc}`../code`
````

We have a working voting add-on, but it currently allows too many people to vote.
Currently, anyone who can view the talks can vote.
We should add custom permissions so that we can make sure only the conference program committee can vote.

(permissions-adding-label)=

## Add custom permissions

Plone has lots of built-in permissions like `View` and `Modify portal content`.
We can also add our own custom permissions in our add-on.

Edit the file {file}`backend/src/ploneconf/votable/permissions.zcml`:

```{code-block} xml
:linenos:

<configure
    xmlns="http://namespaces.zope.org/zope"
    xmlns:zcml="http://namespaces.zope.org/zcml"
    i18n_domain="plone"
    >

  <permission
      id="ploneconf.votable.view_vote"
      title="ploneconf.votable: View votes"
      />

  <permission
      id="ploneconf.votable.can_vote"
      title="ploneconf.votable: Can vote"
      />

  <permission
      id="ploneconf.votable.clear_votes"
      title="ploneconf.votable: Clear votes"
      />

</configure>
```

We are adding three permissions:
- `View votes` will give access to view the voting results
- `Can vote` will give access to add a vote
- `Clear votes` will give access to reset the votes

We use the add-on name `ploneconf.votable` as a prefix for the permission names, to make sure they don't conflict with other add-ons.

Each permission has an `id` and a `title`.
They are used in different places.
The `id` is used when referring to permissions in ZCML, such as in a view declaration.
The `title` is used when checking permissions with `plone.api`.

(permissions-using-label)=

## Check permissions

Now we can update the `@votes` services to check these permissions.

Update {file}`backend/src/ploneconf/votable/services/votes.py:

```{code-block} python
:linenos:
:emphasize-lines: 1, 14-17, 27-28, 41-44, 58-61

from plone import api
from plone.protect.interfaces import IDisableCSRFProtection
from plone.restapi.deserializer import json_body
from plone.restapi.services import Service
from ploneconf.votable.behaviors.votable import IVotable
from zExceptions import Unauthorized
from zope.interface import alsoProvides


class VotingGet(Service):
    """Get voting information about the current object"""

    def reply(self):
        if not api.user.has_permission(
            "ploneconf.votable: View votes", obj=self.context
        ):
            raise Unauthorized("User not authorized to view votes.")
        return vote_info(self.context)


class VotingPost(Service):
    """Vote for an object"""

    def reply(self):
        alsoProvides(self.request, IDisableCSRFProtection)
        voting = IVotable(self.context)
        if not api.user.has_permission("ploneconf.votable: Can vote", obj=self.context):
            raise Unauthorized("User not authorized to vote.")
        data = json_body(self.request)
        vote = data["rating"]
        voting.vote(vote)

        return vote_info(self.context)


class VotingDelete(Service):
    """Clear votes for an object"""

    def reply(self):
        alsoProvides(self.request, IDisableCSRFProtection)
        if not api.user.has_permission(
            "ploneconf.votable: Clear votes", obj=self.context
        ):
            raise Unauthorized("User not authorized to clear votes.")
        voting = IVotable(self.context)
        voting.clear()
        return vote_info(self.context)


def vote_info(obj):
    """Returns voting information about the given object."""
    voting = IVotable(obj)
    info = {
        "average_vote": voting.average_vote(),
        "total_votes": voting.total_votes(),
        "has_votes": voting.has_votes(),
        "already_voted": voting.already_voted(),
        "can_vote": api.user.has_permission("ploneconf.votable: Can vote", obj=obj),
        "can_clear_votes": api.user.has_permission(
            "ploneconf.votable: Clear votes", obj=obj
        ),
    }
    return info
```

Raising the `Unauthorized` exception returns an HTTP response with status 401.

```{tip}
We could also update the `permission` for the services in {file}`configure.zcml`.
But doing the check in Python lets us return a more informative error response.
```

We're also returning `can_vote` and `can_clear_votes` in the `vote_info` data,
so that the frontend component can check what the user is allowed to do.


(permissions-defaults-label)=

## Configure the rolemap

Permissions are designed to provide flexibility about who actually gets the permission.
We need to configure the rolemap to define which roles get the permissions.

Update the file {file}`backend/src/ploneconf/votable/profiles/default/rolemap.xml`.

```{code-block} xml
:linenos:

<?xml version="1.0" encoding="utf-8"?>
<rolemap>
  <permissions>

    <permission acquire="True"
                name="ploneconf.votable: View votes"
    >
      <role name="Authenticated" />
      <role name="Site Administrator" />
      <role name="Manager" />
    </permission>
    <permission acquire="True"
                name="ploneconf.votable: Can vote"
    >
      <role name="Reviewer" />
    </permission>
    <permission acquire="True"
                name="ploneconf.votable: Clear votes"
    >
      <role name="Site Administrator" />
      <role name="Manager" />
    </permission>

  </permissions>
</rolemap>
```

Any authenticated user is allowed to view the voting results.

Only users with the Reviewer role are allowed to add votes.
(For the conference site, it would make sense to put the Program Committee members in a group, and assign the Reviewer role to that group.)

Only users with the Site Administrator or Manager roles are allowed to reset the votes.

After reinstalling the add-on, the updated rolemap takes effect.
