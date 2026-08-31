---
myst:
  html_meta:
    "description": "Create custom REST API endpoints"
    "property=og:description": "Create custom REST API endpoints"
    "property=og:title": "REST API Endpoints"
    "keywords": "Plone, REST API"
---

(endpoints-mastering-label)=

# REST API endpoints [voting story]

```{card}

In this part you will:

- Register and write a custom REST API service

Topics covered:

- Extending plone.restapi
- Services and endpoints
```

````{card}

Check out `mastering-plone-votable-add-on` at tag `behaviors`:

```shell
git checkout behaviors
```

The code at the end of the chapter:

```shell
git checkout endpoints
```

More info in {doc}`../code`
````

## Implement the service

So far, Volto has no access to the logic of the voting behavior from the previous chapter.

We need to create a REST API endpoint that can be addressed by `GET`, `POST` and `DELETE` requests.

The adapter `ploneconf.votable.behaviors.votable.Votable` has the logic needed for voting.
The key methods are `votes` to get the current votes, `vote` to actively cast a vote and `clear` to clear existing votes.

In {file}`backend/src/ploneconf/votable` create a folder structure like the following:

```console
services/
├── __init__.py
├── configure.zcml
├── votes.py
```

We include the new package `services` in the package's main configuration file {file}`backend/src/ploneconf/votable/configure.zcml`:

```{code-block} xml
:emphasize-lines: 2
:linenos:

<include package=".browser" />
<include package=".services" />
```

(endpoints-mastering-services-label)=

Now let's implement the services for the endpoint `@votes` in {file}`backend/src/ploneconf/votable/services/votes.py`.

```{code-block} python
:emphasize-lines: 10-17
:linenos:

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
        voting = IVotable(self.context)
        if not voting.can_vote:
            raise Unauthorized("User not authorized to view votes.")
        return vote_info(self.context)


class VotingPost(Service):
    """Vote for an object"""

    def reply(self):
        alsoProvides(self.request, IDisableCSRFProtection)
        voting = IVotable(self.context)
        if not voting.can_vote:
            raise Unauthorized("User not authorized to vote.")
        data = json_body(self.request)
        vote = data["rating"]
        voting.vote(vote)

        return vote_info(self.context)


class VotingDelete(Service):
    """Clear votes for an object"""

    def reply(self):
        alsoProvides(self.request, IDisableCSRFProtection)
        can_clear_votes = api.user.has_permission(
            "ploneconf.votable: Clear votes", obj=self.context
        )
        if not can_clear_votes:
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
        "can_vote": voting.can_vote,
        "can_clear_votes": api.user.has_permission(
            "ploneconf.votable: Clear votes", obj=obj
        ),
    }
    return info
```

The GET service is highlighted.
If we look at the code, we see that the service inherits necessary properties from `plone.restapi.services.Service` by subclassing.

The `reply` method implements what should be returned on a GET request to endpoint `@votes`.
It checks the permission to vote, and accesses the behavior logic to return the votes.

## Register the service

How can the service be published as part of the Plone REST API?
We will register the services for the behavior's marker interface.

With a registration in {file}`configure.zcml` the endpoint is addressable.

```{code-block} xml
:linenos:

<configure
    xmlns="http://namespaces.zope.org/zope"
    xmlns:browser="http://namespaces.zope.org/browser"
    xmlns:plone="http://namespaces.plone.org/plone"
    i18n_domain="ploneconf.votable"
    >

  <plone:service
      method="GET"
      factory=".votes.VotingGet"
      for="ploneconf.votable.behaviors.votable.IVotableMarker"
      permission="zope2.View"
      name="@votes"
      />

  <plone:service
      method="POST"
      factory=".votes.VotingPost"
      for="ploneconf.votable.behaviors.votable.IVotableMarker"
      permission="zope2.View"
      name="@votes"
      />

  <plone:service
      method="DELETE"
      factory=".votes.VotingDelete"
      for="ploneconf.votable.behaviors.votable.IVotableMarker"
      permission="zope2.View"
      name="@votes"
      />

</configure>
```

Note that all three services have the same name `@votes`, but will provide different functionality depending on the method of the request (GET, POST, or DELETE).
This is not required but is a convention many REST endpoints follow.
We could also give them different names based on their functionality.

In our example, the permission checks are delegated to the services themselves and we use `zope2.View` as permission to access the service.

The services are all only available on content that provides the behavior's marker interface, `ploneconf.votable.behaviors.votable.IVotableMarker`, which we explained in the previous chapter.

## Test the service

If you have an API client like Postman installed, you can access the new endpoint for testing.
Be sure to authenticate and add a header to accept `application/json`.
