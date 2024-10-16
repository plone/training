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

```{card} Backend chapter

To be solved task in this part:

- Provide access to voting for the Volto frontend

In this part you will:

- Register and write a custom endpoint

Topics covered:

- Extending plone.restapi
- Services and Endpoints
```

Out of the box Volto has no access to the logic of the voting behavior of the last chapter.

We need to create a REST API endpoint that can be addressed by GET, POST and DELETE requests.

The adapter `training.votable.behaviors.votable.Votable` has the logic needed for voting.
The key features are `votes` to get the current votes, `vote` to actively cast a vote and `clear` to clear existing votes.

In {file}`src/training/votable/` create a folder structure like the following:

```console
api/
├── __init__.py
├── configure.zcml
├── voting.py
```

We include the new module `api` in the packages' main {file}`configure.zcml`:

```{code-block} xml
:emphasize-lines: 2
:linenos:

<include package=".browser" />
<include package=".api" />
```

(endpoints-mastering-services-label)=

The services for the endpoint `@votes` are now to be implemented in {file}`voting.py`.

```{code-block} python
:emphasize-lines: 15,18-25,63
:linenos:

# -*- coding: utf-8 -*-
from plone import api
from plone.protect.interfaces import IDisableCSRFProtection
from plone.restapi.deserializer import json_body
from plone.restapi.services import Service
from zExceptions import Unauthorized
from zope.globalrequest import getRequest
from zope.interface import alsoProvides

from training.votable import (
    CanVotePermission,
    ClearVotesPermission,
    ViewVotesPermission,
)
from training.votable.behaviors.votable import IVotable


class VotingGet(Service):
    """Voting information about the current object"""

    def reply(self):
        can_view_votes = api.user.has_permission(ViewVotesPermission, obj=self.context)
        if not can_view_votes:
            raise Unauthorized("User not authorized to view votes.")
        return vote_info(self.context, self.request)


class VotingPost(Service):
    """Vote for an object"""

    def reply(self):
        alsoProvides(self.request, IDisableCSRFProtection)
        can_vote = api.user.has_permission(CanVotePermission, obj=self.context)
        if not can_vote:
            raise Unauthorized("User not authorized to vote.")
        voting = IVotable(self.context)
        data = json_body(self.request)
        vote = data["rating"]
        voting.vote(vote, self.request)

        return vote_info(self.context, self.request)


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


def vote_info(obj, request=None):
    """Returns voting information about the given object."""
    if not request:
        request = getRequest()
    voting = IVotable(obj)
    info = {
        "average_vote": voting.average_vote(),
        "total_votes": voting.total_votes(),
        "has_votes": voting.has_votes(),
        "already_voted": voting.already_voted(request),
        "can_vote": api.user.has_permission(CanVotePermission, obj=obj),
        "can_clear_votes": api.user.has_permission(ClearVotesPermission, obj=obj),
    }
    return info

```

The GET service is highlighted.
If we look at the code, we see that the service inherits necessary properties from `plone.restapi.services.Service` by subclassing.

The `reply` method implements what should be returned on a GET request to endpoint `@votes`.
- It checks the permission to vote
- It accesses the behavior logic to return the votes.

How can the service use the features we implemented with the behavior?
We will register the services for the behaviors' marker interface.
With that an instance of a content type that has the behavior enabled, can be adapted by `IVotable(context)`.

We skip the permissions and talk about this in a later chapter {doc}`permissions`.


With a registration in {file}`configure.zcml` the endpoint is addressable.


```{code-block} xml
:linenos:

<configure
    xmlns="http://namespaces.zope.org/zope"
    xmlns:browser="http://namespaces.zope.org/browser"
    xmlns:plone="http://namespaces.plone.org/plone"
    i18n_domain="training.votable">

    <plone:service
    method="GET"
    for="training.votable.behaviors.votable.IVotableMarker"
    factory=".voting.VotingGet"
    name="@votes"
    permission="zope2.View"
    />

  <plone:service
    method="POST"
    for="training.votable.behaviors.votable.IVotableMarker"
    factory=".voting.VotingPost"
    name="@votes"
    permission="training.votable.can_vote"
    />

  <plone:service
    method="DELETE"
    for="training.votable.behaviors.votable.IVotableMarker"
    factory=".voting.VotingDelete"
    name="@votes"
    permission="zope2.ViewManagementScreens"
    />

</configure>
```

Note that all have the same name `@votes` but will provide different functionality depending on the method of the request (GET, POST, DELETE).
This is not required but a convention many endpoints follow.
We could also name them more in sync with their functionality.

In our example the permission checks are delegated to the services themselves and we use `zope2.View` as permission.

The services are all only available on content that provides the behaviors' marker interface `training.votable.behaviors.votable.IVotableMarker` that we declared in the last chapter.

If you have `postman` installed, you can address the new endpoint for testing purpose.
Be sure to authenticate and add a header to accept `JSON`.
