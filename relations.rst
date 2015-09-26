Relations
=========

Relations are a difficult topic. To master relations you must understand the
stack of packages involved.

Relations are based on `zc.relation`. This package allows to store transitive
and intransitive n-ary relationships. It allows for complex relationships
and searches along them. Because of this functionality, the package is a bit
complicated.

The package `zc.relation` provides its own catalog, a relation catalog. This is
a storage optimized for the queries needed. `zc.relation` is sort of an outlier
with regards to zope documentation. It has extensive documentation, with a good
level of doctests for explaining things.

You can use `zc.relation` to store the objects and its relations directly into
the catalog. But the additional packages that make up the relation functionality don't use the catalog this way.

We want to work with schemas to get auto generated forms.
The logic for this is provided by the package `z3c.relationfield`. This package
contains the RelationValue object and everything needed to define a relation
schema, and all the code that is necessary to automatically update the catalog.

A RelationValue Object does not reference all objects directly. For the target,
it uses an id it gets from the `IntId` Utility. This id allows direct recovery
of the object. The source object stores it directly.

Widgets are provided by `plone.app.z3cform`. Some converters are provided by `plone.app.relationfield`.
The widget that Plone uses can also store objects directly.
Because of this, the following happens when saving a relation via a form:

1. The html shows some nice representation of selectable objects.
2. When the user submits the form, selected items are submitted by their UUIDs.
3. The Widget retrieves the original object with the UUID.
4. Some Datamanager gets another unique ID from an IntID Tool.
5. The same datamanager creates a RelationValue from this id, and stores this relation value on the source object.
6. Some Event handlers update the catalogs.

It is surprisingly easy to to use RelationFields.

I show you how to do it TTW...

If you want to modify Relations, you have to create or delete RelationValue objects.
If you want to find out what objects are related to each other, you use the relation catalog.
Here is an example:

.. literalinclude:: ploneconf.site_sneak/chapters/final/src/ploneconf/site/browser/speaker.py

RelationValue objects have a fairly
complete API.
For both target and source, you can receive the IntId, the object and the path.
On a RelationValue, the terms `source` and `target` aren't used. Instead, they
are `from` and `to`. So the API for getting the target is:

- `to_id`
- `to_path`
- `to_object`

In addition, the relation value knows under which attribute it has been
stored. You could delete a Relation like this `delattr(rel.from_object,
rel.from_attribute)`

This is a terrible idea by the way, because when you define in your schema
that one can store multiple RelationValues, your Relation is stored in a list
on this attribute.

Relations depend on a lot of infrastructure to work.
This infrastructure in turn depends a lot on event handlers being thrown
properly. When this is not the case things can break.
Because of this, there is a method `isBroken` which you can use to check if
the target is available.

There are alternatives to using Relations. You could instead just store the UUID of an object.
But Using real relations and the catalog allows for very powerful things. The simplest concrete advantage is the possibility to see what links to your object.
