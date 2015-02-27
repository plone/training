Relations
=========

Relations are a difficult topic. To master relations you must understand the
stack of packages involved.

Relations are based on `zc.relation` This package allows to store transitive
and intransitive n-ary relationships. It allows to for complex relationships
and searches along them. Because of this functionality, the package is a bit
complicated.

The package `zc.relation` provides its own catalog, a relation catalog. This is
a storage optimized for the queries needed. `zc.relation` is sort of an outlier
with regards to documentation. It has extensive documentation, with a good
level of doctests for explaining things.

You can use `zc.relation` to store the objects and its relations directly into
the catalog. But the default way usually involves storing a RelationValue
object that references both sides of a relation.

The logic for this is provided by the package `z3c.relationfield`. This package
contains the RelationValue object and everything needed to define a relation
schema, and all the code that is necessary to automatically update the catalog.

A RelationValue Object does not reference all objects directly. For the target,
it uses an id it gets from the `IntId` Utility. This id allows direct recovery
of the obect. The source object it stores directly.

Luckily you don't need to know most of this for most of the time. There is
a complete API to work with relations.

XXX
You work with RelationValue Objects. RelationValue objects have a fairly
complete API.
for both target and source, you can receive the IntId, the object and the path.
On a RelationValue, the terms `source` and `target` aren't used. Instead, they
are `from` and `to`. So the API for getting the target is:

- `to_id`
- `to_path`
- `to_object`

In addition, the relation value knows, under which attribute it has been
stored. You could delete a Relation like this `delattr(rel.from_object,
rel.from_attribute)`

This is a terrible idea by the way, because when you define in your schema,
that one can store multiple RelationValues, your Relation is stored in a list
on this attribute.

Relations depend on a lot of infrastructure to work.
This infrastructure in turn depends a lot on event handlers being thrown
properly. When this is not the case. things can break.
Because of this, there is a method `isBroken` which you can use to check, if
the target is available.


