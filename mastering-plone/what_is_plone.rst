.. _intro-what-is-plone-label:


==============
What is Plone?
==============

Plone is an open source Content Management System (CMS) built in Python.

* Open-Source Enterprise-CMS
* Written in Python
* Plone 5.1 supports Python 2.7
* Plone 5.2 will support Python 3.6+ and 2.7
* `RESTful hypermedia API <https://github.com/plone/plone.restapi/>`_
* Based on the Web-Framework Zope
* Database: "Zope Object Database" (ZODB) or ORM & SQL/Postgres/Oracle
* Runs on Linux, Mac OS, BSD, Solaris, NixOS and Windows

Plone has a multitude of powerful features, is easily accessible to editors but also fun for programmers.

* Workflow-driven, collaborative management of content
* Industrial Strength Security and Access-Control
* Limitless Extensibility

..  note::

    The modular and open component architecture of Plone allows you to change or extend Plone in every respect!


Core concepts
=============

Traversal
---------

* Plone uses `Traversal <https://docs.plone.org/develop/plone/serving/traversing.html>`_ (portal/folder/document) instead of Routing
* Python objects in a object tree that looks like a huge nested dictionary:

.. code-block:: python

    {'site': {'folder': {'page': page_object}}}

* Objects can be accessed like walking through a file-system:

.. code-block:: python

    root['site']['folder']['page']

.. code-block:: python

    >>> from plone import api
    >>> portal = api.portal.get()
    >>> portal.keys()
    ['folder1', 'document1']
    >>> portal['folder1']
    <Folder at xxxx>


Object publishing
-----------------

Objects can be called and return a representation of itself - usually html.

.. code-block:: python

    >>> obj = portal['folder1']['a-newsitem']
    >>> obj
    <NewsItem at xxx>
    >>> obj()
    u'\n<!DOCTYPE html>\n\n<html xmlns="http://www.w3.org/1999/xhtml...'


Schema-driven content
---------------------

Models/Schemas with fields: Content has fields to store data defined in a schema.

Values of these fields on instances of objects are attributes

.. code-block:: python

    >>> obj.title
    u'A Newsitem'
    >>> obj.description
    u'Some description'
    >>> obj.description = u'A new description'
    >>> obj.description
    u'A new description'
    >>> obj.image
    <plone.namedfile.file.NamedBlobImage object at 0x11634c320>
    >>> obj.image
    <plone.namedfile.file.NamedBlobImage object at 0x11634c320>
    >>> obj.image.data
    '\x89PNG\r\n\x1a\n\x00\x00\x00\...'

Objects can have multiple schemata. Additional schemata are called behaviors.

.. code-block:: python

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

* Each schema can have multiple fields

.. code-block:: python

    >>> [i.namesAndDescriptions(all=True) for i in iterSchemata(obj)]
    [[],
     [('rights', <zope.schema._bootstrapfields.Text object at 0x10bf7dfd0>),
      ('subjects', <zope.schema._field.Tuple object at 0x10bf7d990>),
      ('description', <zope.schema._bootstrapfields.Text object at 0x10bf7d7d0>),
      ('language', <zope.schema._field.Choice object at 0x10bf7da10>),
      ('title', <zope.schema._bootstrapfields.TextLine object at 0x10bf7d790>),
      ('effective', <zope.schema._field.Datetime object at 0x10bf7db90>),
      ('contributors', <zope.schema._field.Tuple object at 0x10bf7df10>),
      ('expires', <zope.schema._field.Datetime object at 0x10bf7dc10>),
      ('creators', <zope.schema._field.Tuple object at 0x10be68750>)],
     [('text', <plone.app.textfield.RichText object at 0x10c274810>)],
     [('allow_discussion', <zope.schema._field.Choice object at 0x10c4f7590>)],
     [('id', <zope.schema._field.ASCIILine object at 0x10c4f7c50>)],
     [('exclude_from_nav', <zope.schema._bootstrapfields.Bool object at 0x10c4ea090>)],
     [('relatedItems', <z3c.relationfield.schema.RelationList object at 0x10c527710>)],
     [('image', <plone.namedfile.field.NamedBlobImage object at 0x10bb89750>),
      ('image_caption', <zope.schema._bootstrapfields.TextLine object at 0x10bb89410>)],
     [('versioning_enabled', <zope.schema._bootstrapfields.Bool object at 0x10c956410>),
      ('changeNote', <zope.schema._bootstrapfields.TextLine object at 0x10c956350>)]]

Plone creates forms from all these schemata to add and edit content.


Component Architecture
----------------------

* Plone logic is wired together by a component architecture.
* A pluggable system of interfaces, adapters, utilities, events and registries.
* ZCA: A Python framework for supporting component based design and programming
* zope.interface
* zope.event
* zope.component

Written by smart people:

* Jim Fulton
* Stephan Richter
* Philipp von Weitershausen
* Guido van Rossum
* Tres Seaver
* Phillip J Eby
* Martijn Faassen
* ...

.. seealso::

    * The Keynote by Cris Ewing at PyCon 2016: https://youtu.be/eGRJbBI_H2w?t=21m47s


Deployment
----------

A deployment setup could look like this:

.. code-block:: text

    ZEO-Server   ->   ZEO-Server (ZRS)

       / | \

    ZEO Clients (as many as you want)

       \ | /

    Load balancer (haproxy or nginx)

         |

       Cache (varnish)

         |

      Webserver (nginx)

         |

      Internet

Zope comes with its own basic Webserver (ZServer). With 5.2 (Python 3) it is replaced by a WSGI-Server like waitress or uwsgi.


