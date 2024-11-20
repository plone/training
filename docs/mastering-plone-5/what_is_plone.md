---
myst:
  html_meta:
    "description": ""
    "property=og:description": ""
    "property=og:title": ""
    "keywords": ""
---

(plone5-intro-what-is-plone-label)=

# What is Plone?

Plone is an open source Content Management System (CMS) built in Python.

- Open-Source Enterprise-CMS
- Written in Python
- Plone 5.1 and below support Python 2.7
- Plone 5.2 and later support Python 3.8, 3.7, 3.6 and 2.7
- [RESTful hypermedia API](https://github.com/plone/plone.restapi/)
- Based on the Web-Framework Zope
- Database: "Zope Object Database" (ZODB) or ORM & SQL/Postgres/Oracle
- Runs on Linux, Mac OS, BSD, Solaris, NixOS and Windows

Plone has a multitude of powerful features, is easily accessible to editors but also fun for programmers.

- Workflow-driven, collaborative management of content
- Industrial Strength Security and Access-Control
- Limitless Extensibility

```{note}
The modular and open component architecture of Plone allows you to change or extend Plone in every respect!
```

## Core concepts

### Traversal

- Plone uses [Traversal](https://5.docs.plone.org/develop/plone/serving/traversing.html) (portal/folder/document) instead of Routing
- Python objects in a object tree that looks like a huge nested dictionary:

```python
{'site': {'folder': {'page': page_object}}}
```

- Objects can be accessed like walking through a file-system:

```python
root['site']['folder']['page']
```

```python
>>> from plone import api
>>> portal = api.portal.get()
>>> portal.keys()
['folder1', 'document1']
>>> portal['folder1']
<Folder at xxxx>
```

### Object publishing

Objects can be called and return a representation of itself - usually html.

```python
>>> obj = portal['folder1']['a-newsitem']
>>> obj
<NewsItem at xxx>
>>> obj()
u'\n<!DOCTYPE html>\n\n<html xmlns="http://www.w3.org/1999/xhtml...'
```

### Schema-driven content

Plone comes with a list of pre-defined content-types.

Content types are defined in models/schemas. A schema can define fields to store data.

Values of these fields on instances of objects are attributes

```python
>>> obj.title
u'A Newsitem'
>>> obj.description
u'Some description'
>>> obj.description = u'A new description'
>>> obj.description
u'A new description'
>>> obj.image
<plone.namedfile.file.NamedBlobImage object at 0x11634c320>
>>> obj.image.data
'\x89PNG\r\n\x1a\n\x00\x00\x00\...'
```

Objects can have multiple schemata. Additional schemata are called behaviors. They are meant to be used across types.

```python
>>> from plone.dexterity.utils import iterSchemata
>>> [i for i in iterSchemata(self.context)]
[<InterfaceClass plone.dexterity.schema.generated.Plone_0_News_1_Item>,
 <SchemaClass plone.app.dexterity.behaviors.metadata.IDublinCore>,
 <SchemaClass plone.app.contenttypes.behaviors.richtext.IRichText>,
 <SchemaClass plone.app.dexterity.behaviors.discussion.IAllowDiscussion>,
 <SchemaClass plone.app.dexterity.behaviors.id.IShortName>,
 <SchemaClass plone.app.dexterity.behaviors.exclfromnav.IExcludeFromNavigation>,
 <SchemaClass plone.app.relationfield.behavior.IRelatedItems>,
 <SchemaClass plone.app.contenttypes.behaviors.leadimage.ILeadImage>,
 <SchemaClass plone.app.versioningbehavior.behaviors.IVersionable>]
```

Each schema can define fields

```python
>>> from plone.dexterity.utils import iterSchemata
>>> from zope.schema import getFieldsInOrder
>>> [getFieldsInOrder(schema) for schema in iterSchemata(obj)]
[[],
 [('title', <zope.schema._bootstrapfields.TextLine object at 0x114f1e790>),
  ('description', <zope.schema._bootstrapfields.Text object at 0x114f1e7d0>),
  ('subjects', <zope.schema._field.Tuple object at 0x114f1e990>),
  ('language', <zope.schema._field.Choice object at 0x114f1ea10>),
  ('effective', <zope.schema._field.Datetime object at 0x114f1eb90>),
  ('expires', <zope.schema._field.Datetime object at 0x114f1ec10>),
  ('creators', <zope.schema._field.Tuple object at 0x114e09750>),
  ('contributors', <zope.schema._field.Tuple object at 0x114f1ef10>),
  ('rights', <zope.schema._bootstrapfields.Text object at 0x114f1efd0>)],
 [('text', <plone.app.textfield.RichText object at 0x115215810>)],
 [('allow_discussion', <zope.schema._field.Choice object at 0x11553c590>)],
 [('id', <zope.schema._field.ASCIILine object at 0x11553cc50>)],
 [('exclude_from_nav', <zope.schema._bootstrapfields.Bool object at 0x11552f090>)],
 [('relatedItems', <z3c.relationfield.schema.RelationList object at 0x11556c710>)],
 [('image', <plone.namedfile.field.NamedBlobImage object at 0x114b2a750>),
  ('image_caption', <zope.schema._bootstrapfields.TextLine object at 0x114b2a410>)],
 [('changeNote', <zope.schema._bootstrapfields.TextLine object at 0x11599b350>),
  ('versioning_enabled', <zope.schema._bootstrapfields.Bool object at 0x11599b410>)]]
```

Plone creates forms from these schemata to add and edit content.

### Component Architecture

- Plone logic is wired together by a component architecture.
- A pluggable system of interfaces, adapters, utilities, events and registries.
- ZCA: A Python framework for supporting component based design and programming
- zope.interface
- zope.event
- zope.component

Written by smart people:

- Jim Fulton

- Stephan Richter

- Philipp von Weitershausen

- Guido van Rossum

- Tres Seaver

- Phillip J Eby

- Martijn Faassen

- ...

```{seealso}
- The Keynote by Cris Ewing at PyCon 2016: <https://www.youtube-nocookie.com/embed/eGRJbBI_H2w?feature=youtu.be&t=21m47s&privacy_mode=1>
```
