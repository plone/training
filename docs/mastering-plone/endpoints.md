---
html_meta:
  "description": ""
  "property=og:description": ""
  "property=og:title": ""
  "keywords": ""
---

(endpoints-mastering-label)=

# Endpoints

````{sidebar} Plone Backend Chapter
```{figure} _static/plone-training-logo-for-backend.svg
:alt: Plone backend 
:class: logo
```

Get the code! ({doc}`More info <code>`)

Code for the beginning of this chapter:

```shell
git checkout TODO tag to checkout
```

Code for the end of this chapter:

```shell
git checkout TODO tag to checkout
```
````

To be solved task in this part:

- Grant access to voting for the Volto frontend

In this part you will:

- Register and write a custom endpoint

Topics covered:

- Extending plone.restapi
- Services and Endpoints

Out of the box Volto has no access to the logic for voting created in the last chapter.

You need to extend a endpoint that can be used by GET, POST and DELETE requests.

The adapter `starzel.votable_behavior.behavior.voting.Vote` has the logic needed for voting, the key features are `votes` to get the current votes, `vote` to actively cast a vote and `clear` to clear existing votes.

For the classic frontend this api is exposed in a Viewlet (see chapter {ref}`viewlets2-label`).
But neither the adapter nor the viewlet is directly accessible by a react frontend.

In {file}`backend/src/starzel.votable_behavior/starzel/votable_behavior/` create a folder {file}`restapi` with a empty {file}`__init__.py`.
In that new folder create a {file}`configure.zcml` where you will register the endpoints.

Don't forget to register the new file in the packages' main {file}`configure.zcml`:

```{code-block} xml
:emphasize-lines: 2
:linenos:

<include package=".browser" />
<include package=".restapi" />
```

Now register the endpoints you plan to write in {file}`restapi/configure.zcml`:

```{code-block} xml
:linenos:

<configure
    xmlns="http://namespaces.zope.org/zope"
    xmlns:plone="http://namespaces.plone.org/plone"
    xmlns:zcml="http://namespaces.zope.org/zcml">

  <plone:service
    method="GET"
    name="@votes"
    for="starzel.votable_behavior.interfaces.IVotable"
    factory=".voting.Votes"
    permission="zope2.View"
    />

  <plone:service
    method="POST"
    name="@votes"
    for="starzel.votable_behavior.interfaces.IVotable"
    factory=".voting.Vote"
    permission="zope2.View"
    />

  <plone:service
    method="DELETE"
    name="@votes"
    for="starzel.votable_behavior.interfaces.IVotable"
    factory=".voting.Delete"
    permission="zope2.View"
    />

</configure>
```

Note that are all have the same name `@votes` but will provide different functionality depending on the method of the request.
This is not required but a convention many endpoints follow.
We could also name them mnore in sync with their functionality.
In our example the permission-checks are delegated to the services themselves and we use `zope2.View` as permission.
The services are all only available on content that provides the marker-interface `starzel.votable_behavior.interfaces.IVotable` that we added in the last chapter via a behavior.

Now create the {file}`voting.py` and write the services that together make the endpoint `@votes`:

```python
# -*- coding: utf-8 -*-
from plone import api
from plone.protect.interfaces import IDisableCSRFProtection
from plone.restapi.deserializer import json_body
from plone.restapi.services import Service
from starzel.votable_behavior import DoVote
from starzel.votable_behavior.interfaces import IVoting
from zope.globalrequest import getRequest
from zExceptions import Unauthorized
from zope.interface import alsoProvides


class Vote(Service):
    """Vote for an object"""

    def reply(self):
        alsoProvides(self.request, IDisableCSRFProtection)
        can_vote = not api.user.is_anonymous() and api.user.has_permission(DoVote, obj=self.context)
        if not can_vote:
            raise Unauthorized("User not authorized to vote.")
        voting = IVoting(self.context)
        data = json_body(self.request)
        vote = data['rating']
        voting.vote(vote, self.request)

        return vote_info(self.context, self.request)


class Delete(Service):
    """Unlock an object"""

    def reply(self):
        alsoProvides(self.request, IDisableCSRFProtection)
        can_vote = not api.user.is_anonymous() and api.user.has_permission(DoVote, obj=self.context)
        if not can_vote:
            raise Unauthorized("User not authorized to delete votes.")
        voting = IVoting(self.context)
        voting.clear()
        return vote_info(self.context, self.request)


class Votes(Service):
    """Voting information about the current object"""

    def reply(self):
        return vote_info(self.context, self.request)


def vote_info(obj, request=None):
    """Returns voting information about the given object."""
    if not request:
        request = getRequest()
    voting = IVoting(obj)
    can_vote = not api.user.is_anonymous() and api.user.has_permission(DoVote, obj=obj)
    can_clear_votes = any(role in api.user.get_roles() for role in ['Manager', 'Site Manager'])
    info = {
        'average_vote': voting.average_vote(),
        'total_votes': voting.total_votes(),
        'has_votes': voting.has_votes(),
        'already_voted': voting.already_voted(request),
        'can_vote': can_vote,
        'can_clear_votes': can_clear_votes,
    }
    return info
```

This endpoint is modeled similar to the locking endpoint of `plone.restapi`: <https://github.com/plone/plone.restapi/blob/master/src/plone/restapi/services/locking/locking.py>
