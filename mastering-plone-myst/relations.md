# Relations

```{eval-rst}
.. todo::

    * Add screenshots for relationfields in Volto
    * Create relations between talk and speaker
    * Display relations (and backrelations)
```

You can model relationships between content items by placing them in a hierarchy (a folder *speakers* containing the (folderish) speakers and within each speaker the talks) or by linking them to each other in Richtext fields. But where would you store a talk that two speakers give together?

Relations allow developers to model relationships between objects without using links or a hierarchy. The behavior {py:class}`plone.app.relationfield.behavior.IRelatedItems` provides the field {guilabel}`Related Items` in the tab {guilabel}`Categorization`. That field simply says `a` is somehow related to `b`.

By using custom relations you can model your data in a much more meaningful way.

## Creating relations in a schema

Relate to one item only.

```{code-block} python
:linenos: true

from plone.app.vocabularies.catalog import CatalogSource
from z3c.relationfield.schema import RelationChoice
from z3c.relationfield.schema import RelationList

evil_mastermind = RelationChoice(
    title=_(u'The Evil Mastermind'),
    vocabulary='plone.app.vocabularies.Catalog',
    required=False,
)
```

Relate to multiple items.

```python
from z3c.relationfield.schema import RelationChoice
from z3c.relationfield.schema import RelationList

minions = RelationList(
    title=_(u'Minions'),
    default=[],
    value_type=RelationChoice(
        vocabulary='plone.app.vocabularies.Catalog',
    )
    required=False,
)
```

We can see that the [code for the behavior IRelatedItems](https://github.com/plone/plone.app.relationfield/blob/master/plone/app/relationfield/behavior.py) does exactly the same.

## Controlling what to relate to

The best way to control wich item should be relatable to is to configure the widget with `directives.widget()`.
In the following example you can only relate to Documents:

```{code-block} python
:emphasize-lines: 12
:linenos: true

from plone.app.z3cform.widget import RelatedItemsFieldWidget

relationchoice_field = RelationChoice(
    title=u"Relationchoice field",
    vocabulary='plone.app.vocabularies.Catalog',
    required=False,
)
directives.widget(
    "relationchoice_field",
    RelatedItemsFieldWidget,
    pattern_options={
        "selectableTypes": ["Document"],
    },
)
```

The following example applies *pattern-option* `basePath` to force the widget to start browsing the site at the site-root using the method `plone.app.multilingual.browser.interfaces.make_relation_root_path`.
By default the widget starts with the current context.

```{code-block} python
:emphasize-lines: 11
:linenos: true

relationlist_field = RelationList(
    title=u"Relationlist Field",
    default=[],
    value_type=RelationChoice(vocabulary='plone.app.vocabularies.Catalog'),
    required=False,
    missing_value=[],
)
directives.widget(
    "relationlist_field",
    RelatedItemsFieldWidget,
    vocabulary='plone.app.vocabularies.Catalog',
    pattern_options={
        "basePath": make_relation_root_path,
    },
)
```

Instead of using a named vocabulary we can also use `source`:

```{code-block} python
:emphasize-lines: 9
:linenos: true

from plone.app.vocabularies.catalog import CatalogSource
from z3c.relationfield.schema import RelationChoice
from z3c.relationfield.schema import RelationList

minions = RelationList(
    title=_(u'Talks by this speaker'),
    value_type=RelationChoice(
        title=_(u'Talks'),
        source=CatalogSource(portal_type=['one_eyed_minion', 'minion'])),
    required=False,
)
directives.widget(
    'minions',
    RelatedItemsFieldWidget,
    pattern_options={'mode': 'search'},
)
```

You can pass to `CatalogSource` the same arguments you use for catalog queries.
This makes it very flexible for limiting relateable items by type, path, date, and so on.

Setting the mode of the widget to `search` makes it easier to select from the content that result form your catalog-query instead of having to navigate through your content-tree.

The `RelatedItemsFieldWidget` also allow you to set favorites:

```{code-block} python
:linenos: true

directives.widget(
    'minions',
    RelatedItemsFieldWidget,
    pattern_options={
        'favorites': [{'title': 'Minions', 'path': '/Plone/minions'}]
    },
)
```

`favorites` can also be a method that takes the current context. Here is a full example as a behavior:

```{code-block} python
:linenos: true

from plone import api
from plone.app.vocabularies.catalog import CatalogSource
from plone.app.z3cform.widget import RelatedItemsFieldWidget
from plone.autoform import directives
from plone.autoform.interfaces import IFormFieldProvider
from plone.supermodel import model
from z3c.relationfield.schema import RelationChoice
from z3c.relationfield.schema import RelationList
from zope.interface import provider


def minion_favorites(context):
    portal = api.portal.get()
    minions_path = '/'.join(portal['minions'].getPhysicalPath())
    one_eyed_minions_path = '/'.join(portal['one-eyed-minions'].getPhysicalPath())
    return [
            {
                'title': 'Current Content',
                'path': '/'.join(context.getPhysicalPath())
            }, {
                'title': 'Minions',
                'path': minions_path,
            }, {
                'title': 'One eyed minions',
                'path': one_eyed_minions_path,
            }
        ]


@provider(IFormFieldProvider)
class IHaveMinions(model.Schema):

    minions = RelationList(
        title='My minions',
        default=[],
        value_type=RelationChoice(
            source=CatalogSource(
                portal_type=['one_eyed_minion', 'minion'],
                review_state='published',
            )
        ),
        required=False,
    )
    directives.widget(
        'minions',
        RelatedItemsFieldWidget,
        pattern_options={
            'mode': 'auto',
            'favorites': minion_favorites,
            }
        )
```

For even more flexibility, you can create your own [dynamic vocabularies](https://docs.plone.org/external/plone.app.dexterity/docs/advanced/vocabularies.html#dynamic-sources).

For more examples how to use relationfields look at {ref}`dexterity_reference-label`.

## Use a tailor shaped widget for relations

Sometimes the widget for relations is not what you want since it can be hard to navigate to the content you want to relate to. With SelectFieldWidget and a custom vocabulary you can shape a widget for an easier selection of related items:

```{code-block} python
:emphasize-lines: 9, 15
:linenos: true

from plone.app.z3cform.widget import SelectFieldWidget
from plone.autoform import directives
from z3c.relationfield.schema import RelationChoice
from z3c.relationfield.schema import RelationList

relationlist_field_select = RelationList(
    title=u'Relationlist with select widget',
    default=[],
    value_type=RelationChoice(vocabulary='ploneconf.site.vocabularies.documents'),
    required=False,
    missing_value=[],
)
directives.widget(
    'relationlist_field_select',
    SelectFieldWidget,
)
```

Register the vocabulary like this in `configure.zcml`:

```xml
<utility
    name="ploneconf.site.vocabularies.documents"
    component="ploneconf.site.vocabularies.DocumentVocabularyFactory" />
```

Note that the value is the object itself, not the uuid. This is a requirement of the field-type:

```{code-block} python
:linenos: true

from plone import api
from zope.interface import implementer
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary

@implementer(IVocabularyFactory)
class DocumentVocabulary(object):
    def __call__(self, context=None):
        terms = []
        # Use getObject since the DataConverter expects a real object.
        for brain in api.content.find(portal_type='Document', sort_on='sortable_title'):
            terms.append(SimpleTerm(
                value=brain.getObject(),
                token=brain.UID,
                title=u'{} ({})'.format(brain.Title, brain.getPath()),
            ))
        return SimpleVocabulary(terms)

DocumentVocabularyFactory = DocumentVocabulary()
```

The field should then look like this:

:::{figure} _static/relations_with_selectwidget.png
:alt: RelationList field with select widget SelectFieldWidget

RelationList field with select widget SelectFieldWidget and custom vocabulary
:::

:::{warning}
This approach is bad for performance if the vocabulary will contain a lot of content.
:::

## Accessing and displaying related items

To display related items you can use the render method of the default widget e.g.:

```html
<div tal:content="structure view/w/evil_mastermind/render" />
```

This would render the related items like this:

:::{figure} https://user-images.githubusercontent.com/453208/77223704-4b714100-6b5f-11ea-855b-c6e209f1c25c.png
:alt: Default rendering of a RelationList (since Plone 5.2.2)
:::

If you want to access and render relations yourself you can use the Plone add-on [collective.relationhelpers](https://pypi.org/project/collective.relationhelpers) and add a method like in the following example.

```{code-block} python
:linenos: true

from collective.relationhelpers import api as relapi
from Products.Five import BrowserView


class EvilMastermindView(BrowserView):

    def minions(self):
        """Returns a list of related items."""
        return relapi.relations(self.context, 'underlings')
```

It returns the related items so that you will able to render them anyhow you like.

## Creating RelationFields through the web

It is surprisingly easy to create RelationFields through the web

- Using the Dexterity schema editor, add a new field and select *Relation List* or *Relation Choice*, depending on whether you want to relate to multiple items or not.
- When configuring the field you can even select the content type the relation should be limited to.

When you click on `Edit XML field model` you will see the fields in the XML schema:

RelationChoice:

```python
<field name="boss" type="z3c.relationfield.schema.RelationChoice">
  <description/>
  <required>False</required>
  <title>Boss</title>
</field>
```

RelationList:

```{code-block} python
:linenos: true

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
```

## Accessing relations and backrelations from code

The recommended way to create and read relations and backrelations as a developer is to use [collective.relationhelpers](https://pypi.org/project/collective.relationhelpers).

## The stack

Relations are based on [zc.relation](https://pypi.org/project/zc.relation/).
This package stores transitive and intransitive relationships.
It allows complex relationships and searches along them.
Because of this functionality, the package is a bit complicated.

The package `zc.relation` provides its own catalog, a relation catalog.
This is a storage optimized for the queries needed.
`zc.relation` is sort of an outlier with regards to Zope documentation. It has extensive documentation, with a good level of doctests for explaining things.

You can use `zc.relation` to store the objects and its relations directly into the catalog.
But the additional packages that make up the relation functionality don't use the catalog this way.

We want to work with schemas to get auto generated forms.
The logic for this is provided by the package [z3c.relationfield](https://pypi.org/project/z3c.relationfield/).
This package contains the RelationValue object and everything needed to define a relation schema, and all the code that is necessary to automatically update the catalog.

A RelationValue Object does not reference all objects directly.
For the target, it uses an id it gets from the `IntId` Utility. This id allows direct recovery of the object. The source object stores it directly.

Widgets are provided by `plone.app.z3cform` and some converters are provided by `plone.app.relationfield`.
The widget that Plone uses can also store objects directly.
Because of this, the following happens when saving a relation via a form:

1. The HTML shows some nice representation of selectable objects.
2. When the user submits the form, selected items are submitted by their UUIDs.
3. The Widget retrieves the original object with the UUID.
4. Some datamanager gets another unique ID from an IntID Tool.
5. The same datamanager creates a RelationValue from this id, and stores this relation value on the source object.
6. Some Event handlers update the catalogs.

You could delete a Relation like this `delattr(rel.from_object, rel.from_attribute)`

This is a terrible idea by the way, because when you define in your schema that one can store multiple RelationValues, your Relation is stored in a list on this attribute.

Relations depend on a lot of infrastructure to work.
This infrastructure in turn depends a lot on event handlers being thrown properly.
When this is not the case things can break.
Because of this, there is a method `isBroken` which you can use to check if the target is available.

There are alternatives to using Relations. You could instead just store the UUID of an object.
But using real relations and the catalog allows for very powerful things.
The simplest concrete advantage is the possibility to see what links to your object.

The built-in linkintegrity feature of Plone 5 is also implemented using relations.

## RelationValues

RelationValue objects have a fairly complete API.
For both target and source, you can receive the IntId, the object and the path.
On a RelationValue, the terms `source` and `target` aren't used. Instead, they are `from` and `to`.
So the API for getting the target is:

- `to_id`
- `to_path`
- `to_object`

In addition, the relation value knows under which attribute it has been stored as `from_attribute`. It is usually the name of the field with which the relation is created.
But it can also be the name of a relation that is created by code, e.g. linkintegrity relations (`isReferencing`) or the relation between a working copy and the original (`iterate-working-copy`).
