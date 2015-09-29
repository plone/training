Relations
=========

You can model relationships between content items by placing them in a hierarchy (a folder *speakers* containing the (folderish) speakers and within each speaker the talks) or by linking them to each other in Richtext-Fields. But where would you store a talk that two speakers give together together?

Relations allow developers to model relationships between objects without a links or a hierarchy. The behavior ``plone.app.relationfield.behavior.IRelatedItems`` provides the field *Related Items* in the tab *Categorization*. That field simply says ``a`` is somehow related to ``b``.

By using custom relations you can model your data in a much more meaningful way.


Creating relations in a schema
------------------------------

Relate to one item only.

.. code-block:: python

    from plone.app.vocabularies.catalog import CatalogSource
    from z3c.relationfield.schema import RelationChoice
    from z3c.relationfield.schema import RelationList

    the_boss = RelationChoice(
        title=_(u'The Boss'),
        vocabulary='plone.app.vocabularies.Catalog',
        required=False,
    )

Relate to multiple items.

.. code-block:: python

    from z3c.relationfield.schema import RelationChoice
    from z3c.relationfield.schema import RelationList

    underlings = RelationList(
        title=_(u'Underlings'),
        default=[],
        value_type=RelationChoice(
            vocabulary='plone.app.vocabularies.Catalog',
        required=False,
    )

We can see that the `code for the behavior IRelatedItems <https://github.com/plone/plone.app.relationfield/blob/master/plone/app/relationfield/behavior.py>`_ does exactly the same.

Instead of using a named vocabulary we can also use ``source``:

.. code-block:: python

    from plone.app.vocabularies.catalog import CatalogSource
    from z3c.relationfield.schema import RelationChoice
    from z3c.relationfield.schema import RelationList

    talks = RelationList(
        title=_(u'Talks by this speaker'),
        value_type=RelationChoice(
            title=_(u'Talks'),
            source=CatalogSource(portal_type=['talk', 'training'])),
        required=False,
    )

To ``CatalogSource`` you can pass the same argument that you use for catalog-queries.
This makes it very flexible to limit relateable items by type, path, date etc.
For even more flexibility you can create your own `dynamic vocabularies <http://docs.plone.org/external/plone.app.dexterity/docs/advanced/vocabularies.html#dynamic-sources>`_.


Accessing and displaying related items
--------------------------------------


TODO!

To display relations in a template the simplest way is to use the render-version of the default-widget.

For reference look at how the default viewlet displays the information for related items stored by the behavior ``IRelatedItems``.
This is the python-path for the viewlet: ``plone.app.layout.viewlets.content.ContentRelatedItems``
This is the file-path for the template: ``plone/app/layout/viewlets/document_relateditems.pt``



Creating Relationfields through the web
---------------------------------------

It is surprisingly easy to create RelationFields through the web

- In the dexterity schema-editor add a new field and select *Relation List* or *Relation Choice*, depending on wether you want to relate to multiple items or not.
- When configuring the field you can even select the content-type the relation should be limited to.

When you click on ``Edit xml field model`` you will see the fields in the xml-schema:

RelationChoice:

..  code-block:: python

    <field name="boss" type="z3c.relationfield.schema.RelationChoice">
      <description/>
      <required>False</required>
      <title>Boss</title>
    </field>

RelationList:

..  code-block:: python

    <field name="underlings" type="z3c.relationfield.schema.RelationList">
      <description/>
      <required>False</required>
      <title>Underlings</title>
      <value_type type="z3c.relationfield.schema.RelationChoice">
        <title i18n:translate="">Relation Choice</title>
        <portal_type>
          <element>Document</element>
          <element>News Item</element>
        </portal_type>
      </value_type>
    </field>


The stack
---------

Relations are based on `zc.relation <https://pypi.python.org/pypi/zc.relation/>`_.
This package allows to store transitive and intransitive relationships.
It allows for complex relationships and searches along them.
Because of this functionality, the package is a bit complicated.

The package `zc.relation` provides its own catalog, a relation catalog.
This is a storage optimized for the queries needed.
`zc.relation` is sort of an outlier with regards to zope documentation. It has extensive documentation, with a good level of doctests for explaining things.

You can use `zc.relation` to store the objects and its relations directly into the catalog.
But the additional packages that make up the relation functionality don't use the catalog this way.

We want to work with schemas to get auto generated forms.
The logic for this is provided by the package `z3c.relationfield <https://pypi.python.org/pypi/z3c.relationfield/>`_.
This package contains the RelationValue object and everything needed to define a relation schema, and all the code that is necessary to automatically update the catalog.

A RelationValue Object does not reference all objects directly.
For the target, it uses an id it gets from the `IntId` Utility. This id allows direct recovery of the object. The source object stores it directly.

Widgets are provided by `plone.app.z3cform` and some converters are provided by `plone.app.relationfield`.
The widget that Plone uses can also store objects directly.
Because of this, the following happens when saving a relation via a form:

1. The html shows some nice representation of selectable objects.
2. When the user submits the form, selected items are submitted by their UUIDs.
3. The Widget retrieves the original object with the UUID.
4. Some datamanager gets another unique ID from an IntID Tool.
5. The same datamanager creates a RelationValue from this id, and stores this relation value on the source object.
6. Some Event handlers update the catalogs.

If you want to modify Relations in code, you have to create or delete RelationValue objects.
If you want to find out what objects are related to each other, you use the relation catalog.
Here is an example:

.. literalinclude:: ploneconf.site_sneak/chapters/final/src/ploneconf/site/browser/speaker.py

RelationValue objects have a fairly complete API.
For both target and source, you can receive the IntId, the object and the path.
On a RelationValue, the terms `source` and `target` aren't used. Instead, they are `from` and `to`.
So the API for getting the target is:

- `to_id`
- `to_path`
- `to_object`

In addition, the relation value knows under which attribute it has been stored. You could delete a Relation like this `delattr(rel.from_object, rel.from_attribute)`

This is a terrible idea by the way, because when you define in your schema that one can store multiple RelationValues, your Relation is stored in a list on this attribute.

Relations depend on a lot of infrastructure to work.
This infrastructure in turn depends a lot on event handlers being thrown properly.
When this is not the case things can break.
Because of this, there is a method `isBroken` which you can use to check if the target is available.

There are alternatives to using Relations. You could instead just store the UUID of an object.
But using real relations and the catalog allows for very powerful things.
The simplest concrete advantage is the possibility to see what links to your object.

The builtin linkintegrity-feature of Plone 5 is also built using relations.
