---
myst:
  html_meta:
    "description": "Extend arbitrary content types with behaviors and fields"
    "property=og:description": "Extend arbitrary content types with behaviors and fields"
    "property=og:title": "Complex behaviors"
    "keywords": "Plone, behavior, fields, extending"
---


(behaviors2-label)=

# Complex Behaviors [voting story]

A group of jury members vote on talks to be accepted for the conference.

````{card} Backend chapter

Get the backend code! 
[training.votable](https://github.com/collective/training.votable)
````

```{card}
In this part you will:

- Write a behavior that enables voting on content
- Use annotations to store the votes on an object

Topics covered:

- Behaviors with a factory class
- Marker interface for a behavior
- Using annotations as storage layer
```


(behaviors2-schema-label)=

## Schema and Annotation

The talks are being voted.
So we provide an additional field with our behavior to store the votes on a talk.
Therefore the behavior will have a schema with a field "votes".

We mark the field "votes" as an omitted field as this field should not be edited directly.

We are going to store the information about "votes" in an `annotation`.
Imagine an add-on that unfortunately uses the same field name "votes" like we do for another purpose.
Here the AnnotationStorage comes in.
The content type instance is equipped by a storage where behaviors do store values with a key unique per behavior.


(behaviors2-code-label)=

## The Code

Open your backend add-on you have been creating in the last chapter in your editor.

Later in your daily work you will use {term}`plonecli` to generate a behavior.
In this training we go step by step through the code to understand a behavior and its capabilities.

To start, we create a directory {file}`behaviors` with an empty {file}`behaviors/__init__.py` file.

To let Plone know about the behavior we are writing, we include the behavior module:

```{code-block} xml
:linenos:

<configure xmlns="...">

  ...
  <include package=".behaviors" />
  ...

</configure>
```

Next, create a {file}`behaviors/configure.zcml` where we register our to be written behavior.

```{code-block} xml
:linenos:
:emphasize-lines: 15-16

<configure
  xmlns="http://namespaces.zope.org/zope"
  xmlns:browser="http://namespaces.zope.org/browser"
  xmlns:plone="http://namespaces.plone.org/plone"
  xmlns:zcml="http://namespaces.zope.org/zcml"
  i18n_domain="plone">

    <include package="plone.behavior" file="meta.zcml"/>

    <plone:behavior
        name="training.votable.votable"
        title="Votable"
        description="Support liking and disliking of content"
        provides=".votable.IVotable"
        factory=".votable.Votable"
        marker=".votable.IVotableMarker"
        />

</configure>
```

There are important differences to the first simple behavior in {ref}`behaviors1-label`:

- There is a marker interface
- There is a factory

The first simple behavior discussed in {ref}`behaviors1-label` has been registered only with the `provides` attributes:

```xml
<plone:behavior
    title="Featured"
    name="ploneconf.featured"
    description="Control if a item is shown on the frontpage"
    provides=".featured.IFeatured"
    />
```

The `factory` is a class that provides the behavior logic and gives access to the attributes we provide.
A factory in Plone/Zope is an `adapter`, that means a function that adapts an object to provide an interface.
We can use the following short form to access the features of a behavior of an object with `votable = IVotable(object)`.
The expression `IVotable(object)` is short for "Get the appropriate adapter for interface `IVotable` and apply it to my object!".
The result is an adopted object with the behavior features.
You can for example get the value of votes by `IVotable(object).votes`.
But you can not get the votes by `object.votes`, as the object does not know about votes.
Only the adapted object `IVotable(object)` does know about votes.

The `marker` is introduced to register REST API endpoints for objects that adapts the behavior.


We now implement what we registered.
Therefore we create a file {file}`/behaviors/votable.py` with the schema, marker interface, and the factory.

```{code-block} python
:linenos:

class IVotableMarker(Interface):
    """Marker interface for content types or instances that should be votable"""

    pass


@provider(IFormFieldProvider)
class IVotable(model.Schema):
    """Behavior interface for the votable behavior

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
        form.omitted("votes")
        form.omitted("voted")

    directives.fieldset(
        "debug",
        label="debug",
        fields=("votes", "voted"),
    )

    def vote(request):
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

    def already_voted(request):
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

We create two schema fields for our internal data structure.
A dictionary to hold the votes given and a list to remember which jury members already voted and should not vote twice.

The directives `form.omitted` from `plone.autoform` allow us to hide the fields.
The fields are there to save the data but should not be edited directly.

Then we define the API that we are going to use in the frontend.
```

Now the only thing that is missing is the behavior implementation, the factory, which we add to {file}`behaviors/votable.py`.
The factory is an adapter that adapts a talk to the behavior interface `IVotable`.


```{code-block} python
:linenos:


KEY = "training.votable.behaviors.votable.Votable"

@implementer(IVotable)
@adapter(IVotableMarker)
class Votable(object):
    """Adapter implementing the votable behavior"""

    def __init__(self, context):
        self.context = context
        annotations = IAnnotations(context)
        if KEY not in annotations.keys():
            # You know what happens if we don't use persistent classes here?
            annotations[KEY] = PersistentDict(
                {"voted": PersistentList(), "votes": PersistentDict()}
            )
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

    def vote(self, vote, request):
        if self.already_voted(request):
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
        total_points = sum(
            [
                vote * count
                for (vote, count) in self.annotations.get("votes", {}).items()
            ]
        )
        return float(total_points) / total_votes

    def has_votes(self):
        return len(self.annotations.get("votes", {})) != 0

    def already_voted(self, request):
        current_user = api.user.get_current()
        return current_user.id in self.annotations["voted"]

    def clear(self):
        annotations = IAnnotations(self.context)
        annotations[KEY] = PersistentDict(
            {"voted": PersistentList(), "votes": PersistentDict()}
        )
        self.annotations = annotations[KEY]

```

In our `__init__` method we get *annotations* from the object.
We look for data with a key unique for this behavior.

If the annotation with this key does not exist, cause the object is not already voted, we create it.
We work with `PersistentDict` and `PersistentList`.

% TODO Explain  `PersistentDict` and `PersistentList` in short.

Next we provide the internal fields via properties.
Using this form of property makes them read-only properties, as we do not define write handlers.

As you have seen in the Schema declaration, if you run your site in debug mode, you will see an edit field for these fields.
But trying to change these fields will throw an exception.


Let's continue with the bahavior adapter:

```{code-block} python
:linenos:

    def vote(self, vote, request):
        if self.already_voted(request):
            raise KeyError("You may not vote twice")
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
        total_points = sum(
            [
                vote * count
                for (vote, count) in self.annotations.get("votes", {}).items()
            ]
        )
        return float(total_points) / total_votes

    def has_votes(self):
        return len(self.annotations.get("votes", {})) != 0

    def already_voted(self, request):
        current_user = api.user.get_current()
        return current_user.id in self.annotations["voted"]

    def clear(self):
        annotations = IAnnotations(self.context)
        annotations[KEY] = PersistentDict(
            {"voted": PersistentList(), "votes": PersistentDict()}
        )
        self.annotations = annotations[KEY]
```

The `voted` method stores names of users that already voted.
Whereas the `already_voted` method checks if the user name is saved in annotation value `voted`.

The `vote` method requires a vote and a request.
We check the precondition that the user did not already vote, then we save that the user did vote and save his vote in `votes` annotation value.

The methods `total_votes` and `average_votes` are self-explaining.
They calculate values that we want to use in a REST API endpoint.
The logic belongs to the behavior not the service.

The method `clear` allows to reset votes.
Therefore the annotation of the context is set to an empty value like the `__init__`method does.
