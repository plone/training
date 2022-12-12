---
myst:
  html_meta:
    "description": ""
    "property=og:description": ""
    "property=og:title": ""
    "keywords": ""
---

# Relations

You can model relationships between content items by placing them in a hierarchy (a folder *speakers* containing the (folderish) speakers and within each speaker the talks) or by linking them to each other in Richtext fields. But where would you store a talk that two speakers give together?

Relations allow developers to model relationships between objects without using links or a hierarchy. The behavior {py:class}`plone.app.relationfield.behavior.IRelatedItems` provides the field {guilabel}`Related Items` in the tab {guilabel}`Categorization`. That field simply says `a` is somehow related to `b`.

By using custom relations you can model your data in a much more meaningful way.

## Creating relations in a schema

Relate to one item only.

```python
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

Instead of using a named vocabulary we can also use `source`:

```python
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
```

You can pass to `CatalogSource` the same arguments you use for catalog queries.
This makes it very flexible for limiting relateable items by type, path, date, and so on.

For even more flexibility, you can create your own [dynamic vocabularies](https://5.docs.plone.org/external/plone.app.dexterity/docs/advanced/vocabularies.html#dynamic-sources).

For more examples how to use relationfields look at {ref}`plone5-dexterity-reference-label`.

Sometimes the widget for relations is not what you want since it can be hard to navigate to the content you want to relate to. To use the SelectFieldWidget you can specify it if you use your own vocabulary:

```python
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

```python
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

```{figure} _static/relations_with_selectwidget.png
:alt: RelationList with select widget

RelationList with select widget
```

## Accessing and displaying related items

It is easiest way to display related items is to use the render method of the default widget. That works well if you use `plone.app.z3cform = 3.2.0` (you can use that in Plone 5.2).

```html
<div tal:content="structure view/w/evil_mastermind/render" />
```

This would render the related items as shown in <https://github.com/plone/plone.app.z3cform/pull/111>.

For Plone 5.2.1 and older you still need to deal with that yourself since the widget only shows the uuid.

If you want or need to access and render relations yourself you could add a method like in the following example.

```python
from plone.app.contentlisting.interfaces import IContentListing
from Products.Five import BrowserView


class EvilMastermindView(BrowserView):

    def minions(self):
        """Returns a list of related items."""
        results = []
        for rel in self.context.underlings:
            if rel.isBroken():
                # skip broken relations
                continue
            obj = rel.to_object
            if api.user.has_permission('View', obj=obj):
                results.append(obj)
        return IContentListing(results)
```

It returns the related items so that you will able to render them anyway you like.

```{note}
Using `IContentListing` to wrap list of objects or brain has a lot of benefits since it allows unified access to them.
It also allows you to use great helper-methods like `obj.MimeTypeIcon()` or `appendViewAction()` that will make your code more concise.
See <https://github.com/plone/plone.app.contentlisting/#methods-of-contentlistingobjects> for a list of all avilable methods.
```

You could display the links like this:

```xml
<ul>
  <li tal:repeat="item view.minions()">
    <span tal:define="item_type           python:item.portal_type;
                      item_type_class     python:item.ContentTypeClass();
                      item_wf_state_class python:item.ReviewStateClass();
                      appendViewAction    python:item.appendViewAction();
                      item_url            python:item.getURL();
                      item_url            python:item_url+'/view' if appendViewAction else item_url;"
          tal:attributes="title item_type">

      <a tal:attributes="href item_url">
        <img class="mime-icon"
             tal:condition="python:item_type =='File'"
             tal:attributes="src python:item.MimeTypeIcon();">

        <span tal:attributes="class string:$item_type_class $item_wf_state_class url;"
              tal:content="python:item.Title()">
            Title
        </span>
        <span class="discreet"
              tal:content="python:item.Description()">
            Description
        </span>
      </a>
    </span>
  </li>
</ul>
```

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

```python
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

## The stack

Relations are based on [zc.relation](https://pypi.org/project/zc.relation/).
This package stores transitive and intransitive relationships.
It allows for complex relationships and searches along them.
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

## Accessing relations and backrelations from code

If you want to find out which objects are related to each other, you use the relation catalog. Here is a convenience method that allows you to find all kinds of relations.

```python
from zc.relation.interfaces import ICatalog
from zope.component import getUtility
from zope.intid.interfaces import IIntIds
from plone.app.linkintegrity.handlers import referencedRelationship


def example_get_backlinks(obj):
    backlinks = []
    for rel in get_backrelations(attribute=referencedRelationship):
        if rel.isBroken():
            backlinks.append(dict(href='',
                                  title='broken reference',
                                  relation=rel.from_attribute))
        else:
            obj = rel.from_object
            backlinks.append(dict(href=obj.absolute_url(),
                                  title=obj.title,
                                  relation=rel.from_attribute))
    return backlinks

def get_relations(obj, attribute=None, backrefs=False):
    """Get any kind of references and backreferences"""
    int_id = get_intid(obj)
    if not int_id:
        return retval

    relation_catalog = getUtility(ICatalog)
    if not relation_catalog:
        return retval

    query = {}
    if attribute:
        # Constrain the search for certain relation-types.
        query['from_attribute'] = attribute

    if backrefs:
        query['to_id'] = int_id
    else:
        query['from_id'] = int_id

    return relation_catalog.findRelations(query)


def get_backrelations(obj, attribute=None):
    return get_relations(obj, attribute=attribute, backrefs=True)


def get_intid(obj):
    """Return the intid of an object from the intid-catalog"""
    intids = component.queryUtility(IIntIds)
    if intids is None:
        return
    # check that the object has an intid, otherwise there's nothing to be done
    try:
        return intids.getId(obj)
    except KeyError:
        # The object has not been added to the ZODB yet
        return
```
