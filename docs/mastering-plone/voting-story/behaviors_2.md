---
myst:
  html_meta:
    "description": "Extend arbitrary content types with behaviors and fields"
    "property=og:description": "Extend arbitrary content types with behaviors and fields"
    "property=og:title": "Complex behaviors"
    "keywords": "Plone, behavior, fields, extending"
---


(behaviors2-label)=

# Complex behaviors [voting story]

```{card}

In this part you will:

- Write a behavior that enables voting on content
- Use annotations to store the votes on an object

Topics covered:

- Behaviors with a factory class
- Marker interface for a behavior
- Using annotations as storage layer
```

````{card}

Check out `mastering-plone-votable-add-on` at tag `initial`:

```shell
git checkout initial
```

The code at the end of the chapter:

```shell
git checkout behaviors
```

More info in {doc}`code`
````

Members of the conference program committee will vote on talks to be accepted for the conference.

(behaviors2-schema-label)=

## Schema design

We will create a behavior with an additional field to store the votes on a talk.
Therefore the behavior will have a schema with a field `votes`.

We mark the field `votes` as an omitted field as this field should not be edited directly.

We are going to store the information about votes in an _annotation_.
Imagine an add-on that uses the same field name `votes` like we do for another purpose.
Here the AnnotationStorage comes in.
The content type instance is equipped with a storage where behaviors can store values with a key unique per behavior.


(behaviors2-code-label)=

## Add the behavior

In your editor, open the `mastering-plone-votable-add-on` add-on that you created in the previous chapter.

```{tip}
Later in your daily work you can use {term}`plonecli` to generate a behavior.
In this training we go step by step through the code to understand a behavior and its capabilities.
```

To start, we create a directory {file}`backend/src/ploneconf/votable/behaviors` with an empty {file}`__init__.py` file.

To let Plone know about the behavior we are writing, we include the `behaviors` module in {file}`backend/src/ploneconf/votable/configure.zcml`:

```{code-block} xml
:linenos:

<configure xmlns="...">

  ...
  <include package=".behaviors" />
  ...

</configure>
```

Next, create a {file}`backend/src/ploneconf/votable/behaviors/configure.zcml` where we register our to-be-written behavior.

```{code-block} xml
:linenos:

<configure
    xmlns="http://namespaces.zope.org/zope"
    xmlns:browser="http://namespaces.zope.org/browser"
    xmlns:plone="http://namespaces.plone.org/plone"
    xmlns:zcml="http://namespaces.zope.org/zcml"
    i18n_domain="plone"
    >

  <include
      package="plone.behavior"
      file="meta.zcml"
      />

  <plone:behavior
      name="ploneconf.votable.votable"
      title="Votable"
      description="Support liking and disliking of content"
      factory=".votable.Votable"
      provides=".votable.IVotable"
      marker=".votable.IVotableMarker"
      />

</configure>
```

There are important differences compared to the first simple behavior in {ref}`behaviors1-label`:

- There is a `marker` interface.
- There is a `factory`.

The first simple behavior discussed in {ref}`behaviors1-label` was registered only with the `provides` attribute:

```xml
<plone:behavior
    title="Featured"
    name="ploneconf.featured"
    description="Control if a item is shown on the front page"
    provides=".featured.IFeatured"
    />
```

The `factory` is a class that provides the behavior logic and controls how the attributes from the behavior schema are accessed.
A factory in Plone/Zope is an `adapter`, which means a function or class that adapts an object to provide an interface.

We can use the following short form to access the features of a behavior of an object: `votable = IVotable(object)`.
The expression `IVotable(object)` is short for "Get the appropriate adapter for interface `IVotable` that is compatible with my object!".
The result is an adapted object with the behavior features.
You can for example get the value of votes with `IVotable(object).votes`.
But you can not get the votes with `object.votes`, as the object itself does not know about votes.
Only the adapted object `IVotable(object)` supports voting.

Since the `provides` interface is now provided by the adapter rather than the object itself,
the `marker` is introduced as a marker interface on the object.
This lets us register additional adapters only for objects that have the behavior.

We now implement what we registered.
Therefore we create a file {file}`backend/src/ploneconf/votable/behaviors/votable.py` with the schema, marker interface, and the factory.

```{code-block} python
:linenos:

from plone import api
from plone.autoform.directives import omitted
from plone.autoform.interfaces import IFormFieldProvider
from plone.supermodel import model
from plone.supermodel.directives import fieldset
from zope import schema
from zope.interface import Interface
from zope.interface import provider


class IVotableMarker(Interface):
    """Marker interface for content types or instances that should be votable"""

    pass


@provider(IFormFieldProvider)
class IVotable(model.Schema):
    """Schema for the votable behavior

    IVotable(object) returns the adapted object with votable behavior
    """

    votes = schema.Dict(
        title="Vote info",
        key_type=schema.TextLine(title="Voted number"),
        value_type=schema.Int(title="Voted so often"),
        default={},
        missing_value={},
        required=False,
    )
    voted = schema.List(
        title="List of users who voted",
        value_type=schema.TextLine(),
        default=[],
        missing_value=[],
        required=False,
    )

    if not api.env.debug_mode():
        omitted("votes")
        omitted("voted")

    fieldset(
        "debug",
        label="debug",
        fields=("votes", "voted"),
    )

    def vote():
        """
        Store the vote information and store the user(name)
        to ensure that the user does not vote twice.
        """

    def average_vote():
        """
        Return the average voting for an item.
        """

    def has_votes():
        """
        Return whether anybody ever voted for this item.
        """

    def already_voted():
        """
        Return the information wether a person already voted.
        """

    def clear():
        """
        Clear the votes. Should only be called by admins.
        """
```

```{only} not presentation
This is a lot of code.

The `IVotableMarker` interface is the marker interface.
It will be used to register REST API endpoints for objects that adapts this behavior.

The `IVotable` interface is the schema with fields and methods.

The `@provider` decorator of the class ensures that the schema fields are known to other packages.
Whenever some code wants all schemas of an object, it receives the schema defined directly on the object and the additional schemata.
Additional schemata are compiled by looking for behaviors and whether they provide the `IFormFieldProvider` functionality.
Only then the fields are used as form fields.

We create two schema fields for our internal data structure:
a dictionary to hold the votes given and a list to remember which jury members already voted and should not vote twice.

The `omitted` directive from `plone.autoform` allows us to hide the fields.
The fields are there to save the data but should not be edited directly.

Then we define the API that we are going to use in the frontend.
```

Now the only thing that is missing is the behavior implementation (the factory), which we add to {file}`backend/src/ploneconf/votable/behaviors/votable.py`.
The factory is an adapter that adapts a content item to the behavior interface `IVotable`.


```{code-block} python
:linenos:

from persistent.mapping import PersistentMapping
from persistent.list import PersistentList
from plone import api
from plone.autoform.directives import omitted
from plone.autoform.interfaces import IFormFieldProvider
from plone.supermodel import model
from plone.supermodel.directives import fieldset
from zope import schema
from zope.annotation.interfaces import IAnnotations
from zope.component import adapter
from zope.interface import implementer
from zope.interface import Interface
from zope.interface import provider

# ...

KEY = "ploneconf.votable.behaviors.votable.Votable"


@implementer(IVotable)
@adapter(IVotableMarker)
class Votable:
    """Adapter implementing the votable behavior"""

    def __init__(self, context):
        self.context = context
        annotations = IAnnotations(context)
        if KEY not in annotations.keys():
            # You know what happens if we don't use persistent classes here?
            annotations[KEY] = PersistentMapping({
                "voted": PersistentList(),
                "votes": PersistentMapping(),
            })
        self.annotations = annotations[KEY]

    # getter
    @property
    def votes(self):
        return self.annotations["votes"]

    # setter
    # def votes(self, value):
    #     """We do not define a setter.
    #     Function 'vote' is the only one that shall set attributes
    #     of the context object."""
    #     self.annotations["votes"] = value

    # getter
    @property
    def voted(self):
        return self.annotations["voted"]

    # setter
    # def voted(self, value):
    #     self.annotations["voted"] = value
```

In our `__init__` method we get *annotations* from the object.
We look for data with a key unique for this behavior.

If the annotation with this key does not exist, because no one has voted on this object yet, we create it.
We work with `PersistentMapping` and `PersistentList`.
A PersistentMapping is simply an implementation of the Python dict type (via the standard library UserDict base class) which ensures that changes are detected to store in the ZODB.

Next we provide the internal fields via properties.
Using this form of property makes them read-only properties, as we do not define setters/mutators.

As you have seen in the schema declaration, if you run your site in debug mode, you will see an edit field for these fields.
But trying to change these fields will throw an exception.

Let's continue with the behavior adapter:

```{code-block} python
:linenos:

    def vote(self, vote):
        if self.already_voted():
            raise KeyError("You may not vote twice.")
        vote = int(vote)
        current_user = api.user.get_current()
        self.annotations["voted"].append(current_user.id)
        votes = self.annotations.get("votes", {})
        if vote not in votes:
            votes[vote] = 1
        else:
            votes[vote] += 1

    def total_votes(self):
        return sum(self.annotations.get("votes", {}).values())

    def average_vote(self):
        total_votes = sum(self.annotations.get("votes", {}).values())
        if total_votes == 0:
            return 0
        total_points = sum([
            vote * count for (vote, count) in self.annotations.get("votes", {}).items()
        ])
        return float(total_points) / total_votes

    def has_votes(self):
        return len(self.annotations.get("votes", {})) != 0

    def already_voted(self):
        current_user = api.user.get_current()
        return current_user.id in self.annotations["voted"]

    def clear(self):
        annotations = IAnnotations(self.context)
        annotations[KEY] = PersistentMapping({
            "voted": PersistentList(),
            "votes": PersistentMapping(),
        })
        self.annotations = annotations[KEY]
```

The `voted` method stores names of users that already voted.
The `already_voted` method checks if the current user is saved in annotation value `voted`.

The `vote` method checks that the user did not already vote, then saves that the user did vote and saves the vote in the `votes` annotation value.

The methods `total_votes` and `average_votes` are self-explaining.
They calculate values that we want to use in a REST API endpoint.
The logic belongs to the behavior, not the service.

The method `clear` resets all votes.
The annotation of the context is set to an empty value like the `__init__` method does.


## Enable the behavior

Enable the behavior 'ploneconf.votable.votable' on content type 'talk':

Back in `mastering-plone-project`, add the behavior in {file}`backend/src/ploneconf/site/profiles/default/types/talk.xml`.

```{code-block} xml
:linenos:
:emphasize-lines: 8

  <property name="behaviors">
    <element value="plone.dublincore" />
    <element value="plone.namefromtitle" />
    <element value="ploneconf.featured" />
    <element value="plone.versioning" />
    <element value="plone.eventbasic" />
    <element value="plone.textindexer" />
    <element value="ploneconf.votable.votable" />
  </property>
```

Restart your backend and re-install the package `ploneconf.site`.
